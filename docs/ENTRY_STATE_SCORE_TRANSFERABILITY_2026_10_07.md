# Activation-trained entry-state score transferability — 2026-10-07

## Question

> **Does the multivariate capture state that predicts entry into downstream migration also behave as a general motor-performance score after migration has begun?**

This analysis compresses two capture-time predictors into one score using **activation outcomes only**:

```
entry-state score
  = 0.756 × ordinal Durif stage
  + 0.379 × capture weight-for-length condition
```

The relative weights are then frozen and transferred without tuning to:
- behavioral onset;
- whole-route post-activation speed;
- the previously frozen per-eel median positive inter-station speed endpoint.

This is a post-hoc transferability diagnostic, not prospective validation.

## Activation training

n = **525** across 11 informative project-year strata.

Independent additive effects in the activation model:
- Durif stage: OR **2.130** per stage, 95% CI **1.596–2.842**, p = **2.8×10⁻7**;
- capture condition: OR **1.460** per SD, 95% CI **1.164–1.832**, p = **0.00105**.

Joint contribution of stage + condition:
- LR χ²(2) = **39.01**;
- p = **3.4×10⁻9**.

There is therefore real multivariate capture-state information at the transition into directed migration.

## Transfer of the frozen score

### Migration activation

Per 1 SD of activation-trained score:
- OR **2.230**
- 95% CI **1.704–2.918**
- p = **5.1×10⁻9**

### Behavioral onset

n = **570**, onset events = **418**.

Per 1 SD score:
- HR **1.317**
- 95% CI **1.168–1.485**
- p = **6.9×10⁻6**

Thus the same activation-trained state vector transfers cleanly from **whether migration begins** to **when it begins**.

### Whole-route speed after activation

n = **418**.

Per 1 SD score:
- speed ratio **0.946**
- 95% CI **0.832–1.076**
- p = **0.396**
- partial R² = **0.0018**

Leave-one-project-out speed ratios are all below one:
- range **0.939–0.968**.

This is a consistent weak negative point-estimate pattern, not interval-supported evidence of slower locomotion.

### Frozen positive inter-station speed

n = **411**.

Per 1 SD score:
- ratio **1.028**
- 95% CI **0.869–1.215**
- p = **0.750**
- partial R² = **0.00026**

Leave-one-project-out estimates cross both sides of one.

## Main ecological result

The strongest statement is now:

> **The multivariate capture state that determines entry into migration is not a general motor-performance score.**

The same entry-state score strongly predicts:
1. **whether** downstream migration is expressed;
2. **when** that expression begins;

but explains essentially none of the variation in:
3. generic whole-route speed after activation;
4. generic positive inter-station transit speed.

That is a sharper result than a Durif-only attenuation claim because it shows that adding continuous body-state information does not rescue the idea that a single pre-migration readiness axis ranks later locomotor performance.

## Relation to the Dutch falsification

The independent Dutch arrival-defined tests do **not** support the specific alternative that high-condition animals generally wait for longer/stronger barrier windows after arrival.

Therefore the paper should not replace the old simple handoff claim with an asset-protection story.

Instead, the Dutch failure strengthens the narrower conclusion:

> **entry state is phase-specific information. What makes an eel ready to enter migration does not automatically determine its realized progression rate once that state is expressed.**

## Novelty boundary

Durif et al. (2005) already defined FIII as pre-migrant and FIV/FV as migrating stages, so showing that Durif predicts migration entry is not by itself novel.

Likewise, state-dependent migration and speed-safety trade-offs are established ideas.

The potentially new contribution is the **within-program transferability test**:

> an activation-trained multivariate phenotype score transfers to onset but not to two independent generic progression-speed summaries.

This makes the paper about the architecture of migratory control rather than simply about silvering stage.

## Current status

**ENTRY_STATE_SCORE_NOT_GENERAL_MOTOR_SCORE**

Canonical result:
- `results/entry_state_score_transferability_v1.json`

Executable analysis:
- `analysis/31_entry_state_score_transferability.py`

Corrected onset endpoint:
- expert-corrected onset events = **418**.
