#!/usr/bin/env python3
"""Phase 6: Extract, rename, and manifest real images from FG-NET + CFD.

Output:
  frontend/public/faces/  — renamed neutral-ID images (gitignored)
  frontend/src/faceManifest.ts — TypeScript manifest for the app
"""

from __future__ import annotations

import csv
import json
import re
import io
import shutil
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# --- Configuration ---

FACES_OUT = Path("frontend/public/faces")
MANIFEST_OUT = Path("frontend/src/faceManifest.ts")

FGNET_ZIP = Path("data/raw/fgnet/FGNET.zip")
CFD_ZIP = Path("data/raw/chicago_faces/cfd.zip")

EXPERIMENT_VERSION = "mvp_004"
TODAY = datetime.now(UTC).strftime("%Y-%m-%d")

BINS: tuple[tuple[str, int, int], ...] = (
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

FGNET_FILENAME_RE = re.compile(
    r"^(?P<identity>\d{3})[Aa](?P<age>\d{1,3})(?P<suffix>[A-Za-z]?)\.(?:jpe?g|png)$",
    re.IGNORECASE,
)

# --- Helpers ---


def age_bin(age: int) -> str:
    for label, low, high in BINS:
        if low <= age <= high:
            return label
    if age <= 3:
        return "0-3_outside_mvp"
    if age >= 61:
        return "61+_outside_mvp"
    return "outside_mvp"


def safe_id(name: str) -> str:
    """Strip non-alphanumeric for TS identifiers."""
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)


# --- FG-NET ---


def process_fgnet(counter: int) -> list[dict[str, Any]]:
    print("Processing FG-NET...")
    entries: list[dict[str, Any]] = []
    with zipfile.ZipFile(FGNET_ZIP) as arch:
        members = sorted(
            m
            for m in arch.namelist()
            if m.lower().startswith("fgnet/images/") and m.lower().endswith((".jpg", ".jpeg", ".png"))
        )
        for member in members:
            filename = Path(member).name
            match = FGNET_FILENAME_RE.match(filename)
            if not match:
                continue
            identity = match.group("identity")
            age = int(match.group("age"))
            suffix = match.group("suffix") or ""

            face_id = f"face_{counter:06d}"
            dest_name = f"{face_id}.jpg"
            dest_path = FACES_OUT / dest_name

            with arch.open(member) as src, open(dest_path, "wb") as dst:
                shutil.copyfileobj(src, dst)

            abin = age_bin(age)

            entries.append(
                {
                    "face_id": face_id,
                    "image_url": f"/faces/{dest_name}",
                    "true_age": age,
                    "true_age_bin": abin,
                    "face_gender": "unknown",
                    "source_dataset": "FG-NET Aging Database",
                    "license_type": "rights_unverified_research_mirror",
                    "is_active": abin in {label for label, _, _ in BINS},
                    "quality_score": 0.5,
                    "created_at": f"{TODAY}T00:00:00.000Z",
                }
            )
            counter += 1
    print(f"  FG-NET: {len(entries)} images extracted")
    return entries


# --- CFD ---


