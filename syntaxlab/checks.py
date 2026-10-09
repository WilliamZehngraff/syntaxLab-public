from dataclasses import asdict, dataclass
from pathlib import Path
import re
import shutil
from syntaxlab.config import Config, inside
from syntaxlab.courses import Exercise
from syntaxlab.progress import Progress
from syntaxlab.runner import run


@dataclass
class CheckResult:
    label: str
    passed: bool
    output: str = ""
    infrastructure: bool = False


def check(e: Exercise, path: Path, config: Config, progress: Progress) -> list[CheckResult]:
    results = []
    for spec in e.checks:
        kind = spec["type"]
        label = spec.get("label", spec.get("path", "Command"))
        if kind == "file":
            result = CheckResult(label, inside(path, spec["path"]).is_file())
        elif kind == "construct":
            source = inside(path, spec["path"])
            result = CheckResult(label, source.exists() and bool(re.search(spec["pattern"], source.read_text())))
        else:
            tools = {"$scala": config.scala, "$cc": config.cc, "$cargo": config.cargo,
                     "$rustc": config.rustc, "$python": config.python}
            missing = [tools.get(t, t) for t in spec.get("requires", [])
                       if shutil.which(tools.get(t, t)) is None]
            if missing:
                results.append(CheckResult(label, False, "Missing required tool: " + ", ".join(missing)
                                           + ". Run syntaxlab doctor.", infrastructure=True))
                break
            args = [tools.get(a, a) for a in spec["args"]]
            executed = run(args, path, spec.get("timeout", config.timeout),
                           env={"CC": config.cc, "RUSTC": config.rustc},
                           stdin=spec.get("stdin", ""))
            passed = executed.ok
            output = executed.stdout + executed.stderr
            if not executed.ok:
                output += f"\nCommand exited with status {executed.code}: {' '.join(args)}\n"
            if "stdout" in spec and executed.stdout.strip() != spec["stdout"].strip():
                passed = False
                output += f"\nExpected output:\n{spec['stdout']}\nActual output:\n{executed.stdout}"
            result = CheckResult(label, passed, output, executed.missing or executed.code == 126)
        results.append(result)
        if not result.passed:
            break  # Never run a stale executable after compilation fails.
    progress.record(e.id, len(results) == len(e.checks) and all(r.passed for r in results),
                    [asdict(r) for r in results])
    return results
