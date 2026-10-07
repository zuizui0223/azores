# Activation-filter diagnostic — 2026-10-07

## Identification problem

The primary progression analysis is conditional on migration activation.

That conditioning is biologically non-trivial because activation itself is strongly stage dependent:

| capture stage | initiated / tracked | initiation rate |
|---|---:|---:|
| FIII | 154 / 261 | 59.0% |
| FIV | 53 / 68 | 77.9% |
| FV | 215 / 246 | 87.4% |

Therefore the FIII eels that enter the post-activation speed analysis are a more selected subset of all FIII eels than the FV entrants are of all FV eels.

The post-activation contrast must consequently be interpreted as:

> **Does capture-time Durif stage rank migration speed among eels that actually entered the classified migratory state?**

It is not, by itself, a causal estimate of what Durif stage would do to migration speed in all tagged eels.

## Diagnostic A — measured capture-phenotype selection

Within each capture stage, initiators were compared with non-initiators using body length and a descriptive weight-for-length residual.

### FIII

- initiator n = **154**
- non-initiator n = **107**
- mean length: **730.6 vs 691.1 mm**
- standardized length difference: **+0.514**
- weight-for-length residual standardized difference: **+0.302**

Thus FIII migration entrants were measurably larger and somewhat heavier for length than FIII non-entrants.

### FIV

- n = **53 vs 15**
- length standardized difference: **+0.028**
- weight-for-length residual difference: **−0.078**

Little measured selection was visible on these two traits.

### FV

- n = **215 vs 31**
- length standardized difference: **+0.266**
- weight-for-length residual difference: **+0.565**

Selection is therefore not restricted to FIII; the activation gate is phenotypically non-random on available capture traits.

## Diagnostic B — inverse-probability reweighting

The canonical initiation model was used to estimate:

~~~text
P(initiation)
  ~ project × release-year
  + within-stratum body length
  + within-stratum release timing
  + ordinal Durif stage
~~~

The model contained:
- n = **525**
- **11** informative project-year strata.

Speed-bearing initiators with an estimable canonical activation propensity:
- n = **373**
- **11** speed strata.

For this same sample, the stage-speed model was fitted twice.

### Unweighted

- ratio per Durif stage = **1.042**
- 95% CI = **0.902–1.205**
- p = **0.575**

### Weighted by 1 / fitted initiation probability

- ratio per stage = **1.062**
- 95% CI = **0.916–1.230**
- p = **0.427**

Weight distribution:
- median = **1.21**
- Q25–Q75 = **1.10–1.50**
- maximum = **6.54**
- effective sample size = **302**

The measured-selection correction therefore moves the point estimate only from 1.042 to 1.062 and does not recover a resolved positive stage-speed gradient.

## Interpretation

Two things are simultaneously true.

### 1. Activation is a biological selection filter

This is not merely a statistical abstraction. In FIII especially, animals that pass Gate 1 differ in measured capture phenotype from those that do not.

So the initiated FIII and initiated FV groups are not random representatives of their original capture-stage populations.

### 2. The measured selection does not explain the weak stage-speed relationship

When the canonical measured predictors of entry are reweighted back toward the activation-eligible population, the downstream stage-speed coefficient remains small and imprecise.

Therefore:

> **selection on measured stage, body length, release timing and their project-year context does not rescue a general positive Durif-speed gradient.**

## What remains unresolved

This diagnostic cannot eliminate **latent activation selection**.

Speed is undefined for eels that never enter the migratory state. The analysis therefore cannot observe the counterfactual speed that a non-initiator would have had if forced into migration.

Unmeasured physiology, endocrine state, energy stores, behavioural motivation or other readiness dimensions could still select FIII entrants more strongly than FV entrants.

The correct inferential boundary is:

> **among observed initiators, capture-time Durif stage does not provide a general speed ranking; this remains a selected post-activation population and is not a causal estimate of stage attenuation.**

## Biological consequence

This sharpens the emerging interpretation.

The evidence is compatible with silvering stage acting more like an **entry-state indicator** than a simple **motor-performance score**:

- it strongly predicts whether migration becomes expressed;
- it predicts when that expression occurs;
- among animals that cross the activation gate, it does not strongly rank generic movement speed.

But the present data cannot distinguish completely between:

1. genuine phase-specific trait-performance coupling; and
2. biological homogenization created by a selective activation threshold on latent readiness.

The first two falsification audits now constrain simpler alternatives:

- strong route-specific sign cancellation: unsupported;
- simple capture-stage staleness/catch-up: unsupported;
- measured activation selection: present, but insufficient to restore the stage-speed gradient.

Latent threshold selection remains the main identification boundary.

## Status

**MEASURED_SELECTION_PRESENT_BUT_DOES_NOT_RESTORE_STAGE_SPEED_GRADIENT**

Machine-readable result:
- `results/activation_filter_diagnostic_v1.json`

Executable analysis:
- `analysis/15_activation_filter_diagnostic.py`

Evidence class:
- post-hoc developmental selection diagnostic.
