from pathlib import Path
import re
import yaml
import pytest
from syntaxlab.config import LabError, inside
from syntaxlab.courses import Catalog
from syntaxlab.languages import LANGUAGES


def test_entire_curriculum_and_real_contracts(catalog):
    assert len(catalog.exercises) == 180
    for language in LANGUAGES:
        skills = [e for e in catalog.ordered(language) if not e.project]
        stages = [e for e in catalog.ordered(language) if e.project]
        assert len(skills) >= 30
        assert len(stages) >= 10
        assert {"foundations", "functions", "control-flow", "recursion"} <= {e.module for e in skills}
        assert any(e.project for e in catalog.exercises.values())
    for e in catalog.exercises.values():
        assert e.solution and e.hints and e.concepts and len(e.assignment) > 150
        assert not {"Main.scala", "main.c", "main.py", "src/main.rs", "src/lib.rs"} & e.files.keys()
        if e.language == "scala":
            assert 'using scala "3.' in e.files["project.scala"]
            assert any(name.endswith(".test.scala") for name in e.files)
        elif e.language == "c":
            assert any(name.startswith("test_") and name.endswith(".py") for name in e.files)
        elif e.language == "python":
            assert any(name.startswith("tests/test_") and name.endswith(".py") for name in e.files)
        elif e.language == "rust":
            assert "Cargo.toml" in e.files
            assert any(name.startswith("tests/") and name.endswith(".rs") for name in e.files)


def test_graph_can_unlock_every_exercise(catalog):
    completed = set()
    while following := catalog.next(completed):
        assert set(following.prerequisites) <= completed
        completed.add(following.id)
    assert completed == set(catalog.exercises)
    assert catalog.unlocked(catalog.exercises["scala-hello"], completed)


def test_languages_are_independent(catalog):
    for language in LANGUAGES:
        assert catalog.next(set(), language).id == f"{language}-hello"
    assert not catalog.unlocked(catalog.exercises["scala-functions-basic"], {"c-hello"})


def test_project_stages_follow_display_order_and_prerequisites(catalog):
    for language in LANGUAGES:
        stages = [e for e in catalog.ordered(language) if e.project]
        assert [e.id for e in stages] == sorted(e.id for e in stages)
        for stage in stages:
            assert all(catalog.exercises[p].order < stage.order for p in stage.prerequisites)


@pytest.mark.parametrize("field,value,match", [
    ("prerequisites", ["nonexistent"], "Unknown prerequisite"),
    ("prerequisites", ["scala-hello"], "cycle"),
    ("language", "haskell", "unknown language/module"),
    ("order", 0, "order"),
    ("title", "", "required"),
    ("checks", [{"type": "shell"}], "unknown check"),
    ("checks", [None], "mapping"),
    ("checks", [{"type": "command", "args": "rm -rf"}], "args"),
    ("checks", [{"type": "command", "args": ["x"], "timeout": -1}], "timeout"),
    ("docs", "no-such-file.md", "missing documentation"),
    ("files", {"../escape": "x"}, "inside"),
    ("project", "../../x", "project"),
])
def test_invalid_course_errors(lab, field, value, match):
    path = lab.config.root / "content/scala/exercises/scala-hello.yaml"
    data = yaml.safe_load(path.read_text())
    data[field] = value
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(LabError, match=match):
        Catalog(lab.config.root)


def test_duplicate_and_unknown_fields(lab):
    original = lab.config.root / "content/scala/exercises/scala-hello.yaml"
    (original.parent / "duplicate.yaml").write_text(original.read_text())
    with pytest.raises(LabError, match="duplicate"):
        Catalog(lab.config.root)


def test_markdown_links_resolve(catalog):
    for module in catalog.modules:
        path = catalog.root / "content" / module["docs"]
        for link in re.findall(r"\]\(([^)]+\.md)\)", path.read_text()):
            assert (path.parent / link).is_file(), (path, link)


@pytest.mark.parametrize("relative", ["../outside", "/etc/passwd", "."])
def test_path_traversal_rejected(tmp_path, relative):
    with pytest.raises(LabError):
        inside(tmp_path, relative)


def test_symlink_escape_rejected(tmp_path):
    (tmp_path / "escape").symlink_to(Path("/etc"), target_is_directory=True)
    with pytest.raises(LabError):
        inside(tmp_path, "escape/passwd")
