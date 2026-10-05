# Durif stage predicts behavioral migration initiation

## Endpoint definition

The source migration algorithm defines `migration=TRUE` from the **first row classified as downstream migration** through the individual's furthest downstream point.

Source code:
- `src/identify_migration_functions.R`
- distance threshold: 4 km;
- migration-speed threshold: 0.01 m/s;
- smoothing threshold prevents a stationary phase from being labelled as migration start.

Therefore the first `migration=TRUE` row is treated here as:

> **algorithmically detected behavioral migration initiation**

It is not interpreted as the physiological onset of silvering.

## Data coverage

Six projects contain public migration tables that can be linked to exact FIII/FIV/FV metadata:

- 2011 Warnow;
- 2012 Leopoldkanaal;
- 2013 Albertkanaal;
- 2015 phd_verhelst_eel;
- 2019 Grotenete;
- ESGL.

Stage-resolved migration-table coverage:

- **575 individuals** total;
- FIII: 261;
- FIV: 68;
- FV: 246.

The separate life4fish metadata contain stage information but no corresponding public migration CSV in the source migration directory, so they are not silently counted as non-initiators.

## Descriptive result

Behavioral migration initiation:

| Durif stage | initiated / tracked | rate |
|---|---:|---:|
| FIII | 161 / 261 | **61.7%** |
| FIV | 54 / 68 | **79.4%** |
| FV | 216 / 246 | **87.8%** |

Among individuals that initiated migration, median time from release to algorithmic onset was:

- FIII: **4.86 d**
- FIV: **0.22 d**
- FV: **0.69 d**

These raw medians are strongly project- and release-design dependent and are descriptive only.

## Project-fixed initiation model

Ordinal coding:

~~~text
FIII = 0
FIV  = 1
FV   = 2
~~~

Project-fixed logistic model:

- OR per one-stage increment: **1.93**
- 95% CI: **1.49–2.50**
- p = **6.9e-7**

Thus more advanced capture-time Durif stage predicts a higher probability of subsequently entering the source study's behavioral migration state.

## Robustness to body size and release timing

A stricter model used:

- project × release-year fixed effects;
- within-stratum body length;
- within-stratum release timing;
- ordinal Durif stage.

This retained 525 individuals in 11 informative project-year strata.

### Durif stage

- OR per stage: **1.99**
- 95% CI: **1.49–2.66**
- p = **3.2e-6**

### Body length

Per 100 mm:

- OR **1.37**
- 95% CI **1.00–1.89**
- p = **0.053**

### Release timing

Per 100 days later within project-year:

- OR **1.30**
- 95% CI **0.68–2.50**
- p = **0.426**

The initiation-stage effect therefore is not explained away by body size or broad release timing.

## Timing among initiators

Among 382 initiators with non-negative release-to-onset times, a project-year-fixed model of:

~~~text
log(1 + days to migration onset)
~~~

with body length and release timing retained an ordinal stage effect:

- exponentiated coefficient per stage = **0.72**
- p = **0.0065**

Conditional on eventual initiation, a one-stage advance was associated with approximately **28% lower log-scale release-to-onset time**.

This is supportive but secondary because monitoring geometry and release protocol affect observed onset time.

## Ecological interpretation

The Europe-wide panel now supports two distinct internal-state observations:

1. more advanced Durif stage predicts the eventual successful-migrant endpoint;
2. more advanced Durif stage predicts entry into the behavioral migration phase itself.

The second result matters because it occurs **before final migration success** and is therefore closer to movement expression than the escapement endpoint.

The defensible statement is:

> **capture-time migratory readiness predicts whether and how quickly later directed downstream movement is expressed.**

## What remains unresolved

The result does not show why the strength of the stage effect differs among landscapes.

Project-specific initiation patterns remain heterogeneous; for example, advanced stages clearly outperform FIII in several projects, while Albertkanaal and ESGL do not show the same simple ordering.

Therefore the next biological question remains:

> **which landscape/hydrological contexts allow advanced internal readiness to be translated into movement, and which constrain it?**

That is the target of the independent consecutive-barrier confirmation programme.

## Evidence boundary

This remains developmental independent evidence:

- source outcomes were inspected during hypothesis refinement;
- migration status is an algorithmic telemetry classification, not a physiological state;
- no universal stage × landscape interaction is claimed from these six projects.
