from dataclasses import dataclass
from pathlib import Path
import tomllib


class LabError(Exception):
    """An actionable infrastructure or configuration error."""


def inside(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or path == root.resolve():
        raise LabError(f"Path must stay inside {root}: {relative}")
    return path


@dataclass(frozen=True)
class Config:
    root: Path
    editor: str = "code"
    scala: str = "scala-cli"
    cc: str = "gcc"
    timeout: int = 120
    database: str = "data/progress.db"
    cargo: str = "cargo"
    rustc: str = "rustc"
    python: str = "python3"

    @classmethod
    def load(cls, root: Path | None = None) -> "Config":
        if root is None:
            root = next((p for p in [Path.cwd(), *Path.cwd().parents]
                         if (p / "content/catalog.yaml").exists()), None)
            if root is None:
                root = Path(__file__).resolve().parent.parent
        root = root.resolve()
        options = {}
        if (root / "syntaxlab.toml").exists():
            options = tomllib.loads((root / "syntaxlab.toml").read_text())
        if set(options) - {"editor", "scala", "cc", "cargo", "rustc", "python", "timeout", "database"}:
            raise LabError("Unknown syntaxlab.toml option")
        if not isinstance(options.get("timeout", 120), int) or options.get("timeout", 120) <= 0:
            raise LabError("timeout must be a positive integer")
        for key in ("editor", "scala", "cc", "cargo", "rustc", "python", "database"):
            if key in options and (not isinstance(options[key], str) or not options[key]):
                raise LabError(f"{key} must be a nonempty string")
        config = cls(root, **options)
        inside(root, config.database)
        return config
