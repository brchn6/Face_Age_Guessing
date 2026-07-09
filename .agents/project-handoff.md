# Handoff Document — Facial Age Estimation Research Experiment

## Project Name

**Face Age Guessing Experiment**

Working title:

> **How Observer Age and Age Exposure Affect Human Facial Age Estimation**

---

## 1. Executive Summary

We are building a short, mobile-first web experiment where participants estimate the age of people shown in face images.

Each participant will:

1. Enter minimal demographic information.
2. Optionally answer a short question about regular exposure to children.
3. View exactly **10 face images**.
4. Guess the age of each person.
5. Complete the full experience in under one minute.

The interface should feel like a fast, smooth, lightweight game — close to a Tinder-like card experience — but the underlying purpose is serious research data collection.

This is **not** an AI age-estimation app.

This is a **human behavioral research data collection platform**.

---

## 2. Critical Research Goal

### Primary Research Objective

The main goal of this project is to understand:

> **How accurately people of different ages estimate the age of other people from face images, and whether this ability is better explained by the observer’s own age or by their regular exposure to people in specific age ranges.**

This distinction is central.

The naive hypothesis is:

> People are better at estimating the age of people close to their own age.

But the deeper hypothesis is:

> People may be better at estimating the ages of people they are regularly exposed to, even if those people are not close to their own age.

Example:

A 35-year-old without children may be poor at estimating whether a child is 4, 6, or 8.

A 35-year-old with a 5-year-old child may be better at estimating children around that age.

This means the experiment is not only about chronological age. It is about **age familiarity**, **social exposure**, and **human perceptual calibration**.

---

## 3. Core Research Question

### Main Question

> Does human facial age estimation accuracy depend primarily on the observer’s chronological age, or on the age ranges the observer is familiar with through regular social exposure?

---

## 4. Secondary Research Questions

### RQ1 — Observer Age Effect

Do participants of different ages differ in their accuracy when estimating facial age?

Measured by:

```text
absolute_error = abs(predicted_age - true_age)
```

### RQ2 — Own-Age Advantage

Are participants more accurate when estimating the age of people close to their own age?

Measured by:

```text
own_age_distance = abs(participant_age - face_true_age)
```

Expected relationship:

```text
lower own_age_distance → lower absolute_error
```

### RQ3 — Age Exposure Effect

Are participants more accurate when estimating age ranges they are regularly exposed to?

Primary exposure case for MVP:

> Regular close exposure to children.

Example:

A participant who is regularly exposed to children aged 3–5 may be more accurate on face images of children aged 3–5 than participants without such exposure.

### RQ4 — Child Exposure Specificity

Is it enough to know whether someone has children, or does the actual age range of the children matter?

Hypothesis:

```text
child_age_bins
```

should explain accuracy better than:

```text
has_child_exposure
```

In other words, a participant with a 4-year-old child may improve mainly around ages 3–5, not across all child ages.

### RQ5 — Age Compression

Do participants compress unfamiliar age ranges?

Example:

A child may see adults aged 24, 35, and 50 as all roughly “adult”.

A non-parent adult may see children aged 4, 7, and 10 as all roughly “kid”.

This can be measured by comparing the slope between:

```text
face_true_age
```

and:

```text
predicted_age
```

Within participant age groups or exposure groups.

A flatter slope suggests compression.

---

## 5. Research Hypotheses

### H1 — Observer Age Matters

Participant age will affect facial age estimation accuracy.

Expected pattern:

```text
very young participants → higher error
adult participants → lower error
```

But the analysis should not assume this is the full explanation.

### H2 — Own-Age Distance Matters

Participants will be more accurate when estimating people closer to their own age.

Expected pattern:

```text
abs(participant_age - face_true_age) increases
→
absolute_error increases
```

### H3 — Exposure Matters

Participants with regular close exposure to children will estimate children’s ages more accurately than participants without such exposure.

But the effect should be local.

Example:

```text
exposure to children aged 3–5
→ better accuracy for faces aged 3–5
→ possibly weaker or no improvement for faces aged 13–17
```

### H4 — Exposure May Explain Part of the Own-Age Effect

