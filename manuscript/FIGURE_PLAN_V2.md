# Final figure plan V2 — endpoint-audited Azores manuscript

This plan is canonical for `AZORES_PHASE_CONTROL_MANUSCRIPT_V3.md`.

## Figure 1 — Biological question and analysis universe

**Purpose:** define the phase-resolved question without making a terminal success/failure claim.

Panel A:
- FIII → FIV → FV capture-time Durif readiness axis.

Panel B:
- movement sequence:
  readiness → migration activation → post-activation progression.

Panel C:
- six-project evaluable cohort;
- 575 stage-coded tracks;
- terminal positive-set observations are not shown as a binary biological gate.

Message:
> internal readiness is measured before telemetry movement and is tested separately against activation and progression.

## Figure 2 — Internal readiness predicts migration activation

### Panel A — activation fraction by stage

- FIII: 154/261 = 59.0%
- FIV: 53/68 = 77.9%
- FV: 215/246 = 87.4%

Adjusted activation:
- OR/stage = **2.08**
- 95% CI **1.56–2.76**

### Panel B — time to behavioral onset

Forest plot:
- primary Cox HR/stage = **1.29**
- 95% CI **1.13–1.47**
- six leave-one-project-out estimates.

Message:
> more advanced readiness predicts both whether and when behavioral migration becomes expressed.

## Figure 3 — The Durif gradient is absent from generic post-activation speed

### Panel A — descriptive migration speed by stage

Median source-defined migration speed among modelled activated eels:

- FIII: **0.0229 m/s**
- FIV: **0.0232 m/s**
- FV: **0.0245 m/s**

These are descriptive; do not infer from raw medians alone.

### Panel B — adjusted stage effect on speed

- multiplicative speed ratio/stage = **0.983**
- 95% CI **0.852–1.134**
- p = **0.815**

Plot on a ratio scale centred at 1.

Message:
> the readiness gradient that is strong at activation is not a generic predictor of migration speed after activation.

Do **not** plot the terminal positive-set OR as a co-primary phase endpoint.

## Figure 4 — Independent barrier system identifies route-specific progression variables

Schematic:
pumping station → lake → tidal sluice → sea

Published Dutch context:
- tagged: 40
- passed pump: 35
- terminal sea-positive: 27
- mean cumulative barrier delay: ~34 d

Annotate published barrier-specific candidate variables at the relevant structures:
- discharge opportunity;
- wind;
- lunar illumination;
- prior barrier passage experience.

Boundary:
> this is independent ecological context/confirmation target, not a direct replication of the Europe-wide activation model.

## Supplementary Figure S1 — terminal positive-set sensitivity

Retain for audit only:

- terminal-set membership OR/stage among activated eels: **1.15**, CI **0.83–1.59**
- former initiation/terminal OR-ratio: **1.81**, CI **1.15–2.84**

Required title/annotation:

> **Sensitivity using an observability-dependent terminal positive set; non-membership is not a validated biological failure state.**

Do not call this “completion probability”.

## Supplementary Figure S2 — project-level WRS context sensitivity

If retained:
- WRS vs activation: rho **0.029**, exact p **0.983**
- WRS vs terminal positive-set membership: rho **−0.928**, exact p **0.022**

Required annotation:
- n = 6 project contexts;
- project-confounded;
- terminal response observability dependent;
- contextual only, not causal.

## Figure data source

Canonical numeric input:
- `manuscript/FIGURE_DATA_CONTRACT_V2.json`

Materialized plotting tables:
- `manuscript/figure_data_v2/`

No main figure may use terminal non-membership as biological failure.
