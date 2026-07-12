# Phase 5C — Preliminary Image Source Review

Date: 2026-07-09  
Current prototype version: `mvp_003`

## Scope

Review possible paths for obtaining real face images for the age-guessing experiment.

This is a **preliminary product/research review**, not a legal review. Any dataset or collection method must still have its license, consent terms, and web-display rights verified before images are downloaded, processed, committed, or shown in the app.

## Source Requirements Recap

A source is usable only if it can provide or support:

- exact or reliable `true_age`
- enough coverage across the 10 MVP age bins
- clear source provenance
- clear license / usage terms
- explicit permission for web experiment display
- especially clear permission for images of minors
- no requirement to reveal identity or true age publicly
- stable metadata suitable for the manifest

## Decision Summary

Recommended path:

> Use a consented/source-controlled collection as the primary path, especially for child images. Consider controlled academic datasets only after explicit usage-rights verification. Do not use scraped celebrity/public web datasets for research deployment.

## Candidate Review Matrix

| Source / Path | Coverage Fit | Metadata Fit | Rights Risk | Child Image Fit | Current Decision |
|---|---:|---:|---:|---:|---|
| Purpose-built consented collection | High if recruited well | High | Low if consent is designed correctly | Best option | Recommended primary path |
| Academic dataset with data-use agreement | Medium to high | Medium to high | Medium; depends on terms | Possible but must verify | Candidate after terms review |
| Clearly licensed public dataset | Medium | Variable | Medium to high | Usually risky | Candidate only if license is explicit |
| UTKFace-style scraped broad-age datasets | High age coverage | Medium | High | High risk | Reject for deployment unless provenance/rights are proven |
| Celebrity datasets such as IMDB-WIKI / CACD / AgeDB | Adult-heavy / celebrity-biased | Medium/noisy | High | Poor | Reject for MVP deployment |
| Age-bin-only datasets such as Adience/FairFace | Poor for exact-age error | Poor for `true_age` | Variable | Poor | Reject for primary experiment |
| AI-generated faces | Not real age perception | Invalid | N/A | N/A | Reject |

## Path A — Purpose-Built Consented Collection

### Summary

Collect images specifically for this experiment with explicit consent and metadata.

### Strengths

- Best ethical and research fit.
- Exact age can be collected at the time of photo.
- Consent language can explicitly allow web experiment display.
- Image quality, crop, and metadata can be standardized.
- Especially important for minors.

### Weaknesses

- Slower than downloading a dataset.
- Requires consent process and storage discipline.
- Child images require parent/guardian consent and careful handling.

### Recommendation

Use this as the preferred long-term route, especially for the child bins:

- `4-6`
- `7-9`
- `10-12`
- `13-17`

### Minimum consent fields to define before collecting

- permission to use image in anonymous age-estimation experiment
- permission to display image to participants online
- whether image may be stored and processed
- whether image may be used in future versions of the same experiment
- withdrawal/removal contact/process
- parent/guardian consent for minors
- confirmation of age at photo

## Path B — Controlled Academic Dataset / Data-Use Agreement

### Summary

Use datasets from academic/institutional sources where terms are explicit and may require application or agreement.

### Strengths

- Better provenance than scraped internet datasets.
- Often includes metadata.
- Some datasets include exact age or age at photo.

### Weaknesses

- Terms may prohibit redistribution or public web display.
- Access may require an application.
- Child coverage may be limited.
- Identity repetition can bias results if many images are from the same person.

### Potential candidates to investigate

These are **not approved** yet. They require terms review.

#### FG-NET Aging Database

Potential value:

- Known for age progression / aging research.
- May include a wide age range, including children.

Risks / questions:

- Small dataset and repeated identities.
- Usage rights and public web display must be verified.
- May not provide enough independent images per MVP bin.

Current decision:

- Candidate for terms review only; not approved.

#### MORPH-style datasets

Potential value:

- Larger age-annotated face datasets.
- Often used in age-estimation research.

Risks / questions:

- Adult-heavy; likely poor child-bin coverage.
- Access and display rights may be restricted.
- May not allow public web experiment display.

