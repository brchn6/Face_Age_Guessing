# Dataset Download / Fetch Inspection

Date: 2026-07-12

## Scope

Admin requested fetching candidate dataset materials with `wget`/`curl`.

This inspection downloaded only into `data/`, which is gitignored. Do **not** commit raw images or archives.

## Local Paths

- `data/raw/fgnet/`
- `data/raw/chicago_faces/`
- `data/raw/faces_lifespan/`
- `data/source_pages/`

## Fetched Materials

### FG-NET

Fetched:

- `data/raw/fgnet/FGNET.zip`
- source page snapshot: `data/source_pages/fgnet_yanweifu.html`

Source page states that the mirror provider does not own the dataset and provides it for research use. This means licensing/provenance remains unresolved for public web deployment.

Archive inspection:

- 1002 image files
- all parsed as `.jpg`
- ages parse from filenames using pattern like `001A02.JPG`
- parsed age range: 0-69

MVP bin counts from filename-parsed ages:

| Bin | Count |
|---|---:|
| 4-6 | 123 |
| 7-9 | 97 |
| 10-12 | 110 |
| 13-17 | 159 |
| 18-24 | 154 |
| 25-31 | 85 |
| 32-38 | 48 |
| 39-45 | 41 |
| 46-52 | 19 |
| 53-60 | 8 |

Assessment:

- Strong age coverage for child/teen bins.
- Weak coverage for older adult bins, especially 53-60.
- Repeated identities likely exist, because FG-NET is age-progression data.
- Not approved for public deployment until rights and web-display permissions are clarified.

### Chicago Face Database

Fetched:

- `data/source_pages/chicago_faces.html`
- `data/source_pages/chicago_download.html`
- `data/raw/chicago_faces/metadata/cfd30norms.zip`
- `data/raw/chicago_faces/metadata/cfdmguide.pdf`

Not fetched:

- full CFD image archive

Reason:

- The full CFD image archive requires completing the official download form.
- The page states the full archive is about 1.5-1.7 GB.
- It requires name, email, university affiliation, materials, research purpose, and agreement to terms.
- We should not bypass or fake that form.

Terms observed from the download page include:

- database materials shall not be redistributed to third parties
- no attempts may be made to identify or contact depicted individuals

Assessment:

- Potentially useful for adult bins only.
- Likely not sufficient for child bins.
- Public web experiment display needs explicit terms review.
- Full image download should be done only through the official form with real admin/institutional information.

### FACES Lifespan Database

Fetched:

- `data/source_pages/faces_lifespan.html`
- `data/raw/faces_lifespan/metadata/Appendix_PerceivedFaceAge.xls`
- `data/raw/faces_lifespan/metadata/Appendix_PerceivedFaceExpression.xls`
- `data/raw/faces_lifespan/api/collections.json`
- `data/raw/faces_lifespan/api/items_*.json`

Not fetched:

- full FACES image database

Reason:

- Full access requires a personal account / request.
- The site states only a subset is available without account.
- A provided API token still returned only the 72 public preview items, so it did not appear to unlock the full 2,052-image database.

Metadata inspection:

- downloaded perceived-age and perceived-expression appendices
- fetched public/API metadata for 72 public preview items
- the 72 API items represent 6 people × 6 emotions × 2 picture groups
- metadata includes item-level age values for the public preview: 20, 25, 45, 48, 70, and 77

FACES public/API preview MVP bin counts:

| Bin | Count |
|---|---:|
| 4-6 | 0 |
| 7-9 | 0 |
| 10-12 | 0 |
| 13-17 | 0 |
| 18-24 | 12 |
| 25-31 | 12 |
| 32-38 | 0 |
| 39-45 | 12 |
| 46-52 | 12 |
| 53-60 | 0 |
| 61+ outside MVP | 24 |

Assessment:

- Useful as background/reference for perceived age research.
- Public/API preview is too small and too sparse to be the main image pool.
- It is adult/older-adult only; not suitable for child bins.
- Full-database access still appears to require proper account/request approval.
- Image integration remains blocked until release agreement and web-display rights are approved.

## Current Recommendation

Do not integrate any of these images into the frontend yet.

Recommended next action:

1. Use FG-NET only for local/private inspection unless rights are clarified.
2. Complete the official Chicago Face Database form manually if admin wants to evaluate full adult images.
3. Request/confirm full FACES access manually if admin wants to evaluate all 2,052 adult/older adult images; the tested token/API path only exposed the 72 public preview items.
4. Continue treating consented/source-controlled collection as the safest route for child images.

## Git Safety

`data/` is gitignored. Keep it that way.

Do not move raw images or downloaded archives outside `data/` unless storage policy is approved.
