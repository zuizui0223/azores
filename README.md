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

**Incremental information beyond Durif (2026-10-08).** In six project-held-out activation-ranking folds (575 eels), adding a continuous weight-for-length residual to Durif, length and release timing improved within-project-year AUC from **0.610 to 0.643** (Δ **+0.0336**, 6,914 initiator/non-initiator pairs). This increment was positive in **4/6 projects**; a six-project cluster bootstrap 95% interval (**−0.0007 to +0.0918**) crosses zero and an exploratory exact project sign-flip gave two-sided **p=0.1875**. At identical Durif stage, ranking AUC rose from **0.480 to 0.555**. This suggests condition can supply stage-within readiness information in some contexts, not that the gain generalizes to every new river. This is developmental public-data evidence, not prospective validation or an estimate of eel escape success.

See [held-out activation AUC result](results/cross_project_condition_increment_v1.json), [project-heterogeneity audit](results/cross_project_condition_increment_project_robustness_v1.json) and [V4 numerical contract](manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V4.json).

**Morphology-controlled test (2026-10-08):** The pinned archive retains horizontal/vertical eye diameter and pectoral-fin length for five focal projects (typed `length2/3/4`, ordered differently among projects). Among **429** morph-complete evaluable fish, four project-held-out nested models yielded within-project-year AUC: baseline stage/length/date **0.706**, +continuous eye/fin **0.716**, +condition alone **0.741**, +both **0.741**. Condition after morphology gained **+0.0244 AUC**, with a five-project bootstrap 95% interval **−0.0151 to +0.0659** (positive in 3/5 projects); morphology after condition gained only **+0.0003**. This does **not** establish independent energetic physiology or stable prediction across rivers. A [post-hoc ridge-penalty sensitivity](results/continuous_morphology_penalty_sensitivity_v1.json) with penalties 0.1, 1 and 10 yielded gains **+0.0269 / +0.0244 / +0.0214**; all five-project uncertainty intervals include zero.

See [morphology-conditioned results](results/continuous_morphology_condition_increment_v1.json), [method](analysis/39_continuous_morphology_condition_increment.py) and [measurement correction](docs/ENTRY_STATE_MEASUREMENT_DEPENDENCE_AUDIT_2026_10_08.md).

**Exploratory follow-up:** Is condition information concentrated within FIII, FIV or FV silvering classes? The [frozen stage-specific test](analysis/contracts/stage_specific_condition_gate_v1.json), [analysis script](analysis/37_stage_specific_condition_gate.py), [CI workflow](.github/workflows/stage-specific-condition-gate.yml) and [competing ecological hypotheses](docs/STAGE_CONDITION_GATE_HYPOTHESES_2026_10_08.md) are available. The stage-specific CI and project-year matched checks have now passed. Descriptively FV shows a stronger increment than FIII in the full panel, but only four projects have shared support, the project-level exact sign-flip gives p=0.25, and a within-project year can reverse direction. These results remain exploratory, not a proven terminal energetic gate; see [interpretation ledger](docs/STAGE_CONDITION_GATE_INTERPRETATION_2026_10_08.md).

A supplementary, explicitly conditional allocation audit (rather than the worst-case bound) found that when **11** of the 100 short-follow-up negative labels are chosen uniformly, none of 10,000 simulated assignments erased the held-out condition AUC gain (median **+0.0337**); an illustrative 3:1 score-disagreement-enriched assignment also had no such losses at k=11 (median **+0.0262**). At k=50 that biased scenario erased the gain in **23.3%** of draws. These are uncalibrated WHAT-IF label distributions, not empirical estimates of hidden migration or detection error. Notably flipping all 100 labels gives **+0.0683**: AUC responses depend on project-year pair composition and **which** animals are relabeled, not just the number. See [scenario results](results/observability_random_hidden_start_sensitivity_v1.json) and [interpretation](docs/OBSERVABILITY_HIDDEN_START_SCENARIOS_2026_10_08.md).

**Physical-receiver observability audit (2026-10-08).** The original source's 100 short-follow-up noninitiators are not a homogeneous nondetection class. **24** have only synthetic release rows and **76** have actual receiver contact. For **70 of those 76**, the same last-contact receiver detected another tagged fish later within 90 days (58 within one day), demonstrating receiver activity at that later point, **not** continuous operation or focal eel residence. Crucially, the exact 11-fish worst-case hypothetical label reassignment included **9 already receiver-detected fish**. Restricting hypothetical label changes to the 24 virtual-only records **cannot** eliminate the added condition AUC even when all 24 are flipped; restricting to the 76 actually detected records requires **13** strategically chosen flips. These are sensitivity bounds, not observed missed departures or estimates of tag/receiver failure. [Receiver inventory](results/receiver_witness_observability_v1.json) · [Receiver-constrained exact bound](results/receiver_stratified_label_tipping_v1.json) · [Interpretation](docs/RECEIVER_EVIDENCE_OBSERVABILITY_2026_10_08.md).

