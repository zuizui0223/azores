# Does release timing gate the condition–migration-start association?

## Audit status

**NO_GENERAL_HELDOUT_SEASONAL_CONDITION_INTERACTION_SUPPORT**

- Source: `results/seasonal_condition_interaction_v1.json`
- Frozen before outcome: `analysis/contracts/seasonal_condition_interaction_v1.json`
- Reproducible code: `analysis/41_seasonal_condition_interaction.py`
- GitHub Actions run: [37752917073](https://github.com/zuizui0223/azores/actions/runs/37752917073) **PASS**, including syntax and three synthetic unit tests.

This is an **exploratory** test after the preceding body-condition and stage analyses, not a prespecified test from the original study.

## Scientific question

If apparently similar silver eels differ in their readiness for migration, one explanation is an interaction between body state and seasonal opportunity. The only available timing proxy in the frozen panel, however, is **tagging/release date relative to each project-year**, not actual river discharge, opening events, water temperature or lunar phase.

## Outcome-blind external-project prediction

For each of the six source projects:

1. Fit ordinal Durif stage + body length + centered release date + centered weight-for-length condition on the other five projects;
2. add a single condition × centered release-day interaction to the extended model;
3. score the completely held-out project without training on its migration outcomes;
4. measure AUC using within-project-year initiator–noninitiator pairs only.

The project-year within-sample AUC benchmark is identical to the previous frozen incremental-condition result; no redefinition of the source cohort.

| Test | Additive condition model | Condition × release-timing model | Difference |
|---|---:|---:|---:|
| 575 eels, 6 projects, 6,914 initiator–noninitiator pairs | **0.64333** | **0.64232** | **−0.00101** |

The 10,000-resample project-bootstrap 95% interval is **−0.02736 to +0.01061**, including zero. Among six held-out projects, four had tiny positive increments, one had a negative increment (Leopoldkanaal −0.03709) and one was exactly unchanged. Dropping Leopoldkanaal alone changes the pooled increment to +0.00861, illustrating the lack of stability. The exploratory 64-sign exact project permutation gives two-sided p = **1.0**.

Interaction coefficient estimates were negative in all six overlapping training folds (range −0.928 to −0.324); those folds reuse most training projects and are **not six independent replications**. Importantly, the consistently signed fitted interaction did **not** translate to increased held-out discrimination.

## Early/late release date split is descriptive only

Grouping each project-year's tagged animals on either side of its median release date (127 exact median ties dropped):

- earlier-release subset: AUC increment **+0.02245** over 1,247 comparable pairs;
- later-release subset: increment **−0.02937** over 1,362 pairs.

The opposite signs can be compatible with overfitting a timing interaction and cannot prove environmental cue gating, since release day can reflect sampling design rather than cue exposure.

## Biological interpretation

The **simple cross-project condition × release-date interaction does not explain the stage-specific or river-specific AUC heterogeneity**.

This narrows, rather than rejects, the broader biological possibilities:
- measured stage and condition may interact with **actual hydrological or thermal triggers**, not tagging dates;
- project-specific receiver geometry and detection opportunity can modify classified onset;
- sex/age and silvering measurement dependence may vary among projects.

A more direct follow-up should assess **detection-follow-up duration** before treating algorithmically classified noninitiators as genuinely inactive, then only investigate hydrological cue interactions if suitable event-matched discharge/tide data can be sourced. Do not infer a causal ecological season gate, migration success, mortality, or improved conservation from the present AUC.
