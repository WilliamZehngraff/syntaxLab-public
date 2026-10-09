from pathlib import Path
import json
import shutil
import uuid
from syntaxlab.config import Config, LabError, inside
from syntaxlab.courses import Catalog, Exercise


class Workspaces:
    def __init__(self, config: Config, catalog: Catalog):
        self.config, self.catalog = config, catalog

    def path(self, e: Exercise) -> Path:
        base = "projects" if e.project else "workspaces"
        relative = f"{base}/{e.language}/{e.project or e.id}"
        target = inside(self.config.root, relative)
        if target != self.config.root.resolve() / relative:
            raise LabError("Workspace directories must not be symlink aliases")
        return target

    def create(self, e: Exercise) -> Path:
        path = self.path(e)
        path.mkdir(parents=True, exist_ok=True)
        marker = path / ".syntaxlab.json"
        if marker.is_symlink():
            raise LabError("Workspace metadata must not be a symlink")
        try:
            existing = json.loads(marker.read_text()) if marker.exists() else None
            if existing is not None and (not isinstance(existing, dict) or "exercise" not in existing):
                raise ValueError("missing exercise")
        except ValueError as exc:
            raise LabError("Invalid workspace metadata; restore .syntaxlab.json from Git") from exc
        if existing and existing["exercise"] == e.id:
            return path
        if existing and not e.project:
            raise LabError("Workspace belongs to another exercise")
        # Stage support is immutable and cumulative; never replace learner files.
        for name, text in e.files.items():
            destination = inside(path, name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                with destination.open("x") as stream:
                    stream.write(text)
            except FileExistsError:
                pass
        temporary = path / f".syntaxlab-{uuid.uuid4().hex}.tmp"
        temporary.write_text(json.dumps({"exercise": e.id}, indent=2) + "\n")
        temporary.replace(marker)
        return path

    def detect(self, cwd: Path) -> Exercise:
        for path in [cwd.resolve(), *cwd.resolve().parents]:
            if not path.is_relative_to(self.config.root):
                break
            marker = path / ".syntaxlab.json"
            if marker.is_file():
                try:
                    e = self.catalog.exercises[json.loads(marker.read_text())["exercise"]]
                except (ValueError, KeyError) as exc:
                    raise LabError("Invalid workspace metadata") from exc
                if self.path(e) != path:
                    raise LabError("Workspace metadata does not match its location")
                return e
        raise LabError("Not inside an exercise. Use syntaxlab continue, then cd to its workspace.")

    def reset(self, e: Exercise) -> Path | None:
        path = self.path(e)
        backup = None
        if path.exists():
            backup = inside(self.config.root, f"backups/{path.name}-{uuid.uuid4().hex[:10]}")
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), backup)
        self.create(e)
        return backup