**Stage-specific observation fragility (2026-10-08).** An exact worst-case, frozen-score audit now isolates hypothetical unseen initiation by silvering stage. Reassigning carefully chosen short-followup source-negative labels in **FIII alone** erases the pooled condition AUC increment at **16/70** possible candidates, while **FIV alone (13)** or **FV alone (17)** cannot erase it even if all candidates are changed. The unrestricted 11-label witness consists of **8 FIII, 2 FIV and 1 FV**. These are hypothetical label configurations, not detected missed departures or an inferred FIII-specific physiology; notably all 70 FIII labels changed yields AUC gain +0.0622, not zero. [Exact result](results/stage_stratified_hidden_start_tipping_v1.json) · [Calculation](analysis/51_stage_stratified_hidden_start_tipping.py) · [Passing workflow](https://github.com/zuizui0223/azores/actions/runs/37768129651).

**Finite sample versus population uncertainty (2026-10-08).** The conditional pooled FV–FIII sharp lower bound is +1.57 percentage points for the observed 575 tagged fish. That does *not* guarantee population-wide silvering order: exploratory resampling of fish within the six project × stage samples gives a 95% percentile span of the **lower bound endpoint** from **−3.91 to +6.87 points**, while resampling the six project contexts gives **−16.65 to +17.96 points**. These are descriptive bound-endpoint stability diagnostics, not confidence intervals for true migration or causal effects. [Frozen result](results/stage_order_dual_uncertainty_v1.json) · [Interpretation](docs/STAGE_ORDER_SAMPLING_IDENTIFICATION_2026_10_08.md).

**Sharp silvering-stage observability bounds (2026-10-08).** Treating the **100** short-follow-up source-negative labels (and *only* those) as possible hidden initiators gives conditional source-initiation intervals **FIII 59.0–85.8%**, **FIV 77.9–97.1%**, and **FV 87.4–94.3%**. Thus the **pooled** FV−FIII ordering remains strictly positive (bound **+1.57 to +35.31 percentage points**) even if all 70 short-followup FIII negatives were hidden initiators. But there is **no universal river-level ordering**: only **2/6** projects have a strictly positive FV−FIII bound, **1/6 has a strictly negative bound**, and the equal-project mean range is **−6.84 to +38.67 points**. More importantly, allowing just **five additional hidden starts among 37 longer-observed FIII negatives** can erase even the pooled ordering. These are mathematical what-if bounds, not inferred missed movements, receiver uptime or escapement. [Canonical bounds](results/stage_entry_observability_bounds_v1.json) · [interpretation](docs/STAGE_ENTRY_PARTIAL_IDENTIFICATION_2026_10_08.md) · [reproducible test](analysis/50_stage_entry_observability_bounds.py).

**Observability-label sensitivity (2026-10-08).** An exact, post-hoc worst-case sensitivity allowed hypothetical hidden migration starts **only among the 100 source noninitiators without 90-day receiver follow-up**. Holding both held-out score models frozen, the original +0.0336 incremental condition AUC can be reduced to near zero if **11** carefully selected source negatives were actually unobserved initiators (minimum ΔAUC **−0.00016**). Ten flips still have a positive minimum **+0.00191**. This is **not an estimated misclassification rate or proof that eleven starts occurred**; it limits how strongly the added condition ranking can be interpreted as physiological readiness. See [source and interpretation ledger](docs/OBSERVATION_GATE_2026_10_08.md), [validated exact bound](results/observability_label_ambiguity_tipping_v1.json) and [passing CI](https://github.com/zuizui0223/azores/actions/runs/37763360099).

**Temporal participation versus onset-order test (2026-10-08).** The same project-held-out activation-trained scores were tested against different observed horizons in the **same 475 eels**: condition added **+0.0077 / +0.0329 / +0.0460 / +0.0549 / +0.0807 AUC** for onset by 7/30/60/90 days and eventually classified activation, respectively. The 30-day versus eventual contrast was positive in four informative projects (mean paired difference **+0.0431**; bootstrap CI **+0.0164 to +0.0697**, exact two-sided sign flip **p=0.125**). **Early-versus-late order among initiators did not show similar additional information.** Among **422 classified initiators**, condition changed onset-order concordance only **0.5446 → 0.5461** (**+0.0015**, project-bootstrap 95% CI **−0.0237 to +0.0202**); excluding onset within 24 hours gave **−0.0086**. These are exploratory descriptive results affected by incomplete receiver observation and selection on entry, **not** physiological timing or escapement estimates.

Evidence: [common-fish frozen-score comparison](results/paired_temporal_endpoint_condition_v1.json), [entrant-only onset-order audit](results/entrant_onset_latency_discrimination_v1.json), [separate fixed-follow-up sensitivity](results/fixed_followup_condition_increment_v1.json), [seasonal timing interaction negative control](results/seasonal_condition_interaction_v1.json), and [ecological interpretation ledger](docs/TEMPORAL_ACTIVATION_ENDPOINT_AUDIT_2026_10_08.md).

Within identical directed receiver links, the boundary is even sharper. A
frozen project-held-out score audit over **17,792** positive segments from
**418** eels and **244** route links gives a speed ratio of **0.962/SD**
(95% CI **0.883–1.048**, p=**0.372**; weighted partial R² **0.0382%**).
The source segment-speed field contains grossly implausible values, but
explicitly post-hoc external-plausibility screens at 2.5, 5 and 10 m/s leave
the ratio at **0.941–0.944**, with all intervals spanning one. These screens
remove **53.0–63.1%** of candidate rows, so absolute source segment speeds
must not be interpreted as direct swimming physiology. The filtered estimates are weakly negative (p≈0.07–0.08), not proof of zero or negative effect.

Thus the canonical V4 statement is:

> **the multivariate capture phenotype that predicts migratory commitment is an
> entry-state indicator, not a transferable general progression-speed score.**

Durif alone shows the same boundary: activation OR **2.08**, onset HR **1.29**,
but post-activation whole-route speed ratio **0.983** and frozen segment-speed
ratio **1.001**.

## Observation-gated temporal result (2026-10-08)

The matched temporal follow-up analysis has a **critical sampling explanation**. Selecting fish eligible for a 90-day horizon keeps **all 422 source-classified migrators** but only **53 of 153 source noninitiators**, excluding 100 with inadequate post-release final receiver arrival. For the exact *same eventual-initiation* label and frozen held-out score weights, the condition AUC increment changes **+0.0336 (575 fish) → +0.0807 (475 fish)**.

An exact algebraic decomposition shows the **+0.0471** gain shift comprises **+0.0515 from reweighting river-specific comparison pairs** and **−0.0044 from changes within projects**. A 20,000-replicate project-year-matched random negative-retention test gave mean **+0.0844** (95% interval **+0.0606–+0.1083**) and observed **+0.0807**, an unexceptional result (two-sided **p=0.764**). In other words, the inflated AUC **does not constitute evidence that physiological readiness gains predictive importance with time**.

[Validated selection audit](results/observability_selection_gate_v1.json) · [exact project-composition identity](results/observability_project_composition_v1.json) · [interpretation and conservation boundary](docs/OBSERVATION_GATE_2026_10_08.md)

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

**Within-link correction completed (2026-10-08):** The initial within-link implementation incorrectly retained nine expert-classified non-migrants. The corrected analysis now uses 422 eligible candidate migratory eels (418 after directed-link support filtering) and passes independent FWL numerical equivalence. The earlier 18,012-segment / 426-fish result is superseded. See [correction ledger](docs/WITHIN_LINK_CORRECTION_LEDGER_2026_10_08.md).

## Canonical V4 artifacts

- [submission manuscript V4](manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md)
- [V4 numeric contract](manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V4.json)
- [V4 QC PASS](manuscript/MANUSCRIPT_QC_V4.json)
- [V4 claim-evidence map](docs/CLAIM_EVIDENCE_MAP_PHASE_CONTROL_V3.md)
- [activation-trained entry-state result](results/entry_state_score_transferability_v1.json)
- [cross-project entry-state robustness](results/cross_project_entry_state_score_v1.json)
- [within-link entry-state speed result](results/within_link_entry_state_speed_v1.json)
- [within-link speed-quality sensitivity](results/within_link_speed_quality_sensitivity_v1.json)
- [within-link FWL numerical audit](results/within_link_fwl_numerical_audit_v1.json)
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
