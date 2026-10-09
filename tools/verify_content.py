"""Verify private references in temporary workspaces, never in learner directories.

python tools/verify_content.py --language c
python tools/verify_content.py --language scala
python tools/verify_content.py --language rust
python tools/verify_content.py --language python
python tools/verify_content.py --exercise scala-hello --plain-scala
Missing external tools are reported as skips and result in exit status 2.
"""
import argparse
from dataclasses import replace
from pathlib import Path
import shutil
import tempfile
from syntaxlab.checks import check
from syntaxlab.config import Config
from syntaxlab.courses import Catalog
from syntaxlab.progress import Progress
from syntaxlab.runner import run
from syntaxlab.workspace import Workspaces
from syntaxlab.languages import LANGUAGES


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=LANGUAGES)
    parser.add_argument("--exercise")
    parser.add_argument("--plain-scala", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    catalog = Catalog(root)
    if args.exercise and (args.exercise not in catalog.exercises or (
        args.language and catalog.exercises[args.exercise].language != args.language
    )):
        parser.error("No exercise matches that ID/language")
    failures, skipped, passed = [], [], []
    with tempfile.TemporaryDirectory(prefix="syntaxlab-reference-") as temporary:
        config = replace(Config.load(root), root=Path(temporary), timeout=240)
        progress = Progress(config.root / "progress.db")
        for e in catalog.ordered(args.language):
            if args.exercise and e.id != args.exercise:
                continue
            required = {"rust": [config.cargo, config.rustc], "python": [config.python]}.get(e.language, [])
            unavailable = [tool for tool in required if shutil.which(tool) is None]
            if unavailable:
                skipped.append(f"{e.id}: unavailable tools: {', '.join(unavailable)}")
                print(f"SKIP {skipped[-1]}", flush=True)
                continue
            exercise_config = replace(config, root=config.root / e.id)
            workspaces = Workspaces(exercise_config, catalog)
            # Independent snapshot plus all earlier project support, without copying other solutions.
            if e.project:
                ancestors = [x for x in catalog.ordered(e.language) if x.project == e.project
                             and int(x.id.rsplit("-", 1)[1]) <= int(e.id.rsplit("-", 1)[1])]
                for ancestor in sorted(ancestors, key=lambda x: x.id):
                    workspaces.create(ancestor)
            path = workspaces.create(e)
            # Earlier snapshots may have introduced source files; remove only developer-written references.
            if e.project and e.language in ("scala", "c"):
                for old in path.glob("*.scala" if e.language == "scala" else "*.c"):
                    if old.name not in e.solution and not old.name.endswith(".test.scala") and not old.name.startswith("test_") and old.name != "project.scala":
                        old.unlink()
            for name, text in e.solution.items():
                target = path / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)
            specs = []
            for spec in e.checks:
                tool = spec.get("args", [""])[0]
                if tool == "make" and not shutil.which("make"):
                    skipped.append(f"{e.id}: make unavailable")
                    continue
                if tool == "./program" and not shutil.which("make") and e.id == "c-makefile":
                    built = run([config.cc, "-std=c17", "-Wall", "-Wextra", "-Wpedantic", "-Werror",
                                 "main.c", "-o", "program"], path)
                    if not built.ok:
                        print(built.stdout + built.stderr)
                if spec.get("args") == ["python3", "test_cli.py"] and not shutil.which("make"):
                    # Verify the actual CLI with GCC even if Make is unavailable.
                    built = run([config.cc, "-std=c17", "-Wall", "-Wextra", "-Wpedantic", "-Werror",
                                 "main.c", "tasks.c", "-o", "program"], path)
                    if not built.ok:
                        print(built.stdout + built.stderr)
                specs.append(spec)
            if args.plain_scala and e.language == "scala":
                result = run([config.scala, "test", "."], path, 240)
                print(result.stdout + result.stderr, flush=True)
                if not result.ok:
                    failures.append(e.id + " (plain scala-cli)")
            results = check(replace(e, checks=specs), path, config, progress)
            if all(r.passed for r in results):
                passed.append(e.id)
                print(f"PASS {e.id}", flush=True)
            else:
                failures.append(e.id)
                print(f"FAIL {e.id}", flush=True)
                for result in results:
                    if not result.passed:
                        print(result.label + "\n" + result.output, flush=True)
    print(f"\n{len(passed)} passed; {len(failures)} failed; {len(skipped)} tool-dependent checks skipped.")
    for message in failures + skipped:
        print(message)
    return 1 if failures else 2 if skipped else 0


if __name__ == "__main__":
    raise SystemExit(main())
