#!/usr/bin/env python3
"""Fill the FACES Release Agreement PDF with pre-populated form content.

Overlays text on the original PDF using exact coordinates extracted from
the PDF's text positions. Output goes to FACES_Release_Agreement_filled.pdf.

Usage:
    uv run python scripts/fill_faces_pdf.py
"""

from pathlib import Path
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PDF = PROJECT_ROOT / "docs" / "FACES_Release_Agreement.pdf"
OUTPUT_PDF = PROJECT_ROOT / "docs" / "FACES_Release_Agreement_filled.pdf"

# ── Form data ──────────────────────────────────────────────────────────────
NAME = "Bar Cohen"
SUPERVISOR = "Tzachi Pilpel"
DATE = "2026-07-12"
ORG = "Weizmann Institute of Science"
UNIT = "Department of Molecular Genetics"
POSITION = "Data Scientist"
ADDRESS_L1 = "Herzl St 234"
ADDRESS_L2 = "Rehovot, Israel"
EMAIL = "bar.cohen@weizmann.ac.il"
PHONE = ""  # leave blank or fill in
STUDY_NAME = (
    "Face Age Estimation: The Role of Estimator Characteristics "
    "in Age Perception Accuracy"
)
STUDY_DESC = (
    "This study investigates how people estimate the chronological age of "
    "unfamiliar faces, and whether estimation accuracy varies with the "
    "estimator\u2019s own age and life experience. Participants complete a "
    "short web-based task where they view face images spanning young "
    "adulthood through older adulthood and provide their best estimate of "
    "each person\u2019s age. The FACES database is needed because it "
    "provides standardized, controlled photographs of adults and older "
    "adults with verified true-age metadata, making it an ideal stimulus "
    "set for the adult age bins. Participants will see images in a "
    "controlled browser-based interface preceded by a mandatory disclaimer "
    "committing them not to distribute, copy, or further disseminate the "
    "stimuli. Images will not be published in reports or presentations. "
    "The study is non-commercial academic research conducted at the "
    "Weizmann Institute of Science."
)


def wrap_text_to_width(text: str, max_width: float, c: canvas.Canvas) -> list[str]:
    """Wrap text to fit within max_width points using Helvetica 10pt."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if c.stringWidth(test, "Helvetica", 10) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def make_overlay(draw_fn):
    """Create a single-page overlay PDF in memory."""
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    draw_fn(c)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


# ── Page 3 (0-index: 2) - Signature block ──────────────────────────────────
# Coordinates from PDF text extraction (underscore line positions):
#   NAME:                 x=288 y=563
#   SIGNATURE:            x=288 y=495  (leave blank)
#   DATE:                 x=288 y=427
#   SUPERVISOR NAME:      x=288 y=282
#   SUPERVISOR SIGNATURE: x=288 y=211  (leave blank)
#   SUPERVISOR DATE:      x=288 y=141

def draw_page3(c):
    c.setFont("Helvetica", 10)
    c.drawString(288, 563, NAME)
    c.drawString(288, 427, DATE)
    c.drawString(288, 282, SUPERVISOR)
    c.drawString(288, 141, DATE)


# ── Page 4 (0-index: 3) - Required information form ────────────────────────
# Underscore line positions (x, y) for each field:
#   Name:              107, 669
#   Organization:      138, 645
#   Unit:              187, 621
#   Position:          258, 597
#   Address L1:        115, 573
#   Address L2:         71, 549
#   Address L3:         71, 525
#   Email:             107, 501
#   Telephone:         129, 477
#   Fax:                98, 453
#   Delivery L1:       155, 429
#   Delivery L2:        71, 405
#   Delivery L3:        71, 381
#   Study name L1:     164, 333
#   Study name L2:      71, 309
#   Study name L3:      71, 285
#   Description L1:     71, 225
#   ... L2..L5:         71, 201/177/153/129

# Page 5 (0-index: 4) - Description continuation:
#   Lines at y=696, 672, 648, 624, 600, 576, 552, 528, 504, 480, 456, 432,
#             408, 384, 360, 336, 312  (17 lines, x=71 each)

# Available width from x=71 to ~540 = ~469pt
DESC_WIDTH = 465  # safe width in points for Helvetica 10pt

def draw_page4(c):
    c.setFont("Helvetica", 10)
    # Place each value on its underscore line
    placements = [
        (107, 669, NAME),
        (138, 645, ORG),
        (187, 621, UNIT),
        (258, 597, POSITION),
        (115, 573, ADDRESS_L1),
        (71,  549, ADDRESS_L2),
        (107, 501, EMAIL),
        (129, 477, PHONE),
        (155, 429, ADDRESS_L1),
        (71,  405, ADDRESS_L2),
    ]
    for x, y, text in placements:
        if text:
            c.drawString(x, y, text)

    # Study name - may wrap across up to 3 lines
    study_lines = wrap_text_to_width(STUDY_NAME, DESC_WIDTH, c)
    study_y = [333, 309, 285]
    for i, line in enumerate(study_lines):
        if i < len(study_y):
            c.drawString(71, study_y[i], line)

    # Study description - wraps across page 4 and page 5
    desc_lines = wrap_text_to_width(STUDY_DESC, DESC_WIDTH, c)
    desc_y_p4 = [225, 201, 177, 153, 129]
    for i, line in enumerate(desc_lines):
        if i < len(desc_y_p4):
            c.drawString(71, desc_y_p4[i], line)
        else:
            break  # remainder goes to page 5


def draw_page5(c):
    """Page 5: Description continuation (17 blank lines at y=696..312)."""
    c.setFont("Helvetica", 10)
    desc_lines = wrap_text_to_width(STUDY_DESC, DESC_WIDTH, c)
    # Lines 0-4 went to page 4
    remaining = desc_lines[5:]
    desc_y_p5 = [696, 672, 648, 624, 600, 576, 552, 528,
                 504, 480, 456, 432, 408, 384, 360, 336, 312]
    for i, line in enumerate(remaining):
        if i < len(desc_y_p5):
            c.drawString(71, desc_y_p5[i], line)


def draw_page6(c):
    """Page 6: Participant disclaimer - mark "I agree"."""
    c.setFont("Helvetica", 10)
    # "I agree" is at x=76 y=502
    c.drawString(90, 504, "X")


def main():
    reader = PdfReader(str(INPUT_PDF))
    writer = PdfWriter()

    overlays = {
        2: make_overlay(draw_page3),   # signature page
        3: make_overlay(draw_page4),   # info form
        4: make_overlay(draw_page5),   # description cont.
        5: make_overlay(draw_page6),   # disclaimer
    }

    for i in range(len(reader.pages)):
        page = reader.pages[i]
        if i in overlays:
            page.merge_page(overlays[i])
        writer.add_page(page)

    with open(OUTPUT_PDF, "wb") as f:
        writer.write(f)

    print(f"✅ Filled PDF → {OUTPUT_PDF}")
    print("   Open it to verify text alignment, then print, sign, and scan.")


if __name__ == "__main__":
    main()