def parse_cfd_norming_xlsx(zip_path: Path) -> dict[str, dict[str, Any]]:
    """Parse the CFD xlsx inside the zip to get Model → {age, gender, ethnicity}."""

    z = zipfile.ZipFile(zip_path)
    xlsx_path = [n for n in z.namelist() if n.endswith(".xlsx")][0]
    xlsx_z = zipfile.ZipFile(io.BytesIO(z.read(xlsx_path)))
    ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"

    # shared strings
    ss_root = ET.fromstring(xlsx_z.read("xl/sharedStrings.xml"))
    strings: list[str] = []
    for si in ss_root.findall(f"{{{ns}}}si"):
        t = si.find(f"{{{ns}}}t")
        if t is not None and t.text:
            strings.append(t.text)
        else:
            parts = [
                (r.find(f"{{{ns}}}t").text or "")
                for r in si.findall(f"{{{ns}}}r")
                if r.find(f"{{{ns}}}t") is not None
            ]
            strings.append("".join(parts))

    def cell_value(cell: ET.Element) -> str:
        v = cell.find(f"{{{ns}}}v")
        value = v.text if v is not None else ""
        if cell.get("t") == "s" and value:
            try:
                return strings[int(value)]
            except (IndexError, ValueError):
                return value
        return value

    def col_letter(ci: int) -> str:
        s = ""
        while ci >= 0:
            s = chr(65 + ci % 26) + s
            ci = ci // 26 - 1
        return s

    def col_number(ref: str) -> int:
        m = re.match(r"([A-Z]+)", ref)
        cols = 0
        for ch in m.group(1):
            cols = cols * 26 + (ord(ch) - 64)
        return cols

    models: dict[str, dict[str, Any]] = {}

    for sheet_name in [f"xl/worksheets/sheet{i}.xml" for i in range(2, 6)]:
        if sheet_name not in xlsx_z.namelist():
            continue
        ws = ET.fromstring(xlsx_z.read(sheet_name))
        rows: dict[int, dict[str, str]] = {}
        for row_el in ws.findall(f"{{{ns}}}sheetData/{{{ns}}}row"):
            rn = int(row_el.get("r"))
            cells = {}
            for c in row_el.findall(f"{{{ns}}}c"):
                cells[c.get("r")] = cell_value(c)
            rows[rn] = cells

        # find header
        header_row = None
        for rn in sorted(rows):
            vals = list(rows[rn].values())
            if "Model" in vals and any("Age" in str(v) for v in vals):
                header_row = rn
                break
        if header_row is None:
            continue

        hdr = rows[header_row]
        col_map: dict[str, str] = {}  # field → column letter
        for ref, val in hdr.items():
            letter = ref.rstrip("0123456789")
            col_map[val] = letter

        model_letter = col_map.get("Model", "A")
        age_letter = col_map.get("AgeSelf", col_map.get("Age"))
        gender_letter = col_map.get("GenderSelf", "")
        ethnicity_letter = col_map.get("EthnicitySelf", "")

        for rn in sorted(rows):
            if rn <= header_row:
                continue
            row = rows[rn]
            model = row.get(f"{model_letter}{rn}", "").strip()
            age_str = row.get(f"{age_letter}{rn}", "") if age_letter else ""
            gender = row.get(f"{gender_letter}{rn}", "").strip() if gender_letter else ""
            ethnicity = row.get(f"{ethnicity_letter}{rn}", "").strip() if ethnicity_letter else ""

            if not model:
                continue
            try:
                age = int(float(age_str)) if age_str else 0
            except (ValueError, TypeError):
                continue

            if model not in models:
                models[model] = {"age": age, "gender": gender, "ethnicity": ethnicity}

    return models