People might not be better at estimating their own age group simply because of their biological age.

They may be better because they are more exposed to people around their own age.

This is a key conceptual point.

The model should eventually compare:

```text
participant_age
```

against:

```text
age exposure profile
```

### H5 — Gender Effects Are Secondary

Participant gender and face gender may influence estimates, but they are not the primary research focus.

Gender should be collected and modeled as a secondary explanatory variable or control variable.

---

## 6. MVP Scope

The MVP must be extremely short and low-friction.

### Participant Inputs

Collect only:

```text
participant_age
participant_gender
```

And, for adult participants only:

```text
child_exposure
child_age_bins
```

No other questions in the MVP.

Do not collect:

```text
country
education
ethnicity
income
occupation
language
name
email
phone
account/login
```

---

## 7. Participant Flow

### Full User Flow

```text
Landing Screen
↓
Short Consent / Explanation
↓
Participant Age + Gender
↓
Child Exposure Question, only if participant is adult
↓
10 Face Guessing Cards
↓
Thank You / Completion Screen
```

The total experience should feel fast, light, and game-like.

Target completion time:

```text
30–60 seconds
```

---

## 8. UX Principles

### Core UX Direction

The product should feel like:

```text
fast
smooth
mobile-first
visual
minimal
game-like
low-pressure
```

It should not feel like:

```text
a survey
a psychological test
a government form
an academic questionnaire
a long experiment
```

The participant should feel:

> “I’m playing a quick age guessing game.”

But internally, the system collects structured research-grade data.

---

## 9. Interface Requirements

### 9.1 Landing Screen

Purpose: introduce the task quickly.

Suggested copy:

```text
Guess Their Age

You’ll see 10 face images.
For each one, guess how old the person is.

It takes less than a minute.
```

Primary button:

```text
Start
```

### 9.2 Consent / Explanation Screen

Keep this very short.

Suggested copy:

```text
This is an anonymous research experiment about how people estimate age from faces.

We do not ask for your name, email, or account.

You can stop at any time.
```

Primary button:

```text
Continue
```

Important: do not overload this screen. If a more formal consent flow is required later, add it as a separate experiment version.

### 9.3 Participant Details Screen

Fields:

```text
Age
Gender
```

Age input:

```text
integer
allowed range: 4–100
```

Gender options:

```text
Female
Male
Other
Prefer not to say
```

Do not force binary gender. Do not ask for anything else here.

### 9.4 Child Exposure Screen

Show only if:

```text
participant_age >= 18
```

Question:

```text
Are there children you are in close regular contact with?
```

Options:

```text
No
Yes
Prefer not to say
```

If the participant selects `Yes`, show:

```text
Which age ranges?
Select all that apply.
```

Options:

```text
0–2
3–5
6–8
9–12
13–17
18+
```

Notes:

- This should not ask “Do you have children?” directly.
- The goal is not biological parenthood.
- The goal is regular exposure to children.
- This includes children, siblings, nephews/nieces, caregiving, teaching, etc.
- Keep it short and non-invasive.

### 9.5 Face Guessing Screen

This is the core screen.

Each trial shows one face image and asks:

```text
How old is this person?
```

The participant enters a single numeric age estimate.

Important UX requirements:

1. Show one image at a time.
2. Show progress, e.g. `3 / 10`.
3. Do not show the correct answer.
4. Do not show performance feedback during the experiment.
5. Do not include a “don’t know” option.
6. Encourage guessing: `Not sure? Make your best guess.`
7. Do not allow going back to previous images.
8. Preload the next image to keep the experience smooth.
9. The interface must work well on mobile.

---

## 10. Age Input Component

Avoid a normal slider if possible.

A slider may create noisy data because users tend to round answers or stop at visually convenient values.

Preferred input styles:

### Option A — Large Number Picker

Display `?` initially. After interaction, show a large number like `34`.

Controls:

```text
-     +
```

And/or keyboard input.

### Option B — Wheel Picker

A mobile-style numeric wheel can work well if it is fast and precise.

### Option C — Hybrid

Recommended MVP approach:

```text
large numeric input
plus +/- buttons
submit button
```

