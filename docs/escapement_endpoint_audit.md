# Escapement-endpoint audit

## Why this audit was necessary

The Azores programme initially treated membership in the upstream file:

`successful_migrants_final_detection.csv`

as a binary completion endpoint, with non-membership interpreted as failure.

The upstream source code does create this file by applying project-specific terminal station/distance rules to migratory eels.

However, the source Europe-wide meta-analysis explicitly states that it **did not analyse escapement success rate** because doing so would require assumptions about:

- fishing intensity;
- detection loss;
- release position;
- whether tagged eels adequately represent the underlying migrating population;
- route-specific monitoring geometry.

Therefore:

> **membership in the terminal positive set is a valid positive observation, but its complement is not a validated biological failure state.**

## Consequence

The following analyses remain reproducible but are **not primary biological inference**:

- conditional terminal-endpoint OR by Durif stage;
- stacked initiation-versus-terminal-endpoint phase interaction;
- project-level WRS correlation with terminal-endpoint membership.

They are retained as **secondary sensitivity / observability-dependent results**.

## Primary evidence after audit

### 1. Migration activation

Expert-corrected binary initiation:

- FIII: 59.0%
- FIV: 77.9%
- FV: 87.4%
- adjusted OR per stage: **2.08**
- 95% CI: **1.56–2.76**

### 2. Time to behavioral onset

Stratified Cox:

- HR per stage: **1.29**
- 95% CI: **1.13–1.47**

### 3. Progression after activation

Source-defined migration speed among activated eels:

- ratio per stage: **0.983**
- 95% CI: **0.852–1.134**
- p = **0.815**

This continuous progression endpoint does not require defining every non-terminal eel as a biological failure.

## Correct ecological interpretation

The current defensible result is:

> **advanced silvering strongly predicts entry into the migratory movement state and earlier onset, but there is no general Durif-stage gradient in migration speed once movement is active.**

This is consistent with increasing importance of route/hydrological context after activation, but does not prove a causal handoff.

## What remains useful from the terminal endpoint

The positive terminal set can still be used for:

- arrival-time description among observed successful migrants;
- source-study figures;
- bounded sensitivity analyses.

It must not be used to estimate an unconditional or conditional biological failure probability without an explicit censoring/observation model.

## Canonical source

Use:

- `results/phase_control_canonical_v2.json`

for manuscript interpretation.

Version 1 is retained for provenance.
