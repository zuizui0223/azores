# Dutch consecutive-barrier control-handoff protocol

## Role

The Europe-wide eel panel established a robust developmental **internal-state signal** but could not cleanly confirm a general state × landscape interaction because WRS is strongly project-confounded.

The Dutch source-to-sea system is therefore used as a **within-landscape confirmation candidate**.

Source:
- van Rijn et al. 2026
- paper DOI: 10.1139/cjfas-2025-0359
- data DOI: 10.17026/LS/WTSUNG

## Why this system is useful

The published study followed 40 tagged European eels through:

1. a pumping station;
2. a lake;
3. a tidal sluice.

Published outcomes:
- 35/40 passed the pumping station;
- 27/40 completed seaward passage through the tidal sluice;
- mean cumulative barrier delay about 34 days.

The same route therefore exposes individuals to **two different barrier/opportunity regimes**.

All retained fish were classified in advanced Durif stages FIII–FV.

## Confirmation question

> **Among eels already in FIII-FV, does progression through consecutive barriers depend more on route-specific opportunity and prior passage experience than on Durif stage itself?**

This is not a rerun of the source paper's overall barrier-driver analysis.

## Primary variables required

Per individual:

- Durif stage FIII/FIV/FV;
- body mass and/or body condition;
- barrier identity;
- passage success;
- passage delay/opportunities;
- discharge/opportunity characteristics;
- timing.

## Model hierarchy

### D0 — source-paper covariates

```text
passage / delay
  ~ body condition
  + body mass
  + discharge/opportunity
  + weather/lunar covariates
```

### D1 — internal readiness

```text
D0 + Durif stage
```

### D2 — state-dependent opportunity

```text
D1 + Durif stage × passage opportunity
```

The interaction is the confirmation target.

## Hard confounding boundary

The source paper reports that at the tidal sluice, Durif stage and body mass could not be separated among successful individuals.

Therefore:

- pump and sluice analyses must be reported separately;
- an interaction is confirmatory only where stage has enough independent variation from mass/condition;
- do not drop body mass merely to make Durif stage significant;
- if the stage effect is not identifiable at the sluice, report **non-identifiable**, not null.

## Cross-barrier biological prediction

A stronger biological prediction is:

> eels with greater migratory readiness should exploit available passage windows more efficiently, but the expression of that readiness should differ between the mechanically controlled pump and tidal sluice.

This predicts **barrier-specific state dependence**, not a universal fixed effect of stage.

## Success condition

The general mobility-gating programme strengthens if:

1. stage or stage × opportunity has a stable effect at at least one barrier after body condition/mass control;
2. the effect does not require post-hoc regrouping of FIII/FIV/FV;
3. the direction is compatible with the Europe-wide internal-state signal;
4. uncertainty and non-identifiability at the second barrier are reported rather than rescued.

## Failure condition

If stage adds no information at either barrier under adequate variation and precision, the Europe-wide stage association should be treated as a context-dependent predictor rather than a general movement-gating mechanism.


## Published result already constrains the hypothesis

The paper itself supplies a critical independent result before any reanalysis:

- pumping-station global individual model included Durif stage, but Durif was dropped during model selection;
- tidal-sluice analysis excluded Durif because FIV body mass was too confounded with stage to separate;
- pumping-station passage was associated with discharge duration and wind;
- tidal-sluice passage was associated with moon illumination;
- prior pumping-station passage experience predicted faster subsequent tidal-sluice passage.

Therefore a reanalysis is **not authorized to hunt for a rescued Durif coefficient**.

The raw-data objective is instead variance/control decomposition across movement phases.
