# Post-activation speed reproducibility and novelty audit — 2026-10-05

## Resolution of the reproducibility check

The initial audit incorrectly interpreted empty content returned by the GitHub file-content connector for three very large CSVs as empty repository files.

That interpretation was wrong.

The files have non-empty Git blob SHAs and can be retrieved directly by blob SHA. Their decoded sizes are approximately:

- `migration_2012_leopoldkanaal.csv`: 5.47 MB;
- `migration_2013_albertkanaal.csv`: 29.0 MB;
- `migration_2015_phd_verhelst_eel.csv`: 2.94 MB.

Using those blobs together with the other three migration files and the pinned metadata source, an independent reimplementation of the committed `analysis/12_post_initiation_speed.py` logic reproduces the canonical result exactly.

## Exact independent reproduction

Pinned upstream commit:

`59578cb622dddbbba5174b4c51bff0807787385a`

After expert corrections and the script's project-year eligibility rule:

- valid speed-bearing initiators before stratum filtering: **422**;
- modelled eels: **418**;
- informative project-year strata: **13**.

Stage counts in the model:

- FIII: **154**;
- FIV: **53**;
- FV: **211**.

Median speed:

- FIII: **0.0228976 m/s**;
- FIV: **0.0232434 m/s**;
- FV: **0.0244765 m/s**.

Adjusted Durif effect:

- speed ratio per stage: **0.9831088159**;
- 95% CI: **0.8524016314–1.1338586275**.

These match the canonical manuscript values.

Therefore:

> **the post-activation speed endpoint is reproducible from the pinned upstream source.**

The earlier STOP based on apparent empty files is withdrawn.

## Why the scientific question is nevertheless reopened

A newly published 2026 European eel study reports that silvering stage contributes to downstream progression rate in a specific river context. That evidence makes a universal interpretation of the pooled near-null stage coefficient inappropriate.

The sharper ecological question is now:

> **Is the post-activation effect of migratory readiness context dependent across water bodies even though its pooled average is near zero?**

This does not invalidate the activation/onset result or the pooled speed result. It changes the novelty target from a simple "handoff" to a possible phase-by-context interaction.

## Next valid analysis

Estimate post-activation Durif effects by project under the same speed definition and covariate structure, then test between-project heterogeneity without tuning project groupings to the observed effects.

If heterogeneity is weak, retain the pooled attenuation interpretation.

If heterogeneity is substantial, the stronger result is:

> readiness has a transferable activation effect but a context-contingent progression effect.

## Status

**PASS_SPEED_REPRODUCTION / OPEN_CONTEXT_HETEROGENEITY_TEST**
