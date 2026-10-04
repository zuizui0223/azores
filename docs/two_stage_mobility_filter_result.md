# Developmental result: internal state gates initiation; landscape filters completion

## The new decomposition

The Azores programme now separates two biological transitions:

1. **initiation** — does the animal enter the classified downstream-migration state?
2. **completion** — among initiators, does it reach the published successful-migrant endpoint?

This matters because “movement readiness” need not control both transitions equally.

## Stage 1 — initiation

The all-project initiation analysis already shows a strong capture-time Durif effect.

Adjusted for project × release year, within-stratum body length and release timing:

- Durif OR per FIII -> FIV -> FV increment: **2.08**
- 95% CI **1.56–2.76**
- p ≈ **4.2e-7**

All six leave-one-project-out estimates remain above 1.

Thus internal migratory readiness robustly predicts whether behavioural migration is expressed.

## Stage 2 — success conditional on initiation

Among expert-corrected initiators:

| stage | initiators | successful | conditional success |
|---|---:|---:|---:|
| FIII | 154 | 106 | **0.688** |
| FIV | 53 | 45 | **0.849** |
| FV | 215 | 116 | **0.540** |

The raw non-monotonic proportions already warn that advanced stage alone does not determine completion.

### Project-fixed model

Among 389 initiators in five informative project contexts:

- Durif OR per stage increment: **1.18**
- 95% CI **0.86–1.61**
- p = **0.31**

### Project-year + body length + release timing

Among 385 initiators in 11 informative project-year strata:

- Durif OR per stage increment: **1.15**
- 95% CI **0.83–1.59**
- p = **0.41**

Body length and release timing are also unsupported in this conditional-success model.

The strong stage effect therefore occurs mainly **before or at migration initiation**, not clearly after initiation.

## Project-level landscape diagnostic

Conditional successful-migrant rates after initiation:

| project | median WRS impact | success / initiators | conditional success |
|---|---:|---:|---:|
| 2019 Grotenete | 0 | 33/33 | **1.000** |
| 2015 phd_verhelst_eel | 0 | 76/86 | **0.884** |
| 2011 Warnow | 1 | 87/107 | **0.813** |
| ESGL | 3 | 10/12 | **0.833** |
| 2012 Leopoldkanaal | 5 | 36/52 | **0.692** |
| 2013 Albertkanaal | 14 | 25/132 | **0.189** |

Across these six project contexts:

- Spearman (ho) = **−0.928**
- exact two-sided permutation p = **0.0222** over all 720 project-label permutations.

This is striking but remains exploratory because WRS is largely a project-level property and project also contains tracking-design and ecological differences.

## Ecological interpretation

The current evidence supports a much more specific story than “advanced eels move more.”

> **Internal state gates the decision/transition into migration; after migration begins, successful realization is increasingly filtered by the external route.**

Conceptually:

```text
internal readiness
      |
      v
migration initiation
      |
      v
landscape / barriers / opportunity
      |
      v
successful progression
```

The Durif signal is strong at the first transition and weak at the second.

This is exactly the distinction needed for a biologically meaningful mobility-gating hypothesis:

> **motivation to move and ability to realize movement are different ecological processes.**

## Why this is stronger than a simple stage association

A simple FIII/FIV/FV result could be explained as “more silvered eels migrate.”

The two-stage decomposition asks where that effect acts.

The result suggests:

- silvering/internal state primarily predicts **initiation**;
- landscape context becomes more important for **completion**.

That is the mechanistic target for the Dutch consecutive-barrier replication.

## Next prediction for the Dutch system

The same individual encounters a pumping station and a tidal sluice.

The preregistered-style prediction becomes:

> **Durif state should matter most for exploiting the opportunity to initiate/proceed, while barrier-specific physical opportunity should dominate passage success/delay after movement is underway.**

This can be falsified separately at each barrier.

## Boundary

Do not call the six-project WRS correlation causal.

With only six project-level contexts, the WRS result is a strong pattern generator, not a landscape-effect estimate.

The causal/general confirmation still requires within-landscape variation in passage opportunity and resistance.


## Within-project WRS identifiability audit

The strongest project-level resistance contrast occurs in Albertkanaal, so the first attempt to reduce project confounding was to inspect WRS variation **within that one project** among migration initiators.

Result:

| WRS impact | initiators | successful | conditional success |
|---|---:|---:|---:|
| 10 | 4 | 0 | 0.000 |
| 12 | 5 | 4 | 0.800 |
| 14 | 123 | 21 | 0.171 |

This is not a usable monotonic resistance gradient:

- 123/132 initiators are concentrated at WRS=14;
- the lower-WRS cells contain only 4 and 5 individuals;
- success is non-monotonic across 10/12/14.

Therefore the Europe-wide panel **cannot identify the stage-independent landscape filter cleanly within project**.

This is an important negative gate. Do not fit a continuous WRS coefficient in Albertkanaal and present it as confirmation.

The six-project WRS–completion correlation remains hypothesis-generating only.

### Consequence

The next landscape test must come from a different design with:

- the same route or population;
- individual variation in independently measured internal state;
- repeated/continuous passage opportunity;
- enough observations at each barrier/opportunity state.

The Dutch pump + tidal-sluice system remains the preferred confirmation candidate.
