# Body-condition consistency across migration activation and onset — 2026-10-07

## Question

A post-hoc multivariate readiness-gate diagnostic found that capture weight-for-length state predicted whether classified downstream migration activated after adjustment for ordinal Durif stage, body length, release timing and project-year context.

This consistency diagnostic asks whether the same capture body-state proxy also predicts **when** migration becomes behaviorally expressed.

## Primary onset result

Stratified Cox model:
- n = **570**
- migration-onset events = **418**
- project × release-year strata = **13**

Adjusted effects:

- Durif stage: **HR 1.284 per stage**  
  95% CI **1.125–1.466**, p = **0.00021**
- capture condition: **HR 1.149 per 1 SD**  
  95% CI **1.029–1.284**, p = **0.0139**
- body length: HR **1.105 per 100 mm**  
  95% CI **0.968–1.261**, p = **0.138**
- within-stratum release timing: HR **1.408 per 100 d**  
  95% CI **1.027–1.931**, p = **0.0336**

Thus better capture weight-for-length state is associated with earlier migration onset in the same direction as its positive association with migration activation probability.

## Stage × condition interaction

Adding Durif × condition did not improve the onset model:

- interaction HR = **0.964**
- 95% CI **0.848–1.095**
- p = **0.570**
- LR p = **0.570**

The data therefore do not support a simple model in which good condition mainly compensates for low Durif stage.

## Leave-one-project-out

The condition HR remained **>1 in all six** leave-one-project-out fits.

Approximate range:
- **1.053–1.215**

Precision varied:
- omitting Leopoldkanaal produced the weakest estimate (HR 1.053, p=0.391);
- omitting the 2015 project produced the strongest (HR 1.215, p=0.0027).

The direction is therefore not created by one project, although the evidence is not independently significant in every leave-one-project-out subset.

## Joint interpretation with activation probability

Across the two post-hoc diagnostics:

- activation odds ratio per condition SD = **1.459**  
  95% CI **1.165–1.827**
- onset hazard ratio per condition SD = **1.149**  
  95% CI **1.029–1.284**

and neither analysis supports a Durif × condition interaction.

The narrow empirical statement is:

> **capture weight-for-length state retains additive predictive information for both whether and when classified migration activates beyond the ordinal Durif label.**

## Critical boundary

Do **not** interpret this as an independent energetic-state axis yet.

The Durif silvering classification itself uses body morphometrics including body length and weight. The condition proxy therefore partly interrogates continuous biometric information that the ordinal stage label compresses.

This result can support:

> continuous capture body-state information is not exhausted by ordinal Durif stage.

It cannot yet support:

> energetic reserves independently cause migration activation.

A stronger physiological interpretation would require independent lipid, endocrine, or repeated physiological measurements.

## Next robustness test

Test whether the positive condition signal survives alternative prespecified body-condition definitions:

1. stage-adjusted allometric log-weight residual (current);
2. project-adjusted allometric residual without stage in the residualization step;
3. Fulton condition factor, standardized within project-year context.

The signal should not be promoted if its direction depends on one residualization convention.

## Status

**CONSISTENT_ADDITIVE_BODY_STATE_SIGNAL_ACROSS_ACTIVATION_AND_ONSET**

Evidence class:
- post-hoc developmental consistency diagnostic.

Canonical result:
- `results/body_condition_onset_diagnostic_v1.json`

Executable analysis:
- `analysis/18_body_condition_onset_diagnostic.py`

CI:
- independent-data-audit run **37563508791**.
