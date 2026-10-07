# Post-activation speed reproducibility and novelty audit — corrected 2026-10-07

## Correction to the initial audit

The initial audit incorrectly interpreted empty content returned by the GitHub file-content connector for three very large CSVs as zero-byte source files.

That interpretation was wrong.

Direct Git blob retrieval by the source blob SHAs shows that the files are present and large:

- `migration_2012_leopoldkanaal.csv`: ~5.47 million characters
- `migration_2013_albertkanaal.csv`: ~29.0 million characters
- `migration_2015_phd_verhelst_eel.csv`: ~2.94 million characters

The earlier apparent absence was therefore a connector large-file retrieval limitation, not missing upstream data.

## Reproducibility audit resolved

Frozen upstream source:

- repository: `PieterjanVerhelst/eel-meta-analysis`
- commit: `59578cb622dddbbba5174b4c51bff0807787385a`

Current Azores script:

- `analysis/12_post_initiation_speed.py`

The six source migration files plus `eel_meta_data.csv` were retrieved at the pinned commit and the committed analysis logic was independently reimplemented.

Exact reconstruction:

- stage-coded metadata records: **603**
- expert-corrected migration-TRUE speed candidates: **422**
- eligible project-year strata after the script's n>=8 and >=2-stage rule: **13**
- modelled individuals: **418**
- ordinal Durif coefficient on log speed: **-0.0170354672**
- multiplicative speed ratio per FIII -> FIV -> FV increment: **0.9831088159**
- 95% CI: **0.8524016314–1.1338586275**

These match the canonical repository result to numerical precision.

Stage-specific modelled counts and medians were also reproduced:

- FIII: n=154, median **0.0228976 m/s**
- FIV: n=53, median **0.0232434 m/s**
- FV: n=211, median **0.0244765 m/s**

Therefore the canonical n=418 post-activation speed endpoint is **reproducible from the pinned public source**.

## What remains open

The reproducibility concern is closed, but the **novelty/generalization question remains open**.

A 2026 River Test study reports that silvering stage contributes to downstream progression rate in one river context. That evidence is compatible with a weak pooled Europe-wide mean if post-activation stage effects are context dependent.

Therefore the next scientifically useful analysis is not another test of the pooled mean. It is a heterogeneity test:

> **Does the effect of Durif readiness on post-activation speed differ among route contexts?**

The next analysis should:

1. estimate project-specific post-activation Durif effects where estimable;
2. quantify between-project heterogeneity without tuning project classes to outcomes;
3. only then compare the effect pattern with independently defined route / barrier / tidal context.

## Current status

**PASS_POST_ACTIVATION_SPEED_REPRO_AUDIT**

The speed endpoint can remain in the manuscript.

The stronger statement that Durif readiness is universally absent after activation is not supported and should not be made. The current canonical wording—no **general** pooled Durif-stage gradient in post-activation speed—remains valid pending the heterogeneity analysis.
