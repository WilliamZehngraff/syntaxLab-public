import json
import pytest
from syntaxlab.config import Config, LabError


def test_empty_source_and_no_overwrite(lab):
    exercise = lab.select("scala-hello")
    path = lab.prepare(exercise)
    assert not (path / "Main.scala").exists()
    assert (path / "Exercise.test.scala").exists()
    (path / "Main.scala").write_text("// My first attempt\n")
    (path / "Exercise.test.scala").write_text("// My test notes\n")
    before = {p.name: p.read_bytes() for p in path.iterdir()}
    lab.prepare(exercise)
    assert {p.name: p.read_bytes() for p in path.iterdir()} == before
    assert lab.progress.get("current") == exercise.id


def test_detection_from_nested_folder(lab):
    e = lab.select("c-hello")
    path = lab.prepare(e) / "src/deep"
    path.mkdir(parents=True)
    assert lab.workspaces.detect(path).id == e.id
    with pytest.raises(LabError, match="Not inside"):
        lab.workspaces.detect(lab.config.root)


def test_wrong_marker_location(lab):
    folder = lab.config.root / "rogue"
    folder.mkdir()
    (folder / ".syntaxlab.json").write_text(json.dumps({"exercise": "scala-hello"}))
    with pytest.raises(LabError, match="location"):
        lab.workspaces.detect(folder)


def test_reset_backs_up_learner_files(lab):
    e = lab.select("c-hello")
    path = lab.prepare(e)
    (path / "main.c").write_text("precious work")
    backup = lab.workspaces.reset(e)
    assert (backup / "main.c").read_text() == "precious work"
    assert not (path / "main.c").exists()


def test_project_stage_reuses_workspace_and_retains_tests(lab):
    first = lab.catalog.exercises["scala-task-desk-01"]
    second = lab.catalog.exercises["scala-task-desk-02"]
    path = lab.workspaces.create(first)
    (path / "Main.scala").write_text("// My growing program")
    assert lab.workspaces.create(second) == path
    assert (path / "Main.scala").read_text() == "// My growing program"
    assert (path / "Stage01.test.scala").exists()
    assert (path / "Stage02.test.scala").exists()
    assert lab.workspaces.detect(path).id == second.id


def test_selection_enforces_prerequisites(lab):
    with pytest.raises(LabError, match="Locked"):
        lab.select("scala-recursion-tail")
    with pytest.raises(LabError, match="Unknown"):
        lab.select("unknown")
    lab.prepare(lab.select("c-hello"))
    assert lab.select().id == "c-hello"
    lab.progress.record("c-hello", True, [])
    assert lab.select(language="c").id != "c-hello"
    assert lab.select("c-hello").id == "c-hello"


def test_workspace_symlink_alias_refused(lab):
    (lab.config.root / "workspaces").symlink_to(lab.config.root / "content", target_is_directory=True)
    with pytest.raises(LabError, match="symlink"):
        lab.workspaces.create(lab.catalog.exercises["c-hello"])


def test_corrupt_metadata_has_actionable_error(lab):
    e = lab.select("c-hello")
    path = lab.prepare(e)
    (path / ".syntaxlab.json").write_text("[]")
    with pytest.raises(LabError, match="metadata"):
        lab.prepare(e)


def test_config_discovery_and_options(lab, monkeypatch):
    folder = lab.prepare(lab.select("c-hello"))
    monkeypatch.chdir(folder)
    assert Config.load().root == lab.config.root
    (lab.config.root / "syntaxlab.toml").write_text('timeout = 25\neditor = "missing-editor"\n')
    assert Config.load().timeout == 25
    (lab.config.root / "syntaxlab.toml").write_text('database = "../outside.db"\n')
    with pytest.raises(LabError):
        Config.load()
