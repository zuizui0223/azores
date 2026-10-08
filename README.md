# azores

## Main ecological question

> **Does the capture phenotype that makes a European eel ready to enter migration
> also rank how fast it moves after migration is active?**

The project began from an extreme Azores yellow-eel system with strong pool
fidelity and no valid receiver-to-receiver movement, but the current paper is a
Europe-wide phase-transferability analysis.

The main result is now **multivariate**, not Durif-only.

An activation model using the public six-project FIII–FV cohort found independent
capture-state information in:

- ordinal Durif stage: OR **2.13 per stage** (95% CI **1.60–2.84**);
- weight-for-length condition: OR **1.46 per SD** (95% CI **1.16–1.83**).

Using those activation coefficients only, the frozen entry-state score is:

```
entry-state score
  = 0.756 × ordinal Durif
  + 0.379 × capture condition
```

Per 1 SD of that score:

- migration activation OR = **2.23** (95% CI **1.70–2.92**);
- behavioral-onset HR = **1.32** (95% CI **1.17–1.49**; **418** events);
- post-activation whole-route speed ratio = **0.946**
  (95% CI **0.832–1.076**; partial R² **0.18%**);
- frozen median positive inter-station speed ratio = **1.028**
  (95% CI **0.869–1.215**; partial R² **0.026%**).

With score weights trained while withholding each project in turn, the same
boundary persists: activation OR **1.97**, onset HR **1.26**, whole-route speed
ratio **0.948**, and frozen inter-station speed ratio **1.013**. Predictor
preprocessing remains panel-derived, so this is cross-project robustness rather
than prospective external validation.

Within identical directed receiver links, the boundary is even sharper. A
frozen project-held-out score audit over **18,012** positive segments from
**426** eels and **248** route links gives a speed ratio of **0.995/SD**
(95% CI **0.912–1.087**, p=**0.918**; weighted partial R² **0.00052%**).
The source segment-speed field contains grossly implausible values, but
explicitly post-hoc external-plausibility screens at 2.5, 5 and 10 m/s leave
the ratio at **0.976–0.979**, with all intervals spanning one. These screens
remove **52.5–62.5%** of candidate rows, so absolute source segment speeds
must not be interpreted as direct swimming physiology.

Thus the canonical V4 statement is:

> **the multivariate capture phenotype that predicts migratory commitment is an
> entry-state indicator, not a transferable general progression-speed score.**

Durif alone shows the same boundary: activation OR **2.08**, onset HR **1.29**,
but post-activation whole-route speed ratio **0.983** and frozen segment-speed
ratio **1.001**.

## Independent Dutch falsification

The full DANS archive associated with van Rijn et al. (2026) was materialized
and its event schema audited. Source passage validity is partly defined from
event duration, so the V4 mechanism test reconstructs risk sets independently:

```
SewerArrival <= Firstquarter <= PassageTime
```

without using event duration or the source `valid` flag for inclusion.

Informative strict-start choice sets:
- EZ pumping station: **14 fish** (FIII 2; FIV/FV 12);
- CL tidal sluice: **15 fish** (FIII 4; FIV/FV 11).

The proposed mechanism — better-conditioned eels preferentially waiting for
longer passage windows after barrier arrival — was **not supported**.

- CL condition × duration: β **−0.095**, p **0.841**,
  permutation p **0.849**.
- EZ conditional choice was near-separated/non-converged and opposite the
  preregistered positive prediction; it is not interpreted biologically.
- Arrival-defined waiting was null at both barriers:
  - EZ condition vs missed events r **0.009**, p **0.960**;
  - CL r **−0.104**, p **0.592**.

The Dutch extension is therefore a useful **falsification**, not positive
confirmation of an internal-to-external control handoff.

## Important endpoint boundary

The upstream terminal/sea-positive set remains a secondary sensitivity only.
Its complement is not validated biological failure, and this project does not
estimate escapement probability.

**Within-link correction notice (2026-10-08):** The first within-link result inadvertently included nine fixed expert-classified 2015 non-migrants. Its 18,012-segment / 426-fish estimates and dependent speed-quality sensitivities are provisional until the corrected analysis and numerical audit pass. See [correction ledger](docs/WITHIN_LINK_CORRECTION_LEDGER_2026_10_08.md).

## Canonical V4 artifacts

