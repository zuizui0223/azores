# Two-gate movement hypothesis

## Main result

The Europe-wide eel panel now separates two biologically distinct stages of movement:

1. **initiation** — does the eel enter the published migratory movement state?
2. **completion / successful endpoint** — among initiators, does the eel reach the published successful-migrant endpoint?

This separation is more informative than a single "movement success" response.

## Gate 1 — internal state controls initiation

Among FIII/FIV/FV individuals actually represented in the processed migration tables:

- FIII initiation: **161 / 261 = 61.7%**
- FIV initiation: **54 / 68 = 79.4%**
- FV initiation: **216 / 246 = 87.8%**

Coverage of exact-stage metadata in the processed migration tables is approximately 95% overall.

A project × release-year fixed-effect logistic model, controlling for within-stratum body length and release timing, gives:

> **OR = 1.99 per one Durif-stage increment**
>
> 95% CI **1.49–2.66**
>
> p ≈ **3.2e-6**

Thus independently measured migratory readiness strongly predicts whether later movement is initiated.

## Gate 2 — stage is much weaker after initiation

Among individuals that entered the published migratory movement state, the published successful-migrant endpoint rates were:

- FIII: **106 / 161 = 65.8%**
- FIV: **45 / 54 = 83.3%**
- FV: **116 / 216 = 53.7%**

After project × release-year fixed effects, body length and release timing:

> **OR = 1.29 per Durif-stage increment**
>
> 95% CI **0.94–1.77**
>
> p ≈ **0.12**

The strong stage gradient therefore does **not** persist clearly into the second gate.

## Strong system dependence after initiation

Completion rates among initiators vary strongly among projects:

| project | dominant WRS impact | successful / initiated | rate |
|---|---:|---:|---:|
| 2015 phd_verhelst_eel | 0 | 76 / 95 | 0.80 |
| 2019 Grotenete | 0 | 33 / 33 | 1.00 |
| 2011 Warnow | 1 | 87 / 107 | 0.81 |
| ESGL | 3 | 10 / 12 | 0.83 |
| 2012 Leopoldkanaal | 5 | 36 / 52 | 0.69 |
| 2013 Albertkanaal | mostly 14 | 25 / 132 | 0.19 |

At the six-project level, representative WRS impact and completion rate have:

- Spearman rho ≈ **-0.70**
- exact two-sided permutation p ≈ **0.14**

This is descriptive only. WRS is substantially confounded with project/system identity.

## Ecological interpretation

The strongest current hypothesis is:

> **Internal state opens the movement gate; landscape and system context determine how successfully that movement can be completed.**

This is different from saying that advanced-stage eels simply "move more."

Conceptually:

```text
internal readiness
      |
      v
migration initiation
      |
      v
landscape / barrier / hydrological filter
      |
      v
successful progression / escapement
```

## Why this matters

A single movement endpoint mixes two different ecological processes:

- motivation / readiness to leave;
- external opportunity / resistance after leaving.

The current results suggest these may be governed by different controls.

That distinction can explain why advanced Durif stage has a strong average association with migration, yet project-specific successful-migrant effects are highly heterogeneous.

## Testable predictions

### G1 — initiation prediction

Within the same landscape and season, advanced independently measured migratory state should increase the probability or hazard of migration initiation.

### G2 — context filtering

Conditional on initiation, variation in passage/escapement should be more strongly structured by barrier and hydrological opportunity than by Durif stage alone.

### G3 — interaction at difficult barriers

Internal readiness may matter most when passage opportunities are intermittent rather than impossible.

This predicts a state × opportunity interaction, not necessarily a monotonic stage effect on final success.

## Confirmation target

The Dutch pump -> tidal-sluice system is useful because the same individuals encounter two different passage regimes.

The key test is not simply whether FV eels succeed more often.

It is whether:

> **Durif state changes how efficiently individuals exploit available passage windows at each barrier.**

## Claim boundary

- processed migration-table absence is not treated as failure to initiate;
- initiation analyses use only tags represented in the migration tables;
- project/system effects are not relabelled as WRS causation;
- the six-project WRS correlation is descriptive;
- the published endpoint was inspected during hypothesis development, so these are developmental independent results.
