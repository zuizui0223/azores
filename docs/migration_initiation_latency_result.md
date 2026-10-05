# Developmental result: Durif stage predicts migratory trajectory classification and earlier direct downstream detection

## Correction to the first latency interpretation

The public migration tables contain two related but distinct indicators:

- `downstream_migration`: row-level evidence that a sufficiently fast downstream displacement is supported from that row;
- `migration`: the broader migration segment running from the first `downstream_migration=TRUE` row to the farthest downstream point.

Because the row-level classifier can legitimately classify the **release row itself** as the first migration row when subsequent movement satisfies the distance/speed rule, "days from release to first `migration=TRUE` row" is **not** a clean natural migration-onset time.

Therefore the earlier provisional latency interpretation is withdrawn.

## A. Probability that the later trajectory is classified as migratory

Across the six projects:

- exact-stage metadata individuals: **603**
- represented in migration tables: **575**
- missing from migration tables: **28**

Raw proportions among represented individuals:

| Stage | n | Any migratory trajectory | Proportion |
|---|---:|---:|---:|
| FIII | 261 | 161 | 0.617 |
| FIV | 68 | 54 | 0.794 |
| FV | 246 | 216 | 0.878 |

Adjusted model:

~~~text
trajectory classified migratory
  ~ project × release-year fixed effects
  + within-stratum body length
  + within-stratum release timing
  + ordinal Durif stage
~~~

Eleven informative project-year strata contributed **525** individuals.

Per one-stage FIII -> FIV -> FV increment:

- OR = **1.99**
- 95% CI = **1.49–2.66**
- p = **3.2e-6**

Body length per 100 mm:

- OR = **1.37**
- 95% CI = **1.00–1.89**
- p = **0.053**

Release timing per 100 days:

- OR = **1.30**
- 95% CI = **0.68–2.50**
- p = **0.426**

Thus independently measured silvering state predicts whether the later observed trajectory satisfies the published migration criterion.

## B. Adversarial missingness sensitivity

Missing by stage:

- FIII: 13
- FIV: 2
- FV: 13

To bias maximally against a positive stage effect:

- every missing FIII individual was forced to migratory;
- every missing FIV/FV individual was forced to non-migratory.

Under the same project-year/body-size/release-timing structure:

- OR per stage = **1.74**
- 95% CI = **1.32–2.28**

The positive stage gradient survives this deliberately hostile assignment.

## C. First directly detected downstream movement away from release

To avoid the release-row issue, a second endpoint was constructed.

For each individual, define:

> the first row with `downstream_migration=TRUE` at a non-release receiver with non-zero distance from the release source.

This is a directly detected downstream movement step.

It is still constrained by receiver spacing and detection geometry, so it is **not** interpreted as the exact physiological onset of migration.

Among individuals with such a direct downstream detection:

| Stage | n | Median days from release | Q25 | Q75 |
|---|---:|---:|---:|---:|
| FIII | 156 | **7.10** | 1.50 | 83.61 |
| FIV | 53 | **2.08** | 0.67 | 52.73 |
| FV | 209 | **5.76** | 0.75 | 49.10 |

Adjusted latency model:

~~~text
log(1 + days to first direct non-release downstream detection)
  ~ project fixed effects
  + within-project body length
  + within-project release timing
  + ordinal Durif stage
~~~

Among **418** individuals:

Per one-stage increment:

- multiplicative factor = **0.696**
- 95% CI = **0.562–0.863**
- p = **0.00093**

Body length per 100 mm:

- factor = **1.11**
- 95% CI = **0.87–1.42**
- p = **0.402**

Release timing per 100 days later:

- factor = **0.900**
- 95% CI = **0.840–0.963**
- p = **0.0024**

Thus more advanced Durif stage is associated with earlier **directly detected downstream movement away from the release station**.

## Ecological interpretation

The Europe-wide evidence now supports three sequential internal-state associations:

1. movement classification — advanced stage is more likely to produce a trajectory meeting the published migration criterion;
2. direct movement timing — advanced stage reaches a downstream migration detection sooner after release;
3. successful progression — advanced stage has higher odds of the published successful-migrant endpoint.

The strongest defensible statement is:

> **Internal migratory readiness is expressed across multiple components of realised movement, not only in final migration success.**

## Why this still points to environmental gating

The stage effect is not homogeneous across projects.

Some systems show a very large advanced-stage advantage; others show little or reversed contrast.

Likewise, even highly advanced individuals can wait much longer in some projects than in others.

This motivates—but does not itself prove—the next mechanism:

> **internal state determines readiness, while landscape/hydrological opportunity determines how readily that state is translated into realised movement.**

## Claim boundary

- Capture-time Durif stage is independent of the later movement outcome.
- The published migration classifier is an outcome, not the predictor.
- First `migration=TRUE` row is not called natural migration onset.
- First non-release `downstream_migration=TRUE` detection is a detection-based timing endpoint, not exact departure time.
- Project differences cannot be causally attributed to WRS, hydrology or barrier type without an independent within-system test.
- The general state × opportunity law still requires external confirmation.