- [submission manuscript V4](manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md)
- [V4 numeric contract](manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V4.json)
- [V4 QC PASS](manuscript/MANUSCRIPT_QC_V4.json)
- [V4 claim-evidence map](docs/CLAIM_EVIDENCE_MAP_PHASE_CONTROL_V3.md)
- [activation-trained entry-state result](results/entry_state_score_transferability_v1.json)
- [cross-project entry-state robustness](results/cross_project_entry_state_score_v1.json)
- [within-link entry-state speed result](results/within_link_entry_state_speed_v1.json)
- [within-link speed-quality sensitivity](results/within_link_speed_quality_sensitivity_v1.json)
- [canonical stage-only benchmark](results/phase_control_canonical_v2.json)
- [Dutch condition-choice falsification](results/dutch_condition_choice_test_v1.json)
- [Dutch arrival-defined waiting falsification](results/dutch_arrival_waiting_diagnostic_v1.json)
- [condition-specific activation-selection IPW](results/body_condition_activation_selection_ipw_v1.json)

## Stage-only benchmark and scale boundary

The canonical stage-only post-activation speed endpoint reproduces exactly:
**n=418**, Durif-stage speed ratio **0.9831088159**
(95% CI **0.8524016–1.1338586**).

Project-specific stage effects do not show supported heterogeneity
(**Q=2.47, df=5, p=0.781**), and the frozen median positive inter-station
endpoint is likewise near null (**1.001**, 95% CI **0.831–1.204**).

A 2026 River Test study is retained as an external scope boundary showing that
silvering stage can still contribute at a finer reach scale. The V4 conclusion
is therefore about **transferability across generic progression summaries**,
not disappearance of all internal-state effects after activation.

## Post-activation project heterogeneity audit

The pooled near-null Durif effect on post-activation speed is not explained by obvious cancellation of strong opposing project effects.

Using the same speed definition and covariate structure within each of the six projects, stage-specific speed ratios ranged from approximately **0.915 to 1.272**. A Cochran heterogeneity audit gave **Q = 2.47**, **df = 5**, **p = 0.781**.

Thus the current data do not support a strong Durif-stage × water-body interaction in overall migration speed.

The supported interpretation is narrower:

> **silvering readiness has a strong general predictive signal for activation/onset, whereas its general predictive signal for already-active overall migration speed is weak.**

This does not imply that internal state becomes biologically irrelevant after activation, and it does not demonstrate that route opportunity causally replaces internal control. A recent River Test study uses a different reach-level progression endpoint and shows that silvering stage can still contribute within a particular route context.

See [post-activation project heterogeneity audit](docs/post_activation_speed_project_heterogeneity.md).

## Evidence boundary

These are developmental independent results, not outcome-blind confirmation.

Durif stages already encode migratory readiness, so the initiation association is biologically expected and is not novelty by itself. The stronger contribution is the **cross-phase transferability test** showing that an activation-trained multivariate capture-state score predicts activation and onset but carries almost no general information about the two generic post-activation speed summaries.

## Role of EOG

EOG is only the discovery route. It exposed temporal structure in a system with no observed receiver-to-receiver propagation, motivating the question of when latent mobility is actually expressed and what controls movement after activation.

## Three separate EOG-derived ecology programmes

Azores is one of three independent ecological projects:

- **Azores:** state-dependent mobility gating;
- **Louisiana:** within-home-range micro-niche tracking;
- **Tampa:** buffered persistence under quantitative degradation.

These are not intended as one umbrella analysis or one shared endpoint.

See [three independent ecology programmes](docs/three_ecology_programs.md).


- [three-programme current status](docs/three_ecology_programs_status.md)


## Legacy V2 submission figures

The endpoint-audited V2 reference renders remain committed for provenance, but they predate the V4 multivariate entry-state framing and are **not yet the canonical V4 figure set**:

- `manuscript/rendered_figures_v2/Figure1.svg`
- `manuscript/rendered_figures_v2/Figure2.svg`
- `manuscript/rendered_figures_v2/Figure3.svg`
- `manuscript/rendered_figures_v2/Figure4.svg`

Render QC:
- `manuscript/RENDERED_FIGURE_QC_V2.json` — **PASS_REFERENCE_RENDER**

V2 numeric content remains locked to `FIGURE_DATA_CONTRACT_V2.json`; terminal positive-set sensitivity remains supplementary only. A V4 figure contract should center the activation-trained entry-state transferability result rather than reuse V2 unchanged.
