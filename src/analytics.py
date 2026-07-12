"""Research analytics and data quality for Face Age Guessing experiment.

Computes metrics directly from the SQLite database.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Optional

from . import database as db


def get_analytics() -> dict[str, Any]:
    """Return research and operational metrics."""
    conn = db.get_connection()

    total_sessions = conn.execute(
        "SELECT COUNT(*) FROM participant_sessions"
    ).fetchone()[0]
    completed = conn.execute(
        "SELECT COUNT(*) FROM participant_sessions WHERE status='completed'"
    ).fetchone()[0]
    abandoned = conn.execute(
        "SELECT COUNT(*) FROM participant_sessions WHERE status='active'"
    ).fetchone()[0]
    total_responses = conn.execute("SELECT COUNT(*) FROM responses").fetchone()[0]

    # --- MAE by participant age group ---
    mae_by_participant_group = _rows_to_list(
        conn.execute(
            """SELECT ps.participant_age_group,
                      ROUND(AVG(ABS(r.predicted_age - fi.true_age)), 2) AS mae,
                      COUNT(*) AS n
               FROM responses r
               JOIN participant_sessions ps ON r.session_id = ps.session_id
               JOIN face_images fi ON r.face_id = fi.face_id
               WHERE ps.status = 'completed'
               GROUP BY ps.participant_age_group
               ORDER BY ps.participant_age_group"""
        ).fetchall()
    )

    # --- MAE by face age bin ---
    mae_by_face_bin = _rows_to_list(
        conn.execute(
            """SELECT fi.true_age_bin,
                      ROUND(AVG(ABS(r.predicted_age - fi.true_age)), 2) AS mae,
                      COUNT(*) AS n
               FROM responses r
               JOIN participant_sessions ps ON r.session_id = ps.session_id
               JOIN face_images fi ON r.face_id = fi.face_id
               WHERE ps.status = 'completed'
               GROUP BY fi.true_age_bin
               ORDER BY fi.true_age_bin"""
        ).fetchall()
    )

    # --- MAE heatmap: participant age group × face age bin ---
    heatmap = _rows_to_list(
        conn.execute(
            """SELECT ps.participant_age_group,
                      fi.true_age_bin,
                      ROUND(AVG(ABS(r.predicted_age - fi.true_age)), 2) AS mae,
                      COUNT(*) AS n
               FROM responses r
               JOIN participant_sessions ps ON r.session_id = ps.session_id
               JOIN face_images fi ON r.face_id = fi.face_id
               WHERE ps.status = 'completed'
               GROUP BY ps.participant_age_group, fi.true_age_bin
               ORDER BY ps.participant_age_group, fi.true_age_bin"""
        ).fetchall()
    )

    # --- Bias ---
    bias = conn.execute(
        """SELECT ROUND(AVG(r.predicted_age - fi.true_age), 3) AS mean_signed_error,
                  COUNT(*) AS n
           FROM responses r
           JOIN participant_sessions ps ON r.session_id = ps.session_id
           JOIN face_images fi ON r.face_id = fi.face_id
           WHERE ps.status = 'completed'"""
    ).fetchone()

    # --- Compression: slope of predicted_age ~ true_age ---
    slope_row = conn.execute(
        """SELECT ROUND(
                  (COUNT(*) * SUM(fi.true_age * r.predicted_age) - SUM(fi.true_age) * SUM(r.predicted_age))
                  / (COUNT(*) * SUM(fi.true_age * fi.true_age) - SUM(fi.true_age) * SUM(fi.true_age)),
                  4
                ) AS slope,
                COUNT(*) AS n
           FROM responses r
           JOIN participant_sessions ps ON r.session_id = ps.session_id
           JOIN face_images fi ON r.face_id = fi.face_id
           WHERE ps.status = 'completed'"""
    ).fetchone()

    # --- Child exposure MAE ---
    child_exposure_mae = _rows_to_list(
        conn.execute(
            """SELECT CASE
                      WHEN ps.has_child_exposure = 1 THEN 'Yes'
                      WHEN ps.has_child_exposure = 0 THEN 'No'
                      ELSE 'Prefer not to say'
                    END AS exposure,
                    ROUND(AVG(ABS(r.predicted_age - fi.true_age)), 2) AS mae,
                    COUNT(*) AS n
               FROM responses r
               JOIN participant_sessions ps ON r.session_id = ps.session_id
               JOIN face_images fi ON r.face_id = fi.face_id
               WHERE ps.status = 'completed'
               GROUP BY ps.has_child_exposure
               ORDER BY ps.has_child_exposure"""
        ).fetchall()
    )

    # --- Response time distribution ---
    rt_stats = conn.execute(
        """SELECT MIN(response_time_ms), MAX(response_time_ms),
                  ROUND(AVG(response_time_ms)), COUNT(*)
           FROM responses r
           JOIN participant_sessions ps ON r.session_id = ps.session_id
           WHERE ps.status = 'completed'"""
    ).fetchone()

    # --- Data quality flags ---
    quality_flags = {
        "too_fast_responses": conn.execute(
            "SELECT COUNT(*) FROM responses WHERE response_time_ms < 300"
        ).fetchone()[0],
        "too_slow_responses": conn.execute(
            "SELECT COUNT(*) FROM responses WHERE response_time_ms > 60000"
        ).fetchone()[0],
        "sessions_too_fast": conn.execute(
            """SELECT COUNT(*) FROM participant_sessions
               WHERE status='completed'
               AND (julianday(completed_at) - julianday(started_at)) * 86400 < 5"""
        ).fetchone()[0],
        "sessions_under_10_seconds": conn.execute(
            """SELECT COUNT(*) FROM participant_sessions
               WHERE status='completed'
               AND (julianday(completed_at) - julianday(started_at)) * 86400 < 10"""
        ).fetchone()[0],
    }

    # --- Low-effort detection: same guess for all 10 responses ---
    low_effort_sessions = conn.execute(
        """SELECT COUNT(DISTINCT session_id) FROM (
               SELECT session_id, COUNT(DISTINCT predicted_age) as distinct_guesses
               FROM responses GROUP BY session_id
               HAVING distinct_guesses = 1
           )"""
    ).fetchone()[0]
    quality_flags["low_effort_all_same_guess"] = low_effort_sessions

    # --- Per-session average response time ---
    avg_session_duration = conn.execute(
        """SELECT ROUND(AVG((julianday(completed_at) - julianday(started_at)) * 86400), 1)
           FROM participant_sessions WHERE status='completed'"""
    ).fetchone()[0]

    # --- Device split ---
    device_split = _rows_to_list(
        conn.execute(
            """SELECT device_type, COUNT(*) as n
               FROM participant_sessions
               WHERE status='completed'
               GROUP BY device_type"""
        ).fetchall()
    )

    # --- Gender split ---
    gender_split = _rows_to_list(
        conn.execute(
            """SELECT participant_gender, COUNT(*) as n
               FROM participant_sessions
               WHERE status='completed'
               GROUP BY participant_gender"""
        ).fetchall()
    )

    conn.close()

    return {
        "operational": {
            "total_sessions": total_sessions,
            "completed_sessions": completed,
            "abandoned_sessions": abandoned,
            "completion_rate_pct": round(completed / total_sessions * 100, 1) if total_sessions else 0,
            "total_responses": total_responses,
            "avg_session_duration_sec": avg_session_duration,
            "device_split": device_split,
            "gender_split": gender_split,
        },
        "research": {
            "mae_by_participant_age_group": mae_by_participant_group,
            "mae_by_face_age_bin": mae_by_face_bin,
            "mae_by_child_exposure": child_exposure_mae,
            "heatmap": heatmap,
            "overall_bias": {
                "mean_signed_error": bias["mean_signed_error"] if bias else None,
                "n": bias["n"] if bias else 0,
            },
            "compression": {
                "slope": slope_row["slope"] if slope_row and slope_row["n"] else None,
                "n": slope_row["n"] if slope_row else 0,
                "interpretation": _compression_interpretation(slope_row),
            },
        },
        "quality": {
            **quality_flags,
            "response_time_ms_min": rt_stats[0],
            "response_time_ms_max": rt_stats[1],
            "response_time_ms_avg": rt_stats[2],
            "response_count_for_timing": rt_stats[3],
        },
    }


def _compression_interpretation(slope_row: Optional[Any]) -> str:
    if not slope_row or not slope_row["n"]:
        return "Not enough data"
    slope = slope_row["slope"]
    if slope is None:
        return "Not enough data"
    if slope > 0.9:
        return "Excellent age differentiation (slope near 1)"
    if slope > 0.7:
        return "Moderate age differentiation"
    if slope > 0.5:
        return "Moderate age compression"
    return "Strong age compression — participants flatten age distinctions"


def _rows_to_list(rows: list) -> list[dict]:
    return [dict(r) for r in rows]
