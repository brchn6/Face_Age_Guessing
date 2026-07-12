"""SQLite database for the Face Age Guessing experiment.

Schema follows the research data model from .agents/project-handoff.md.
"""

from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DB_PATH = Path("data/experiment.db")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS participant_sessions (
            session_id      TEXT PRIMARY KEY,
            participant_age INTEGER NOT NULL,
            participant_age_group TEXT NOT NULL,
            participant_gender   TEXT NOT NULL,
            has_child_exposure   INTEGER,  -- 0=false 1=true NULL=prefer_not_to_say
            experiment_version   TEXT NOT NULL,
            device_type     TEXT NOT NULL,
            started_at      TEXT NOT NULL,
            completed_at    TEXT,
            status          TEXT NOT NULL DEFAULT 'created'
        );

        CREATE TABLE IF NOT EXISTS participant_child_exposure (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id      TEXT NOT NULL REFERENCES participant_sessions(session_id),
            child_age_bin   TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS face_images (
            face_id         TEXT PRIMARY KEY,
            image_url       TEXT NOT NULL,
            true_age        INTEGER NOT NULL,
            true_age_bin    TEXT NOT NULL,
            face_gender     TEXT NOT NULL DEFAULT 'unknown',
            source_dataset  TEXT NOT NULL,
            license_type    TEXT NOT NULL,
            is_active       INTEGER NOT NULL DEFAULT 1,
            quality_score   REAL NOT NULL DEFAULT 0,
            created_at      TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS trial_assignments (
            trial_id        TEXT PRIMARY KEY,
            session_id      TEXT NOT NULL REFERENCES participant_sessions(session_id),
            face_id         TEXT NOT NULL REFERENCES face_images(face_id),
            trial_index     INTEGER NOT NULL,
            assigned_at     TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS responses (
            response_id     TEXT PRIMARY KEY,
            trial_id        TEXT NOT NULL REFERENCES trial_assignments(trial_id),
            session_id      TEXT NOT NULL REFERENCES participant_sessions(session_id),
            face_id         TEXT NOT NULL REFERENCES face_images(face_id),
            predicted_age   INTEGER NOT NULL,
            response_time_ms INTEGER NOT NULL,
            submitted_at    TEXT NOT NULL,
            client_order_index INTEGER NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_child_exposure_session
            ON participant_child_exposure(session_id);
        CREATE INDEX IF NOT EXISTS idx_trial_assignments_session
            ON trial_assignments(session_id);
        CREATE INDEX IF NOT EXISTS idx_responses_session
            ON responses(session_id);
    """)
    conn.commit()
    conn.close()


# ── Operations ──────────────────────────────────────────────────────────


def seed_face_images(images: list[dict]) -> int:
    """Insert face images from the app manifest. Returns count inserted."""
    conn = get_connection()
    count = 0
    for img in images:
        try:
            conn.execute(
                """INSERT OR IGNORE INTO face_images
                   (face_id, image_url, true_age, true_age_bin, face_gender,
                    source_dataset, license_type, is_active, quality_score, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (
                    img["face_id"],
                    img["image_url"],
                    img["true_age"],
                    img["true_age_bin"],
                    img.get("face_gender", "unknown"),
                    img.get("source_dataset", ""),
                    img.get("license_type", ""),
                    1 if img.get("is_active") else 0,
                    img.get("quality_score", 0),
                    img.get("created_at", _now_iso()),
                ),
            )
            count += conn.total_changes
        except Exception:
            pass
    conn.commit()
    conn.close()
    return count


def create_session(
    participant_age: int,
    participant_gender: str,
    has_child_exposure: Optional[bool],
    experiment_version: str,
    device_type: str,
) -> str:
    session_id = _uid("session")
    age_group = _compute_age_group(participant_age)
    started_at = _now_iso()
    conn = get_connection()
    conn.execute(
        """INSERT INTO participant_sessions
           (session_id, participant_age, participant_age_group, participant_gender,
            has_child_exposure, experiment_version, device_type, started_at, status)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (
            session_id,
            participant_age,
            age_group,
            participant_gender,
            None if has_child_exposure is None else (1 if has_child_exposure else 0),
            experiment_version,
            device_type,
            started_at,
            "active",
        ),
    )
    conn.commit()
    conn.close()
    return session_id


def add_child_exposure(session_id: str, child_age_bins: list[str]) -> None:
    if not child_age_bins:
        return
    conn = get_connection()
    conn.executemany(
        "INSERT INTO participant_child_exposure (session_id, child_age_bin) VALUES (?,?)",
        [(session_id, b) for b in child_age_bins],
    )
    conn.commit()
    conn.close()


def create_trial_assignments(
    session_id: str, face_ids: list[str]
) -> list[dict]:
    assigned_at = _now_iso()
    conn = get_connection()
    trials = []
    for i, face_id in enumerate(face_ids, start=1):
        trial_id = _uid("trial")
        conn.execute(
            "INSERT INTO trial_assignments (trial_id, session_id, face_id, trial_index, assigned_at) VALUES (?,?,?,?,?)",
            (trial_id, session_id, face_id, i, assigned_at),
        )
        trials.append({"trial_id": trial_id, "face_id": face_id, "trial_index": i})
    conn.commit()
    conn.close()
    return trials


def submit_response(
    session_id: str,
    trial_id: str,
    face_id: str,
    predicted_age: int,
    response_time_ms: int,
    client_order_index: int,
) -> dict:
    response_id = _uid("response")
    submitted_at = _now_iso()
    conn = get_connection()
    conn.execute(
        """INSERT INTO responses
           (response_id, trial_id, session_id, face_id, predicted_age,
            response_time_ms, submitted_at, client_order_index)
           VALUES (?,?,?,?,?,?,?,?)""",
        (response_id, trial_id, session_id, face_id, predicted_age, response_time_ms,
         submitted_at, client_order_index),
    )
    conn.commit()
    conn.close()
    return {"response_id": response_id}


def complete_session(session_id: str) -> None:
    conn = get_connection()
    conn.execute(
        "UPDATE participant_sessions SET completed_at=?, status='completed' WHERE session_id=?",
        (_now_iso(), session_id),
    )
    conn.commit()
    conn.close()


def get_session_state(session_id: str) -> Optional[dict]:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM participant_sessions WHERE session_id=?", (session_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ── Helpers ──────────────────────────────────────────────────────────────


def _compute_age_group(age: int) -> str:
    if age <= 12:
        return "4-12"
    if age <= 17:
        return "13-17"
    if age <= 24:
        return "18-24"
    if age <= 34:
        return "25-34"
    if age <= 44:
        return "35-44"
    if age <= 54:
        return "45-54"
    if age <= 64:
        return "55-64"
    return "65+"