Important:

- Do not pre-fill with a default value such as 30.
- A default value would anchor participants and bias the data.
- Initial state should be empty or show `?`.
- Only allow submission after the participant actively selects or types a number.

---

## 11. Trial Rules

Each participant should receive exactly:

```text
10 images
```

A completed session means:

```text
10 valid responses
```

If a participant quits early, keep the partial data but mark the session as abandoned or incomplete.

Do not throw away raw partial data.

---

## 12. Face Image Pool

Each face image must have metadata.

Required metadata:

```text
face_id
image_url
true_age
true_age_bin
face_gender
source_dataset
license_type
is_active
quality_score
```

Optional metadata:

```text
ethnicity
image_resolution
lighting_quality
pose_quality
```

But optional fields should not block the MVP.

---

## 13. Image Age Bins

For the MVP, use balanced age bins.

Recommended face age bins:

```text
4–6
7–9
10–12
13–17
18–24
25–31
32–38
39–45
46–52
53–60
```

Each session should ideally include one image from each bin.

This gives every participant a broad set of ages while keeping the task short.

---

## 14. Sampling Strategy

### MVP Sampling Rule

For each session:

1. Assign one image from each face age bin.
2. Prefer images with fewer total ratings.
3. Prefer images with fewer ratings from the participant’s age group.
4. Randomize the order of the 10 images.
5. Save the assignment before the experiment begins.

Important: the sampler should **not** adapt based on child exposure in the MVP.

Reason: if child-exposed participants receive more child faces than non-child-exposed participants, the experiment becomes harder to interpret. All participant groups should receive comparable image sets.

---

## 15. Data Model

### 15.1 participant_sessions

One row per participant session.

```text
session_id
participant_age
participant_age_group
participant_gender
has_child_exposure
experiment_version
device_type
started_at
completed_at
status
```

Allowed status values:

```text
created
active
completed
abandoned
invalid
```

### 15.2 participant_child_exposure

One row per selected child age range. A participant can have multiple rows.

```text
session_id
child_age_bin
```

### 15.3 face_images

One row per image.

```text
face_id
image_url
true_age
true_age_bin
face_gender
source_dataset
license_type
is_active
quality_score
created_at
```

### 15.4 trial_assignments

Created at the beginning of the experiment.

```text
trial_id
session_id
face_id
trial_index
assigned_at
```

### 15.5 responses

One row per participant answer.

```text
response_id
trial_id
session_id
face_id
predicted_age
response_time_ms
submitted_at
client_order_index
```

Do not overwrite responses. If a future version supports edits, store revisions separately. For MVP, do not allow edits.

---

## 16. Derived Metrics

These can be computed later from raw data.

### Response-Level Metrics

```text
signed_error = predicted_age - true_age
absolute_error = abs(predicted_age - true_age)
own_age_distance = abs(participant_age - true_age)
```

### Child Exposure Match

```text
child_age_match = 1
```

If the face’s true age falls inside one of the participant’s selected child exposure bins. Otherwise:

```text
child_age_match = 0
```

### Distance to Child Exposure

For each selected child exposure bin, define a midpoint.

Example:

```text
3–5 → 4
6–8 → 7
9–12 → 10.5
```

Then compute:

```text
distance_to_nearest_child_age =
min(abs(face_true_age - child_age_bin_midpoint))
```

If the participant has no child exposure:

```text
distance_to_nearest_child_age = null
```

---

## 17. Primary Research Metrics

### Main Accuracy Metric

```text
MAE = mean(abs(predicted_age - true_age))
```

This is the central accuracy measure.

### Bias Metric

```text
mean_signed_error = mean(predicted_age - true_age)
```

Interpretation:

```text
positive bias → participants guessed too old
negative bias → participants guessed too young
```

### Compression Metric

For each participant group, estimate the relationship:

```text
predicted_age ~ true_age
```

If the slope is close to 1: good age differentiation. If the slope is much lower than 1: age compression.

---

## 18. Dashboard Requirements

The internal dashboard should eventually show both operational and research metrics.

### Operational Metrics

