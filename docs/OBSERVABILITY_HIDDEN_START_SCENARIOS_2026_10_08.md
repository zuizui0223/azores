# Adversarial versus non-adversarial hidden migration starts — 2026-10-08

**Evidence class: post-hoc scenario analysis, not an estimated detection error rate.**

Canonical source: `results/observability_random_hidden_start_sensitivity_v1.json`. GitHub Actions run [37764416827](https://github.com/zuizui0223/azores/actions/runs/37764416827) and exhaustive synthetic formula test both **PASS**.

## Ecological question

The six-project eel panel has **575** animals, of whom **422** were classified as initiators and **153** were not. **100 of the 153 source noninitiators** lack 90-day receiver-follow-up support. Distinguishing biological failure to depart from an unobserved downstream departure is therefore a real measurement problem.

An exact adversarial sensitivity established that a carefully chosen set of **11 of these 100 source negatives** is sufficient to erase the extra initiation-ranking AUC from the weight-for-length condition score (+0.03356 at the source labels; exact worst-case 11-label AUC increment −0.00016). That bound is an *existence result*, not a claim that 11 missed starts occurred.

We now ask how representative the 11-label adversarial result is under **explicit hypothetical label assignment assumptions**.

## Locked scenario definitions

Holding both six-fold project-held-out activation scores frozen, change exactly k of the 100 questionable labels from negative to positive, without changing the 53 90-day-observed negatives or the 422 source positives. Recompute the positive–negative pair-weighted AUC increment **including the altered number of comparison pairs within every project-year stratum**. 10,000 conditional random subsets per budget/scenario; 0 and 100 are deterministic.

Scenarios:
- **Uniform:** all 100 short-follow-up source negatives have equal chance of being chosen for hypothetical relabeling; this is a neutral *assignment reference*, not missing-at-random inferred from tracking.
- **FV enriched:** FV individuals are three times as likely to be selected as FIII/FIV. The multiplier is illustrative, not empirically fitted.
- **Rank-disagreement enriched:** individuals whose relabeling most harms the condition-versus-base AUC gain (lowest third of the exact per-fish impact) have triple the selection weight. This intentionally makes a score-related missing-not-at-random scenario; it does **not** establish that biological behavior or telemetry observability follows model disagreement.

## Verified conditional distributions

| Hypothetical flipped labels (k) | Uniform median gain | FV-enriched median gain | Rank-disagreement-enriched median gain | Rank-disagreement: fraction with gain ≤0 |
|---|---:|---:|---:|---:|
| 0 | +0.03356 | +0.03356 | +0.03356 | 0 |
| 11 | +0.03374 | +0.03277 | +0.02623 | 0 / 10,000 |
| 20 | +0.03411 | +0.03243 | +0.02080 | 0.0006 |
| 30 | +0.03471 | +0.03267 | +0.01505 | 0.0325 |
| 50 | +0.03776 | +0.03482 | +0.00758 | 0.2330 |
| 75 | +0.04542 | +0.04263 | +0.01281 | 0.1018 |
| 100 | +0.06833 | +0.06833 | +0.06833 | 0 |

At **k=11**, the empirical 2.5–97.5% assignment ranges were:
- uniform: **+0.02309 to +0.04463**;
- FV-enriched: **+0.02268 to +0.04339**;
- rank-disagreement-enriched: **+0.01578 to +0.03738**.

None of 10,000 draws at k=11 yielded a nonpositive AUC gain in any tested scenario. This establishes only that such a combination was not sampled under the specified allocation models; it does **not** estimate a real probability of model failure.

At **k=30**, model-disagreement enrichment gave 3.25% nonpositive draws, versus 0/10,000 under uniform or FV-enriched allocations. At **k=50**, the corresponding values were 23.30%, 0.02% and 0.05%.

Crucially, **the AUC response is not monotone in k**: even if all 100 short-follow-up negatives were hypothetically moved to the positive class, the frozen-score AUC increment would be **+0.06833**. Changing the labels also changes which positive–negative pairs exist; *how* detection failures map onto project, stage and score disagreement matters much more than a single missing-label count.

## Ecological interpretation and current hard limit

The data support an **observability-vulnerable apparent entry-state association**, not an estimate of hidden initiation prevalence or evidence that eels with lower condition actually move unseen. This sensitivity also cannot establish a specific stage-dependent energetic checkpoint or transfer to post-activation speed.

The next substantive observational requirement is **effort data**: time-varying receiver operation, coverage at each downstream barrier, tag detection/retention, hydrology and independent verification of ambiguous animals. These would allow estimates of detection conditional on actual movement and stage/condition, rather than assigning hypothetical labels arbitrarily.

For conservation, count separately:
1. silver eel cohort production and silvering morphology;
2. telemetry-verified initiation *conditional on adequate observation*;
3. exposure to barriers and successful downstream passage;
4. actual escapement/survival.

Treating non-detection as nonmigration or using a movement-speed score as a surrogate for escapement can misallocate intervention priority. The current panel cannot estimate how many of the 100 actually initiated, and neither simulation should be used to do so.

## Frozen-scope rules

- Preserve the original source labels and six-fold training weights in every principal result.
- All scenario distributions are post-hoc, uncalibrated sensitivity analyses and are not project-level inferential confidence intervals.
- The model-disagreement-enriched draw deliberately refers to the score itself; do not misstate it as a biological observation model.
- The exact 11-label tipping remains valid as a mathematical lower bound on worst-case assignment, not as a typical case.
