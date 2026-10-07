# Entry state versus realized movement performance — novelty positioning

Date: 2026-10-07

## What is **not** new

The paper should not claim that movement has separable internal-state and
motion-capacity components. That distinction is already explicit in the
movement-ecology framework (Nathan et al. 2008).

It should also not claim that Durif stage was newly shown to predict migratory
status. The original Durif classification explicitly defines FIII as
pre-migrant and FIV/FV as migrating stages (Durif et al. 2005), and later work
linked these stages to downstream-migration status and maturation.

Nor is it novel simply to observe a weak silvering-stage effect on migration
speed. A Loire-estuary telemetry study reported that migration descriptors did
not differ significantly among maturity stages, while directional migration
speed covaried with body size (Béguer-Pon et al. 2014).

Finally, body condition is already widely expected to carry over into movement
performance. In red knots, capture condition predicted departure behaviour,
faster ground speed and shorter stopovers (Duijns et al. 2017). The physiology
of movement literature likewise summarizes many cases in which better
condition is associated with faster or more efficient integrated migration
(Goossens et al. 2020).

## The sharper gap

The under-tested question is not:

> does internal state matter for migration?

It is:

> **does a phenotype shown empirically to rank migratory entry retain that
> ranking when transferred, without outcome-specific retuning, to subsequent
> realized movement performance?**

That is a transferability question across sequential phases of the same
movement programme.

## What Azores currently contributes

### 1. The entry phenotype is empirically multivariate

In the Europe-wide panel, both ordinal Durif stage and continuous
weight-for-length condition independently predict migration activation.

The activation-trained score is therefore not merely the Durif classification
renamed. It is an empirical combination of two capture-state signals.

### 2. The same weights transfer to timing of entry

Without re-estimating their relative weights for the onset endpoint, the score
predicts earlier behavioral onset.

This establishes internal coherence within the **entry process**:
- whether migration becomes expressed;
- when it becomes expressed.

### 3. The same weights fail to transfer to two generic progression summaries

The score explains essentially none of the variation in:
- whole-route post-activation speed;
- the frozen per-eel median positive inter-station speed.

This is an empirical cross-phase decoupling, not just a null single-predictor
test.

### 4. The boundary survives project-held-out score training

When each project's migration outcomes are excluded while training the
Durif/condition score weights, the held-out-project score still predicts
activation and onset but not either generic speed endpoint.

Thus the pattern is not simply in-sample reuse of the focal project's outcome
when defining the score.

### 5. The boundary survives exact-link comparison

The frozen within-link audit compares realized positive source speeds on the
same directed receiver-to-receiver links, gives each eel total weight one, and
clusters uncertainty by eel.

Primary frozen result:
- **18,012** segment rows;
- **426** eels;
- **248** directed station pairs;
- entry-state speed ratio **0.995 per SD**;
- 95% CI **0.912–1.087**;
- p = **0.918**;
- weighted partial R² approximately **0.00052%**.

Pair-support sensitivities remain close to one:
- >=3 fish/pair: **0.991**;
- >=10 fish/pair: **1.032**.

Leave-one-project-out estimates cross both sides of one.

This directly weakens the objection that the phase boundary is created only by
pooling unlike rivers, route lengths or station geometries.

## Important data-quality boundary

The source segment-speed field contains grossly implausible values generated
when kilometre-scale inter-station distances are divided by very short
last-to-first detection intervals.

The frozen primary intentionally retained all positive source values because
outliers were not excluded after inspecting their relationship with the
entry-state score.

The registered post-hoc external-plausibility sensitivity is complete and
supports promotion of the within-link result as robustness evidence while
retaining the source-speed quality warning.

External context:
- European silver-eel Ucrit about **0.94 m/s** and Uopt about **0.64 m/s**
  (Tudorache et al. 2015);
- a compiled European-eel swimming-performance database reports observed
  speeds up to about **2.26 m/s**;
- the source within-link candidate data contain values above **3,700 m/s**.

The registered quality sensitivity repeats the exact primary model at
externally motivated upper screens of 2.5, 5 and 10 m/s. The all-positive-speed
primary remains frozen regardless of the sensitivity result.

Observed quality-sensitivity result:
- <=2.5 m/s: ratio **0.978**, 95% CI **0.911–1.049**;
- <=5 m/s: ratio **0.979**, 95% CI **0.913–1.049**;
- <=10 m/s: ratio **0.976**, 95% CI **0.910–1.047**.

These screens remove **62.5%**, **58.1%** and **52.5%** of candidate rows,
respectively, yet all retain the same null-compatible conclusion.

## Current novelty claim

With the quality sensitivity remaining near null, the strongest defensible
contribution is:

> **Migratory commitment and realized transit speed are distinct prediction
> targets: a multivariate capture phenotype trained to rank entry into
> migration transfers to onset, but not to generic or same-link realized
> movement speed.**

This is more specific than the general statement that internal state and motion
capacity are conceptually distinct.

It is also different from a conventional predictor-by-endpoint comparison:
the **same activation-derived weights** are transferred across phases, and the
result survives project-held-out training and route-link control.

## What still cannot be claimed

Do not claim:
- a universal biological law that readiness never predicts speed;
- intrinsic swimming capacity was measured directly;
- internal state ceases to matter after activation;
- route environment causally replaces internal state;
- the score is a validated latent physiological readiness variable;
- the source-derived link speeds are direct measurements of intrinsic
  swimming capacity; the quality screen only shows that gross speed artifacts
  do not create the near-null entry-state coefficient.

Moyo et al. (2026) remains an important scope boundary because silvering stage
was retained in a finer reach-level progression model. The likely general
principle is therefore about **transferability across phase and scale**, not
universal disappearance of internal-state effects.
