from dataclasses import dataclass
from pathlib import Path
import os
import signal
import shutil
import subprocess


@dataclass
class Result:
    args: list[str]
    code: int
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False
    missing: bool = False

    @property
    def ok(self) -> bool:
        return self.code == 0 and not self.timed_out


def run(args: list[str], cwd: Path, timeout: int = 120, env: dict[str, str] | None = None,
        stdin: str = "") -> Result:
    if not cwd.is_dir():
        return Result(args, 126, stderr=f"Working directory does not exist: {cwd}")
    environment = {**os.environ, **(env or {})}
    # Inaccessible PATH entries can make exec report EACCES even for a missing name.
    if "/" not in args[0] and shutil.which(args[0], path=environment.get("PATH")) is None:
        return Result(args, 127, stderr=f"Tool not found: {args[0]}. Run syntaxlab doctor.", missing=True)
    try:
        process = subprocess.Popen(args, cwd=cwd, env=environment,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, errors="replace", start_new_session=True)
    except FileNotFoundError:
        return Result(args, 127, stderr=f"Tool not found: {args[0]}. Run syntaxlab doctor.", missing=True)
    except OSError as exc:
        return Result(args, 126, stderr=str(exc))
    try:
        out, err = process.communicate(stdin, timeout=timeout)
        return Result(args, process.returncode, out, err)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        out, err = process.communicate()
        return Result(args, 124, out, err + f"\nTimed out after {timeout}s", timed_out=True)
    except KeyboardInterrupt:
        os.killpg(process.pid, signal.SIGKILL)
        process.communicate()
        raise


def checkpoint(root: Path, workspace: Path, database: Path, message: str) -> Result:
    """Stage only project/progress. Refuse unrelated or already staged changes."""
    allowed = [str(workspace.relative_to(root)), str(database.relative_to(root))]
    status = run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], root)
    if not status.ok:
        return status
    for entry in status.stdout.split("\0"):
        if not entry:
            continue
        name = entry[3:]
        if entry[0] != " " and entry[:2] != "??":
            return Result([], 1, stderr="Checkpoint refused: staged changes exist. Commit them manually first.")
        if not any(name == p or name.startswith(p + "/") for p in allowed):
            return Result([], 1, stderr=f"Checkpoint refused: unrelated changes in {name}. Commit manually first.")
    for args in (["git", "diff"], ["git", "log", "--oneline", "-10"], ["git", "add", "--", *allowed]):
        result = run(args, root)
        if not result.ok:
            return result
    return run(["git", "commit", "-m", message], root)
