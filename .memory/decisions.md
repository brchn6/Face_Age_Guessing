
# Decisions Log

## Initial Decisions

* Use `uv` for Python environment and dependency management.
* Use `.venv/` as the local virtual environment.
* Use `.agents/init.md` for agent operating instructions.
* Use `.memory/progress.md` to track work progress.
* Use `.memory/decisions.md` to track project decisions.
* Prefer `uv run` for running commands inside the project environment.

## 2026-07-09 — Research Design and MVP Direction

* Project is a human behavioral research data collection platform, not an AI age-estimation app.
* Preserve the core research question: are people better at estimating ages they personally resemble, or ages they are regularly exposed to?
* MVP must be anonymous, mobile-first, low-friction, and exactly 10 face-image age guesses per participant.
* Collect only participant age, participant gender, and adult-only child exposure/child age bins. Do not collect name, email, login, country, education, income, occupation, language, phone, or unnecessary personal data.
* Do not add feedback, correct answers, default age values, confidence ratings, leaderboards, account creation, AI predictions, or other features that could bias the experiment or increase friction.
* Initial experiment version is `mvp_001`. Meaningful changes to image set, questions, age input, feedback, trial count, sampling algorithm, or allowed age range require a new experiment version.
* First deliverable is a frontend-only MVP prototype using mock images/data and final JSON output; backend/database/analytics come after the UI flow is stable.

## 2026-07-09 — Frontend Stack and Scaffold

* Use Vite + React + TypeScript for the frontend MVP prototype.
* Keep the frontend app in `frontend/` instead of reusing the repository-level `src/` directory, preserving the existing Python/uv scaffold for future scripts, analytics, or backend work.
* Use npm for frontend dependency management and keep `frontend/package-lock.json` committed for reproducible installs.

## 2026-07-09 — MVP Prototype Data Handling

* Use internal SVG mock face placeholders for the frontend prototype; these are not research images and are marked with `source_dataset: internal_mock_svg_placeholders` and `license_type: internal_mock_only_not_research_data`.
* Keep all prototype session data in React/browser state and print the completed structured JSON output to the console and thank-you screen.
* Preserve `mvp_001` for this initial prototype because it implements the already-approved initial experiment version rather than changing it.

## 2026-07-09 — Bilingual Prototype Requirement

* The frontend MVP prototype must support both English and Hebrew.
* Add an in-app language toggle and support right-to-left layout for Hebrew.
* Keep the language toggle UI-only for the prototype and do not add a participant language question or extra personal-data field.
* Keep research data keys and enum values in English to preserve the planned data model and backend/API compatibility.

## 2026-07-09 — Pre-Game Countdown Reassurance

* Add lightweight countdown/reassurance copy on pre-game screens so participants understand the age-guessing game starts soon and they are not entering a long survey.
* Keep the countdown purely presentational; do not add new questions, data fields, tracking, or backend requirements.
* Do not bump `mvp_001` for this prototype-stage copy refinement because no live research data has been collected yet.

## 2026-07-09 — Slider Age Input Admin Override

* Admin requested slider-based age guessing instead of typing.
* This changes the age input component, which is a meaningful experiment-version change under the research design rules, so the frontend prototype version is now `mvp_002`.
* To reduce anchoring risk, keep the initial guess visually empty as `?`; the continue button remains disabled until the participant actively moves the slider.
* Keep optional − / + controls for precision after slider selection.

## 2026-07-09 — Completion Actions and Local Dashboard

* Add a clearer post-completion thank-you state with two actions: start a fresh 10-image session or view the recent-result dashboard.
* Starting “10 more” creates a new session with exactly 10 trials; it does not append extra trials to the completed session.
* Store the most recent completed prototype result in browser localStorage so the local dashboard can show it without a backend.
* The visible local dashboard should show recent responses and timing but avoid showing correct ages, because revealing correct answers could bias anyone who chooses to do another session.
* The full structured output remains logged to the browser console for prototype/admin inspection.
* Update the frontend prototype version to `mvp_003` because the post-completion flow now encourages optional repeat sessions and adds a local result dashboard.

## 2026-07-09 — Phase 4 Data Shape Validation

* Treat the `mvp_003` frontend output shape as passing prototype validation against the planned research data model.
* Include `created_at` on mock face image records to align with the planned `face_images` table shape.
* Keep UI language out of the research payload for now; the bilingual toggle remains UI-only and should not become a participant data field unless there is a later explicit analysis reason.
* Keep visible dashboard previews free of correct ages to avoid biasing repeat sessions.
* Do not proceed to backend/database implementation until admin approves the Phase 4 validation document.

## 2026-07-09 — Phase 5A UX/Mobile Polish

* Keep Phase 5A limited to visual/mobile QA polish; do not add backend, analytics, new questions, or new participant data fields.
* Do not bump the experiment version for the Phase 5A CSS/mobile changes because they do not alter the research flow, trial count, sampler, stored data fields, or age-input semantics from `mvp_003`.
* Preserve the no-anchor slider start state during polish: `?` readout, hidden slider thumb, and disabled Continue until active slider interaction.

