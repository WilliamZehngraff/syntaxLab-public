from contextlib import closing
from copy import copy
from dataclasses import replace
import shutil
import sys
import tomllib

import pytest
from textual.widgets import Select

from syntaxlab.checks import check
from syntaxlab.cli import main
from syntaxlab.config import Config
from syntaxlab.languages import LANGUAGES
from syntaxlab.progress import Progress
from syntaxlab.runner import Result, run
from syntaxlab.tui import SyntaxLabApp


def reference_workspace(lab, key):
    exercise = lab.catalog.exercises[key]
    if exercise.project:
        for stage in lab.catalog.ordered(exercise.language):
            if stage.project == exercise.project and stage.order <= exercise.order:
                lab.workspaces.create(stage)
    path = lab.workspaces.create(exercise)
    for name, text in exercise.solution.items():
        target = path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    return exercise, path


def test_catalog_update_preserves_existing_learner_progress(catalog, tmp_path):
    legacy = copy(catalog)
    legacy.modules = [m for m in catalog.modules if m["language"] in ("scala", "c")]
    legacy.exercises = {key: e for key, e in catalog.exercises.items() if e.language in ("scala", "c")}
    progress = Progress(tmp_path / "progress.db")
    progress.sync(legacy)
    with closing(progress.connect()) as db, db:
        db.execute("DELETE FROM languages WHERE id IN ('rust', 'python')")
    progress.record("scala-hello", True, [{"passed": True}])
    progress.record("c-hello", False, [{"passed": False}])
    progress.set("current", "scala-functions-basic")
    progress.set("hint:scala-functions-basic", "2")
    with closing(progress.connect()) as db:
        attempts = db.execute("SELECT * FROM attempts").fetchall()
        completions = db.execute("SELECT * FROM completions").fetchall()
        version = db.execute("PRAGMA user_version").fetchone()[0]
    progress.sync(catalog)
    with closing(progress.connect()) as db:
        assert db.execute("SELECT * FROM attempts").fetchall() == attempts
        assert db.execute("SELECT * FROM completions").fetchall() == completions
        assert db.execute("PRAGMA user_version").fetchone()[0] == version
        assert {row[0] for row in db.execute("SELECT id FROM languages")} == set(LANGUAGES)
        assert db.execute("SELECT count(*) FROM exercises").fetchone()[0] == 180
    assert progress.get("current") == "scala-functions-basic"
    assert progress.get("hint:scala-functions-basic") == "2"


@pytest.mark.parametrize("language,filename", [("rust", "src/main.rs"), ("python", "main.py")])
def test_workspace_creation_detection_no_overwrite_and_continue(lab, language, filename):
    exercise = lab.select(language=language)
    path = lab.prepare(exercise)
    assert not (path / filename).exists()
    source = path / filename
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("learner work")
    before = {p.relative_to(path): p.read_bytes() for p in path.rglob("*") if p.is_file()}
    lab.prepare(exercise)
    assert {p.relative_to(path): p.read_bytes() for p in path.rglob("*") if p.is_file()} == before
    assert lab.workspaces.detect(source.parent) == exercise
    lab.progress.record(exercise.id, True, [])
    following = lab.select()
    assert following.language == language and following.id != exercise.id


@pytest.mark.parametrize("language,project,filename", [
    ("rust", "task-trail", "src/main.rs"), ("python", "study-planner", "main.py")])
def test_project_stage_adds_tests_without_replacing_source(lab, language, project, filename):
    first = lab.catalog.exercises[f"{language}-{project}-01"]
    second = lab.catalog.exercises[f"{language}-{project}-02"]
    path = lab.workspaces.create(first)
    source = path / filename
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("existing project work")
    support = {name: (path / name).read_bytes() for name in first.files}
    assert lab.workspaces.create(second) == path
    assert source.read_text() == "existing project work"
    assert all((path / name).read_bytes() == text for name, text in support.items())
    assert lab.workspaces.detect(path).id == second.id
    assert all((path / name).exists() for name in second.files)


def test_rust_manifests_and_portable_checks(catalog):
    for exercise in catalog.ordered("rust"):
        manifest = tomllib.loads(exercise.files["Cargo.toml"])
        assert manifest["package"]["edition"] == "2021"
        assert manifest["package"]["rust-version"] == "1.70"
        assert not manifest.get("dependencies")
        assert any(spec.get("args") == ["$cargo", "test", "--offline"] for spec in exercise.checks)
        assert "src/main.rs" in exercise.solution


@pytest.mark.parametrize("key", ["python-hello", "python-input", "python-functions-basic", "python-parsing",
                                  "python-dataclasses", "python-modules", "python-json", "python-study-planner-10"])
def test_python_real_behavior_and_persistence(lab, key):
    exercise, path = reference_workspace(lab, key)
    results = check(exercise, path, replace(lab.config, python=sys.executable), lab.progress)
    assert all(result.passed for result in results), results
    assert key in lab.progress.completed()


