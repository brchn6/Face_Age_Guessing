
# Progress Log

## Initial State

* Project initialized.
* Basic Python project structure created.
* uv workflow configured.
* Agent workflow files created.

## Current Open Tasks

* Phase 8 complete — analytics + data quality. All pushed to GitHub.
* After approval: run backend + frontend together, complete test sessions, review analytics.
* Next: decide between image rights resolution, deployment, or participant recruitment.
* Future dataset-fetch work must follow `docs/data-fetch-agent-runbook.md` so agents do source/terms review when requested, but do not integrate real images before approval.

## 2026-07-09 — First Project Step

* Added the full research/product handoff to `.agents/project-handoff.md`.
* Updated `.agents/init.md` so future agents must read the handoff before planning or coding.
* Immediate next task: implement the frontend MVP prototype with mock data: Landing, Consent, Participant details, Child exposure, 10 image cards, Thank-you screen, and final JSON output.

## 2026-07-09 — Phase 2 Frontend Scaffold

* Added a Vite + React + TypeScript frontend scaffold under `frontend/`.
* Added initial placeholder app shell for the browser prototype.
* Added frontend npm scripts: `dev`, `typecheck`, `build`, and `preview`.
* Added frontend setup/run commands to `README.md`.
* Verified the scaffold with `npm run typecheck` and `npm run build`.

## 2026-07-09 — Phase 3 Frontend MVP Prototype

* Implemented the full frontend-only research flow: Landing, Consent, Participant details, adult-only Child exposure, exactly 10 image cards, Thank-you screen, and final JSON output.
* Added internal SVG mock face placeholders with one face per planned MVP age bin.
* Added randomized 10-trial assignment at session start and saved assignments before responses are collected.
* Added numeric age guessing with no default/anchoring value; submission is disabled until the participant actively enters a valid age.
* Added response timing, session completion status, child exposure rows, trial assignment rows, response rows, and console output of the completed JSON.
* Verified the prototype with `npm run typecheck` and `npm run build`.

## 2026-07-09 — Phase 2/3 Bilingual Revision

* Added English/Hebrew language support across the frontend prototype.
* Added an in-app language toggle available on every screen.
* Added right-to-left layout handling for Hebrew screens.
* Kept the language toggle UI-only; no participant language question or extra personal-data field was added.
* Kept JSON/data model keys and enum values in English for planned backend/API compatibility.
* Verified the bilingual prototype with `npm run typecheck` and `npm run build`.

## 2026-07-09 — Pre-Game Countdown Reassurance

* Added short countdown/reassurance copy on the Landing, Consent, Participant details, and Child exposure screens.
* Added English and Hebrew countdown text.
* Kept the change UI-only: no extra participant question, no data model change, and no backend change.
* Verified with `npm run typecheck` and `npm run build`.

## 2026-07-09 — Admin Review

* Admin approved/passed the bilingual Phase 3 prototype with pre-game countdown reassurance.
* Next phase is Phase 4: validate the final JSON/data shape against the planned research data model before any backend/database work.

## 2026-07-09 — Slider Age Input Revision

* Replaced typed trial age input with a slider-based age input.
* Preserved a no-anchor initial state: the readout shows `?`, the slider thumb is visually hidden, and Continue stays disabled until the participant moves the slider.
* Kept − / + controls for fine-tuning after slider selection.
* Updated experiment version from `mvp_001` to `mvp_002` because the age input component changed.
* Updated English and Hebrew trial microcopy for the slider interaction.
* Verified with `npm run typecheck` and `npm run build`.

## 2026-07-09 — Completion Actions and Local Dashboard

* Reworked the end state so participants see a clear thank-you message instead of only JSON.
* Added a “Do 10 more” action that starts a fresh 10-image session while preserving exactly 10 trials per session.
* Added a local recent-result dashboard screen and dashboard link from the thank-you screen.
* Saved the latest completed prototype result in browser localStorage for the local dashboard.
* Dashboard shows session status, completion time, average response time, and response rows without visible correct ages.
* Full structured output remains logged to the browser console for prototype/admin inspection.
* Updated experiment version from `mvp_002` to `mvp_003`.
* Verified with `npm run typecheck` and `npm run build`.

