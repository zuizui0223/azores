# Developmental result: Durif stage predicts detected migration onset

## Why this outcome matters

The earlier analysis used the published successful-migrant endpoint.

A stronger biological question is upstream of final success:

> **does capture-time migratory readiness predict whether and how quickly directed migration is detected to begin?**

The public per-project migration tables allow the first later row classified as migration to be reconstructed for six projects.

Large migration files were read through the Git blob/raw data path rather than the GitHub Contents API size-limited response.

## Data coverage

Exact FIII/FIV/FV individuals with usable migration-table records:

- joined stage-tagged individuals: **575**;
- final Cox analysis after project-year/follow-up eligibility: **525**;
- informative project × release-year strata: **11**.

The corresponding `life4fish` stage-coded cohort cannot be included because the public migration directory contains no `migration_life4fish.csv`.

Stage-tagged metadata individuals with no rows in a migration table are not silently counted as non-migrants.

## Descriptive detected-onset pattern

Within the Cox-analysis cohort:

| Durif stage | n | detected onset | descriptive fraction | median detected onset among events |
|---|---:|---:|---:|---:|
| FIII | 255 | 155 | 60.8% | 5.85 d |
| FIV | 67 | 53 | 79.1% | 0.16 d |
| FV | 203 | 174 | 85.7% | 0.70 d |

These fractions are descriptive because observation follow-up differs.

## Stratified survival result

Cox proportional-hazards model stratified by **project × release year**.

### Stage-only

Per one Durif increment FIII -> FIV -> FV:

- hazard ratio = **1.32**
- 95% CI **1.16–1.50**
- p = **1.9e-5**

### Adjusted model

Covariates:
- ordinal Durif stage;
- body length centered within project-year, per 100 mm;
- release day-of-year centered within project-year, per 100 days.

Durif stage:

- HR = **1.30**
- 95% CI **1.14–1.48**
- p = **9.5e-5**

Body length:

- HR = **1.04**
- 95% CI **0.91–1.19**
- p = **0.54**

Release timing:

- HR = **1.19**
- 95% CI **0.84–1.66**
- p = **0.33**

## Biological interpretation

Together with the successful-migrant analysis, this strengthens the internal-state result.

More advanced Durif stage is associated with:

1. greater odds of the later successful-migrant endpoint;
2. earlier **detected** onset of migration.

The signal therefore is not confined to final passage success.

## Important censoring boundary

Non-onset individuals are right-censored at their final recorded detection.

That is an observation endpoint, not guaranteed continued biological presence.

In particular, descriptive censor times differ among stages, so loss of detection could be informative.

Therefore the correct claim is:

> **capture-time Durif readiness predicts earlier detected migration onset in the observed telemetry histories.**

Do not write:

> Durif stage proves the physiological hazard of migration initiation.

The stronger causal/physiological interpretation requires tracking designs with known observation coverage or independent state-transition measurements.

## Consequence for the Azores paper

The internal-state half of mobility gating is now supported by two distinct telemetry outcomes:

- final successful migration;
- detected migration onset.

The unresolved—and now more interesting—part is why the size of the stage advantage differs among landscapes.

That is the target of the independent consecutive-barrier confirmation programme.
