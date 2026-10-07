# Multivariate readiness-gate diagnostic — 2026-10-07

## Question

The activation-filter diagnostic showed that migration entry is phenotypically selective within Durif stage.

A natural mechanism hypothesis was **compensatory readiness**:

> less advanced FIII eels might need unusually large body size or good body condition to cross the activation gate, whereas those traits should matter less after silvering advances to FIV/FV.

This was tested post hoc with the public six-project cohort.

## Data and body-state proxy

Evaluable exact-stage animals with body weight:
- **575**

Primary model:
- **n = 525**
- **11 informative project-year strata**

The condition proxy is the standardized residual of log body weight after adjustment for:
- log body length;
- project;
- capture Durif stage.

It is a **capture body-state proxy**, not a direct lipid or endocrine measurement.

## Additive model

Adjusted activation effects:

- Durif stage: **OR 2.15 per stage**  
  95% CI **1.61–2.87**, p = **2.3×10⁻7**
- body condition: **OR 1.46 per 1 SD**  
  95% CI **1.16–1.83**, p = **0.0010**
- body length: **OR 1.31 per 100 mm**  
  95% CI **0.96–1.78**, p = **0.090**
- within-stratum release timing: **OR 1.17 per 100 d**  
  95% CI **0.60–2.28**, p = **0.644**

Thus ordinal silvering stage does not exhaust the information in capture body state.

## Compensation test

Adding:

- Durif × body length;
- Durif × condition

did **not** improve the model:

- likelihood-ratio χ² = **0.143**, df = 2
- p = **0.931**

Interactions:

- Durif × length OR = **1.002**, p = **0.993**
- Durif × condition OR = **1.055**, p = **0.706**

The condition association was positive at every stage:

- FIII: OR **1.40** per SD, 95% CI **1.04–1.90**
- FIV: OR **1.48**, 95% CI **1.17–1.87**
- FV: OR **1.56**, 95% CI **1.03–2.36**

So the simple prediction that good condition mainly compensates for low Durif stage is not supported.

## Leave-one-project-out direction

The additive condition coefficient remained positive after omitting each project.

Approximate ORs per 1 SD across the six leave-one-project-out fits:
- **1.23–1.65**

Several intervals widen after project removal, but no leave-one-project-out estimate reverses direction.

## Current interpretation

The developmental result is:

> **migration activation is better described by additive capture-state information than by a single ordinal silvering axis.**

However, this does **not** yet establish two mechanistically independent physiological axes.

Durif silvering classifications are themselves based on external morphometrics that include body length and body weight. Therefore the extra condition term may partly recover continuous biometric information that an ordinal stage label compresses.

The defensible wording is:

> **capture weight-for-length state retains predictive information for migration activation beyond the ordinal Durif label.**

Do not call this an energetic threshold without an independent lipid, endocrine or repeated physiological measurement.

## Biological context

Earlier work already links eel condition and energetic reserves to reproductive potential and migration biology. The new contribution here, if independently reproduced, would be narrower: within a multi-project telemetry cohort and after accounting for ordinal silvering stage, continuous capture body-state information predicts behavioral migration activation.

## Next falsification

A consistency diagnostic is now required:

> if the condition signal reflects the same activation process rather than only a binary-classification artifact, does better capture condition also predict **earlier migration onset**?

Executable test:
- `analysis/18_body_condition_onset_diagnostic.py`

## Status

**ADDITIVE_BODY_STATE_SIGNAL_WITHOUT_STAGE_COMPENSATION**

Evidence class:
- post-hoc developmental mechanism diagnostic.

Executable source:
- `analysis/17_multivariate_readiness_gate_diagnostic.py`

CI source:
- independent-data-audit run 37562109034.
