# Phase 5B — Real Image Sourcing Plan

Date: 2026-07-09  
Current prototype version: `mvp_003`

## Scope

Plan how to replace mock SVG faces with real, licensed, research-safe face images.

This phase is a planning/requirements phase only. It does **not** add real images, backend storage, database tables, participant recruitment, or analytics.

## Core Rule

Do **not** use random scraped faces from the internet.

Every face image must be traceable to a source with clear usage rights and enough metadata to support analysis.

## Why This Phase Matters

The app’s research value depends on knowing each face image’s true age and metadata. Poor image sourcing would make the experiment unusable or unethical.

The key research question is:

> Are people better at estimating ages they personally resemble, or ages they are regularly exposed to?

So the image pool must be balanced enough that participant groups see comparable face-age coverage.

## Required Face Image Metadata

Each real image must have at minimum:

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

Recommended additional source-control fields:

- `source_record_id`
- `source_url_or_reference`
- `license_url_or_terms_reference`
- `usage_notes`
- `attribution_required`
- `web_display_allowed`
- `commercial_use_allowed`
- `research_use_allowed`
- `age_at_photo_verified`
- `image_processed_at`

## MVP Age Bins

The MVP session design requires exactly one image from each bin:

- `4-6`
- `7-9`
- `10-12`
- `13-17`
- `18-24`
- `25-31`
- `32-38`
- `39-45`
- `46-52`
- `53-60`

## Minimum Image Pool Targets

### Absolute minimum pilot

- 5 usable images per age bin
- 50 images total

This is enough only for internal testing and very early pilots.

### Better MVP launch target

- 20 usable images per age bin
- 200 images total

This reduces repeated images and gives the sampler room to balance ratings per image.

### Stronger research target

- 50+ usable images per age bin
- 500+ images total

This is preferable once real participant collection begins.

## Balance Requirements

For each age bin, aim for:

- balanced or at least recorded face gender
- consistent image quality
- no visible age labels or filename clues
- frontal or near-frontal faces where possible
- similar crop/framing
- no extreme filters or distortions
- no celebrity/recognizable-public-figure bias if avoidable

Ethnicity can be recorded only if ethically and legally appropriate for the source and if it is already part of the dataset metadata. It is optional for MVP and must not block launch.

## Child Image Caution

Child images are essential for the research question, but they are also the highest-risk category.

For any image under 18:

- require especially clear source permissions
- require clear research/display rights
- avoid ambiguous web-scraped datasets
- prefer controlled datasets, institutional datasets, or explicit consented collection
- do not expose true age in public image paths or filenames

If child-image licensing is not clear, do not use the image.

## Source Strategy Options

### Option A — Purpose-built consented image collection

Best research/ethics option if feasible.

Pros:

- explicit consent
- exact age can be collected
- consistent metadata
- usage rights are controlled

Cons:

- slower
- requires consent process
- harder to collect children ethically

### Option B — Controlled academic datasets / data-use agreements

Good option if terms allow web experiment display.

Pros:

- often has metadata and consent procedures
- better provenance than scraped datasets

Cons:

- access may require applications or agreements
- terms may prohibit redistribution or public web display
- child coverage may be limited

### Option C — Open/public datasets with clear licenses

Only acceptable if licensing and web-display rights are explicit.

Pros:

- faster to prototype with real faces

Cons:

- license ambiguity is common
- age labels may be noisy
- some datasets are scraped or celebrity-based
- child-image rights may be unclear

## Rejected For Now

Do not use these for research deployment without explicit later approval:

- random Google Images / social media / web scraping
- AI-generated faces
- faces with no known true age
- faces where only broad age group is known
- datasets whose license does not clearly allow this use
- datasets where public web display is prohibited
- public filenames/URLs that reveal age or identity

AI-generated faces are rejected because this is a human age-estimation study on real facial age perception, not synthetic-face perception.

## Image Processing Rules

Before integration:

1. Store raw/source images outside the frontend bundle.
2. Create processed display images with neutral filenames, e.g. `face_000123.webp`.
3. Do not include true age or age bin in public filenames.
4. Use consistent crop/framing where possible.
5. Resize/compress for mobile performance.
6. Keep source provenance in metadata, not filenames.
7. Mark questionable images `is_active: false` instead of deleting them.

## Manifest Workflow

1. Create a candidate source review.
2. Confirm license/terms.
3. Acquire images outside git, e.g. `data/raw/`.
4. Build a manifest using the template in `docs/face-image-manifest-template.csv`.
5. Run manual quality review.
6. Process selected images into display assets.
7. Assign stable `face_id` values.
8. Integrate the manifest into the future backend/database.

Do not commit real face images to git until storage and license policy are explicitly approved.

## Experiment Versioning

Replacing the mock image set with a real image set is a meaningful experiment-version change.

When real images are integrated, the experiment version should move from:

```text
mvp_003
```

to a new version, likely:

```text
mvp_004
```

The exact version should be recorded when the final image set is approved.

## Acceptance Criteria Before Real Images Are Used

Real images may be used only when:

- each image has required metadata
- each image has clear source/license documentation
- public display is allowed
- child images have especially clear permission
- image filenames do not leak true age
- each MVP age bin has enough active images
- the sampler can still assign exactly one image per age bin
- admin approves the source and manifest

## Phase 5B Result

Status: **plan ready for admin review**

Recommended next step:

1. Admin chooses preferred sourcing path: consented collection, academic datasets, or clearly licensed public datasets.
2. Create a source review document for specific candidate datasets before downloading or integrating images.
