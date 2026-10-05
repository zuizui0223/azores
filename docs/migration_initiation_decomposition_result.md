# Developmental result: internal readiness gates migration onset more strongly than completion

## Scope

The public Europe-wide eel repository contains per-detection migration classifications for six projects that also contain exact female Durif stages FIII/FIV/FV.

The onset analysis includes **575 stage-coded tags with public migration rows**.

`life4fish` is not counted as a non-initiating system: its exact Durif stages exist in metadata, but the public `data/interim/migration/` directory contains no matching per-project migration CSV.

## Raw initiation pattern

| Durif stage | n | initiated | initiation rate | median onset delay |
|---|---:|---:|---:|---:|
| FIII | 261 | 161 | **61.7%** | **4.86 d** |
| FIV | 68 | 54 | **79.4%** | **0.22 d** |
| FV | 246 | 216 | **87.8%** | **0.69 d** |

The raw timing distribution is highly heterogeneous among projects, so the table is descriptive only.

## Adjusted initiation model

Project × release-year fixed effects plus within-stratum body length and release timing:

### Durif stage

Per FIII -> FIV -> FV increment:

- OR **1.99**
- 95% CI **1.49–2.66**
- p = **3.2e-6**

### Body length

Per 100 mm:

- OR **1.37**
- 95% CI **1.00–1.89**
- p = **0.053**

### Release timing

Per 100 days:

- OR **1.30**
- 95% CI **0.68–2.50**
- p = **0.43**

Thus the stage signal in migration initiation is not explained by broad release timing or body size.

## Onset timing among initiators

Among individuals that initiated migration, a project × release-year fixed-effect model of `log(1 + onset delay days)` gave:

Durif one-stage increment:

- multiplicative effect **0.75**
- 95% CI **0.60–0.93**
- p = **0.0088**

Interpretation:

> more advanced capture-time Durif stage is associated not only with a higher probability of migration initiation, but also with earlier initiation among those that migrate.

This timing model is conditional on initiation and is not a survival model with censoring. It should therefore be treated as a robustness/description of initiators rather than the primary onset estimator.

## What happens after migration starts?

Among initiators, the published successful-migrant endpoint was analysed with the same project × release-year, body-size and release-timing adjustment.

Durif one-stage increment:

- OR **1.29**
- 95% CI **0.94–1.77**
- p = **0.12**

The stage effect is therefore much less resolved after migration has already begun.

## Biological interpretation

The combined pattern is consistent with a two-stage movement process:

### Stage 1 — departure gate

Internal migratory readiness affects:

- whether downstream migration starts;
- how quickly it starts.

### Stage 2 — route completion

Once migration has started, the final successful endpoint is less clearly related to initial Durif stage and may depend more strongly on:

- barriers;
- hydrological passage opportunity;
- route structure;
- project-specific detection geometry;
- other unmeasured context.

This is more specific than the earlier statement that “stage predicts movement”.

A candidate ecological formulation is:

> **internal state gates the release of mobility; the landscape filters whether released mobility becomes successful migration.**

## What is not yet proven

Do not yet write:

> landscape resistance causes the stage effect to disappear after departure.

The current Europe-wide dataset has strong project–WRS confounding, and the attenuation of the stage coefficient is not itself a formal mediation test.

The Dutch consecutive-barrier dataset remains the key independent confirmation system for the second half of the hypothesis.

## Why this matters for the Azores seed

Flores yellow eels occupy the opposite end of this behavioural continuum:

- strong growth-stage residence;
- no observed receiver-to-receiver movement.

The Europe-wide result now supplies a direct life-history contrast:

> when migratory readiness advances, the probability and timing of movement change sharply even within the same species complex.

The Azores project should therefore focus on **mobility release across life-history state**, not on rediscovering site fidelity.
