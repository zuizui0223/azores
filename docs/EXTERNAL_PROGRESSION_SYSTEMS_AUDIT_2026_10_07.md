# External post-activation systems audit — 2026-10-07

## Why this audit exists

The six-project Europe-wide analysis gives a strong capture-time Durif signal for migration activation/onset but little general signal for whole-route speed after activation.

That pattern has at least three biologically distinct explanations:

1. **phase-specific performance coupling** — capture-time readiness primarily predicts entry into migration, not subsequent locomotor speed;
2. **scale dependence** — readiness still matters after activation, but its signal is visible at reach/event scale and is averaged away by a whole-route speed metric;
3. **state convergence / predictor ageing** — initially less advanced eels can progress physiologically before migration is expressed, so capture-time Durif stage becomes a stale proxy for state at the time progression is measured.

External systems must therefore be assigned distinct roles rather than all being called "confirmation".

## 1. River Test, England — external scale boundary

Source:
- Moyo et al. 2026, *Hydrobiologia*
- DOI: 10.1007/s10750-026-06406-6

Design:
- 25 silver eels tracked acoustically;
- 24 were detected migrating downstream;
- 19 reached the lower/tidal area;
- 13 were subsequently detected in the marine environment;
- river progression was resolved by receiver-defined reaches;
- candidate predictors included silvering stage, temperature, river flow, moon illumination, tide and barrier context.

Published model selection retained silvering stage in the reach-level progression model together with environmental/route variables.

### Role

**Best current external boundary against a strong "internal state stops mattering after activation" interpretation.**

It shows that a capture-time silvering signal can remain detectable for finer-scale progression even though the Europe-wide whole-route speed coefficient is near zero.

### What it does not show

- it is not a preregistered replication of the Azores phase model;
- it does not establish a general stage × barrier interaction;
- it does not show that the six-project pooled null is caused by spatial aggregation;
- it does not repeatedly measure physiological state after tagging.

## 2. Dutch pump -> tidal sluice — event-level mechanism candidate

Source:
- van Rijn et al. 2026
- DOI: 10.1139/cjfas-2025-0359
- DANS: 10.17026/LS/WTSUNG

Published cohort:
- 40 FIII–FV eels;
- FIII = 11, FIV = 6, FV = 23;
- 35 passed the pumping station;
- 27 completed seaward passage through the tidal sluice.

The public archive contains event-resolved passage/environment tables and acoustic detections.

### Strength

This is the strongest available system for asking how already-migrating eels exploit discrete hydrological passage windows at two consecutive barriers.

### Three design boundaries

#### A. Source opportunity eligibility is duration-dependent

The source study defined passage opportunities partly by asking whether an eel could reach the barrier within a discharge event. Event duration therefore contributes to whether a row is called an opportunity.

A new `readiness × duration` mechanism test must not use those source-defined opportunity rows as its primary risk set.

Current solution:
- reconstruct first direct barrier arrival from telemetry;
- include subsequent discharge events before confirmed downstream passage;
- only then use discharge duration as an exposure.

See:
- `docs/dutch_barrier_confirmation_protocol.md`
- `analysis/13_dutch_arrival_riskset_gate.py`

#### B. Durif stage is associated with release cohort

Published counts by release group:

| release | FIII | FIV | FV |
|---|---:|---:|---:|
| 11 Oct 2021 | 9 | 3 | 8 |
| 18 Oct 2021 | 1 | 1 | 7 |
| 26 Oct 2021 | 1 | 2 | 8 |

Thus 9/11 FIII eels came from the earliest release.

The source study also reports unusually high movement speed in the third release group coinciding with an exceptionally long discharge event. Any readiness × event-duration interpretation therefore requires a release-group/calendar-hydrology sensitivity.

#### C. Durif stage and body mass are partly non-identifiable

At the tidal sluice, the source study could not separate Durif stage adequately from body mass.

A matched eel-stratified model removes constant individual main effects but does not remove confounding between stage × event and body mass × event.

### Role

**Developmental event-level mechanism test, not clean external replication.**

Allowed outcomes include supported, unsupported, stage-vs-release confounded, stage-vs-mass non-identifiable, or non-reconstructable risk set.

## 3. Lithuania free-flowing rivers -> Curonian Lagoon — bottleneck-location contrast

Source:
- Dainys et al. 2026, *Estuarine, Coastal and Shelf Science*
- DOI: 10.1016/j.ecss.2026.110163

