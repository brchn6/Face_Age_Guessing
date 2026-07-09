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

Age guesses use a slider with a large numeric readout and optional − / + fine-tuning. The initial state still shows `?` and cannot be submitted until the participant actively moves the slider.

After completion, the participant can start a fresh 10-image session or open a local dashboard showing the most recent completed result in this browser. The dashboard is also addressable with `#dashboard`. The full structured JSON is still logged to the console for prototype inspection; the visible dashboard preview avoids showing correct ages.

Phase 4 data-shape validation is documented in `docs/phase-4-data-shape-validation.md`.

The prototype is frontend-only. It uses internal SVG mock face placeholders, stores responses in browser state/localStorage, logs the final JSON to the console, and does not use a backend.

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
