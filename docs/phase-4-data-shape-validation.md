# Phase 4 — Data Shape Validation

Date: 2026-07-09  
Prototype version: `mvp_003`

## Scope

Validate that the frontend-only prototype emits data that can map cleanly to the planned research data model before any backend or database work begins.

This phase does **not** add a backend, database, analytics pipeline, user accounts, or extra participant questions.

## Validation Result

Status: **pass for frontend prototype**

The completed session object contains the planned tables/collections:

- `participant_sessions`
- `participant_child_exposure`
- `face_images`
- `trial_assignments`
- `responses`

## Model Checklist

### `participant_sessions`

Required fields present:

- `session_id`
- `participant_age`
- `participant_age_group`
- `participant_gender`
- `has_child_exposure`
- `experiment_version`
- `device_type`
- `started_at`
- `completed_at`
- `status`

Notes:

- Status becomes `completed` only after exactly 10 submitted responses.
- `experiment_version` is currently `mvp_003`.
- UI language is not stored; the language toggle remains UI-only.

### `participant_child_exposure`

Required fields present:

- `session_id`
- `child_age_bin`

Notes:

- Rows are created only when an adult participant selects child exposure age bins.
- Under-18 participants skip this section and produce no child exposure rows.

### `face_images`

Required/planned fields present:

- `face_id`
- `image_url`
- `true_age`
- `true_age_bin`
- `face_gender`
- `source_dataset`
- `license_type`
- `is_active`
- `quality_score`
- `created_at`

Notes:

- Current images are internal SVG placeholders only.
- They are explicitly marked as mock data and are not valid research face images.
- Real data collection still requires licensed/traceable face images.

### `trial_assignments`

Required fields present:

- `trial_id`
- `session_id`
- `face_id`
- `trial_index`
- `assigned_at`

Notes:

- Assignments are created before the trial flow starts.
- Each session has exactly 10 assignments.
- “Do 10 more” creates a fresh session with fresh assignment IDs; it does not append to the completed session.

### `responses`

Required fields present:

- `response_id`
- `trial_id`
- `session_id`
- `face_id`
- `predicted_age`
- `response_time_ms`
- `submitted_at`
- `client_order_index`

Notes:

- One response is added per submitted trial.
- A completed session has exactly 10 responses.
- Response timing is captured client-side in milliseconds.

## Privacy / Friction Check

The prototype does **not** collect:

- name
- email
- phone
- account/login
- country
- education
- occupation
- income
- free text
- confidence rating

## Dashboard Check

The local dashboard shows the latest completed result stored in browser `localStorage`.

Visible dashboard data intentionally excludes `true_age` and `true_age_bin` so participants are not shown correct answers before choosing to do another session.

The full structured object is still logged to the browser console for prototype/admin inspection.

## Known Prototype Limitations

- No backend persistence yet.
- `localStorage` is only a browser-local prototype mechanism.
- The mock image pool has only 10 placeholder images, so repeated sessions reuse the same mock faces in a new randomized order.
- Real data collection requires a larger licensed image pool and backend persistence.
- Data quality flags such as `too_fast`, `too_slow`, and `session_too_fast` are not implemented yet.

## Phase 4 Conclusion

The `mvp_003` frontend prototype data shape is ready for admin review. The next phase should not start backend implementation until this validation is approved.