def process_cfd(counter: int, models: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    print("Processing CFD...")
    entries: list[dict[str, Any]] = []

    with zipfile.ZipFile(CFD_ZIP) as arch:
        for member in sorted(arch.namelist()):
            if not member.lower().endswith(".jpg"):
                continue
            filename = Path(member).name

            # Parse model ID from CFD filename, e.g. CFD-AF-200-228-N.jpg → AF-200
            cfd_re = re.match(r"CFD-([A-Z]+)-(\d+)", filename)
            if not cfd_re:
                continue
            model_id = f"{cfd_re.group(1)}-{cfd_re.group(2)}"

            model_info = models.get(model_id, {})
            age = model_info.get("age", 0)
            gender_raw = model_info.get("gender", "unknown")
            ethnicity = model_info.get("ethnicity", "")

            # Map gender
            gender_map = {"F": "female", "M": "male"}
            face_gender = gender_map.get(gender_raw.strip(), "unknown")

            face_id = f"face_{counter:06d}"
            dest_name = f"{face_id}.jpg"
            dest_path = FACES_OUT / dest_name

            with arch.open(member) as src, open(dest_path, "wb") as dst:
                shutil.copyfileobj(src, dst)

            abin = age_bin(age) if age > 0 else "outside_mvp"

            entries.append(
                {
                    "face_id": face_id,
                    "image_url": f"/faces/{dest_name}",
                    "true_age": age if age > 0 else None,
                    "true_age_bin": abin,
                    "face_gender": face_gender,
                    "source_dataset": "Chicago Face Database 3.0",
                    "license_type": "personal_research_use_only",
                    "is_active": abin in {label for label, _, _ in BINS},
                    "quality_score": 0.85,
                    "created_at": f"{TODAY}T00:00:00.000Z",
                }
            )
            counter += 1

    print(f"  CFD: {len(entries)} images extracted")
    return entries


# --- Manifest writer ---


def write_manifest(entries: list[dict[str, Any]]) -> None:
    """Write TypeScript manifest file."""

    bin_counts: dict[str, int] = {}
    gender_counts: Counter = Counter()
    source_counts: Counter = Counter()
    age_counts: Counter = Counter()

    for e in entries:
        bin_counts[e["true_age_bin"]] = bin_counts.get(e["true_age_bin"], 0) + 1
        gender_counts[e["face_gender"]] += 1
        source_counts[e["source_dataset"]] += 1
        if e["true_age"] is not None:
            age_counts[e["true_age"]] += 1

    # Sanitize entries for TS: replace null with 0
    ts_entries = []
    for e in entries:
        ts_e = dict(e)
        if ts_e["true_age"] is None:
            ts_e["true_age"] = 0
        ts_entries.append(ts_e)

    manifest_ts = f"""// Auto-generated by scripts/build_real_face_set.py
// Experiment version: {EXPERIMENT_VERSION}
// Generated: {datetime.now(UTC).isoformat()}
// DO NOT EDIT MANUALLY.
//
// Total images: {len(entries)}
// Sources: {dict(source_counts)}
// Gender: {dict(gender_counts)}
// MVP bin counts:
{chr(10).join(f'//   {b}: {bin_counts.get(b, 0)}' for b, _, _ in BINS)}

export const EXPERIMENT_VERSION = "{EXPERIMENT_VERSION}";

export type FaceImage = {{
  face_id: string;
  image_url: string;
  true_age: number;
  true_age_bin: string;
  face_gender: string;
  source_dataset: string;
  license_type: string;
  is_active: boolean;
  quality_score: number;
  created_at: string;
}};

export const FACE_IMAGES: FaceImage[] = {json.dumps(ts_entries, indent=2)};

export const FACE_IMAGE_BY_ID: Record<string, FaceImage> = {{}};
for (const img of FACE_IMAGES) {{
  FACE_IMAGE_BY_ID[img.face_id] = img;
}}
"""

    MANIFEST_OUT.write_text(manifest_ts, encoding="utf-8")
    print(f"\nManifest written: {MANIFEST_OUT} ({MANIFEST_OUT.stat().st_size:,} bytes)")


# --- Main ---


def main() -> None:
    FACES_OUT.mkdir(parents=True, exist_ok=True)

    # Clear previous
    for f in FACES_OUT.iterdir():
        f.unlink()

    print("Extracting and renaming images...")
    entries = process_fgnet(counter=1)
    cfd_models = parse_cfd_norming_xlsx(CFD_ZIP)
    print(f"  CFD norming data: {len(cfd_models)} models with age")
    entries += process_cfd(counter=len(entries) + 1, models=cfd_models)

    write_manifest(entries)

    # Summary
    total_images = len(entries)
    total_mb = sum(f.stat().st_size for f in FACES_OUT.iterdir()) / (1024 * 1024)
    print(f"\nDone. {total_images} images, {total_mb:.0f} MB in {FACES_OUT}")
    print(f"Experiment version: {EXPERIMENT_VERSION}")


if __name__ == "__main__":
    main()
