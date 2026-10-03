# Direct phase-interaction result: Durif control attenuates after initiation

## Question

Separate models showed:

- a strong Durif-stage effect on **migration initiation**;
- a weak Durif-stage effect on **completion after initiation**.

Comparing two p-values is not enough to establish a biological handoff.

The direct question is:

> **Is the Durif-stage effect itself significantly weaker after migration has begun?**

## Stacked two-phase model

Each tracked individual contributes:

1. an **initiation** row;
2. if it initiated migration, a **completion** row.

The model gives each phase:

- its own project × release-year baseline;
- its own body-length coefficient;
- its own release-timing coefficient;
- its own Durif-stage coefficient.

Because initiators appear in both phases, uncertainty uses a sandwich covariance clustered by individual tag.

Data:

- **575 individuals**
- **910 stacked phase observations**
- **22 informative phase × project-year strata**

## Stage effect on initiation

Per FIII -> FIV -> FV increment:

- OR = **2.08**
- cluster-robust 95% CI = **1.55–2.77**
- p = **7.3e-7**

## Stage effect on completion after initiation

Per stage increment:

- OR = **1.15**
- cluster-robust 95% CI = **0.81–1.62**
- p = **0.431**

## Direct attenuation test

The difference in stage coefficients is:

```text
beta_initiation - beta_completion = 0.593
```

Equivalent ratio of stage odds ratios:

```text
OR_initiation / OR_completion = 1.81
```

Cluster-robust 95% CI:

**1.15–2.84**

Direct interaction test:

**p = 0.0099**

## Ecological meaning

This is stronger than saying one model was significant and the other was not.

It directly supports:

> **internal migratory readiness exerts substantially stronger control over whether migration is activated than over the fate of migration after activation.**

Together with the independent Dutch consecutive-barrier evidence, the current biological model is:

```text
internal silvering/readiness
          |
          v
migration activation
          |
          v
external opportunity + route history
increasingly constrain progression
```

The handoff is not absolute. Internal traits may still matter after initiation, and external conditions can also affect activation.

The supported statement is about a **shift in relative control**, not a switch from 100% internal to 100% external control.

## Why this matters

A single final-success model collapses two different filters:

1. whether the animal enters the migratory movement state;
2. whether an already migrating animal can progress through its route.

The phase interaction shows that those filters have measurably different relationships with internal readiness.

## Remaining causal gap

The direct phase interaction identifies **attenuation of internal-state control**.

It does not by itself identify the external driver replacing it.

The Dutch system supplies plausible independent candidates:

- discharge opportunity;
- wind;
- moon illumination;
- prior barrier experience.

A future raw-data confirmation should estimate those progression controls without attempting to rescue a Durif effect.

## Evidence boundary

The source outcomes were already inspected during programme development.

This remains developmental independent evidence rather than preregistered confirmation.
