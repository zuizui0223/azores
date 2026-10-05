# Corrected result: Durif stage gates migration initiation, not completion

## Why the earlier result was corrected

An earlier developmental analysis treated every FIII/FIV/FV individual in the metadata table as the denominator for the published successful-migrant endpoint.

That was too broad.

The source workflow first constructs per-project migration tables and then filters to:

```text
migration == TRUE
```

before identifying which migratory eels ultimately reach the project-specific sea/escapement endpoint.

Therefore two biological transitions must be separated:

1. **migration initiation** — does a tracked eel ever enter the published migratory state?
2. **migration completion** — among initiators, does it reach the successful escapement endpoint?

The denominator has now been rebuilt from individuals actually present in the six relevant migration CSVs, with the source paper's expert-judgement exclusions for the 2015 project applied.

## Correct cohort

Primary stages: FIII, FIV, FV.

Six projects with exact stage data and migration tables:

- 2011 Warnow;
- 2012 Leopold Canal;
- 2013 Albert Canal;
- 2015 Scheldt project;
- 2019 Grote Nete;
- ESGL / Grand Lieu Lake.

Total exact-stage individuals actually observed in those migration tables:

**575**

Coverage relative to stage-coded metadata is generally high (~89–100% depending on project/stage).

## Stage 1 — migration initiation

Unadjusted:

| Durif stage | observed individuals | initiated | initiation rate |
|---|---:|---:|---:|
| FIII | 261 | 154 | **59.0%** |
| FIV | 68 | 53 | **77.9%** |
| FV | 246 | 215 | **87.4%** |

Project × release-year fixed-effect model, additionally controlling within stratum for body length and release timing:

- analyzable n = **525**
- informative project-year strata = **11**
- Durif-stage OR per FIII -> FIV -> FV increment = **2.08**
- 95% CI = **1.56–2.76**
- p = **4.2e-7**

Body length and release timing did not explain away the stage effect.

### Ecological interpretation

> **Internal migratory readiness strongly gates whether movement is initiated.**

This is a cleaner biological claim than the earlier successful-migrant analysis.

## Stage 2 — completion among migration initiators

Among the 422 stage-coded initiators:

| Durif stage | initiators | successful migrants | completion rate |
|---|---:|---:|---:|
| FIII | 154 | 106 | **68.8%** |
| FIV | 53 | 45 | **84.9%** |
| FV | 215 | 116 | **54.0%** |

These raw rates are strongly system-confounded and should not be read directly.

After project × release-year fixed effects plus body length and release timing:

- analyzable n = **385**
- informative project-year strata = **11**
- Durif-stage OR per increment = **1.15**
- 95% CI = **0.83–1.59**
- p = **0.412**

### Ecological interpretation

> **Once an eel has initiated migration, advanced Durif stage does not show a robust general advantage for completing the source-to-sea route.**

This suggests a two-stage control architecture:

~~~text
internal physiological readiness
        |
        v
migration initiation
        |
        v
landscape / barriers / hydrology / route geometry
        |
        v
migration completion
~~~

## Strong ecological result

The corrected result is therefore:

> **Internal state gates the decision or transition into migration, whereas successful completion becomes much more context dependent once movement has begun.**

This is more specific than saying "more silvered eels migrate better."

## Why this matters for the Azores programme

Flores represents the opposite end of the same behavioural architecture:

- yellow-stage animals remain deeply resident;
- advanced silvering state in the Europe-wide panel strongly increases the probability of entering migration;
- after initiation, success is no longer explained by stage alone.

The next independent question is therefore sharply defined:

> **What environmental opportunities or barriers determine whether internally released mobility can actually be expressed to completion?**

That is where the Dutch consecutive-barrier system becomes relevant.

## Evidence boundary

This is developmental independent evidence.

The outcome and stage patterns were inspected during hypothesis refinement, so it is not preregistered confirmation.

The earlier metadata-denominator successful-migrant OR documents should not be used as the current biological result.