Published result:
- overall riverine migration success = 76%;
- individual river sections generally 72–92%, with many downstream sections at 100%;
- only 65.8% of eels detected in the Curonian Lagoon were subsequently recorded escaping to the Baltic Sea;
- 24 eels, 48% of the tagged cohort, were detected entering the Baltic Sea.

### Role

**Strong external example that the dominant bottleneck can move between route compartments.**

The river itself was comparatively permeable, while the lagoon became the major downstream constraint.

### What it does not establish

The available publication-level evidence does not yet show that individual Durif variation is sufficient for a readiness-gradient analysis. Therefore this system is a route-bottleneck contrast, not a stage-effect replication.

## 4. Historical/source cohorts already inside the Europe-wide panel

Warnow, Leopoldkanaal, Albertkanaal, the Scheldt PhD cohort, Grotenete and ESGL contribute to the six-project Azores reanalysis.

Open telemetry records from those systems are valuable for reproducibility and new endpoint construction, but they are **not external replications** of the six-project result.

## 5. Newly recognized biological alternative — state convergence

Capture-time Durif stage is a time-varying developmental state, not an immutable trait.

Palstra et al. (2011) showed strong temporal progression in silvering/maturation during the downstream migration season: stage-3 and stage-4 frequencies declined while stage-5 increased substantially over time.

In the current six-project cohort, among expert-corrected initiators:

- FIII median release-to-threshold latency = **7.21 d**;
- FIV = **2.14 d**;
- FV = **2.15 d**;
- adjusted multiplier per Durif increment = **0.715**.

Therefore initially less advanced eels have more elapsed time before the post-activation response is measured.

This creates a plausible alternative:

> **the capture-time stage gradient may attenuate because the underlying physiological states converge before or during migration, not because internal state loses biological importance after activation.**

The frozen diagnostic is now complete.

- Durif × log-latency interaction ratio = **1.036**, p = **0.382**;
- <=1 d stage-speed ratio = **0.942**;
- <=3 d = **0.953**;
- <=7 d = **0.963**.

The simple prediction that an early positive stage-speed advantage decays with longer pre-activation waiting time is therefore **not supported**. The diagnostic cannot rule out physiological convergence because individuals were not repeatedly staged.

See:
- `analysis/14_stage_staleness_diagnostic.py`
- `results/stage_staleness_diagnostic_v1.json`
- `docs/STAGE_STALENESS_DIAGNOSTIC_RESULT_2026_10_07.md`

## 6. Newly recognized identification boundary — activation filtering

Post-activation speed is observed only among eels that crossed a strongly stage-dependent activation gate.

Measured capture phenotype confirms that the gate is selective. Among FIII eels, initiators versus non-initiators differed by:

- length SMD = **+0.514**;
- weight-for-length residual SMD = **+0.302**.

However, among 373 speed-bearing initiators with estimable canonical initiation propensities, inverse-probability weighting changes the same-sample stage-speed ratio only:

- unweighted: **1.042** (0.902–1.205);
- weighted: **1.062** (0.916–1.230).

Thus measured activation selection exists but does not restore a general positive speed gradient.

This does not solve the principal-stratum problem: unmeasured latent readiness can still determine which FIII eels cross the gate, and speed is undefined for animals that never migrate.

See:
- `analysis/15_activation_filter_diagnostic.py`
- `results/activation_filter_diagnostic_v1.json`
- `docs/ACTIVATION_FILTER_DIAGNOSTIC_RESULT_2026_10_07.md`

## Current evidence hierarchy

1. **Primary internal result:** capture-time Durif strongly predicts migration activation and onset.
2. **Primary progression result:** no general Durif gradient in six-project whole-route post-activation speed.
3. **External scale boundary:** River Test shows a silvering-stage signal can persist at reach scale.
4. **Event mechanism candidate:** Dutch system can test opportunity exploitation, but only with arrival-defined risk sets and explicit release/mass confounding checks.
5. **Route bottleneck boundary:** Lithuania shows that the location of post-activation limitation can shift from river to lagoon.
6. **State-convergence alternative:** simple tested pattern unsupported, but repeated physiological state is unavailable.
7. **Activation-filter boundary:** measured selection is real but does not restore a general stage-speed gradient; latent selection remains unresolved.

## Manuscript consequence

Avoid wording that implies:

> internal readiness itself becomes weaker after activation.

Prefer:

> **capture-time Durif stage strongly predicts entry into migration, but among eels selected through that stage-dependent gate it does not provide a transferable general speed ranking; simple predictor ageing and measured activation selection do not explain the weak gradient, while finer route-specific effects and latent readiness selection remain possible.**
