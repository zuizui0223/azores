# Post-activation speed reproducibility and novelty audit — 2026-10-05

## Why this audit was reopened

The post-activation speed result had been treated as scientifically closed. Two new checks require that status to be reopened before submission:

1. the current committed analysis script does not reproduce the manuscript sample size from the pinned upstream source;
2. a newly published 2026 European eel study reports a detectable silvering-stage contribution to downstream progression rate in a specific river context, so a universal "stage disappears after activation" interpretation is not tenable.

## Frozen upstream source inspected

Repository: `PieterjanVerhelst/eel-meta-analysis`  
Pinned commit: `59578cb622dddbbba5174b4c51bff0807787385a`

Current repository script audited:

- `analysis/12_post_initiation_speed.py`

That script defines post-initiation speed from rows with `migration == TRUE`, using the six named migration CSVs listed in the script.

## Reproducibility discrepancy

At the pinned upstream commit, three of the six migration files named by the current script are zero-byte files:

- `migration_2012_leopoldkanaal.csv`
- `migration_2013_albertkanaal.csv`
- `migration_2015_phd_verhelst_eel.csv`

The three non-empty files contain stage-coded `migration == TRUE` individuals as follows before the script's project-year eligibility filter:

- 2011 Warnow: 107
- 2019 Grotenete: 33
- ESGL: 12

Thus the current script has at most 152 speed-bearing stage-coded individuals from the pinned source, not 418.

An independent reimplementation of the committed script's stated filtering/model logic gives:

- eligible project-year strata: Warnow 2011; Grotenete 2019; Grotenete 2020; ESGL 2015
- n = 152
- Durif speed ratio per ordinal stage ≈ 0.968
- approximate 95% CI ≈ 0.779–1.203

These numbers are **audit values only**. They do not replace the canonical manuscript result until the provenance of the existing n=418 / ratio=0.983 result is resolved using the exact original input artifact or corrected source path.

## Immediate scientific consequence

The canonical post-activation speed result is currently **not submission-safe**.

Do not use the speed endpoint as primary evidence for a phase-control handoff until one of the following is established:

1. the exact historical input files that generated n=418 are recovered and pinned; or
2. the current script/source route is corrected, rerun and all manuscript contracts are regenerated.

The activation and onset results are separate analyses and are not invalidated by this audit.

## New external evidence

Moyo et al. (Hydrobiologia, published 2026-10-01; DOI 10.1007/s10750-026-06406-6) analysed 25 silver European eels in the River Test and found that model selection retained silvering stage as a contributor to downstream progression rate together with environmental/context variables.

This does not contradict a weak pooled stage effect across heterogeneous systems. It does contradict a strong universal claim that silvering state ceases to matter after activation.

The sharper ecological hypothesis is therefore:

> **The effect of migratory readiness is phase-dependent and context-dependent: readiness consistently predicts activation, while its effect on progression is contingent on route and environmental context rather than universally absent.**

## Next valid analysis

After the speed-input provenance is repaired, the next analysis should be a pre-specified heterogeneity test, not another pooled-null test:

- estimate post-activation stage effects by system/project where estimable;
- test whether between-system heterogeneity exceeds sampling variation;
- relate any heterogeneity only to independently defined route classes or environmental opportunity variables;
- do not tune route classes against the stage-effect estimates.

A nonzero stage effect in one system and a near-zero pooled mean would then be biologically informative rather than treated as conflict.

## Status

**STOP_POST_ACTIVATION_SPEED_REPRO_AUDIT**

Azores is not scientifically closed for submission until this discrepancy is resolved.
