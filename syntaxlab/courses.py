from dataclasses import dataclass
from pathlib import Path
import re
import yaml
from syntaxlab.config import LabError, inside
from syntaxlab.languages import LANGUAGES


@dataclass(frozen=True)
class Exercise:
    id: str
    language: str
    module: str
    title: str
    order: int
    prerequisites: list[str]
    concepts: list[str]
    assignment: str
    docs: str
    hints: list[str]
    files: dict[str, str]
    checks: list[dict]
    solution: dict[str, str]
    project: str = ""
    difficulty: int = 1


class Catalog:
    def __init__(self, root: Path):
        self.root = root
        try:
            data = yaml.safe_load((root / "content/catalog.yaml").read_text())
            if not isinstance(data, dict) or data.get("version") != 1:
                raise ValueError("catalog version must be 1")
            self.modules = data["modules"]
            if not isinstance(self.modules, list):
                raise ValueError("modules must be a list")
            module_keys = set()
            for module in self.modules:
                if not isinstance(module, dict) or any(
                    not isinstance(module.get(field), str) or not module[field].strip()
                    for field in ("language", "id", "title", "docs")
                ):
                    raise ValueError("each module needs string language, id, title and docs")
                if not isinstance(module.get("roadmap", False), bool):
                    raise ValueError("module roadmap must be true or false")
                key = (module["language"], module["id"])
                if key in module_keys or key[0] not in LANGUAGES:
                    raise ValueError(f"invalid/duplicate module: {key}")
                module_keys.add(key)
                if not inside(root / "content", module["docs"]).is_file():
                    raise ValueError(f"missing module documentation: {key}")
            self.exercises: dict[str, Exercise] = {}
            for path in sorted((root / "content").glob("*/exercises/*.yaml")):
                try:
                    exercise = Exercise(**yaml.safe_load(path.read_text()))
                    self._validate(exercise, module_keys)
                    if exercise.id in self.exercises:
                        raise ValueError(f"duplicate id {exercise.id}")
                    self.exercises[exercise.id] = exercise
                except (TypeError, ValueError, KeyError) as exc:
                    raise ValueError(f"{path.name}: {exc}") from exc
            if not self.exercises:
                raise ValueError("No exercises found")
            visited: set[str] = set()
            visiting: set[str] = set()

            def visit(key: str) -> None:
                if key not in self.exercises:
                    raise ValueError(f"Unknown prerequisite: {key}")
                if key in visiting:
                    raise ValueError(f"Prerequisite cycle at {key}")
                if key in visited:
                    return
                visiting.add(key)
                for parent in self.exercises[key].prerequisites:
                    visit(parent)
                visiting.remove(key)
                visited.add(key)
            for exercise_id in self.exercises:
                visit(exercise_id)
        except (OSError, yaml.YAMLError, ValueError, TypeError, KeyError, AttributeError, re.error) as exc:
            raise LabError(f"Invalid course data: {exc}") from exc

    def _validate(self, e: Exercise, modules: set) -> None:
        if not isinstance(e.id, str) or not re.fullmatch(r"[a-z0-9-]+", e.id):
            raise ValueError("invalid exercise id")
        if (e.language, e.module) not in modules:
            raise ValueError("unknown language/module")
        if type(e.order) is not int or e.order < 1:
            raise ValueError("order must be positive")
        if type(e.difficulty) is not int or not 1 <= e.difficulty <= 5:
            raise ValueError("difficulty must be an integer from 1 to 5")
        for value in (e.title, e.assignment, e.docs):
            if not isinstance(value, str) or not value.strip():
                raise ValueError("title, assignment and docs are required")
        if not isinstance(e.project, str) or (e.project and not re.fullmatch(r"[a-z0-9-]+", e.project)):
            raise ValueError("invalid project name")
        for values in (e.prerequisites, e.concepts, e.hints):
            if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                raise ValueError("prerequisites, concepts and hints must be string lists")
        if not inside(self.root / "content", e.docs).is_file():
            raise ValueError(f"missing documentation {e.docs}")
        for files in (e.files, e.solution):
            if not isinstance(files, dict):
                raise ValueError("files/solution must be mappings")
            for name, text in files.items():
                if not isinstance(name, str):
                    raise ValueError("file paths must be strings")
                inside(self.root, name)
                if name.startswith(".syntaxlab") or not isinstance(text, str):
                    raise ValueError("invalid workspace file")
        if not isinstance(e.checks, list) or not e.checks:
            raise ValueError("checks must be a nonempty list")
        for check in e.checks:
            if not isinstance(check, dict):
                raise ValueError("each check must be a mapping")
            kind = check.get("type")
            if kind not in ("file", "command", "construct"):
                raise ValueError(f"unknown check type {kind}")
            allowed = {"type", "label"} | ({"args", "timeout", "stdin", "stdout", "requires"} if kind == "command"
                                            else {"path", "pattern"} if kind == "construct" else {"path"})
            if set(check) - allowed:
                raise ValueError(f"unknown {kind} check fields: {set(check) - allowed}")
            if "label" in check and not isinstance(check["label"], str):
                raise ValueError("check label must be a string")
            if kind in ("file", "construct"):
                inside(self.root, check["path"])
            if kind == "construct":
                re.compile(check["pattern"])
            if kind == "command":
                args = check["args"]
                if not isinstance(args, list) or not args or not all(isinstance(a, str) for a in args):
                    raise ValueError("command args must be a nonempty string list")
                if not isinstance(check.get("timeout", 120), int) or check.get("timeout", 120) <= 0:
                    raise ValueError("command timeout must be positive")
                for field in ("stdin", "stdout"):
                    if field in check and not isinstance(check[field], str):
                        raise ValueError(f"command {field} must be a string")
                required = check.get("requires", [])
                if not isinstance(required, list) or not all(isinstance(t, str) and t for t in required):
                    raise ValueError("command requires must be a list of executable names")

    def ordered(self, language: str | None = None) -> list[Exercise]:
        return sorted((e for e in self.exercises.values() if not language or e.language == language),
                      key=lambda e: (e.order, e.id))

    def unlocked(self, e: Exercise, completed: set[str]) -> bool:
        return e.id in completed or set(e.prerequisites) <= completed

    def next(self, completed: set[str], language: str | None = None) -> Exercise | None:
        return next((e for e in self.ordered(language) if e.id not in completed
                     and self.unlocked(e, completed)), None)
