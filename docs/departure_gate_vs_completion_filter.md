# Departure gate versus progression filter — canonical summary

## Primary biological result

The Europe-wide eel panel supports a **phase-dependent association of internal migratory readiness**.

### Gate 1 — migration activation

Expert-corrected tracked stage totals:

| Durif stage | tracked | initiated | rate |
|---|---:|---:|---:|
| FIII | 261 | 154 | **59.0%** |
| FIV | 68 | 53 | **77.9%** |
| FV | 246 | 215 | **87.4%** |

Adjusted activation model:

- OR/stage = **2.08**
- 95% CI = **1.56–2.76**
- p ≈ **4.2e-7**

The effect remains positive after deleting each entire project.

### Gate 2 — sea escapement after activation

The upstream source defines successful migration as **successful escapement to the sea**, with project-specific terminal station/distance rules.

Adjusted among initiators:

- OR/stage = **1.15**
- 95% CI = **0.83–1.59**
- p = **0.412**

### Direct phase test

A stacked continuation-ratio model gives each phase separate:

- project × release-year baselines;
- body-length effects;
- release-timing effects;
- Durif-stage coefficients.

Because initiators contribute to both phases, uncertainty is clustered by individual tag.

Direct attenuation:

- initiation/completion stage-OR ratio = **1.81**
- 95% CI = **1.15–2.84**
- p = **0.0099**

Leave-one-project-out:

- direction preserved in **6/6** deletions;
- OR-ratio range **1.55–2.13**;
- **5/6** remain p < 0.05.

Therefore the main result is not based on comparing one significant p-value with one non-significant p-value.

> **The stage effect itself is significantly stronger at activation than after activation.**

## Independent post-activation check

Using the source-study migration-speed definition among expert-corrected initiators:

- speed ratio/stage = **0.983**
- 95% CI = **0.852–1.134**
- p = **0.815**

The attenuation therefore appears in both sea escapement and generic post-activation speed.

## External-context bridge

Across six project contexts:

- WRS vs activation: rho **0.029**, exact p **0.983**
- WRS vs completion: rho **-0.928**, exact p **0.022**

This is descriptive bridge evidence only. WRS is strongly confounded with project/system context.

## Ecological interpretation

The supported developmental interpretation is:

> **internal silvering state is most informative at the transition into migratory behaviour; after activation, movement outcome becomes substantially more context dependent.**

This is a shift in **relative predictive control**, not a switch from purely internal to purely external control.

## Novelty boundary

The biology of silvering, environmental migration cues and barrier effects is already established.

The novelty candidate is the **empirical phase-specific dissociation in one continental telemetry panel**, not the phrase "two-gate migration."

## Confirmation target

The Dutch pump -> tidal-sluice system should test the unresolved second half:

> once migration is active, do measured barrier-specific passage opportunities explain progression more strongly than residual Durif differences?

## Numeric source of truth

Use:

- `results/phase_control_canonical_v1.json`
- `manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V1.json`
- `docs/phase_stage_interaction_result.md`