## 2026-07-09 — Phase 5B Image Sourcing Rules

* Do not use random scraped faces from the internet.
* Do not use AI-generated faces for the research image pool because the study is about human perception of real facial age.
* Do not download, commit, or integrate real face images until source licensing, web-display rights, child-image permissions, and admin approval are complete.
* Use a manifest-first workflow for real images, with required metadata matching the planned `face_images` model plus license/provenance fields.
* Do not expose true age or age bin in public image filenames or URLs.
* Replacing the mock image set with real images is a meaningful experiment-version change and should move beyond `mvp_003`, likely to `mvp_004` once approved.

## 2026-07-09 — Preliminary Source Review Outcome

* Prefer consented/source-controlled image collection as the primary route, especially for images of minors.
* Treat controlled academic datasets as possible supplemental sources only if terms explicitly allow the intended web experiment display.
* Reject scraped/public-provenance-unclear age-face datasets for deployment unless provenance and rights are proven.
* Reject celebrity-heavy datasets for the MVP because recognizability, noisy age labels, and licensing concerns can bias or weaken the experiment.
* Reject age-bin-only datasets as primary sources because the main metric requires exact `true_age`.

## 2026-07-09 — Free Dataset Search Outcome

* No free/no-cost dataset is approved for use yet.
* FG-NET, APPA-REAL/ChaLearn-style datasets, controlled adult face datasets, and AFAD-style datasets are only terms-review candidates.
* UTKFace-style datasets remain rejected for public MVP deployment unless provenance, consent, child-image rights, and web-display rights are explicitly proven.
* Celebrity datasets such as IMDB-WIKI/CACD/AgeDB remain rejected for MVP deployment.
* Continue to treat consented/source-controlled collection as the lowest-risk path, especially for child bins.

## 2026-07-12 — Dataset Fetch Agent Clarification

* Previous dataset-fetch failures were caused by an over-broad interpretation of the no-real-images rule.
* Fetching public dataset source pages, license pages, and metadata descriptions for terms review is allowed and should proceed when requested.
* Downloading dataset archives/images requires explicit local-only admin approval and must stay under ignored paths such as `data/raw/<source>/`.
* Integrating real images into the app remains blocked until licensing, public web-display rights, child-image permissions, manifest mapping, experiment-version bump, and admin approval are complete.
* Future agents must read `docs/data-fetch-agent-runbook.md` before acting on dataset fetch requests.

## 2026-07-12 — Dataset Fetch Guardrails

* Store downloaded/fetched dataset materials only under gitignored `data/` paths.
* FG-NET may be inspected locally, but it is not approved for public deployment because the mirror page states the mirror provider does not own the dataset and rights remain unresolved.
* Do not bypass official download/access forms for Chicago Face Database or FACES; those must be completed manually with real admin/institutional information if pursued.
* Metadata/norming files may be inspected, but image integration remains blocked until source terms and web-display rights are approved.

## 2026-07-12 — Candidate Manifest Guardrails

* Candidate manifests generated from local datasets must mark all real-image rows `is_active: false` until rights, web-display permission, and admin approval are complete.
* FACES public/API metadata can be used for source evaluation, but the 72 public preview items are not enough for the MVP image pool and do not cover child/teen bins.
* FG-NET has enough child/teen coverage for local inspection, but remains blocked for public deployment due to unresolved rights/provenance.

## 2026-07-12 — Phase 6 Real Image Integration

* Replace mock SVG placeholders with extracted real images from FG-NET and Chicago Face Database.
* Store extracted/renamed images under gitignored `frontend/public/faces/`.
* Generate a versioned TypeScript manifest `frontend/src/faceManifest.ts` from the norming data.
* Use the manifest's `mvp_004` experiment version in the frontend.
* The frontend sampler now picks exactly one active image per MVP age bin (10 total), randomly, from the available pool.
* Face image metadata may be committed; raw image files stay under ignored paths.
* Real images are for local/dev use only until rights and display terms are approved.

## 2026-07-12 — Phase 7A Backend + Database

* Use SQLite as the database (zero-config, file-based, reproducible, easy to inspect).
* Use FastAPI for the backend (type-safe, auto-documented, Python-native).
* Keep the frontend fully functional without the backend (localStorage fallback) so development and testing never depend on a running server.
* Auto-seed the face_images table from the frontend manifest at startup rather than duplicating metadata.
* The backend sampler uses SQL `ORDER BY RANDOM()` to pick one active image per MVP bin per session.
* Database file at `data/experiment.db` stays gitignored; schema is defined in code only.

## 2026-07-12 — UX Polish (Soft / Warm Redesign)

* Move from cold blue-gray to warm purple-lavender design.
* Replace red validation errors with soft amber nudges.
* No experiment version bump — cosmetic changes only.

## 2026-07-12 — Phase 8 Analytics + Data Quality

* Compute all research metrics from the SQLite database, not from frontend JavaScript.
* Expose analytics via API so it can be inspected without running the frontend.
* Flag suspicious data (too fast, too slow, low effort, all-same-guess) but do not delete it.
* Analytics dashboard is embedded in the local result dashboard, only shown when backend is running.



