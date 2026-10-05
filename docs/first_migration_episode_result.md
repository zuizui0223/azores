# First classified migration episode — all available Durif projects

## Definition corrected

The upstream eel classifier does **not** define a permanently absorbing physiological migration state.

It first identifies qualifying downstream-migration starts using:

- 4 km distance threshold;
- 0.01 m/s migration-speed threshold;
- 1005 m stationary-range smoothing;

and then marks the general migration process from the first qualifying start to the maximum downstream distance.

Therefore this analysis uses:

> **first classified migration episode**

not "yellow-to-silver transition onset".

Upstream source is pinned to:

`PieterjanVerhelst/eel-meta-analysis@59578cb622dddbbba5174b4c51bff0807787385a`.

## Coverage

Large upstream migration CSVs were read through the Git blob/raw route rather than the GitHub Contents API.

Stage-coded metadata coverage in migration files:

- Warnow: 141/146;
- Leopoldkanaal: 80/80;
- Albertkanaal: 144/157;
- 2015 phd_verhelst_eel: 126/135;
- Grotenete: 38/38;
- ESGL: 46/47.

`life4fish` contains Durif-stage metadata but has **no project migration CSV** in the upstream migration directory and therefore cannot enter this onset analysis.

The source's nine expert-judgement exclusions for the 2015 project were applied.

## Descriptive result

Across available processed migration files after the source expert exclusions:

| Durif stage | n | classified episode | fraction | median days among initiators |
|---|---:|---:|---:|---:|
| FIII | 261 | 154 | **59.0%** | **4.95 d** |
| FIV | 68 | 53 | **77.9%** | **0.27 d** |
| FV | 246 | 215 | **87.4%** | **0.69 d** |

These raw summaries are strongly project- and season-dependent and are not the primary inference.

## Stratified survival result

A Breslow-tie Cox model retained non-initiators as censored observations at their last processed detection.

Strata:

> project × release year

Covariates within strata:

- body length per 100 mm;
- release timing per 100 days;
- ordinal Durif stage: FIII=0, FIV=1, FV=2.

Model size:

- **570 individuals**
- **418 classified episodes**
- **13 project-year strata**

### Durif stage

Per one-stage increment:

- hazard ratio = **1.28**
- 95% CI = **1.12–1.45**
- p = **2.2e-4**

### Body length

Per 100 mm:

- HR = **1.08**
- 95% CI = **0.95–1.23**
- p = **0.244**

### Release timing

Per 100 days later within project-year:

- HR = **1.31**
- 95% CI = **0.95–1.79**
- p = **0.094**

## Biological interpretation

This gives a second movement endpoint consistent with the prior successful-migrant analysis.

Capture-time Durif readiness is associated with:

1. greater odds of later successful migration;
2. greater hazard of entering the source classifier's migration episode.

The stage signal is not removed by body length or broad within-year release timing.

The supported statement is therefore:

> **internal migratory readiness is associated with both the initiation and eventual realization of downstream movement.**

## Boundary

This still does not establish:

- physiological transition timing;
- a causal effect of silvering;
- a universal stage × landscape-resistance interaction.

The stronger landscape-gating claim still requires the independently frozen Dutch consecutive-barrier confirmation or another system with better within-landscape resistance variation.
