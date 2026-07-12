# Data Fetch Agent Runbook

Date: 2026-07-12

Purpose: prevent future agent confusion when the admin asks to "fetch data" or "fetch the dataset".

## Diagnosis of the previous failure mode

The project docs correctly blocked unsafe use of real face images, but the wording was easy for an agent to interpret too broadly.

The intended rule was:

> Do not download, commit, integrate, or publicly display real face images until rights and admin approval are clear.

The agent appears to have treated that as:

> Do not fetch anything related to datasets.

That is too restrictive. Source-page review, license review, metadata inspection, and approved local-only acquisition are different actions.

## Meaning of “fetch” in this project

### 1. Fetch source pages / terms for review — allowed

When asked to review or fetch information about a candidate dataset, the agent should proceed without looping, if network access is available.

Allowed actions:

- read public dataset pages
- download or save license/terms pages for review
- inspect public metadata/schema descriptions
- summarize access requirements
- create or update a terms-review document

This does **not** approve the images for app use.

### 2. Download dataset files locally — allowed only with explicit admin approval

The agent may download candidate dataset files only when the admin explicitly names the source and approves local acquisition for review.

Required constraints:

- store files only under ignored local paths such as `data/raw/<source>/`
- do not commit raw images or archives
- do not copy images into `frontend/`
- do not integrate images into the app
- record the source URL, command used, timestamp, and any license/terms notes
- stop if access requires login, application approval, a data-use agreement, or manual consent

A safe approval phrase is:

```text
Approve local-only download of <SOURCE> to data/raw/<source>/ for license/metadata review. Do not integrate into the app.
```

### 3. Integrate real images into the app — blocked until full approval

The agent must not integrate real face images into the frontend or backend until all approval checklist items are complete:

- exact true age is available
- license/terms are documented
- research use is allowed
- public web experiment display is allowed
- child-image permissions are explicit if minors are included
- image processing/resizing is allowed
- metadata maps into `docs/face-image-manifest-template.csv`
- admin approves the source and manifest
- experiment version is bumped from `mvp_003`, likely to `mvp_004`

## Required agent behavior when asked to fetch data

1. Identify which fetch level the admin means:
   - source/terms review
   - local-only dataset acquisition
   - app integration
2. If the request is source/terms review, proceed.
3. If the request is local download but approval is missing, ask for the exact approval phrase once.
4. If the request is integration, verify the full approval checklist first.
5. If blocked, state the exact blocker and the next command/approval needed. Do not silently refuse and do not repeat generic warnings.

## Candidate-specific handling

### FG-NET

Current preferred first candidate for terms review.

Agent should:

- fetch/review public source pages and terms if accessible
- determine whether exact ages are available
- determine whether public web experiment display is allowed
- determine whether access requires registration/application
- stop before downloading images unless local-only admin approval is explicit

### Chicago Face Database / FACES Lifespan

Adult-only backup candidates.

Agent should:

- review terms and access process
- confirm exact true age availability
- confirm whether online experiment display is allowed
- treat them as adult-bin supplements only unless documentation says otherwise

### UTKFace / IMDB-WIKI / CACD / AgeDB / Adience / FairFace

Do not use for MVP deployment under current project decisions.

Agent may only review terms if explicitly asked. Do not download or integrate them unless the admin gives a separate, explicit local-only review instruction and acknowledges they are not approved for deployment.

## Practical next action from current state

Current fetched-materials status is documented in `docs/dataset-download-inspection.md`.

The next safe action is:

> Review the fetched FG-NET/Chicago/FACES inspection results, decide whether to complete official access forms for Chicago Face Database and FACES, and keep all real images out of the app until source/manifest approval is complete.