```text
total sessions
completed sessions
abandoned sessions
completion rate
total responses
average session duration
average response time per image
responses per image
responses per face age bin
responses per participant age group
```

### Research Metrics

```text
MAE by participant age group
Bias by participant age group
MAE by face age bin
Bias by face age bin
MAE by participant age group × face age bin
MAE by child exposure status × face age bin
MAE by child age match
```

Key visualization:

```text
participant_age_group × face_age_bin → MAE heatmap
```

Second key visualization:

```text
distance_to_nearest_child_age → absolute_error
```

---

## 19. Architecture Overview

### Logical Architecture

```text
Frontend Web App
        |
        v
Backend API
        |
        +--> Session Service
        |
        +--> Sampler Service
        |
        +--> Response Service
        |
        +--> Experiment Config Service
        |
        v
Database
        |
        +--> Sessions
        +--> Child Exposure
        +--> Face Metadata
        +--> Assignments
        +--> Responses
        |
        v
Analytics / Dashboard
```

---

## 20. Suggested Technical Direction

The implementation should stay portable because deployment may later move to Cloudflare.

Recommended direction:

```text
Frontend:
React / Next.js / TypeScript

Backend:
API routes or lightweight backend service

Database:
PostgreSQL-compatible database

Image storage:
Object storage

Analytics:
Python notebooks, SQL views, or lightweight dashboard
```

Future deployment may use:

```text
Cloudflare Pages
Cloudflare Workers
Cloudflare R2
```

But the MVP should not hard-code Cloudflare-specific assumptions unless explicitly requested later.

---

## 21. API Contract — MVP

### Create Session

```http
POST /api/session
```

Request:

```json
{
  "participant_age": 35,
  "participant_gender": "male",
  "has_child_exposure": true,
  "child_age_bins": ["3-5", "6-8"],
  "device_type": "mobile",
  "experiment_version": "mvp_001"
}
```

Response:

```json
{
  "session_id": "session_abc123",
  "assigned_trials": [
    {
      "trial_id": "trial_001",
      "trial_index": 1,
      "face_id": "face_827",
      "image_url": "/images/face_827.jpg"
    }
  ]
}
```

The response should include all 10 assigned trials.

### Submit Response

```http
POST /api/response
```

Request:

```json
{
  "session_id": "session_abc123",
  "trial_id": "trial_001",
  "face_id": "face_827",
  "predicted_age": 34,
  "response_time_ms": 4200,
  "client_order_index": 1
}
```

Response:

```json
{
  "ok": true
}
```

### Complete Session

```http
POST /api/session/complete
```

Request:

```json
{
  "session_id": "session_abc123"
}
```

Response:

```json
{
  "ok": true,
  "status": "completed"
}
```

---

## 22. Data Quality Rules

Do not delete suspicious data immediately. Flag it.

Suggested flags:

```text
response_time_ms < 300        → too_fast
response_time_ms > 60000      → too_slow
predicted_age < 1 or > 100    → reject/prevent in UI
same predicted_age for all 10 → low_effort_possible
session completed < 5 seconds → session_too_fast
```

These flags should not automatically delete the data. They should allow filtering during analysis.

---

## 23. Privacy and Ethics Notes

This project should collect the minimum possible participant data.

Do not collect:

```text
name
email
phone
exact location
IP-derived identity
account login
free text personal information
```

Participant data should be anonymous or pseudonymous.

Important: if children are allowed to participate, there may be consent requirements depending on jurisdiction and research context.

For the MVP, the system should at least include:

```text
simple explanation
anonymous participation notice
ability to stop at any time
```

Face images must come from a dataset or source with appropriate usage rights. Every image must be traceable to:

```text
source_dataset
license_type
```

Do not use random scraped faces from the internet.

---

## 24. MVP Frontend Build Order

The first implementation should focus on the interface, not complex analytics.

### Build Step 1 — Static Prototype

Use mock image data.

Implement:

```text
Landing screen
Consent screen
Age/gender screen
Child exposure screen
10-card guessing flow
Thank-you screen
```

Store responses temporarily in frontend state and print final JSON to console.

### Build Step 2 — Local Data Structure

Create mock objects:

