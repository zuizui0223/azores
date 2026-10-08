# Within-link audit correction ledger — 2026-10-08

## Status
**CORRECTION_VERIFIED_AND_SUPERSEDED_RESULTS_REPLACED**

## Discovered issue

The first within-link speed audit (`analysis/33_within_link_entry_state_speed.py`) reconstructed positive `migration == TRUE` source rows but did not apply the **nine fixed expert-classified 2015 non-migrants**. Those individuals were excluded from the canonical activation and post-activation analyses before this audit was designed.

The first within-link run reported **431 raw candidate fish**, exactly **422 canonical expert-corrected initiators + 9 expert non-migrants**. Therefore the previous main-result values:
- 18,012 segment rows;
- 426 fish;
- 248 directed pairs;
- speed ratio 0.995/SD;
and all within-link quality-screen coefficients calculated from that same candidate set are **superseded** as canonical cohort results; they remain in commit history solely for provenance.

This is a cohort-consistency implementation error, not grounds to change the scientific eligibility rule.

## Repairs

- `analysis/33_within_link_entry_state_speed.py` now excludes every tag in `B.EXPERT_NON` before processing movement segments.
- A fail-closed assertion tests that no excluded fish appears in the output.
- The frozen contract now explicitly references the pre-existing expert correction.
- `analysis/34_within_link_speed_quality_sensitivity.py` reads the *same-run corrected primary* when invoked from CI.
- Syntax and QC variable errors introduced in the repair have been corrected.

## Corrected verification — GitHub Actions run 37706923860

The correction passed all required checks.

- Candidate migration universe: **422** eels; excluded expert-non-migrant segment rows: **0**.
- Exact-link primary after five-fish-per-pair support: **17,792** segment rows, **418** eels, **244** directed links.
- Entry-state score ratio: **0.961625** per SD, 95% CI **0.882525–1.047814**, p=**0.371581**.
- Weighted partial R²: **0.0382%**.
- Pair-support sensitivities: >=3 fish ratio **0.9562**; >=10 fish ratio **0.9985**; leave-one-project-out **0.9334–1.0126**.
- Upper speed screens 2.5/5/10 m s⁻¹: ratios **0.9421/0.9437/0.9411**; candidate rows removed **63.1/58.6/53.0%**. All 95% intervals span 1; p≈0.07–0.08.
- FWL numerical check: **PASS**. Corrected beta discrepancy below **4×10⁻14** and clustered-SE discrepancy below **4×10⁻7**.

The corrected primary, quality and FWL results are committed at:
- `results/within_link_entry_state_speed_v1.json`;
- `results/within_link_speed_quality_sensitivity_v1.json`;
- `results/within_link_fwl_numerical_audit_v1.json`.

The original near-null interpretation remains, but the earlier **0.995** estimate is not the corrected primary. The corrected estimate **0.962** with CI spanning 1 is not evidence that the association is precisely zero.

## Historical verification checklist (completed)

The new run must report:
1. zero expert-non-migrant segment rows;
2. corrected fish, pair and segment counts;
3. corrected primary coefficient and uncertainty;
4. 2.5/5/10 m/s quality sensitivities on the exact corrected population;
5. FWL numerical-equivalence status for the high-dimensional fixed effects.

All are checked. The old coefficients remain superseded; use the corrected results above.

## Scope of the correction

The 9-fish error affects only the **new within-link speed audit** and its dependent quality screens. It does **not** retroactively reclassify the previously frozen canonical stage analyses or the project-held-out entry-state score. Those upstream programmes already applied the expert judgement rule.

Historical commits preserve the original result files for provenance. A corrected result should be written back to the canonical result paths only after successful, inspectable re-execution.
