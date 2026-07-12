#!/usr/bin/env python3
"""Build a local-only candidate manifest for fetched FACES metadata.

This script uses FACES/imeji metadata JSON under `data/raw/faces_lifespan/api/`.
It does not download image files and does not approve FACES for deployment.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

INPUT_GLOB = "items_*.json"
API_DIR = Path("data/raw/faces_lifespan/api")
OUTPUT_DIR = Path("data/manifests")
MANIFEST_PATH = OUTPUT_DIR / "faces_lifespan_candidate_manifest.csv"
SUMMARY_PATH = OUTPUT_DIR / "faces_lifespan_candidate_summary.json"

SOURCE_DATASET = "FACES Lifespan Database public/API metadata"
TERMS_REFERENCE = "data/source_pages/faces_lifespan.html"
LICENSE_TYPE = "account_or_release_agreement_required"

MVP_BINS: tuple[tuple[str, int, int], ...] = (
    ("4-6", 4, 6),
    ("7-9", 7, 9),
    ("10-12", 10, 12),
    ("13-17", 13, 17),
    ("18-24", 18, 24),
    ("25-31", 25, 31),
    ("32-38", 32, 38),
    ("39-45", 39, 45),
    ("46-52", 46, 52),
    ("53-60", 53, 60),
)


@dataclass(frozen=True)
class CandidateRow:
    face_id: str
    image_url: str
    true_age: int
    true_age_bin: str
    face_gender: str
    source_dataset: str
    license_type: str
    is_active: bool
    quality_score: float
    created_at: str
    source_record_id: str
    source_url_or_reference: str
    license_url_or_terms_reference: str
    usage_notes: str
    attribution_required: str
    web_display_allowed: bool
    commercial_use_allowed: bool
    research_use_allowed: str
    age_at_photo_verified: str
    image_processed_at: str
    item_id: str
    filename: str
    emotion: str
    picture_group: str
    person_id: str
    age_group: str


def metadata_dict(item: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for row in item.get("metadata", []):
        out[row["index"]] = row.get("text", row.get("number"))
    return out


def age_bin(age: int) -> str:
    for label, low, high in MVP_BINS:
        if low <= age <= high:
            return label
    if age <= 3:
        return "0-3_outside_mvp"
    if age >= 61:
        return "61+_outside_mvp"
    return "outside_mvp"


def source_files() -> list[Path]:
    return sorted(API_DIR.glob(INPUT_GLOB))


def build_rows() -> list[CandidateRow]:
    created_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    rows: list[CandidateRow] = []
    seen_ids: set[str] = set()

    for path in source_files():
        payload = json.loads(path.read_text(encoding="utf-8"))
        for item in payload.get("results", []):
            if item["id"] in seen_ids:
                continue
            seen_ids.add(item["id"])
            md = metadata_dict(item)
            age_value = md.get("age")
            if age_value is None:
                continue
            true_age = int(float(age_value))
            person_id = str(md.get("person ID", "unknown"))
            filename = item.get("filename", item["id"])
            emotion = str(md.get("emotion", "unknown"))
            picture_group = str(md.get("picture group", "unknown"))

            rows.append(
                CandidateRow(
                    face_id=f"faces_{item['id']}",
                    image_url=item.get("fileUrl", ""),
                    true_age=true_age,
                    true_age_bin=age_bin(true_age),
                    face_gender=str(md.get("gender", "unknown")),
                    source_dataset=SOURCE_DATASET,
                    license_type=LICENSE_TYPE,
                    is_active=False,
                    quality_score=0.0,
                    created_at=created_at,
                    source_record_id=filename,
                    source_url_or_reference=item.get("fileUrl", ""),
                    license_url_or_terms_reference=TERMS_REFERENCE,
                    usage_notes=(
                        "Candidate metadata-only record. Public preview/API access does not equal "
                        "approval for app integration; confirm release agreement and web-display rights."
                    ),
                    attribution_required="yes_citation_required_per_source_page",
                    web_display_allowed=False,
                    commercial_use_allowed=False,
                    research_use_allowed="requires_terms_review_or_release_agreement",
                    age_at_photo_verified="metadata_age_unverified_by_project",
                    image_processed_at="",
                    item_id=item["id"],
                    filename=filename,
                    emotion=emotion,
                    picture_group=picture_group,
                    person_id=person_id,
                    age_group=str(md.get("age group", "unknown")),
                )
            )
    return rows


def main() -> None:
    rows = build_rows()
    if not rows:
        raise RuntimeError("No FACES candidate rows parsed")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))

    by_bin: dict[str, int] = {}
    by_age: dict[str, int] = {}
    by_person: dict[str, int] = {}
    for row in rows:
        by_bin[row.true_age_bin] = by_bin.get(row.true_age_bin, 0) + 1
        by_age[str(row.true_age)] = by_age.get(str(row.true_age), 0) + 1
        by_person[row.person_id] = by_person.get(row.person_id, 0) + 1

    summary = {
        "source_dataset": SOURCE_DATASET,
        "manifest_path": str(MANIFEST_PATH),
        "total_candidate_items": len(rows),
        "unique_person_ids": len(by_person),
        "mvp_bin_counts": {label: by_bin.get(label, 0) for label, _, _ in MVP_BINS},
        "outside_mvp_counts": {
            label: count
            for label, count in sorted(by_bin.items())
            if label not in {mvp_label for mvp_label, _, _ in MVP_BINS}
        },
        "age_counts": dict(sorted(by_age.items(), key=lambda item: int(item[0]))),
        "person_image_counts": dict(sorted(by_person.items())),
        "active_records": 0,
        "active_records_reason": "All records are inactive pending release agreement / web-display approval.",
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Wrote {len(rows)} candidate rows to {MANIFEST_PATH}")
    print(f"Wrote summary to {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
