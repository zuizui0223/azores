# Time-to-event result: Durif stage predicts migration onset

## Why this replaces the 30-day threshold as the cleaner developmental result

The 30-day onset endpoint is intuitive but the threshold was chosen during developmental analysis.

A stratified time-to-event analysis removes that arbitrary cutoff.

## Cohort

Public per-project migration files were reconstructed for:

- 2011 Warnow;
- 2012 Leopoldkanaal;
- 2013 Albertkanaal;
- 2015 phd_verhelst_eel;
- 2019 Grotenete;
- ESGL.

The published 2015 expert exclusions were preserved.

Exact FIII/FIV/FV individuals were followed from release until:

- first row meeting the published migration criterion; or
- last available telemetry row if migration was not initiated.

Life4Fish is not included because an equivalent public per-project migration file is absent from the source migration directory used here.

Final time-to-event dataset:

- **570 individuals**
- **418 migration-onset events**
- **13 project × release-year strata**

## Model

Stratified Cox model with a separate baseline hazard for each project × release year.

Covariates:

- body length centered within stratum, per 100 mm;
- release timing centered within stratum, per 100 days;
- ordinal Durif stage: FIII=0, FIV=1, FV=2.

## Result

### Durif stage

Per one-stage increment:

- hazard ratio = **1.28**
- 95% CI = **1.12–1.45**
- p = **0.00022**

Interpretation:

> at a given project-year baseline hazard and after body-size/timing adjustment, more advanced Durif stage is associated with earlier expression of the migration phenotype.

### Body length

Per 100 mm:

- HR = **1.08**
- 95% CI = **0.95–1.23**
- p = **0.244**

### Release timing

Per 100 days:

- HR = **1.31**
- 95% CI = **0.95–1.79**
- p = **0.094**

## Leave-one-project-out stability

Durif-stage HR after excluding each project:

| omitted project | HR |
|---|---:|
| Warnow | 1.41 |
| Leopoldkanaal | 1.22 |
| Albertkanaal | 1.47 |
| 2015 phd_verhelst_eel | 1.10 |
| Grotenete | 1.26 |
| ESGL | 1.27 |

All leave-one-project-out estimates remain above 1.

However, after excluding the 2015 project, the 95% interval includes 1.

Thus the most defensible interpretation is:

> **a positive average internal-state effect with meaningful project dependence.**

## How this changes the Azores paper

The Europe-wide evidence now supports the internal-state half of mobility gating at three levels:

1. advanced Durif stage predicts the final successful-migrant endpoint;
2. advanced stage predicts migration onset within a developmental 30-day window;
3. without any arbitrary onset threshold, advanced stage predicts a higher instantaneous migration-onset hazard.

The unresolved ecological question is no longer whether internal state matters.

It is:

> **why does the strength of that internal-state effect differ among systems, and does landscape resistance/hydrological opportunity explain the heterogeneity?**

That is the target of the independent barrier-confirmation line.

## Evidence boundary

The source outcome and timing distributions were inspected during development.

This remains developmental independent evidence, not preregistered confirmation.
