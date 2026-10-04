# Durif stage predicts migration onset in the observable telemetry cohort

## Scope

This analysis uses the six project-level processed migration tables in which FIII/FIV/FV individuals have usable migration histories:

- 2011 Warnow
- 2012 Leopoldkanaal
- 2013 Albertkanaal
- 2015 phd_verhelst_eel
- 2019 Grotenete
- ESGL

The processed migration tables contain **575** exact-stage individuals.

This is not the full 737-individual FIII/FIV/FV metadata cohort. Therefore all initiation statements are conditional on inclusion in the processed migration tables.

Do **not** interpret the raw rates below as population-wide migration probabilities.

## Raw observable-cohort pattern

Within the 575-individual processed cohort:

| Durif stage | n | migration classified | proportion |
|---|---:|---:|---:|
| FIII | 261 | 161 | 0.617 |
| FIV | 68 | 54 | 0.794 |
| FV | 246 | 216 | 0.878 |

Among individuals with a migration event, crude median release-to-onset time was:

- FIII: ~4.86 d in the full observable cohort;
- FIV: ~0.22 d;
- FV: ~0.69 d.

These crude medians are heavily project/timing dependent and are not the primary inference.

## Adjusted initiation model

A logistic model was restricted to informative project × release-year strata with:

- at least one event and one non-event;
- at least two Durif stages.

Covariates:

- project × release-year fixed effects;
- within-stratum body length per 100 mm;
- within-stratum release timing per 100 d;
- ordinal Durif score FIII=0, FIV=1, FV=2.

Adjusted cohort:

- **n = 525**
- 11 informative project-year strata.

Results:

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

Per 100 d:

- OR = **1.30**
- 95% CI = **0.68–2.50**
- p = **0.426**

## Time-to-onset model

To retain non-initiators rather than analysing event times only, the same observable cohort was analysed with a **project-year-stratified Cox model**.

For non-initiators, follow-up was censored at the final processed arrival in the migration table.

Usable model:

- n = **525**
- migration events = **382**

### Durif stage

Per one-stage increment:

- HR = **1.29**
- 95% CI = **1.14–1.48**
- p = **1.1e-4**

### Body length

Per 100 mm:

- HR = **1.04**
- 95% CI = **0.91–1.19**
- p = **0.573**

### Release timing

Per 100 d:

- HR = **1.19**
- 95% CI = **0.85–1.67**
- p = **0.311**

## Ecological interpretation

Three increasingly direct results now agree:

1. advanced Durif state predicts the published successful-migrant endpoint;
2. advanced Durif state predicts whether a migration state is identified in the processed track;
3. advanced Durif state predicts **earlier migration onset** under censoring.

Thus the current evidence supports:

> **internal migratory readiness is associated not only with eventual migration success but with the expression and timing of movement itself.**

This substantially strengthens the internal-state half of the mobility-gating programme.

## What remains unresolved

This does not establish the full hypothesis that landscape resistance changes the effect of internal state.

Project heterogeneity remains strong, and resistance is substantially project-confounded in the Europe-wide panel.

The next decisive ecological question remains:

> **when does advanced migratory readiness successfully translate into movement, and when does landscape resistance suppress that expression?**

## Important denominator boundary

The processed migration files are not a complete census of all exact-stage metadata records.

Accordingly:

- use “conditional on the processed/observable telemetry cohort”;
- do not report FIII/FIV/FV initiation proportions as population-wide probabilities;
- do not classify metadata-only missing tags as non-migrants without reconstructing the upstream inclusion process.

## Evidence class

Developmental independent evidence.

The source data and migration classifier predate this hypothesis, but the relevant outcomes were inspected during hypothesis development.
