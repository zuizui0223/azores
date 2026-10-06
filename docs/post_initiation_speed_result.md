# Post-initiation speed result: Durif stage predicts activation, not migration speed

## Current interpretation boundary (2026-10-07)

This file records an earlier **control-handoff hypothesis** and is retained for provenance. It is not the current manuscript-level claim.

The canonical interpretation is the narrower **transferability boundary**:

> **Capture-time silvering readiness is a strong and transferable predictor of migration activation/onset in the six-project cohort, but it provides little general predictive information for pooled whole-route post-activation speed.**

The pooled speed endpoint reproduces exactly (n=418; ratio 0.983, 95% CI 0.852–1.134), and project-specific speed coefficients show no detectable heterogeneity (Q=2.47, df=5, p=0.781). This does **not** establish that internal state becomes irrelevant after activation or that external opportunity universally takes over control. A River Test study published in 2026 provides an explicit external boundary where silvering stage contributes to a route-specific progression metric.

Use `manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V3.md`, `docs/CLAIM_EVIDENCE_MAP_PHASE_CONTROL_V2.md`, and `docs/POST_ACTIVATION_SPEED_REPRO_AUDIT_2026_10_05.md` for current claims.


## Question

The current Azores programme separates migration into:

1. **activation/initiation**;
2. **progression after activation**.

Durif stage strongly predicts Gate 1. The next test asks whether the same internal-readiness gradient also predicts how fast an already initiated migration proceeds.

## Speed definition

The analysis reproduces the source meta-analysis definition:

```text
time
  = max(departure) - min(arrival)

distance
  = max(distance_to_source_m) - min(distance_to_source_m)

migration_speed
  = distance / time
```

calculated only over expert-corrected `migration == TRUE` rows.

## Descriptive speed

Among the stage-coded initiators retained in informative project-year strata:

- FIII median: **0.0229 m/s**
- FIV median: **0.0232 m/s**
- FV median: **0.0245 m/s**

There is little raw separation.

## Adjusted model

Model:

```text
log(migration speed)
  ~ project × release-year fixed effects
  + within-stratum body length
  + within-stratum release timing
  + ordinal Durif stage
```

N = **418** initiated eels.

### Durif stage

Per FIII -> FIV -> FV increment:

- multiplicative speed ratio = **0.983**
- 95% CI = **0.852–1.134**
- p = **0.815**

Thus there is essentially no general stage gradient in post-initiation speed.

### Body length

Per +100 mm:

- ratio = **1.09**
- 95% CI = **0.93–1.27**
- p = **0.306**

### Release timing

Per +100 days later:

- ratio = **1.45**
- 95% CI = **1.01–2.07**
- p = **0.044**

The release-timing effect is secondary/developmental and should not be promoted to a new mechanism claim.

## Contrast with Gate 1

The same ordinal Durif variable strongly predicts:

- whether migration initiates: OR **2.08** per stage increment;
- onset timing in the stratified Cox analysis: HR **1.28**;
- but not post-initiation speed: ratio **0.983**;
- and not completion conditional on initiation: OR **1.15**.

This yields a much more specific ecological pattern:

> **advanced silvering primarily changes the probability and timing of entering the migratory state, not the generic speed or success of movement after that state has been entered.**

## Biological interpretation

The evidence is consistent with an **initiation–progression control handoff**:

```text
internal readiness
    -> activates movement

after activation
    -> route opportunity / barriers / hydrology / route history
       increasingly determine progression
```

The external variables in the second line are candidates, not identified causes from this speed model.

## Why this matters

A single final-success analysis would obscure the distinction between:

- motivation/readiness to leave;
- locomotor progression after leaving;
- landscape passage.

The speed result independently supports the phase separation already seen in the completion endpoint and direct phase-interaction test.

## Evidence boundary

Developmental independent evidence only.

The upstream telemetry and source outcomes were public and inspected during programme development. The result is not preregistered confirmation.
