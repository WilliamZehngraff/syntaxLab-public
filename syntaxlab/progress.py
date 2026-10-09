"""All SQL lives here. DELETE journaling keeps Git sync predictable."""
from contextlib import closing
from pathlib import Path
import json
import sqlite3
from syntaxlab.config import LabError
from syntaxlab.courses import Catalog
from syntaxlab.languages import LANGUAGES

MIGRATIONS = ["""
CREATE TABLE languages (id TEXT PRIMARY KEY);
CREATE TABLE modules (language TEXT, id TEXT, title TEXT, PRIMARY KEY(language,id));
CREATE TABLE exercises (id TEXT PRIMARY KEY, language TEXT, module TEXT, project TEXT);
CREATE TABLE attempts (id INTEGER PRIMARY KEY, exercise TEXT NOT NULL, passed INTEGER NOT NULL,
 details TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE completions (exercise TEXT PRIMARY KEY, completed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE state (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE project_stages (exercise TEXT PRIMARY KEY, project TEXT NOT NULL);
CREATE TABLE encounters (kind TEXT, item TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY(kind,item));
"""]


class Progress:
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self.connect()) as db:
            version = db.execute("PRAGMA user_version").fetchone()[0]
            if version > len(MIGRATIONS):
                raise LabError("Progress database is newer than this SyntaxLab; update the application")
            for index in range(version, len(MIGRATIONS)):
                db.executescript("BEGIN IMMEDIATE;\n" + MIGRATIONS[index]
                                 + f"\nPRAGMA user_version={index + 1};\nCOMMIT;")

    def connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path, timeout=10)
        db.execute("PRAGMA foreign_keys=ON")
        return db

    def sync(self, catalog: Catalog) -> None:
        with closing(self.connect()) as db, db:
            for language in LANGUAGES:
                db.execute("INSERT OR IGNORE INTO languages VALUES (?)", (language,))
            for m in catalog.modules:
                db.execute("INSERT INTO modules VALUES (?,?,?) ON CONFLICT(language,id) DO UPDATE SET "
                           "title=excluded.title WHERE title<>excluded.title", (m["language"], m["id"], m["title"]))
            for e in catalog.exercises.values():
                db.execute("INSERT INTO exercises VALUES (?,?,?,?) ON CONFLICT(id) DO UPDATE SET "
                           "language=excluded.language,module=excluded.module,project=excluded.project "
                           "WHERE language<>excluded.language OR module<>excluded.module OR project<>excluded.project",
                           (e.id, e.language, e.module, e.project))
                if e.project:
                    db.execute("INSERT OR IGNORE INTO project_stages VALUES (?,?)", (e.id, e.project))

    def completed(self) -> set[str]:
        with closing(self.connect()) as db:
            return {r[0] for r in db.execute("SELECT exercise FROM completions")}

    def get(self, key: str) -> str | None:
        with closing(self.connect()) as db:
            row = db.execute("SELECT value FROM state WHERE key=?", (key,)).fetchone()
            return row[0] if row else None

    def set(self, key: str, value: str) -> None:
        with closing(self.connect()) as db, db:
            db.execute("INSERT INTO state VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value "
                       "WHERE value<>excluded.value", (key, value))

    def record(self, exercise: str, passed: bool, details: list[dict]) -> None:
        with closing(self.connect()) as db, db:
            db.execute("INSERT INTO attempts(exercise,passed,details) VALUES (?,?,?)",
                       (exercise, passed, json.dumps(details)))
            if passed:
                db.execute("INSERT OR IGNORE INTO completions(exercise) VALUES (?)", (exercise,))

    def encounter(self, kind: str, item: str) -> None:
        with closing(self.connect()) as db, db:
            db.execute("INSERT OR IGNORE INTO encounters(kind,item) VALUES (?,?)", (kind, item))

    def reset(self, ids: list[str]) -> None:
        with closing(self.connect()) as db, db:
            db.executemany("DELETE FROM completions WHERE exercise=?", [(i,) for i in ids])

    def healthy(self) -> bool:
        with closing(self.connect()) as db:
            return db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"


def percentage(ids: list[str], completed: set[str]) -> int:
    return round(100 * len(set(ids) & completed) / len(ids)) if ids else 0
