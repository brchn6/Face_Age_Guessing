# Phase 5B — Free Dataset Search

Date: 2026-07-09  
Current prototype version: `mvp_003`

## Scope

Search and triage free/no-cost face-age datasets that might support the age-guessing experiment.

This is **not approval to use any dataset yet**. “Free to download” does not mean “safe to use in a public web experiment.” Each candidate still needs license, provenance, child-image permissions, and web-display rights verified before any image is downloaded or integrated.

No images were downloaded in this phase.

## Research Requirements

The experiment needs real face images with:

- exact or reliable `true_age`
- coverage across MVP age bins
- clear licensing and provenance
- permission for web display in an experiment
- especially clear rights for images of minors
- metadata compatible with `docs/face-image-manifest-template.csv`

MVP bins:

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

## Shortlist Result

### Best candidates for terms review

These are not approved yet, but are worth checking first:

1. **FG-NET Aging Database**
   - Why: includes children and adults; age-progression research dataset.
   - Problem: small, repeated identities, public web-display rights unclear.
   - Use case if approved: small pilot / child-bin proof of concept, not full MVP alone.

2. **APPA-REAL / ChaLearn apparent-age style datasets**
   - Why: age-perception context; may include real and apparent age labels.
   - Problem: source licensing and web-display rights must be checked carefully.
   - Use case if approved: candidate for age-estimation pilot with real-age labels.

3. **Controlled adult face databases** such as Chicago Face Database / FACES-style datasets / lab-created adult sets
   - Why: better consent/provenance than scraped datasets.
   - Problem: usually adult-only; exact age and web-display permission must be confirmed.
   - Use case if approved: adult bins only, as supplement to separate child source.

4. **AFAD / similar age-estimation research datasets**
   - Why: may include exact age labels and non-celebrity face data.
   - Problem: limited age range, demographic concentration, rights need review.
   - Use case if approved: teen/adult bins only.

### Not recommended for deployment

These may be free/no-cost but are poor or risky fits:

- **UTKFace-style broad-age web datasets**
  - Broad ages, but provenance/consent/public-display rights are unclear.
  - Especially risky for child images.

- **IMDB-WIKI / CACD / AgeDB-style celebrity datasets**
  - Celebrity/public-figure bias.
  - Noisy age labels.
  - Recognizability can affect participant behavior.
  - Rights/public-display concerns.

- **Adience / FairFace-style age-bin datasets**
  - Age bins, not exact true age.
  - Cannot support the primary metric `abs(predicted_age - true_age)`.

- **MORPH-style datasets**
  - Often restricted/not free or adult-heavy.
  - Could be reviewed only if access and display rights are available.

- **AI-generated faces**
  - No real chronological age.
  - Rejected because this is a real human facial-age perception experiment.

## Candidate Notes

### FG-NET Aging Database

Potential strengths:

- Has age-progression images.
- Includes children, which is rare and important here.
- Often referenced in facial aging research.

Risks:

- Small sample size.
- Multiple images per identity may create repeated-identity bias.
- Dataset terms and public web display rights need explicit confirmation.
- May not provide enough independent active images per MVP bin.

Verdict:

> Review terms first. Candidate for limited pilot only if web display is allowed.

### APPA-REAL / ChaLearn apparent age datasets

Potential strengths:

- Built around perceived/apparent age tasks.
- May include real-age labels.
- Relevant to human age-estimation framing.

Risks:

- Must distinguish apparent age labels from true chronological age.
- Source image rights and web display rights must be confirmed.
- Child coverage may be insufficient or unclear.

Verdict:

> Good terms-review candidate. Do not use until exact true-age availability and display rights are confirmed.

### Chicago Face Database / controlled adult datasets

Potential strengths:

- Better-controlled images.
- More likely to have consent/provenance than scraped datasets.
- Useful for adult age bins if exact age is available.

Risks:

- Usually adult-only.
- May not include enough older adults.
- May restrict redistribution/public display.
- Some datasets include perceived age rather than exact true age.

Verdict:

> Candidate for adult bins only after terms review.

### FACES-style adult lifespan datasets

Potential strengths:

- Controlled face images across adult age ranges.
- Better provenance than scraped web sets.

Risks:

- Usually not children.
- Access/usage may require application.
- Public web display may not be allowed.

Verdict:

> Candidate for adult/older bins only after terms review.

### AFAD-style datasets

Potential strengths:

- Age-estimation research context.
- Exact age labels may be available.

Risks:

- Often limited to specific demographics/age ranges.
- May not cover children or older adults well.
- License/web-display rights need review.

Verdict:

> Candidate for teen/adult bins only if license allows.

### UTKFace-style datasets

Potential strengths:

- Broad age coverage.
- Convenient age/gender labels.
- Easy to find/download.

Risks:

- Commonly distributed as web-collected images.
- Consent/provenance unclear.
- Public display rights unclear.
- Child image rights unclear.
- Filenames often expose metadata unless reprocessed.

Verdict:

> Reject for public MVP deployment unless rights/provenance are explicitly proven. Not recommended.

### IMDB-WIKI / CACD / AgeDB-style celebrity datasets

Potential strengths:

- Large and easy to access.
- Many age-labeled images.

Risks:

- Celebrity bias.
- Recognizable faces may bias estimates.
- Age labels can be inferred/noisy.
- Rights/public-display issues.
- Weak child coverage for this experiment.

Verdict:

> Reject for MVP deployment.

### Adience / FairFace-style datasets

Potential strengths:

- Common benchmarks.
- Some demographic metadata.

Risks:

- Age bins instead of exact true age.
- Does not support primary response-level error metric.
- May have license/display constraints.

Verdict:

> Reject as primary source.

## Practical Recommendation

For a real MVP, use a hybrid sourcing plan:

1. **Children / teens (`4-17`)**: consented/source-controlled collection is strongly preferred.
2. **Adults (`18-60`)**: review controlled adult datasets first; use only if exact age and web display are allowed.
3. **Fallback**: consented collection for all bins if dataset terms are too restrictive.

## Next Concrete Step

Before downloading anything, create a terms-review checklist for the top candidates:

1. FG-NET
2. APPA-REAL / ChaLearn apparent-age dataset family
3. One controlled adult face dataset, e.g. Chicago Face Database or FACES-style adult dataset
4. AFAD-style age dataset if adult/teen coverage is needed

For each candidate, answer:

- Is exact true age available?
- Are minors included?
- Is public web display allowed?
- Is research use allowed?
- Is redistribution prohibited?
- Can images be processed/resized?
- Are attribution or citation requirements compatible with the app?
- Can source metadata map into the manifest?

## Current Decision

No free dataset is approved for use yet.

The least risky path remains consented/source-controlled collection, especially for child images.
