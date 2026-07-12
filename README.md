# Face_Age_Guessing

## Description

Describe your project here.

## Setup

This project uses `uv` for Python environment and dependency management.

### Create environment

```bash
uv venv --python 3.11
```

### Activate environment

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
uv sync
```

### Add dependencies

```bash
uv add package-name
```

### Add development dependencies

```bash
uv add --dev pytest ruff mypy
```

### Run the Python project

```bash
uv run python main.py
```

### Run Python tests

```bash
uv run pytest
```

## Backend API

The backend lives in `src/` and uses FastAPI + SQLite.

### Run the backend

```bash
uv run python -m src.server
```

The API is available at `http://127.0.0.1:8000`. Endpoints:

- `POST /api/session` - create session and assign trials
- `POST /api/response` - submit a single response
- `POST /api/session/complete` - mark session as completed

The frontend calls these automatically when the backend is running. If the backend is unavailable, the frontend still works fully with `localStorage` as a fallback.

### Database

SQLite database at `data/experiment.db`. Inspect with:

```bash
sqlite3 data/experiment.db
```

Schema follows the research data model (participant_sessions, participant_child_exposure, face_images, trial_assignments, responses).

## Frontend prototype

The frontend MVP prototype lives in `frontend/` and uses Vite + React + TypeScript.

Current prototype flow:

1. Landing
2. Short anonymous consent/explanation
3. Participant age and gender
4. Adult-only child exposure question
5. Exactly 10 mock face cards
6. Thank-you screen with option to do 10 more
7. Local recent-result dashboard link

The prototype supports English and Hebrew with an in-app language toggle. Hebrew screens use right-to-left layout. The toggle is UI-only in this prototype and does not add a participant language question. Pre-game screens include short countdown/reassurance copy so participants know the actual game starts soon.

As of `mvp_004`, the prototype uses real face images from FG-NET and the Chicago Face Database (local/dev use only). The sampler picks one active image per MVP age bin. Mock SVGs are no longer used.

Age guesses use a slider with a large numeric readout and optional − / + fine-tuning. The initial state still shows `?` and cannot be submitted until the participant actively moves the slider.

After completion, the participant can start a fresh 10-image session or open a local dashboard showing the most recent completed result in this browser. The dashboard is also addressable with `#dashboard`. The full structured JSON is still logged to the console for prototype inspection; the visible dashboard preview avoids showing correct ages.

Phase 4 data-shape validation is documented in `docs/phase-4-data-shape-validation.md`. Phase 5A UX/mobile QA is documented in `docs/phase-5a-ux-qa.md`. Phase 5B real image sourcing is documented in `docs/phase-5b-image-sourcing-plan.md`, with a manifest template in `docs/face-image-manifest-template.csv`. The preliminary image source review is in `docs/phase-5c-source-review.md`. Free/no-cost dataset candidates are reviewed in `docs/phase-5b-free-dataset-search.md` and `docs/free-dataset-candidates.csv`. Quick source links for admin review are in `docs/dataset-source-links.md`. Agent rules for dataset fetching are in `docs/data-fetch-agent-runbook.md`.

The prototype is frontend-only. It uses internal SVG mock face placeholders, stores responses in browser state/localStorage, logs the final JSON to the console, and does not use a backend. Do not add real face images until source licensing, child-image permissions, and the image manifest are approved. Fetching public source pages and license terms for review is allowed; downloading dataset files requires explicit local-only admin approval and must stay under ignored `data/raw/` paths.

### Install frontend dependencies

```bash
cd frontend
npm install
```

### Run frontend locally

```bash
cd frontend
npm run dev
```

### Typecheck and build frontend

```bash
cd frontend
npm run typecheck
npm run build
```

## Structure

```
src/       Source code
tests/     Tests
docs/      Documentation
data/      Local datasets
scripts/   Utility scripts
.agents/   Agent operating instructions
.memory/   Project memory, decisions, and progress
```