## 2026-07-09 — Phase 4 Data Shape Validation

* Validated the frontend output shape against the planned research data model.
* Added `created_at` to mock `face_images` so the frontend object matches the planned face image record more closely.
* Confirmed completed sessions contain `participant_sessions`, `participant_child_exposure`, `face_images`, `trial_assignments`, and `responses`.
* Confirmed the prototype still avoids forbidden participant data such as name, email, login, country, education, occupation, free text, and confidence rating.
* Converted the thank-you dashboard action into an actual hash link (`#dashboard`) while keeping it in-app.
* Added `docs/phase-4-data-shape-validation.md` with the validation checklist, pass status, and known prototype limitations.
* Verified with `npm run typecheck` and `npm run build`.

## 2026-07-09 — Phase 5A UX QA / Mobile Polish

* Improved mobile viewport handling with `100svh` fallbacks.
* Reduced small-screen trial layout pressure so the image, slider, and submit button fit better.
* Added mobile tap polish for buttons, links, and slider controls.
* Improved slider styling across Chromium/WebKit and Firefox while preserving the initial `?` no-anchor state.
* Improved small-screen dashboard layout by stacking stat cards and tightening response-table columns.
* Added `docs/phase-5a-ux-qa.md` with a manual QA checklist.
* No experiment-version bump: changes are visual/mobile polish only and do not change questions, trial count, sampling, stored fields, or age-input semantics from `mvp_003`.
* Verified with `npm run typecheck` and `npm run build`.

## 2026-07-09 — Phase 5B Real Image Sourcing Plan

* Added `docs/phase-5b-image-sourcing-plan.md` defining image-source requirements, child-image cautions, minimum pool targets, metadata requirements, rejected sources, processing rules, and acceptance criteria.
* Added `docs/face-image-manifest-template.csv` as the future real-image metadata manifest template.
* Confirmed no real face images should be downloaded, committed, or integrated until licensing, source provenance, child-image permissions, and admin approval are complete.
* Recorded that replacing mock images with real images will require a new experiment version, likely `mvp_004`.

## 2026-07-09 — Phase 5C Preliminary Image Source Review

* Added `docs/phase-5c-source-review.md` reviewing source paths and common dataset categories.
* Recommended consented/source-controlled collection as the primary path, especially for child images.
* Marked controlled academic datasets as candidates only after explicit terms and web-display-rights review.
* Rejected scraped, celebrity-heavy, age-bin-only, and AI-generated face datasets for MVP deployment.
* No images were downloaded, committed, or integrated.

## 2026-07-09 — Phase 5B Free Dataset Search

* Added `docs/phase-5b-free-dataset-search.md` reviewing free/no-cost face-age dataset candidates.
* Added `docs/free-dataset-candidates.csv` with candidate verdicts and risk notes.
* Shortlisted FG-NET, APPA-REAL/ChaLearn-style datasets, controlled adult face databases, and AFAD-style datasets for formal terms review only.
* Rejected UTKFace-style broad web-collected datasets for public MVP deployment unless provenance and rights can be proven.
* Rejected IMDB-WIKI/CACD/AgeDB-style celebrity datasets, age-bin-only datasets, and AI-generated faces for MVP deployment.
* No real images were downloaded, committed, or integrated.

## 2026-07-12 — Dataset Fetch / Local Inspection

* Created `data/raw/fgnet/`, `data/raw/chicago_faces/`, `data/raw/faces_lifespan/`, and `data/source_pages/` for local ignored dataset inspection.
* Downloaded FG-NET zip into `data/raw/fgnet/FGNET.zip` for local inspection only; `data/` remains gitignored.
* Parsed FG-NET archive listing: 1002 JPG images with filename-parsed ages 0–69; MVP bins are strong for child/teen ages but weak for older adult bins.
* Downloaded Chicago Face Database source/download pages, norming data zip, and measurement guide only; full images require official form submission and were not downloaded.
* Downloaded FACES source page and perceived-age/expression appendices only; full images require account/request and were not downloaded.
* Added `docs/dataset-download-inspection.md` summarizing fetched files, limitations, and next actions.

