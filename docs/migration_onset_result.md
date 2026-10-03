# Developmental result: Durif stage predicts rapid migration onset

## Question

The previous Europe-wide analysis used the published successful-migrant endpoint.

A more direct movement-ecology question is:

> **Does capture-time migratory readiness predict whether directed migration is expressed soon after release?**

## Data reconstruction

Six public per-project migration files were read directly from the source Git blobs:

- 2011 Warnow;
- 2012 Leopoldkanaal;
- 2013 Albertkanaal;
- 2015 phd_verhelst_eel;
- 2019 Grotenete;
- ESGL.

The 2015 expert exclusions declared in the source `process_migration_data.R` were preserved.

Exact-stage telemetry coverage among FIII/FIV/FV individuals was high in all six projects (about 91.7–100% by project). The Life4Fish exact-stage cohort is not included because the corresponding migration file is not present in the public migration directory used here.

## Descriptive migration initiation

Among exact-stage individuals represented in the six migration files:

- FIII: **154/261 = 59.0%** ever met the published migration criterion;
- FIV: **53/68 = 77.9%**;
- FV: **215/246 = 87.4%**.

Among individuals that initiated migration, the median delay from release to first classified migration row was:

- FIII: **4.95 days**;
- FIV: **0.27 days**;
- FV: **0.69 days**.

These onset medians are descriptive only because they condition on initiation.

## 30-day onset endpoint

To reduce that selection problem, a second developmental endpoint was defined:

> migration begins within 30 days of release.

Eligibility requires either:

- observed migration onset within 30 days; or
- at least 30 days of observable telemetry after release without such onset.

This produced **463** individuals across **12 informative project × release-year strata**.

Raw eligible proportions:

- FIII: **105/189 = 55.6%**;
- FIV: **38/54 = 70.4%**;
- FV: **156/220 = 70.9%**.

## Adjusted model

The logistic model included:

- project × release-year fixed effects;
- body length centered within stratum, per 100 mm;
- release timing centered within stratum, per 100 days;
- ordinal Durif stage FIII=0, FIV=1, FV=2.

### Durif stage

Per one-stage increment:

- OR = **1.54**
- 95% CI = **1.17–2.03**
- p = **0.0021**

### Body length

Per 100 mm:

- OR = **0.83**
- 95% CI = **0.61–1.13**
- p = **0.241**

### Release timing

Per 100 days later within project-year:

- OR = **2.25**
- 95% CI = **0.97–5.21**
- p = **0.057**

## Biological interpretation

The internal-state result now appears at two distinct response levels:

1. **successful migration endpoint** — advanced Durif stage predicts later success;
2. **rapid movement onset** — advanced Durif stage predicts expression of directed migration within 30 days.

This strengthens the biological interpretation:

> **silvering state is associated with release of the movement phenotype itself, not merely with downstream success after movement has already begun.**

## Important boundary

The 30-day cutoff was introduced during developmental analysis after the migration-time distributions had been inspected.

Therefore this is **not** an outcome-blind or preregistered threshold.

It should be treated as mechanistic developmental evidence. A future independent system should freeze its onset/time-to-event endpoint before outcome inspection.

## Remaining unresolved question

The current panel still cannot establish the stronger law:

> **how strongly does landscape resistance suppress or delay movement at different internal states?**

That requires the independent within-landscape barrier confirmation line.
