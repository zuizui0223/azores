# Which silvering class carries the apparent extra condition signal?

**Evidence:** exact post-hoc frozen-score label-sensitivity audit; [GitHub Actions run 37768129651](https://github.com/zuizui0223/azores/actions/runs/37768129651) passed synthetic exhaustive rank-pair tests, pinned source analysis, and artifact upload.

Canonical results:
- `results/stage_stratified_hidden_start_tipping_v1.json`
- `results/observability_label_ambiguity_tipping_v1.json`
- `results/stage_specific_condition_gate_v1.json`
- `analysis/51_stage_stratified_hidden_start_tipping.py`

## Distinguish three ecological questions

1. **What stage does the source classify as starting migration?** Original 575-eel panel: FIII 154/261; FIV 53/68; FV 215/246. This is telemetry classifier output, not latent physiology.
2. **Does capture condition add prediction beyond the ordinal stage?** Across six held-out projects, the added condition score improves within-project-year AUC by +0.03356, though six-project uncertainty includes zero.
3. **Where can missed migration classification hypothetically break that incremental prediction?** This analysis answers only this third question, with fixed scores and original source labels except a restricted set of short-followup negatives.

## Exact stage-restricted tipping result

| Allowed hypothetical relabelings | Short-followup candidates | First number that can erase +0.03356 | Most adverse gain if exactly 11 changed | Gain if all stage candidates changed |
|---|---:|---:|---:|---:|
| FIII only | 70 | **16** | +0.00640 | +0.06220 |
| FIV only | 13 | **None** | +0.02497 | +0.02757 |
| FV only | 17 | **None** | +0.02115 | +0.02795 |
| Any of the three stages | 100 | **11** | ≤0 | +0.06833 (all 100, from earlier audit) |

The original adversarial 11-label witness consists of **8 FIII, 2 FIV and 1 FV** source-negative fish; within that particular worst-case set, 8 belong to the 2011 Warnow project. This is neither a random sample of negative labels nor an observed distribution of missed starts.

An FIII-only witness reaching a nonpositive increment at 16 includes **8 Warnow, 2 Leopoldkanaal, 2 Verhelst and 4 ESGL** hypothetical changes. Crucially, **changing all 70 FIII labels restores a positive increment**: as positive/negative pair sets change, the AUC increment is not monotone in the number of hypothetical unobserved initiators.

## Biological meaning and why FIII does not automatically become a mechanism

This is an exact mathematical diagnostic of an **observation-dependent prediction claim**, not evidence that 16 FIII eels truly started unseen. FIII contributes **70 of the 100** candidate short-followup negatives, giving it greater capacity to perturb the cross-stage AUC comparison; this quantity alone cannot establish preferential FIII detection failure.

The data remain compatible with several processes:
- true individual heterogeneity in readiness within the premigrant FIII class;
- project-specific migration cues and receiver exposure;
- body-size, age, sex or silvering-score measurement dependence;
- missing onset labels caused by observation geometry, survival or tag loss.

No data in this test isolate any of these possibilities.

## Falsifiable field and analysis extension

Record full receiver-array deployment/recovery histories and fish-specific observation windows, then test whether independent downstream confirmations show a stage-dependent missed-onset rate. Link these to continuous morphometrics, body state, environmental windows and physical passage outcomes.

The decisive comparison is **FIII versus FV true-start misclassification**, not FIII versus FV performance on the original algorithmic label. Until independently measured, sample-level stage gradients and body-condition AUC should not be called verified biological readiness or increased escapement.

## Relationship to the partial-identification result

The pooled FV>FIII source-classified initiation rate remains positive even if all 70 *short-followup* FIII negatives were hidden starts, conditional on freezing 53 longer-observed negatives. Yet the weaker **+0.03356 continuous-condition AUC gain** can be eliminated by choosing just 16 shortfollowup FIII negatives. These are distinct estimands: **marginal stage ordering versus predictive rank information within and across stages**. They need not have identical sensitivity to missing observations.

The apparent pooled stage-order robustness does not carry to the population: [dual uncertainty diagnostic](results/stage_order_dual_uncertainty_v1.json) yields lower-bound-endpoint percentile spans crossing zero under both individual and project resampling.
