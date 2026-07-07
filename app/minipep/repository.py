import sqlite3
from typing import Optional

from .models import EquipmentCreate, JobCreate, JobUpdate


def row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


def list_equipment(db: sqlite3.Connection) -> list[dict]:
    rows = db.execute("SELECT * FROM equipment ORDER BY id").fetchall()
    return [row_to_dict(row) for row in rows]


def create_equipment(db: sqlite3.Connection, payload: EquipmentCreate) -> dict:
    cursor = db.execute(
        """
        INSERT INTO equipment (name, type, location, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))
        """,
        (payload.name, payload.type, payload.location, payload.status),
    )
    db.commit()
    return get_equipment(db, cursor.lastrowid)


def get_equipment(db: sqlite3.Connection, equipment_id: int) -> dict:
    row = db.execute("SELECT * FROM equipment WHERE id = ?", (equipment_id,)).fetchone()
    if row is None:
        raise KeyError(equipment_id)
    return row_to_dict(row)


def list_jobs(db: sqlite3.Connection) -> list[dict]:
    rows = db.execute(
        """
        SELECT
            jobs.*,
            equipment.name AS equipment_name
        FROM jobs
        LEFT JOIN equipment ON equipment.id = jobs.equipment_id
        ORDER BY jobs.id DESC
        """
    ).fetchall()
    return [row_to_dict(row) for row in rows]


def create_job(db: sqlite3.Connection, payload: JobCreate) -> dict:
    validate_equipment(db, payload.equipment_id)
    completed_at_sql = "datetime('now')" if payload.status == "completed" else "NULL"
    cursor = db.execute(
        f"""
        INSERT INTO jobs (equipment_id, title, description, status, priority, created_at, updated_at, completed_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'), {completed_at_sql})
        """,
        (
            payload.equipment_id,
            payload.title,
            payload.description,
            payload.status,
            payload.priority,
        ),
    )
    db.commit()
    return get_job(db, cursor.lastrowid)


def get_job(db: sqlite3.Connection, job_id: int) -> dict:
    row = db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if row is None:
        raise KeyError(job_id)
    return row_to_dict(row)


def update_job(db: sqlite3.Connection, job_id: int, payload: JobUpdate) -> dict:
    validate_equipment(db, payload.equipment_id)
    get_job(db, job_id)
    completed_at_sql = "datetime('now')" if payload.status == "completed" else "NULL"
    db.execute(
        f"""
        UPDATE jobs
        SET equipment_id = ?,
            title = ?,
            description = ?,
            status = ?,
            priority = ?,
            updated_at = datetime('now'),
            completed_at = {completed_at_sql}
        WHERE id = ?
        """,
        (
            payload.equipment_id,
            payload.title,
            payload.description,
            payload.status,
            payload.priority,
            job_id,
        ),
    )
    db.commit()
    return get_job(db, job_id)


def delete_job(db: sqlite3.Connection, job_id: int) -> None:
    get_job(db, job_id)
    db.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    db.commit()


def validate_equipment(db: sqlite3.Connection, equipment_id: Optional[int]) -> None:
    if equipment_id is None:
        return
    if db.execute("SELECT id FROM equipment WHERE id = ?", (equipment_id,)).fetchone() is None:
        raise ValueError(f"equipment_id {equipment_id} does not exist")
