# Azores paper spine v1 — phase-specific control of eel migration

## Working title

**Internal migratory readiness governs activation but attenuates during progression in European eel**

Alternative, slightly broader:

**The biological control of migration shifts across sequential movement phases in European eel**

Do not put EOG in the title.

## One-sentence question

> **Does the same internal migratory state control both the activation and the subsequent progression of migration, or does its influence weaken once movement has begun?**

## Why this question matters

Movement ecology already recognises that animal movement reflects both internal state and external environment.

European eel is unusually useful for separating those components because:

- silvering provides an independently measured internal migratory-readiness axis;
- downstream migration can be decomposed into activation, timing, speed, barrier passage and final completion;
- multiple telemetry systems span sharply different route contexts.

The unresolved ecological problem is not whether physiology and environment both matter.

It is whether **their relative importance changes across sequential phases of the same migration**.

## Biological prediction

### Gate 1 — activation

If silvering state represents movement readiness:

> FIII -> FIV -> FV should increase the probability and hazard of entering directed downstream migration.

### Gate 2 — progression

If post-activation progression becomes increasingly constrained by route opportunity:

> the general Durif effect should weaken after initiation, while route/barrier context should become more informative.

The decisive test is the **change in the same Durif coefficient across phases**.

## Primary Europe-wide evidence

### Cohort

Six projects with compatible exact-stage migration reconstruction:

- Warnow;
- Leopoldkanaal;
- Albertkanaal;
- Scheldt / phd_verhelst_eel;
- Grote Nete;
- ESGL.

Tracked exact-stage cohort:

**n = 575 FIII/FIV/FV individuals**

The nine source-study 2015 expert non-migrant corrections are retained unchanged.

### Result 1 — migration initiation

Raw expert-corrected initiation:

| Stage | Initiated / tracked | Fraction |
|---|---:|---:|
| FIII | 154 / 261 | 0.590 |
| FIV | 53 / 68 | 0.779 |
| FV | 215 / 246 | 0.874 |

Adjusted initiation model:

- Durif OR per one-stage increment = **2.08**
- 95% CI **1.56–2.76**
- p ≈ **4.2e-7**

Controls:
- project × release-year baseline;
- within-stratum body length;
- within-stratum release timing.

### Result 2 — onset timing

Stratified Cox model:

- n = **570**
- onset events = **418**
- Durif HR per stage = **1.28**
- 95% CI **1.12–1.45**
- p = **0.00022**

Leave-one-project-out HR remains above 1 in all six omissions.

### Result 3 — completion after initiation

Among classified initiators:

- adjusted Durif OR per stage = **1.15**
- 95% CI **0.83–1.59**
- p = **0.412**

Thus advanced stage does not provide a general completion advantage once migration has started.

### Result 4 — post-initiation migration speed

Among initiated eels in informative strata:

- adjusted Durif speed ratio per stage = **0.983**
- 95% CI **0.852–1.134**
- p = **0.815**

The attenuation is therefore not specific to one binary endpoint.

### Result 5 — direct phase interaction

Stacked initiation/completion model with tag-clustered uncertainty:

- initiation OR per stage = **2.08**
- completion OR per stage = **1.15**
- OR ratio = **1.81**
- 95% CI **1.15–2.84**
- interaction p = **0.0099**

This is the central statistical result.

## Context evidence for Gate 2

Across the six projects:

### WRS vs initiation

- Spearman rho = **+0.029**
- exact p = **0.983**

### WRS vs completion conditional on initiation

- rho = **-0.928**
- exact p = **0.022**

The completion gradient remains strongly negative under leave-one-project-out analysis.

This is **bridge evidence only**, because WRS is project-confounded.

Do not present it as a causal barrier effect.

## Independent Dutch progression constraint

The 2026 Dutch consecutive-barrier study followed 40 FIII–FV European eels through a pumping station and tidal sluice.

Published progression:

- 35 passed the pumping station;
- 27 completed tidal-sluice passage to sea;
- cumulative barrier delay about 34 days.

Post-activation passage was associated with route-specific factors including:

- discharge-event duration;
- wind;
- lunar illumination;
- prior passage experience;
- movement speed/body condition at specific steps.