## 2026-07-12 — Candidate Dataset Manifests

* Added `scripts/build_fgnet_candidate_manifest.py` and generated a local ignored FG-NET candidate manifest under `data/manifests/`.
* FG-NET candidate manifest includes 1002 images, 82 unique identities, parsed ages 0–69, and all rows inactive pending rights/web-display approval.
* Added `scripts/fetch_faces_lifespan_metadata.py`; admin ran it with a provided FACES token, but it still returned only the 72 public preview items.
* Added `scripts/build_faces_lifespan_candidate_manifest.py` and generated a local ignored FACES public/API candidate manifest under `data/manifests/`.
* FACES public/API candidate manifest includes 72 items, 6 unique people, ages 20/25/45/48/70/77, no child/teen coverage, and all rows inactive pending release agreement/web-display approval.
* Updated `docs/dataset-download-inspection.md` with the FACES API/token outcome and FACES public preview bin counts.

## 2026-07-12 — Phase 6 Real Image Integration

* Created `scripts/build_real_face_set.py` to extract, rename, and manifest real images from FG-NET + CFD archives.
* Extracted 2,443 real images to gitignored `frontend/public/faces/` with neutral filenames that do not expose age.
* Generated `frontend/src/faceManifest.ts` with per-image metadata including `true_age`, `true_age_bin`, `face_gender`, `is_active`, and source provenance.
* Updated `frontend/src/App.tsx` to import the real manifest, remove mock SVGs, and sample one active image per MVP age bin.
* Updated experiment version from `mvp_003` to `mvp_004` via the auto-generated manifest.
* Full typecheck and build passing with real images.
* Real images remain under gitignored paths; only metadata manifests are committed.

## 2026-07-12 — Phase 7A Backend + Database

* Added FastAPI + SQLite backend under `src/`.
* Created `src/database.py` with full schema matching the research data model.
* Created `src/api.py` with FastAPI endpoints: session creation, response submission, session completion.
* Created `src/server.py` as the uvicorn entry point.
* The backend auto-seeds face images from the frontend manifest on startup.
* Added `frontend/src/api.ts` as the frontend API client.
* Updated `frontend/src/App.tsx` to call the backend API alongside localStorage.
* The frontend works fully offline when the backend is unreachable.
* Added `uv add fastapi uvicorn` to pyproject.toml.
* Verified the API returns proper session/trial assignments with real face URLs.
* Verified full frontend typecheck and build pass.

## 2026-07-12 — Soft UX Polish

* Replaced harsh red error messages with soft amber nudges.
* Changed color palette from cold blue-gray to warm purple-lavender gradient.
* Added glass-effect cards with backdrop blur.
* Added purple gradient primary buttons with glow.
* Softer focus rings, warmer input backgrounds, hover states on choices.
* Gradient progress bar and warmer stepper buttons.
* All cosmetic — no experiment version bump, no feature changes.

## 2026-07-12 — Phase 8 Analytics + Data Quality

* Added `src/analytics.py` with research metric computation from SQLite.
* Metrics: MAE by participant age group, MAE by face age bin, MAE heatmap, overall bias, compression slope, child exposure MAE.
* Data quality flags: too-fast responses (<300ms), too-slow responses (>60s), low-effort sessions (all same guess), sessions under 10 seconds.
* Added `GET /api/analytics` endpoint to FastAPI.
* Added `fetchAnalytics()` to frontend API client.
* Added `AnalyticsDisplay` component in the local dashboard with sessions, data quality, research metrics, and MAE tables.
* Analytics shown only when backend is connected.
* Verified full frontend typecheck and build pass.


## 2026-07-12 — Dataset Fetch Agent Clarification

* Diagnosed the likely agent failure mode: the no-real-images rule was interpreted as "do not fetch anything," instead of only blocking unsafe image download/integration.
* Added `docs/data-fetch-agent-runbook.md` to define allowed source/terms review, approval requirements for local-only downloads, and blockers for app integration.
* Updated `.agents/init.md`, `README.md`, `docs/dataset-source-links.md`, and `.memory/decisions.md` so future agents know to read the runbook before dataset fetch work.