@pytest.mark.skipif(not (shutil.which("cargo") and shutil.which("rustc")), reason="Rust/Cargo not installed")
@pytest.mark.parametrize("key", ["rust-hello", "rust-mutable-borrow", "rust-task-trail-10"])
def test_rust_real_cargo_tests(lab, key):
    exercise, path = reference_workspace(lab, key)
    # This is exactly the standalone command used by a learner, with no SyntaxLab test runner.
    standalone = run(["cargo", "test"], path)
    assert standalone.ok, standalone.stdout + standalone.stderr
    results = check(exercise, path, lab.config, lab.progress)
    assert all(result.passed for result in results), results


def test_missing_rust_toolchain_is_infrastructure_error(lab):
    exercise, path = reference_workspace(lab, "rust-hello")
    config = replace(lab.config, cargo="syntaxlab-missing-cargo", rustc="syntaxlab-missing-rustc")
    results = check(exercise, path, config, lab.progress)
    assert not results[-1].passed and results[-1].infrastructure
    assert "syntaxlab-missing-cargo" in results[-1].output and "syntaxlab-missing-rustc" in results[-1].output
    assert exercise.id not in lab.progress.completed()


def test_python_syntax_and_assertion_diagnostics(lab):
    exercise = lab.select("python-hello")
    path = lab.prepare(exercise)
    (path / "main.py").write_text('print("wrong greeting")\n')
    result = check(exercise, path, lab.config, lab.progress)
    assert not result[-1].passed and "AssertionError" in result[-1].output
    (path / "main.py").write_text("def missing_colon()\n    pass\n")
    result = check(exercise, path, lab.config, lab.progress)
    assert not result[-1].passed and "SyntaxError" in result[-1].output
    assert not result[-1].infrastructure


def test_new_tool_configuration_and_argument_arrays(lab, monkeypatch):
    (lab.config.root / "syntaxlab.toml").write_text(
        'cargo = "/tools with spaces/cargo"\nrustc = "/tools with spaces/rustc"\npython = "python3"\n')
    config = Config.load(lab.config.root)
    assert config.cargo == "/tools with spaces/cargo"
    calls = []
    def fake_run(args, cwd, timeout, env, stdin):
        calls.append((args, env))
        return Result(args, 0)
    monkeypatch.setattr("syntaxlab.checks.run", fake_run)
    monkeypatch.setattr("syntaxlab.checks.shutil.which", lambda tool: tool)
    exercise, path = reference_workspace(lab, "rust-hello")
    assert all(r.passed for r in check(exercise, path, config, lab.progress))
    assert calls[0][0] == [config.cargo, "test", "--offline"]
    assert calls[0][1]["RUSTC"] == config.rustc


@pytest.mark.parametrize("language,topic", [("rust", "ownership"), ("python", "functions")])
def test_cli_new_language_flows(lab, capsys, language, topic):
    root = ["--root", str(lab.config.root)]
    assert main(root + ["continue", "--language", language]) == 0
    assert main(root + ["docs", language, topic]) == 0
    assert main(root + ["status"]) == 0
    assert main(root + ["progress"]) == 0
    assert main(root + ["projects"]) == 0
    output = capsys.readouterr().out
    assert f"{language}-hello" in output
    assert "RUST" in output and "PYTHON" in output
    assert "task-trail" in output and "study-planner" in output
    assert "0/10" in output  # Implemented growing-project modules must not be labeled as roadmap-only.


def test_cli_python_check_from_nested_directory(lab, monkeypatch):
    exercise, path = reference_workspace(lab, "python-hello")
    lab.progress.set("current", exercise.id)
    monkeypatch.chdir(path / "tests")
    assert main(["check"]) == 0
    assert exercise.id in lab.progress.completed()
    assert lab.select().language == "python"


def test_doctor_checks_new_toolchains(lab, monkeypatch, capsys):
    def fake_run(args, cwd, timeout):
        return Result(args, 127, missing=True) if args[0] in ("rustc", "cargo") else Result(args, 0, "version 1\n")
    monkeypatch.setattr("syntaxlab.cli.run", fake_run)
    assert main(["--root", str(lab.config.root), "doctor"]) == 1
    output = capsys.readouterr().out
    assert "Rust compiler" in output and "Cargo" in output and "https://rustup.rs/" in output
    assert "Python course interpreter" in output


async def test_tui_cycles_all_languages_and_selects_directly(lab):
    app = SyntaxLabApp(lab)
    async with app.run_test(size=(120, 42)) as pilot:
        await pilot.pause()
        for language in ("c", "rust", "python", "scala"):
            await pilot.press("l")
            await pilot.pause()
            assert app.language == language
            assert app.selected.id == f"{language}-hello"
            assert app.query_one("#language", Select).value == language
        app.query_one("#language", Select).value = "python"
        await pilot.pause()
        assert app.selected.id == "python-hello"
        await pilot.press("enter")
        await pilot.pause()
        assert lab.progress.get("current") == "python-hello"
        await pilot.press("p")
        await pilot.pause()
        assert len(app.items) == 10 and all(e.project == "study-planner" for e in app.items)


async def test_tui_resumes_new_language_current_exercise(lab):
    lab.prepare(lab.select("rust-hello"))
    app = SyntaxLabApp(lab)
    async with app.run_test(size=(110, 40)) as pilot:
        await pilot.pause()
        assert app.language == "rust" and app.selected.id == "rust-hello"