Durif did not remain a generic passage predictor at the pump and was non-identifiable at the sluice because of mass confounding.

This is independent ecological corroboration of a **post-activation opportunity filter**, not a direct replication of the Europe-wide phase interaction.

## Central result

The paper should state:

> **Internal silvering state strongly predicts whether and when migration is activated, but its general predictive advantage attenuates once migration begins.**

Then:

> **Post-activation movement is increasingly filtered by route-specific ecological opportunity and migration history.**

The second sentence is supported collectively, not by one causal coefficient.

## Novelty boundary

Do not claim novelty for:

- silvering as migration readiness;
- environmental triggers of eel departure;
- barrier effects;
- internal-state/external-environment interaction in movement ecology.

The novelty candidate is:

> **directly demonstrating that the effect of one independently measured internal-state predictor changes across sequential phases of realised migration.**

The phase interaction—not the label "control handoff"—is the evidence.

## Conservation implication

A management-relevant distinction follows:

> **Producing migration-ready silver eels and allowing those eels to escape to sea are separate conservation bottlenecks.**

Gate 1:
- physiological readiness / activation.

Gate 2:
- discharge windows;
- barrier operations;
- route connectivity;
- cumulative delay.

Therefore a high abundance of migration-ready individuals does not guarantee escapement when route opportunity is poor.

## Manuscript structure

### Introduction

1. Migration requires both readiness to depart and opportunity to progress.
2. Most studies analyse triggers or passage separately.
3. European eel supplies a measurable internal readiness axis plus heterogeneous migration routes.
4. Prediction: Durif state should dominate activation more strongly than progression.

### Methods

1. Europe-wide source panel and exact-stage cohort.
2. Inherited source migration classifier and expert corrections.
3. Gate 1 binary initiation model.
4. Gate 1 stratified Cox onset model.
5. Gate 2 conditional completion model.
6. Post-initiation speed model.
7. Direct clustered phase interaction.
8. Project-context WRS bridge.
9. Independent Dutch progression comparison.

### Results

Order exactly:

1. stage strongly predicts activation;
2. stage predicts earlier onset;
3. stage effect weakens for completion;
4. stage does not predict generic post-initiation speed;
5. direct phase interaction confirms attenuation;
6. project WRS aligns with Gate 2, not Gate 1;
7. Dutch barrier system shows route-specific post-activation controls.

### Discussion

1. Migration is a sequence of bottlenecks, not one movement phenotype.
2. Silvering readiness mainly regulates entry into movement.
3. External route opportunity increasingly constrains realised progression.
4. Why pooled "migration success" can hide mechanism.
5. Conservation: activation and escapement require different interventions.
6. Limits: developmental analyses, project confounding, Dutch stage/mass identifiability.

## Figure plan

### Figure 1 — conceptual + system design

Panel A:
FIII -> FIV -> FV readiness axis.

Panel B:
two gates:

~~~text
readiness -> activation -> progression -> escapement
~~~

Panel C:
six-project map/context only if needed.

### Figure 2 — Gate 1

- stage-specific initiation fractions;
- Cox adjusted HR / onset curves;
- leave-one-project-out stage HR.

### Figure 3 — direct handoff

Primary figure:

- initiation stage coefficient;
- completion stage coefficient;
- direct difference / OR ratio with CI.

Add post-initiation speed coefficient as secondary evidence.

### Figure 4 — Gate 2 context

- project median WRS vs initiation;
- project median WRS vs completion;
- clearly mark n=6 project-level diagnostic.

### Figure 5 / schematic — Dutch external route

Pump -> lake -> tidal sluice;
published passage counts and barrier-specific drivers.

Could remain Supplement if journal space is limited.

## Claims that must not appear

Do not say:

- "internal state causes migration";
- "WRS causes completion failure";
- "control switches completely from internal to external";
- "Durif no longer matters after initiation";
- "Dutch data independently confirm the exact phase interaction";
- "EOG predicted the mechanism".

Preferred language:

- "predicts";
- "is associated with";
- "attenuates";
- "is compatible with";
- "increasingly filtered by";
- "phase-specific control".
