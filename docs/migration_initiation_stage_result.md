# Durif readiness predicts behavioural migration initiation

## Correction to the onset definition

An earlier development pass used the arrival time of the first row with `migration=TRUE` as the onset clock.

That is not the correct biological timing variable.

The upstream classifier in `src/identify_migration_functions.R` first identifies rows with `downstream_migration=TRUE`, then labels the whole interval from the first qualifying row to the maximum-distance row as `migration=TRUE`.

Therefore:

- **initiation-positive** = at least one row with `downstream_migration=TRUE`;
- **threshold-crossing time** = `time_first_dist_to_use` from the first qualifying downstream-migration row;
- the arrival time of the first `migration=TRUE` row is not treated as onset.

The source processing also identifies nine 2015 Scheldt tags as classifier-positive but non-migratory by expert judgement. The primary result follows that source correction; the algorithm-only result is retained as sensitivity.

## Question

> **Does capture-time morphological migratory readiness predict whether a tracked eel later expresses behavioural migration?**

This is distinct from asking whether stage predicts only final successful escapement.

## Data scope

Compatible project-level migration tables are available for six Durif-rich projects:

- Warnow;
- Leopold Canal;
- Albert Canal;
- Scheldt / phd_verhelst_eel;
- Grote Nete;
- ESGL.

Life4fish has stage metadata but no compatible public project-level migration table in the source repository and is therefore outside the onset analysis.

Joined FIII/FIV/FV individuals: **575**.

## Descriptive initiation pattern

After applying the source expert correction:

| stage | n | initiated | proportion | median days to distance-threshold crossing among initiators |
|---|---:|---:|---:|---:|
| FIII | 261 | 154 | **0.590** | **7.21** |
| FIV | 68 | 53 | **0.779** | **2.14** |
| FV | 246 | 215 | **0.874** | **2.15** |

Algorithm-only sensitivity before the nine source expert corrections was:

- FIII: 161/261 = 0.617;
- FIV: 54/68 = 0.794;
- FV: 216/246 = 0.878.

Thus the source correction does not create the stage gradient.

## Adjusted initiation model

Primary developmental model:

~~~text
migration_initiated
  ~ project × release-year fixed effects
  + within-stratum body length
  + within-stratum release timing
  + ordinal Durif stage
~~~

Ordinal coding:

~~~text
FIII = 0
FIV  = 1
FV   = 2
~~~

Model cohort:
- **525 individuals**;
- **11 informative project-year strata**.

### Durif effect

Per one-stage increment:

- OR = **2.08**
- 95% CI = **1.56–2.76**
- p = **4.2e-7**

### Body length

Per 100 mm:

- OR = **1.29**
- 95% CI = **0.95–1.76**
- p = **0.107**

### Release timing

Per 100 days later within project-year:

- OR = **1.30**
- 95% CI = **0.68–2.50**
- p = **0.426**

The initiation-stage effect therefore does not reduce to body size or broad release timing.

## Leave-one-project-out stability

Durif OR after excluding each project:

- remove Warnow: **2.34** [1.69, 3.24]
- remove Leopold Canal: **2.01** [1.47, 2.75]
- remove Albert Canal: **2.35** [1.73, 3.19]
- remove Scheldt: **1.67** [1.19, 2.32]
- remove Grote Nete: **1.92** [1.44, 2.56]
- remove ESGL: **2.21** [1.62, 3.01]

Every leave-one-project-out interval remains above 1.

The strongest current conclusion is therefore robust to deleting any single project.

## Threshold-crossing latency among initiators

Among expert-corrected initiators, a secondary project-year fixed-effects model used:

~~~text
log(1 + days to first threshold crossing)
  ~ body length
  + release timing
  + ordinal Durif stage
~~~

Full model:
- n = **418**
- multiplicative change per stage increment = **0.715**
- 95% CI = **0.585–0.872**
- p = **0.0010**

On average, advanced-stage eels cross the migration distance threshold sooner.

However this timing effect is **not fully project-robust**:

- removing Scheldt gives multiplier **0.98** [0.80, 1.20], p = 0.84;
- the other project deletions remain mostly below 1.

Therefore latency is secondary, system-dependent evidence rather than the main general claim.

## Ecological result

The strongest developmental statement is:

> **Morphological migratory readiness robustly predicts whether later behavioural migration is expressed.**

This moves the evidence upstream from final successful escapement to the initiation of the movement process itself.

It supports a real biological distinction between:

- **internal readiness**;
- **realised movement expression**.

## What remains unresolved

This still does not establish the stronger mobility-gating law:

> **landscape resistance changes how internal readiness is translated into movement.**

The initiation probability is robust; the timing varies substantially among systems. That heterogeneity is exactly what the independent within-landscape barrier test is intended to explain.

## Evidence boundary

- The migration outcome was inspected during hypothesis development.
- This is developmental independent evidence, not preregistered confirmation.
- The movement thresholds and nine expert corrections are inherited from the source workflow and are not retuned.
- Life4fish is excluded because compatible migration products are unavailable, not because of its outcome.