Current decision:

- Possible adult-bin source only if terms allow; not a full MVP solution.

#### Controlled adult face databases

Examples include lab-created adult face datasets.

Potential value:

- Higher image quality and controlled conditions.
- More reliable rights than scraped datasets.

Risks / questions:

- Usually adult-only.
- Often provides perceived age rather than true age.
- May not cover child bins or older bins adequately.

Current decision:

- Useful only as supplementary adult-bin source if true age and display rights are clear.

## Path C — Clearly Licensed Public Datasets

### Summary

Use public datasets only if their license explicitly permits this experiment, including online display.

### Strengths

- Faster to test than building a consented collection.
- May have broad age coverage.

### Weaknesses

- Many public face-age datasets are scraped, celebrity-based, or license-ambiguous.
- True age may be noisy or inferred.
- Child-image rights are often unclear.
- Public display may be prohibited even if research download is allowed.

### Potential candidates to investigate

#### APPA-REAL-style apparent-age datasets

Potential value:

- Designed around age perception tasks.
- May include real/apparent age labels depending on source.

Risks / questions:

- Need to verify exact true-age availability.
- Need to verify image-source licenses and public display rights.
- Need to confirm child coverage.

Current decision:

- Candidate for terms review only; not approved.

#### UTKFace-style broad-age datasets

Potential value:

- Broad age coverage.
- Convenient labels.

Risks / questions:

- Commonly distributed as internet-collected images.
- Source consent/provenance may be unclear.
- Public display rights are not automatically established.
- Some filenames expose age unless reprocessed.

Current decision:

- Reject for deployment unless provenance and rights are explicitly proven.

## Rejected / Not Suitable for MVP Deployment

### Celebrity datasets: IMDB-WIKI, CACD, AgeDB-style sources

Reasons:

- celebrity/public figure bias
- age labels can be noisy or inferred from timestamps
- often adult-heavy
- child-image coverage is weak or ethically complicated
- licenses/public display rights may be unclear
- recognizable identity may change participant behavior

Decision:

- Reject for MVP deployment.

### Age-bin-only datasets: Adience/FairFace-style sources

Reasons:

- do not reliably provide exact `true_age`
- cannot support the primary metric `absolute_error = abs(predicted_age - true_age)`
- age bins are not enough for precise response-level analysis

Decision:

- Reject as primary research image source.

### AI-generated faces

Reasons:

- no real chronological age
- does not test perception of real human facial age
- would change the scientific question

Decision:

- Reject.

## Recommended Source Strategy

### Short-term internal pilot

Use mock placeholders only until a real source is approved.

Do not use scraped placeholder faces.

### MVP real-image route

Use a hybrid plan:

1. Build or acquire a consented/source-controlled child image set for ages 4–17.
2. Review controlled academic/adult datasets for ages 18–60 if terms allow online display.
3. If no adult dataset has acceptable rights, extend consented collection to adults as well.
4. Use the manifest template before integration.
5. Keep all raw images out of git.

## Source Approval Checklist

A candidate source can move forward only if all are true:

- [ ] Exact age or age at photo is available.
- [ ] License/terms are documented.
- [ ] Web experiment display is allowed.
- [ ] Research use is allowed.
- [ ] Child image rights are explicit if minors are included.
- [ ] Images can be stored/processed for display.
- [ ] Public filenames can be neutralized.
- [ ] Metadata can be mapped into `docs/face-image-manifest-template.csv`.
- [ ] Admin approves the source before download/integration.

## Open Questions for Admin

1. Are we willing to run a consented image collection, especially for child images?
2. Is this project affiliated with an institution that can request academic dataset access?
3. Is public web display required for the first real-image pilot, or can early testing be private/internal?
4. Should the first real-image target be the absolute minimum pilot size of 50 images, or the better MVP target of 200 images?

## Recommendation

Start with consented collection planning for child bins and parallel terms review for one or two controlled adult datasets.

Do **not** download or integrate any public/scraped age-face dataset yet.
