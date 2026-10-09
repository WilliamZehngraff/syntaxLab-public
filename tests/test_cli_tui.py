import sys
import os
import pty
import select
import subprocess
import time
from textual.widgets import ListView, Markdown, Select, Static
from syntaxlab.cli import main
from syntaxlab.runner import run
from syntaxlab.tui import SyntaxLabApp


def test_cli_help_as_real_process(tmp_path):
    result = run([sys.executable, "-m", "syntaxlab.cli", "--help"], tmp_path)
    assert result.ok and "continue" in result.stdout and "doctor" in result.stdout


def test_real_terminal_launch_and_quit(lab):
    master, slave = pty.openpty()
    process = subprocess.Popen([sys.executable, "-m", "syntaxlab.cli", "--root", str(lab.config.root)],
                               stdin=slave, stdout=slave, stderr=slave, env={**os.environ, "TERM": "xterm-256color"})
    os.close(slave)
    output = b""
    try:
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline and b"Skill path" not in output:
            if select.select([master], [], [], 0.2)[0]:
                output += os.read(master, 65536)
        assert b"SyntaxLab" in output and b"Skill path" in output
        os.write(master, b"q")
        process.wait(timeout=10)
        assert process.returncode == 0
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        os.close(master)


def test_cli_common_commands(lab, capsys):
    root = ["--root", str(lab.config.root)]
    for args in (["init"], ["validate"], ["status"], ["progress"], ["docs"], ["docs", "scala", "functions"],
                 ["docs", "c", "pointers"], ["projects"], ["continue", "--language", "c"], ["hint"]):
        assert main(root + args) == 0
    assert "Workspace:" in capsys.readouterr().out
    assert main(root + ["docs", "c", "unknown"]) == 2


def test_cli_missing_editor_preserves_workspace(lab, capsys):
    (lab.config.root / "syntaxlab.toml").write_text('editor = "syntaxlab-missing-editor"\n')
    assert main(["--root", str(lab.config.root), "open", "c-hello"]) == 1
    assert "Workspace is ready" in capsys.readouterr().out
    assert (lab.workspaces.path(lab.catalog.exercises["c-hello"]) / "test_exercise.py").exists()


def test_cli_reset_and_solution_require_confirmation(lab, monkeypatch, capsys):
    root = ["--root", str(lab.config.root)]
    path = lab.prepare(lab.select("c-hello"))
    (path / "main.c").write_text("my code")
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert main(root + ["reset", "c-hello"]) == 0
    assert (path / "main.c").read_text() == "my code"
    assert main(root + ["solution", "c-hello"]) == 0
    assert "#include" not in capsys.readouterr().out
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert main(root + ["solution", "c-hello"]) == 0
    assert "#include" in capsys.readouterr().out
    assert main(root + ["reset", "c-hello"]) == 0
    assert not (path / "main.c").exists()
    assert any((lab.config.root / "backups").glob("*/main.c"))


def test_cli_check_from_current_directory_and_persistence(lab, monkeypatch):
    e = lab.select("c-hello")
    path = lab.prepare(e)
    monkeypatch.chdir(path)
    assert main(["check"]) == 1  # no learner file yet
    (path / "main.c").write_text(e.solution["main.c"])
    assert main(["check"]) == 0
    assert e.id in lab.progress.completed()
    assert lab.catalog.unlocked(lab.catalog.exercises["c-variables"], lab.progress.completed())


async def test_tui_navigation_docs_workspace_and_locks(lab):
    app = SyntaxLabApp(lab)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        assert app.selected.id == "scala-hello"
        await pilot.press("d")
        await pilot.pause()
        assert app.query_one("#lesson", Markdown) is not None
        await pilot.press("l")
        await pilot.pause()
        assert app.language == "c" and app.selected.id == "c-hello"
        await pilot.click("#prepare")
        await pilot.pause()
        assert lab.workspaces.path(app.selected).is_dir()
        await pilot.press("p")
        await pilot.pause()
        assert app.project_mode and all(e.project for e in app.items)
        await pilot.click("#prepare")
        await pilot.pause()
        assert not lab.workspaces.path(app.selected).exists()  # prerequisite still locked
        await pilot.press("p")
        await pilot.pause()
        app.query_one(ListView).focus()
        await pilot.press("down")
        assert app.selected.id == "c-variables"
        await pilot.press("q")


async def test_tui_check_worker_records_progress(lab):
    e = lab.select("c-hello")
    path = lab.prepare(e)
    (path / "main.c").write_text(e.solution["main.c"])
    app = SyntaxLabApp(lab)
    async with app.run_test(size=(100, 35)) as pilot:
        await pilot.pause()
        await pilot.press("c")
        await app.workers.wait_for_complete()
        await pilot.pause()
        assert e.id in lab.progress.completed()
        assert "complete" in str(app.query_one("#results", Static).render()).lower()


async def test_tui_module_filter_enter_docs_links_and_progress(lab):
    app = SyntaxLabApp(lab)
    async with app.run_test(size=(110, 38)) as pilot:
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        assert lab.workspaces.path(lab.catalog.exercises["scala-hello"]).is_dir()
        app.query_one("#module", Select).value = "recursion"
        await pilot.pause()
        assert len(app.items) == 4 and all(e.module == "recursion" for e in app.items)
        await pilot.press("d")
        app.documentation_link(Markdown.LinkClicked(app.query_one("#lesson", Markdown), "functions.md"))
        await pilot.pause()
        assert app.doc_path == "scala/docs/functions.md"
        await pilot.press("g")
        await pilot.press("b")
        await pilot.pause()
        assert app.selected.module == "recursion"
