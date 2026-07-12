"""FastAPI backend for Face Age Guessing experiment."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import database as db
from . import analytics

app = FastAPI(title="Face Age Guessing API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request / Response models ──────────────────────────────────────────


class SessionRequest(BaseModel):
    participant_age: int
    participant_gender: str
    has_child_exposure: Optional[bool] = None
    child_age_bins: list[str] = []
    device_type: str = "desktop"
    experiment_version: str


class TrialAssignmentOut(BaseModel):
    trial_id: str
    trial_index: int
    face_id: str
    image_url: str


class SessionResponse(BaseModel):
    session_id: str
    assigned_trials: list[TrialAssignmentOut]


class ResponseRequest(BaseModel):
    session_id: str
    trial_id: str
    face_id: str
    predicted_age: int
    response_time_ms: int
    client_order_index: int


class CompleteRequest(BaseModel):
    session_id: str


class StatusResponse(BaseModel):
    ok: bool
    status: Optional[str] = None


# ── Endpoints ────────────────────────────────────────────────────────


@app.on_event("startup")
async def startup() -> None:
    db.init_db()
    _seed_from_manifest()


@app.post("/api/session", response_model=SessionResponse)
async def create_session(req: SessionRequest) -> SessionResponse:
    session_id = db.create_session(
        participant_age=req.participant_age,
        participant_gender=req.participant_gender,
        has_child_exposure=req.has_child_exposure,
        experiment_version=req.experiment_version,
        device_type=req.device_type,
    )
    db.add_child_exposure(session_id, req.child_age_bins)

    # Sample: get active face images from DB, pick one per bin
    face_ids = _sample_one_per_bin()
    trials = db.create_trial_assignments(session_id, face_ids)

    # Resolve image URLs
    face_urls = _lookup_face_urls(face_ids)

    assigned = []
    for idx, trial in enumerate(trials):
        fid = trial["face_id"]
        assigned.append(
            TrialAssignmentOut(
                trial_id=trial["trial_id"],
                trial_index=trial["trial_index"],
                face_id=fid,
                image_url=face_urls.get(fid, ""),
            )
        )

    return SessionResponse(session_id=session_id, assigned_trials=assigned)


@app.post("/api/response")
async def submit_response(req: ResponseRequest) -> StatusResponse:
    db.submit_response(
        session_id=req.session_id,
        trial_id=req.trial_id,
        face_id=req.face_id,
        predicted_age=req.predicted_age,
        response_time_ms=req.response_time_ms,
        client_order_index=req.client_order_index,
    )
    return StatusResponse(ok=True)


@app.post("/api/session/complete")
async def complete_session(req: CompleteRequest) -> StatusResponse:
    db.complete_session(req.session_id)
    return StatusResponse(ok=True, status="completed")


@app.get("/api/analytics")
async def get_analytics() -> dict:
    return analytics.get_analytics()


# ── Sampling ──────────────────────────────────────────────────────────


MVP_BINS = [
    "4-6", "7-9", "10-12", "13-17", "18-24",
    "25-31", "32-38", "39-45", "46-52", "53-60",
]


def _sample_one_per_bin() -> list[str]:
    conn = db.get_connection()
    face_ids: list[str] = []
    for bin_label in MVP_BINS:
        row = conn.execute(
            """SELECT face_id FROM face_images
               WHERE is_active=1 AND true_age_bin=?
               ORDER BY RANDOM() LIMIT 1""",
            (bin_label,),
        ).fetchone()
        if row:
            face_ids.append(row["face_id"])
    conn.close()
    return face_ids


def _lookup_face_urls(face_ids: list[str]) -> dict[str, str]:
    if not face_ids:
        return {}
    conn = db.get_connection()
    placeholders = ",".join("?" for _ in face_ids)
    rows = conn.execute(
        f"SELECT face_id, image_url FROM face_images WHERE face_id IN ({placeholders})",
        face_ids,
    ).fetchall()
    conn.close()
    return {r["face_id"]: r["image_url"] for r in rows}


# ── Seed from manifest ────────────────────────────────────────────────


def _seed_from_manifest() -> None:
    """Load face images from the frontend manifest into the database."""
    manifest_path = Path("frontend/src/faceManifest.ts")
    if not manifest_path.exists():
        return

    raw = manifest_path.read_text(encoding="utf-8")

    # Extract the JSON array after "export const FACE_IMAGES"
    import re, json

    match = re.search(r"export const FACE_IMAGES[^=]*=\s*(\[[\s\S]*?\]);", raw)
    if not match:
        return

    try:
        images = json.loads(match.group(1))
    except json.JSONDecodeError:
        return

    count = db.seed_face_images(images)
    if count > 0:
        print(f"Seeded {count} face images into database")