```ts
type FaceImage = {
  face_id: string;
  image_url: string;
  true_age: number;
  true_age_bin: string;
  face_gender: "female" | "male" | "other" | "unknown";
};
```

Create session object:

```ts
type ParticipantSession = {
  session_id: string;
  participant_age: number;
  participant_age_group: string;
  participant_gender: string;
  has_child_exposure: boolean | null;
  child_age_bins: string[];
  experiment_version: string;
  started_at: string;
};
```

Create response object:

```ts
type TrialResponse = {
  trial_id: string;
  session_id: string;
  face_id: string;
  predicted_age: number;
  response_time_ms: number;
  trial_index: number;
  submitted_at: string;
};
```

### Build Step 3 — Smooth Experiment Flow

Requirements:

```text
no page reloads
preload next image
progress indicator
large image card
large numeric age input
fast submit
mobile-first layout
```

### Build Step 4 — Backend Integration

Only after the UI flow is stable:

```text
POST /api/session
POST /api/response
POST /api/session/complete
```

---

## 25. Visual Direction

The UI should be clean and minimal.

### Style

```text
large face card
rounded corners
high contrast text
one primary action per screen
minimal copy
mobile-first spacing
smooth transitions
```

### Card Layout

Approximate mobile structure:

```text
------------------------------------------------
3 / 10

[            FACE IMAGE CARD                  ]
[                                             ]
[                                             ]
[                                             ]

How old is this person?

              [?]
          -         +

          Continue
------------------------------------------------
```

After the participant selects a number:

```text
              34
```

Continue button becomes active.

---

## 26. Strict Product Constraints

The agent must not add features that increase friction.

Do not add:

```text
login
account creation
email collection
leaderboard
sharing requirement
long survey
country question
education question
confidence rating
free text input
feedback after each image
correct answer after each image
AI prediction
```

Not in MVP.

---

## 27. Experiment Versioning

Every meaningful change should create a new experiment version.

Examples of version-changing modifications:

```text
changing image set
changing age input component
showing feedback
changing number of trials
changing question wording
changing sampling algorithm
changing allowed age range
```

Initial version:

```text
mvp_001
```

---

## 28. Non-Goals

This project is not currently trying to:

```text
train an AI model
build a commercial app
identify users
score individual intelligence
diagnose perceptual ability
rank participants
produce clinical conclusions
```

The goal is population-level behavioral data.

---

## 29. Success Criteria for MVP

The MVP is successful if:

```text
participants can complete the full flow in under 60 seconds
the app works well on mobile
each participant sees exactly 10 images
responses are saved with response time
sessions are anonymous
image assignment is stored
research metrics can be computed from the saved data
```

Minimum viable dataset for early analysis:

```text
at least 100 completed sessions
at least 1,000 total responses
coverage across multiple participant age groups
coverage across all face age bins
```

A stronger dataset would require much more balanced recruitment across ages, especially children and older adults.

---

## 30. Most Important Instruction to the Development Agent

The most important thing is not the UI, the database, or the deployment.

The most important thing is preserving the research design.

This app must collect data that can answer the core question:

> **Are people better at estimating ages they personally resemble, or ages they are regularly exposed to?**

Every product and engineering decision should protect that research question.

Do not add convenience features that bias the experiment.

Do not add feedback that creates learning during the session.

Do not add default values that anchor guesses.

Do not collect unnecessary personal data.

Do not make the task longer than necessary.

Build a fast, clean, anonymous, 10-image age-estimation experiment that produces analyzable research data.

---

## 31. Immediate Task for Claude

Start by implementing the **frontend MVP prototype**.

The first deliverable should be a working browser flow with mock data:

```text
Landing
Consent
Participant details
Child exposure
10 image cards
Thank-you screen
Final JSON output
```

Use placeholder/mock images at first.

The frontend should generate a mock session and collect responses into a structured object matching the planned data model.

No real backend is required for the first prototype unless explicitly requested.

The first prototype should prove:

```text
the user experience is smooth
the task feels short
the data structure is correct
the research flow is preserved
```

Only after that should backend, database, deployment, and analytics be implemented.
