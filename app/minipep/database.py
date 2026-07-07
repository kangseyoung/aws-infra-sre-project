import os
import sqlite3
from pathlib import Path


DB_PATH = Path(os.getenv("MINIPEP_DB_PATH", "data/minipep.db"))


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    with connect() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                location TEXT,
                status TEXT NOT NULL DEFAULT 'available',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipment_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'queued',
                priority TEXT NOT NULL DEFAULT 'normal',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                completed_at TEXT,
                FOREIGN KEY(equipment_id) REFERENCES equipment(id)
            );
            """
        )
        seed_if_empty(db)


def seed_if_empty(db: sqlite3.Connection) -> None:
    equipment_count = db.execute("SELECT COUNT(*) FROM equipment").fetchone()[0]
    if equipment_count:
        return

    db.executescript(
        """
        INSERT INTO equipment (name, type, location, status, created_at, updated_at)
        VALUES
          ('Mixer-01', 'Mixer', 'Line A', 'running', datetime('now'), datetime('now')),
          ('Press-02', 'Hydraulic Press', 'Line B', 'available', datetime('now'), datetime('now')),
          ('Conveyor-03', 'Conveyor', 'Packaging', 'maintenance', datetime('now'), datetime('now'));

        INSERT INTO jobs (equipment_id, title, description, status, priority, created_at, updated_at, completed_at)
        VALUES
          (1, 'Morning production run', 'Batch PEP-1001', 'in_progress', 'high', datetime('now'), datetime('now'), NULL),
          (2, 'Inspect pressure gauge', 'Routine pre-shift check', 'queued', 'normal', datetime('now'), datetime('now'), NULL),
          (3, 'Replace belt sensor', 'Maintenance ticket from packaging line', 'completed', 'urgent', datetime('now'), datetime('now'), datetime('now'));
        """
    )
