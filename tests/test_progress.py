from contextlib import closing
import sqlite3
import pytest
from syntaxlab.config import LabError
from syntaxlab.progress import MIGRATIONS, Progress, percentage
from syntaxlab.languages import LANGUAGES


def test_persist_attempt_completion_state_and_encounters(tmp_path):
    path = tmp_path / "progress.db"
    p = Progress(path)
    p.record("lesson", False, [{"message": "compile error"}])
    assert not p.completed()
    p.record("lesson", True, [{"message": "success"}])
    p.set("current", "lesson")
    p.encounter("hint", "lesson:1")
    fresh = Progress(path)
    assert fresh.completed() == {"lesson"}
    assert fresh.get("current") == "lesson"
    with closing(fresh.connect()) as db:
        assert db.execute("SELECT count(*) FROM attempts").fetchone()[0] == 2
        assert db.execute("SELECT completed_at FROM completions").fetchone()[0]
        assert db.execute("PRAGMA journal_mode").fetchone()[0] == "delete"
    assert fresh.healthy()
    assert not list(tmp_path.glob("*.db-*"))


def test_read_only_dashboard_does_not_rewrite_database(lab):
    lab.progress.set("current", "scala-hello")
    before = lab.progress.path.read_bytes()
    stat = lab.progress.path.stat().st_mtime_ns
    p = Progress(lab.progress.path)
    p.sync(lab.catalog)
    p.get("current")
    p.completed()
    p.healthy()
    p.set("current", "scala-hello")
    assert p.path.read_bytes() == before
    assert p.path.stat().st_mtime_ns == stat


def test_migration_preserves_progress(tmp_path, monkeypatch):
    path = tmp_path / "progress.db"
    p = Progress(path)
    p.record("x", True, [])
    monkeypatch.setattr("syntaxlab.progress.MIGRATIONS", [*MIGRATIONS, "CREATE TABLE future (id INTEGER);"])
    upgraded = Progress(path)
    assert upgraded.completed() == {"x"}
    with closing(upgraded.connect()) as db:
        assert db.execute("PRAGMA user_version").fetchone()[0] == 2
        assert db.execute("SELECT * FROM future").fetchall() == []


def test_reject_future_schema(tmp_path):
    path = tmp_path / "new.db"
    with closing(sqlite3.connect(path)) as db:
        db.execute("PRAGMA user_version=999")
    with pytest.raises(LabError, match="newer"):
        Progress(path)


def test_percentage_and_reset(lab):
    assert percentage([], set()) == 0
    assert percentage(["a", "b", "c", "d"], {"a", "b", "unrelated"}) == 50
    lab.progress.record("c-hello", True, [])
    assert lab.catalog.unlocked(lab.catalog.exercises["c-variables"], lab.progress.completed())
    lab.progress.reset(["c-hello"])
    assert not lab.catalog.unlocked(lab.catalog.exercises["c-variables"], lab.progress.completed())


def test_catalog_metadata_persisted(lab):
    with closing(lab.progress.connect()) as db:
        assert db.execute("SELECT count(*) FROM languages").fetchone()[0] == len(LANGUAGES)
        assert db.execute("SELECT count(*) FROM modules").fetchone()[0] == len(lab.catalog.modules)
        assert db.execute("SELECT count(*) FROM project_stages").fetchone()[0] == sum(
            bool(e.project) for e in lab.catalog.exercises.values())
