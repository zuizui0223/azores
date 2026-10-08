# Within-link audit correction ledger — 2026-10-08

## Status
**SUPERSEDED_WITHIN_LINK_PRIMARY_PENDING_CORRECTED_REBUILD**

## Discovered issue

The first within-link speed audit (`analysis/33_within_link_entry_state_speed.py`) reconstructed positive `migration == TRUE` source rows but did not apply the **nine fixed expert-classified 2015 non-migrants**. Those individuals were excluded from the canonical activation and post-activation analyses before this audit was designed.

The first within-link run reported **431 raw candidate fish**, exactly **422 canonical expert-corrected initiators + 9 expert non-migrants**. Therefore the previous main-result values:
- 18,012 segment rows;
- 426 fish;
- 248 directed pairs;
- speed ratio 0.995/SD;
and all within-link quality-screen coefficients calculated from that same candidate set are **provisionally invalid** as canonical cohort results.

This is a cohort-consistency implementation error, not grounds to change the scientific eligibility rule.

## Repairs

- `analysis/33_within_link_entry_state_speed.py` now excludes every tag in `B.EXPERT_NON` before processing movement segments.
- A fail-closed assertion tests that no excluded fish appears in the output.
- The frozen contract now explicitly references the pre-existing expert correction.
- `analysis/34_within_link_speed_quality_sensitivity.py` reads the *same-run corrected primary* when invoked from CI.
- Syntax and QC variable errors introduced in the repair have been corrected.

## Pending verification

The new run must report:
1. zero expert-non-migrant segment rows;
2. corrected fish, pair and segment counts;
3. corrected primary coefficient and uncertainty;
4. 2.5/5/10 m/s quality sensitivities on the exact corrected population;
5. FWL numerical-equivalence status for the high-dimensional fixed effects.

Until all are checked, do not use the old within-link coefficients as final manuscript evidence.

## Scope of the correction

The 9-fish error affects only the **new within-link speed audit** and its dependent quality screens. It does **not** retroactively reclassify the previously frozen canonical stage analyses or the project-held-out entry-state score. Those upstream programmes already applied the expert judgement rule.

Historical commits preserve the original result files for provenance. A corrected result should be written back to the canonical result paths only after successful, inspectable re-execution.
