# Time-to-event result: Durif stage predicts earlier threshold-defined migration onset

## Correction

This analysis now uses the same onset clock as the canonical initiation analysis.

Event time is:

> **time from release to `time_first_dist_to_use` attached to the first row with `downstream_migration = TRUE`.**

It does not use the first arrival time of the broader `migration = TRUE` interval label.

The nine source-study 2015 expert non-migrant corrections are retained unchanged.

## Cohort

Six compatible exact-stage projects:

- Warnow;
- Leopold Canal;
- Albert Canal;
- Scheldt / phd_verhelst_eel;
- Grote Nete;
- ESGL.

After restricting the Cox model to project × release-year strata with migration events and at least two Durif stages:

- **n = 570**
- **418 threshold-defined onset events**
- **13 strata**

## Model

Stratified Cox model with Breslow ties.

Covariates:

- within-stratum body length / 100 mm;
- within-stratum release timing / 100 days;
- ordinal Durif stage FIII=0, FIV=1, FV=2.

## Corrected result

### Durif stage

Per one-stage increment:

- HR = **1.29**
- 95% CI **1.13–1.47**
- p = **0.00016**

### Body length

Per +100 mm:

- HR = **1.08**
- 95% CI **0.95–1.23**
- p = **0.222**

### Release timing

Per +100 days:

- HR = **1.40**
- 95% CI **1.02–1.92**
- p = **0.039**

## Leave-one-project-out stage effect

| omitted project | HR | 95% CI | p |
|---|---:|---:|---:|
| Warnow | **1.43** | 1.22–1.69 | 0.000013 |
| Leopold Canal | **1.20** | 1.04–1.39 | 0.012 |
| Albert Canal | **1.52** | 1.32–1.76 | <1e-7 |
| Scheldt / 2015 | **1.09** | 0.94–1.27 | 0.252 |
| Grote Nete | **1.29** | 1.12–1.48 | 0.00029 |
| ESGL | **1.29** | 1.12–1.47 | 0.00025 |

The average onset-hazard effect is positive, but its formal precision depends meaningfully on the Scheldt system.

## Ecological interpretation

The time-to-event analysis supports:

> **advanced morphological readiness is associated with earlier expression of directed downstream migration.**

But timing is more system dependent than the binary initiation probability.

Therefore the hierarchy of evidence is:

1. **strongest:** stage predicts whether migration is activated;
2. **secondary:** stage predicts earlier threshold-defined activation on average;
3. **not supported generally after activation:** stage does not provide a general speed or completion advantage.

## Boundary

The Cox result does not establish a stage × landscape interaction.

Its project dependence strengthens the motivation for phase-specific external-opportunity tests rather than justifying a universal onset-rate constant.
