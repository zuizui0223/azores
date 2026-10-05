# Post-activation speed reproducibility audit — resolved 2026-10-05

## Resolution

The apparent discrepancy in the post-activation speed endpoint was caused by the GitHub connector's normal file-content path returning empty content for three very large CSV blobs. Fetching those inputs directly by Git blob SHA recovered their full contents.

The canonical speed result is reproducible from the pinned upstream source.

Pinned upstream:

- repository: `PieterjanVerhelst/eel-meta-analysis`
- commit: `59578cb622dddbbba5174b4c51bff0807787385a`

Audited repository script:

- `analysis/12_post_initiation_speed.py`

## Exact reproduction

Stage-coded expert-corrected migration-positive individuals available by project:

- 2011 Warnow: 107
- 2012 Leopold Canal: 52
- 2013 Albert Canal: 132
- 2015 Scheldt: 86
- 2019 Grote Nete: 33
- ESGL: 12

Total expert-corrected initiators represented before the project-year model filter: **422**.

Applying the committed script's informative-stratum rule leaves **418** individuals across **13** project-year strata.

The independently reconstructed model exactly reproduces the canonical result:

- Durif speed ratio per FIII -> FIV -> FV increment: **0.9831088159**
- 95% CI: **0.8524016314–1.1338586275**
- canonical n: **418**

Stage medians also reproduce:

- FIII: n=154, median **0.02290 m/s**
- FIV: n=53, median **0.02324 m/s**
- FV: n=211, median **0.02448 m/s**

Therefore the canonical post-activation speed endpoint is **reproducible and submission-safe with respect to this audit**.

## Project-specific diagnostic

The same model form was fit separately within each project where estimable.

| Project | n | speed ratio / Durif stage | 95% CI |
|---|---:|---:|---:|
| Warnow | 107 | 0.915 | 0.682–1.228 |
| Leopold Canal | 52 | 0.981 | 0.678–1.420 |
| Albert Canal | 128 | 1.272 | 0.899–1.799 |
| Scheldt | 86 | 1.011 | 0.856–1.193 |
| Grote Nete | 33 | 1.035 | 0.731–1.465 |
| ESGL | 12 | 1.219 | 0.675–2.201 |

A fixed-effect Cochran heterogeneity diagnostic on the six log-speed stage coefficients gives:

- Q = **2.469**
- df = **5**
- p = **0.781**
- I² = **0%**

Thus the current six-project dataset does **not** support detectable between-system heterogeneity in the Durif effect on this generic post-activation speed endpoint.

## Ecological interpretation

The stronger supported statement is:

> **Capture-time silvering readiness strongly predicts migration activation and onset, but provides little transferable information about generic post-activation migration speed across the six analysed systems.**

The result should not be upgraded to:

- Durif state has exactly zero post-activation effect;
- external context universally replaces internal control;
- all progression metrics are stage-independent.

A context-specific study can still detect a stage effect on a different progression endpoint without contradicting this pooled result.

## Status

**RESOLVED_REPRO_AUDIT**

The previous STOP caused by the apparent n=418 mismatch is removed.
