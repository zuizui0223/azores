# Developmental result: Durif stage predicts migration initiation and latency

## Data reconstruction

All six large/small public per-project migration tables were read through the Git blob API and joined to the public capture metadata.

Primary female stages:

- FIII
- FIV
- FV

Across the six projects, **575** exact-stage individuals were represented in the migration tables.

Coverage relative to the corresponding primary-stage metadata was high but not complete:

- 575/603 primary-stage metadata individuals represented;
- 28 missing from migration files;
- missing by stage: FIII 13, FIV 2, FV 13.

## Raw initiation pattern

Among individuals represented in the migration files:

| Stage | n | Initiated migration | Proportion | Median days to first migration among initiators |
|---|---:|---:|---:|---:|
| FIII | 261 | 161 | 0.617 | 4.86 d |
| FIV | 68 | 54 | 0.794 | 0.22 d |
| FV | 246 | 216 | 0.878 | 0.69 d |

These raw values are descriptive only because projects, years, body size and release timing differ among stages.

## Adjusted initiation model

The initiation model used:

- project × release-year fixed effects;
- body length centered within project-year, per 100 mm;
- release timing centered within project-year, per 100 days;
- ordinal Durif stage FIII=0, FIV=1, FV=2.

Eleven informative project-year strata contributed **525** individuals.

### Durif stage

Per one-stage increment:

- OR = **1.99**
- 95% CI = **1.49–2.66**
- p = **3.2e-6**

### Body length

Per 100 mm:

- OR = **1.37**
- 95% CI = **1.00–1.89**
- p = **0.053**

### Release timing

Per 100 days later:

- OR = **1.30**
- 95% CI = **0.68–2.50**
- p = **0.426**

Thus advanced capture-time silvering stage predicts whether movement begins even after major design/timing covariates are represented.

## Latency among initiators

Among **431** individuals with a detected migration onset, log(1 + days to first migration) was modelled with project fixed effects plus body length, release timing and ordinal Durif stage.

Per one-stage increment:

- multiplicative factor on 1+latency = **0.656**
- 95% CI = **0.524–0.821**
- p = **0.00023**

Thus advanced stage is associated not only with a higher probability of beginning migration, but with shorter delay before movement.

## Adversarial missingness test

Twenty-eight primary-stage metadata individuals were absent from the migration tables.

To bias maximally **against** a positive stage effect, all missing FIII individuals were forced to "initiated" and all missing FIV/FV individuals were forced to "not initiated".

Under the same project-year/body-size/release-timing model:

- OR per stage = **1.74**
- 95% CI = **1.32–2.28**

The positive stage gradient therefore survives this deliberately hostile missing-outcome assignment.

## Ecological interpretation

The Europe-wide evidence now supports a stronger internal-state statement:

> **Silvering stage predicts multiple sequential components of realised migration: initiation probability, delay to initiation, and eventual successful-migrant status.**

This is more informative than a single final success endpoint.

## External gating clue from project-specific latency

The raw project patterns also show that high readiness does not produce the same timing everywhere.

Examples:

- Leopoldkanaal: median onset FIII ≈ 71 d, FIV/FV ≈ 0 d;
- 2015 phd_verhelst_eel: FIII ≈ 322 d, FIV/FV ≈ 0.1 d;
- Warnow: all stages relatively fast, advanced stages <1 d;
- Grotenete: even FIV/FV individuals waited roughly 30–37 d;
- ESGL: onset remained slow and initiation uncommon across stages.

This heterogeneity is biologically important.

It is compatible with:

> **internal state sets readiness to move, while hydrological/landscape opportunity determines when that readiness can be expressed.**

It does not by itself identify which external variable caused the project differences.

## Claim boundary

- The published migration classifier is used as the **outcome**, not the Durif predictor.
- This analysis is developmental independent evidence because the public endpoint was inspected during hypothesis refinement.
- Project-specific delay differences cannot be attributed to WRS, discharge or barrier type without direct within-system tests.
- The general state × landscape-opportunity law still requires independent confirmation.
