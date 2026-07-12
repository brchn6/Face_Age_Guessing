# Candidate Dataset Source Links

Date: 2026-07-09

Purpose: quick admin review links for candidate real face-age data sources.

Important: these are **links for review only**. No dataset below is approved for use yet. Agents should read `docs/data-fetch-agent-runbook.md` before acting on any "fetch data" request. Fetching public source pages and license terms for review is allowed. Downloading dataset files requires explicit local-only admin approval. Committing or integrating images is blocked until license terms, public web-display rights, child-image permissions, source provenance, manifest mapping, and admin approval are complete.

## Priority candidates to inspect first

### FG-NET Aging Database

Useful because it may include child and adult age-progression images.

- https://yanweifu.github.io/FG_NET_data/
- https://www.fgnet.rsunit.com/

Review questions:

- Are exact ages available?
- Are child image rights clear?
- Is public web experiment display allowed?
- Are repeated identities acceptable for a pilot?

### ChaLearn / APPA-REAL apparent-age datasets

Useful because it is close to age-estimation / apparent-age research.

- https://chalearnlap.cvc.uab.cat/dataset/26/description/

Review questions:

- Does the dataset include true chronological age, not only apparent age?
- Are source images licensed for public web display?
- Does it include enough child/teen images?

### Chicago Face Database

Controlled adult face dataset. Likely adult-bin only.

- https://www.chicagofaces.org/

Review questions:

- Is exact age available?
- Are images allowed in an online experiment?
- Are redistribution/display restrictions compatible with this project?

### FACES Lifespan Database

Controlled adult/older adult face dataset. Likely adult/older-bin only.

- https://faces.mpdl.mpg.de/

Review questions:

- Is exact age available?
- Is online experiment display allowed?
- Does the age range cover the MVP adult bins?

## Free/no-cost but risky candidates

### UTKFace

Broad age coverage but high provenance/consent/public-display risk.

- https://susanqq.github.io/UTKFace/

Current project verdict: not approved for public MVP deployment unless rights/provenance are proven.

### IMDB-WIKI

Large celebrity dataset; rejected for MVP because of celebrity bias, noisy labels, and rights concerns.

- https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/

Current project verdict: rejected for MVP deployment.

### Adience

Age-bin dataset, not exact true age; cannot support the main absolute-error metric.

- https://talhassner.github.io/home/projects/Adience/Adience-data.html

Current project verdict: rejected as primary source.

## Search terms for additional candidate discovery

Use these only for source review, not automatic download:

- `face aging database exact age license web display`
- `facial age estimation dataset true age license`
- `academic face database age metadata usage agreement`
- `child face aging dataset consent research license`
- `apparent age dataset true age license`

## Minimum approval checklist before download

For any candidate source, answer all of these first:

- [ ] Exact true age is available.
- [ ] License or terms are documented.
- [ ] Public web experiment display is allowed.
- [ ] Research use is allowed.
- [ ] Image processing/resizing is allowed.
- [ ] Child image permissions are explicit if minors are included.
- [ ] Source metadata can map into `docs/face-image-manifest-template.csv`.
- [ ] Admin approves before download/integration.
