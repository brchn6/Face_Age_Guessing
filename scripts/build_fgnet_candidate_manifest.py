#!/usr/bin/env python3
"""Build a local-only candidate manifest for the FG-NET archive.

This script does not extract images and does not approve FG-NET for deployment.
It scans the gitignored local archive and writes manifest/summary files under
`data/manifests/`, which is also ignored through the repository's `data/` rule.
"""

from __future__ import annotations

import csv
import json
import re
import zipfile
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

ARCHIVE_PATH = Path("data/raw/fgnet/FGNET.zip")
OUTPUT_DIR = Path("data/manifests")
MANIFEST_PATH = OUTPUT_DIR / "fgnet_candidate_manifest.csv"
SUMMARY_PATH = OUTPUT_DIR / "fgnet_candidate_summary.json"

SOURCE_DATASET = "FG-NET Aging Database"
SOURCE_REFERENCE = "http://yanweifu.github.io/FG_NET_data/FGNET.zip"
TERMS_REFERENCE = "data/source_pages/fgnet_yanweifu.html"
LICENSE_TYPE = "rights_unverified_research_mirror"

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

FILENAME_RE = re.compile(r"^(?P<identity>\d{3})[Aa](?P<age>\d{1,3})(?P<suffix>[A-Za-z]?)\.(?:jpe?g|png)$", re.IGNORECASE)


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
    archive_member_path: str
    fgnet_identity_id: str


def age_bin(age: int) -> str:
    for label, low, high in MVP_BINS:
        if low <= age <= high:
            return label
    if age <= 3:
        return "0-3_outside_mvp"
    if age >= 61:
        return "61+_outside_mvp"
    return "outside_mvp"


def make_face_id(identity: str, age: int, suffix: str) -> str:
    suffix_part = suffix.lower() if suffix else ""
    return f"fgnet_{identity}_a{age:02d}{suffix_part}"


def iter_image_members(archive: zipfile.ZipFile) -> list[str]:
    return sorted(
        member
        for member in archive.namelist()
        if member.lower().startswith("fgnet/images/")
        and member.lower().endswith((".jpg", ".jpeg", ".png"))
    )


def build_rows() -> list[CandidateRow]:
    if not ARCHIVE_PATH.exists():
        raise FileNotFoundError(f"FG-NET archive not found: {ARCHIVE_PATH}")

    created_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    rows: list[CandidateRow] = []

    with zipfile.ZipFile(ARCHIVE_PATH) as archive:
        for member in iter_image_members(archive):
            filename = Path(member).name
            match = FILENAME_RE.match(filename)
            if not match:
                continue

            identity = match.group("identity")
            age = int(match.group("age"))
            suffix = match.group("suffix")

            rows.append(
                CandidateRow(
                    face_id=make_face_id(identity, age, suffix),
                    image_url=f"local_archive://{ARCHIVE_PATH}!/{member}",
                    true_age=age,
                    true_age_bin=age_bin(age),
                    face_gender="unknown",
                    source_dataset=SOURCE_DATASET,
                    license_type=LICENSE_TYPE,
                    is_active=False,
                    quality_score=0.0,
                    created_at=created_at,
                    source_record_id=filename,
                    source_url_or_reference=SOURCE_REFERENCE,
                    license_url_or_terms_reference=TERMS_REFERENCE,
                    usage_notes=(
                        "Candidate local-only record. Rights and public web-display permission "
                        "are unresolved; do not integrate into app."
                    ),
                    attribution_required="unknown",
                    web_display_allowed=False,
                    commercial_use_allowed=False,
                    research_use_allowed="unverified_mirror_claims_research_use",
                    age_at_photo_verified="filename_encoded_unverified",
                    image_processed_at="",
                    archive_member_path=member,
                    fgnet_identity_id=identity,
                )
            )

    return rows


def write_manifest(rows: list[CandidateRow]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = list(asdict(rows[0]).keys()) if rows else list(CandidateRow.__dataclass_fields__)

    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_summary(rows: list[CandidateRow]) -> None:
    age_counts = Counter(row.true_age for row in rows)
    bin_counts = Counter(row.true_age_bin for row in rows)
    identity_counts = Counter(row.fgnet_identity_id for row in rows)

    summary = {
        "source_dataset": SOURCE_DATASET,
        "archive_path": str(ARCHIVE_PATH),
        "manifest_path": str(MANIFEST_PATH),
        "total_candidate_images": len(rows),
        "unique_identities": len(identity_counts),
        "min_age": min(age_counts) if age_counts else None,
        "max_age": max(age_counts) if age_counts else None,
        "mvp_bin_counts": {label: bin_counts[label] for label, _, _ in MVP_BINS},
        "outside_mvp_counts": {
            label: count
            for label, count in sorted(bin_counts.items())
            if label not in {mvp_label for mvp_label, _, _ in MVP_BINS}
        },
        "active_records": 0,
        "active_records_reason": "All records are inactive because rights/web-display permission are unresolved.",
        "largest_identity_image_counts": identity_counts.most_common(10),
    }

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    if not rows:
        raise RuntimeError("No FG-NET image rows parsed from archive")

    write_manifest(rows)
    write_summary(rows)
    print(f"Wrote {len(rows)} candidate rows to {MANIFEST_PATH}")
    print(f"Wrote summary to {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
