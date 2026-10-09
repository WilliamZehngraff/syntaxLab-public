import argparse
from pathlib import Path
import platform
import sqlite3
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from syntaxlab.checks import check
from syntaxlab.config import Config, LabError, inside
from syntaxlab.progress import percentage
from syntaxlab.runner import checkpoint, run
from syntaxlab.service import Lab
from syntaxlab.languages import LANGUAGES

console = Console()


def bar(value: int) -> str:
    return "━" * (value // 5) + "─" * (20 - value // 5) + f" {value:3}%"


def show_status(lab: Lab, detailed: bool = False) -> None:
    done = lab.progress.completed()
    console.print("[bold cyan]SyntaxLab[/]  ·  Read → Write → Compile → Test")
    console.print("Overall  " + bar(percentage(list(lab.catalog.exercises), done)))
    table = Table("Learning path", "Progress", "Completed")
    for language in LANGUAGES:
        items = lab.catalog.ordered(language)
        ids = [e.id for e in items]
        table.add_row(language.upper(), bar(percentage(ids, done)), f"{len(set(ids) & done)}/{len(ids)}")
        if detailed:
            for m in lab.catalog.modules:
                if m["language"] != language:
                    continue
                ids = [e.id for e in items if e.module == m["id"]]
                table.add_row("  " + m["title"], bar(percentage(ids, done)) if ids else "Roadmap",
                              f"{len(set(ids) & done)}/{len(ids)}" if ids else "—")
            concepts = sorted({c for e in items for c in e.concepts})
            for concept in concepts:
                ids = [e.id for e in items if concept in e.concepts]
                table.add_row("    · " + concept, bar(percentage(ids, done)), "")
    console.print(table)
    console.print("Current: " + (lab.progress.get("current") or "Choose a language with syntaxlab continue --language c"))


def doctor(lab: Lab) -> int:
    console.print("[bold]SyntaxLab environment[/]")
    console.print(f"✓ Python {platform.python_version()}")
    problems = 0
    tools = [("Git", "git", "--version", "sudo apt install git"),
             ("VS Code CLI", lab.config.editor, "--version", "Install VS Code and its WSL extension; enable the code command"),
             ("Java", "java", "-version", "sudo apt install default-jdk"),
             ("scala-cli", lab.config.scala, "version", "Install Scala CLI: https://scala-cli.virtuslab.org/install/"),
             ("GCC", lab.config.cc, "--version", "sudo apt install build-essential"),
             ("Make", "make", "--version", "sudo apt install build-essential"),
             ("Rust compiler", lab.config.rustc, "--version", "Install Rust via https://rustup.rs/; reopen your shell"),
             ("Cargo", lab.config.cargo, "--version", "Install Rust via https://rustup.rs/; reopen your shell"),
             ("Python course interpreter", lab.config.python, "--version", "Install Python 3.11+ or configure python in syntaxlab.toml")]
    for name, command, argument, help_text in tools:
        result = run([command, argument], lab.config.root, 20)
        if result.ok:
            console.print(f"✓ {name}: " + (result.stdout or result.stderr).splitlines()[0], markup=False)
        else:
            problems += 1
            console.print(f"✗ {name}: {command} unavailable. {help_text}", markup=False)
    healthy = lab.progress.healthy()
    console.print("✓ Database healthy" if healthy else "✗ Database integrity failed")
    console.print(f"✓ Course data valid ({len(lab.catalog.exercises)} exercises/stages)")
    console.print("Ready." if not problems and healthy else "Install the missing tools for their corresponding workflows.")
    return int(bool(problems or not healthy))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="SyntaxLab — local programming practice")
    p.add_argument("--root", type=Path, help="SyntaxLab repository root (normally discovered automatically)")
    sub = p.add_subparsers(dest="command")
    for name in ("init", "status", "progress", "doctor", "validate", "projects"):
        sub.add_parser(name)
    for name in ("continue", "open"):
        s = sub.add_parser(name)
        s.add_argument("exercise", nargs="?")
        s.add_argument("--language", choices=LANGUAGES)
    s = sub.add_parser("check")
    s.add_argument("--checkpoint", action="store_true", help="Explicitly authorize a Git stage checkpoint")
    s = sub.add_parser("docs")
    s.add_argument("language", nargs="?", choices=LANGUAGES)
    s.add_argument("topic", nargs="?")
    s = sub.add_parser("reset")
    s.add_argument("exercise")
    s.add_argument("--yes", action="store_true", help="Confirm backup/reset without prompting")
    for name in ("hint", "solution"):
        s = sub.add_parser(name)
        s.add_argument("exercise", nargs="?")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        lab = Lab(Config.load(args.root))
        command = args.command
        if command is None:
            from syntaxlab.tui import SyntaxLabApp
            SyntaxLabApp(lab).run()
        elif command in ("init", "validate"):
            console.print(f"Ready: {len(lab.catalog.exercises)} exercises/stages. Database: {lab.progress.path}")
        elif command in ("status", "progress"):
            show_status(lab, command == "progress")
        elif command == "doctor":
            return doctor(lab)
        elif command in ("continue", "open"):
            if command == "open" and not args.exercise and not args.language:
                try:
                    e = lab.workspaces.detect(Path.cwd())
                except LabError:
                    e = lab.select()
            else:
                e = lab.select(args.exercise, args.language)
            path = lab.prepare(e)
            console.print(Markdown(f"# {e.title}\n\n{e.assignment}"))
            console.print(f"Reference: syntaxlab docs {e.language} {e.module}")
            console.print(f"\nWorkspace: {path}\ncd {path}\nsyntaxlab check", markup=False)
            if command == "open":
                result = run([lab.config.editor, str(path)], lab.config.root, 20)
                if not result.ok:
                    console.print(result.stderr, markup=False)
                    console.print("Workspace is ready. Open this directory manually in your editor.")
                    return 1
        elif command == "check":
            e = lab.workspaces.detect(Path.cwd())
            lab.select(e.id)
            results = check(e, lab.workspaces.path(e), lab.config, lab.progress)
            for r in results:
                console.print(f"{'✓' if r.passed else '✗'} {r.label}", markup=False)
                if r.output:
                    console.print(r.output, markup=False, highlight=False)
            passed = all(r.passed for r in results)
            console.print(f"{sum(r.passed for r in results)} / {len(e.checks)} passed")
            if not passed:
                console.print("Infrastructure error; see doctor." if results[-1].infrastructure
                              else "Not complete yet. Read the diagnostics, edit, and try again.")
                return 1
            console.print("[bold green]Exercise complete.[/]")
            next_e = lab.catalog.next(lab.progress.completed(), e.language)
            if next_e:
                console.print(f"Next: {next_e.id} — {next_e.title}")
            if args.checkpoint and e.project:
                result = checkpoint(lab.config.root, lab.workspaces.path(e), lab.progress.path,
                                    f"syntaxlab: complete {e.language} {e.project} {e.id} - {e.title}")
                console.print(result.stdout + result.stderr, markup=False)
                return int(not result.ok)
        elif command == "docs":
            modules = [m for m in lab.catalog.modules if not args.language or m["language"] == args.language]
            if args.topic:
                module = next((m for m in modules if m["id"] == args.topic), None)
                if not module:
                    raise LabError("Unknown documentation topic; run syntaxlab docs for the index")
                console.print(Markdown(inside(lab.config.root / "content", module["docs"]).read_text()))
                lab.progress.encounter("docs", module["docs"])
            else:
                for m in modules:
                    console.print(f"syntaxlab docs {m['language']} {m['id']}  — {m['title']}")
        elif command == "projects":
            done = lab.progress.completed()
            for language in LANGUAGES:
                projects = sorted({e.project for e in lab.catalog.ordered(language) if e.project})
                for project in projects:
                    stages = [e for e in lab.catalog.ordered(language) if e.project == project]
                    console.print(f"\n{language.upper()} / {project}  " + bar(percentage([e.id for e in stages], done)))
                    for e in stages:
                        symbol = "✓" if e.id in done else "○" if lab.catalog.unlocked(e, done) else "🔒"
                        console.print(f" {symbol} {e.id} — {e.title}")
        elif command == "reset":
            if args.exercise not in lab.catalog.exercises:
                raise LabError(f"Unknown exercise: {args.exercise}")
            e = lab.catalog.exercises[args.exercise]
            if not args.yes and input("Back up workspace and reset this exercise (whole project for a stage)? [y/N] ").lower() != "y":
                return 0
            ids = {x.id for x in lab.catalog.exercises.values() if e.project and x.project == e.project
                   and x.language == e.language} or {e.id}
            # Invalidate dependent completions so the graph remains coherent.
            while True:
                expanded = ids | {x.id for x in lab.catalog.exercises.values() if set(x.prerequisites) & ids}
                if expanded == ids:
                    break
                ids = expanded
            first = min((x for x in lab.catalog.exercises.values() if x.id in ids), key=lambda x: x.order)
            backup = lab.workspaces.reset(first if e.project else e)
            lab.progress.reset(list(ids))
            lab.progress.set("current", first.id if e.project else e.id)
            console.print(f"Reset complete. Preserved previous work at {backup}. Attempts retained.")
        elif command in ("hint", "solution"):
            if args.exercise:
                e = lab.select(args.exercise)
            else:
                try:
                    e = lab.workspaces.detect(Path.cwd())
                except LabError:
                    e = lab.select()
            if command == "hint":
                key = "hint:" + e.id
                level = min(int(lab.progress.get(key) or "0") + 1, len(e.hints))
                console.print(e.hints[level - 1] if level else "No further hints; review the documentation.")
                lab.progress.set(key, str(level))
            elif input("This reveals the full solution and may reduce learning value. Continue? [y/N] ").lower() == "y":
                for name, text in e.solution.items():
                    console.print(f"\n{name}\n{text}", markup=False, highlight=False)
                lab.progress.encounter("solution", e.id)
        return 0
    except (LabError, OSError, ValueError, sqlite3.Error) as exc:
        console.print(f"SyntaxLab: {exc}", style="red", markup=False)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
