# Two-stage mobility result: internal state opens movement, but does not generally predict completion

## Question

The Europe-wide eel panel now supports a strong capture-time Durif-stage effect on **migration initiation**.

The next question is whether the same stage effect remains after migration has already begun.

If it does, internal state may control both motivation and subsequent passage.

If it does not, a cleaner two-stage interpretation becomes possible:

> **internal state opens movement; downstream ecological context filters completion.**

## Cohort

Primary female stages FIII/FIV/FV represented in the six readable migration projects:

- total tracked: **575**
- classified migration initiators after published 2015 expert exclusions: **422**

Among initiators:

| stage | initiators | successful endpoint | completion fraction |
|---|---:|---:|---:|
| FIII | 154 | 106 | 0.688 |
| FIV | 53 | 45 | 0.849 |
| FV | 215 | 116 | 0.540 |

The raw fractions are strongly project-confounded and should not be interpreted directly.

## Adjusted completion model

Among initiators only:

~~~text
successful_migrant_endpoint
  ~ project × release_year fixed effects
  + within-stratum body length
  + within-stratum release timing
  + ordinal Durif stage
~~~

Eleven informative project-year strata contributed **385** initiators.

Durif stage per FIII -> FIV -> FV increment:

- OR = **1.15**
- 95% CI = **0.83–1.59**
- p = **0.412**

## Contrast with initiation

The corresponding adjusted effect on **whether migration began at all** was:

- OR = **2.08** per stage increment
- 95% CI = **1.56–2.76**
- p = **4.2e-7**

Thus the same internal-state predictor behaves very differently across two sequential movement stages.

## Independent progression metric — migration speed

The same internal-state gradient was also tested against the source meta-analysis's
continuous migration-speed definition.

Among **418** initiated eels in informative project-year strata:

- FIII median speed: **0.0229 m/s**
- FIV median speed: **0.0232 m/s**
- FV median speed: **0.0245 m/s**

Adjusted log-speed model:

- Durif multiplicative speed ratio per stage increment: **0.983**
- 95% CI: **0.852–1.134**
- p = **0.815**

Thus the attenuation of the stage effect is not specific to the binary completion
endpoint. Advanced stage strongly predicts **activation**, but not a general
increase in post-activation migration speed.

See [post-initiation speed result](post_initiation_speed_result.md).

## Direct phase-interaction test

A stacked continuation-ratio model directly compares the stage coefficient
between initiation and completion while clustering uncertainty by individual.

- initiation OR per stage: **2.08**
- completion OR per stage: **1.15**
- ratio of ORs: **1.81**
- 95% CI: **1.15–2.84**
- phase interaction p = **0.0099**

This directly supports attenuation of internal-state control after activation.

See [phase interaction result](phase_stage_interaction_result.md).

## Ecological interpretation

The strongest current interpretation is:

### Stage 1 — mobility release

Advanced silvering state strongly increases the probability that directed downstream migration is expressed.

### Stage 2 — passage/completion

Once migration has begun, advanced Durif stage no longer provides a general project-independent advantage for reaching the published successful endpoint.

This suggests that later movement is governed more strongly by **route-specific ecological opportunity, barriers, hydrology, delay, or other system context** than by the same internal-readiness gradient that triggered migration.

That second sentence is a mechanism hypothesis, not yet identified causally.

## Why this is more informative than one success model

A single endpoint model mixes:

```text
motivation / readiness to start
+
landscape opportunity to proceed
+
barrier passage
+
monitoring geometry
```

The two-stage decomposition separates the first component empirically.

The result is compatible with:

> **internal state controls movement initiation, while landscape context controls the fate of initiated movement.**

The Dutch consecutive-barrier system is now a direct confirmation target for the second half.

## What would falsify that interpretation

The two-stage interpretation weakens if an independent within-landscape study shows that:

- Durif stage strongly predicts passage/completion even after migration has begun and after barrier opportunity is controlled; or
- route/barrier opportunity adds little once internal state is represented.

## Evidence boundary

This is developmental independent evidence:

- the published endpoint was inspected during programme development;
- the migration classifier and 2015 expert exclusions are inherited unchanged;
- project/system conditions remain heterogeneous.

Do not label the conditional completion null as proof that landscape resistance is causal.
