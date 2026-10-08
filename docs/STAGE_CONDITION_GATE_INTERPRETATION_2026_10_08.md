# Stage-specific body-condition ranking: what the eel data show

**Status: observed exploratory pattern, NOT demonstrated energetic checkpoint.**
2026-10-08; canonical sources:
- `results/stage_specific_condition_gate_v1.json`
- `results/stage_gate_context_matched_robustness_v1.json`
- GitHub Actions `stage-specific-condition-gate` run 37743766753 (PASS)

## All six projects, held-out coefficients

Within each Durif stage and project-year, compare which tagged fish entered the canonical algorithmic migration state. The model has length, release timing and ordinal stage; its expansion adds weight-for-length residual. Rank AUC changes:

| Stage | Evaluable fish | Initiators | Non-initiators | Informative within-stage positive–negative pairs | AUC base → condition | Gain | Project bootstrap 95% interval |
|---|---:|---:|---:|---:|---|---:|---|
| FIII | 261 | 154 | 107 | 2,474 | 0.481 → 0.528 | +0.047 | −0.032 to +0.191 |
| FIV | 68 | 53 | 15 | 108 | 0.565 → 0.787 | +0.222 | 0.000 to +0.250 |
| FV | 246 | 215 | 31 | 617 | 0.459 → 0.621 | +0.161 | +0.033 to +0.407 |

The apparent maximum at FIV is **not a dependable biological peak**: 92 of 108 informative pairs (85.2%) come from the single 2011 Warnow project, and removing that project leaves only 16 pairs.

FV's gain is positive after excluding any single project, but the projects differ strongly in sign and magnitude (e.g. −0.017 Warnow vs +0.490 Leopoldkanaal), and 337/617 FV pairs come from Albertkanaal.

## Directly comparable project-year contexts

Because FIII and FV are not sampled with identical project/year composition, the pooled FIII–FV gain difference (+0.114 favouring FV) may reflect composition. The stricter comparison uses only project-years with both FIII and FV positive–negative pairs.

Five comparable project-years from **four projects** remain.

- Weighted FV-minus-FIII incremental AUC contrast: **+0.1495** (weight=min(FIII pair count, FV pair count)).
- Leave-one-project-out matched contrasts: **+0.0818 to +0.2603**.
- Exact two-sided project-level paired sign-flip: **p=0.25**, based on just four independent projects.
- Sensitivity requiring at least five FV non-initiators leaves only two project-years and yields a smaller contrast **+0.0459**.

A particularly useful warning is that the same 2015 Verhelst project changes direction by release year: **2016 contrast −0.243**, **2017 contrast +0.504**. The FV negative outcome support is tiny (respectively 1 and 2 non-initiators), so that reversal cannot identify a temporal cause; it only demonstrates why a fixed, context-independent FV threshold claim is premature.

## A second, more fundamental ambiguity

The Durif stages represent premigrant female eels (FIII) versus morphologically migrant female eels (FIV/FV). They are constructed partly from **body mass and length**, alongside eye and fin traits (Durif et al. 2005; Sundin et al. 2022). Therefore using weight-for-length residual in addition to an ordinal silvering label can recover information lost in class binning; it does not automatically measure a distinct energetic physiology.

Critically, five of six original study projects also contain **continuous horizontal/vertical eye diameters and pectoral-fin length**, stored in `length2/3/4` with project-dependent order. These measurements have now been located and harmonization is documented in
`docs/ENTRY_STATE_MEASUREMENT_DEPENDENCE_AUDIT_2026_10_08.md`.

The strongest next test is not another stage-only re-fit: it is whether condition still adds held-out AUC beyond the *continuous* morphology (eye and fin), in the five projects with those measurements. This is specified in `analysis/contracts/continuous_morphology_condition_increment_v1.json` and implemented in `analysis/39_continuous_morphology_condition_increment.py`.

## Ecological interpretation at this stage

A possible interpretation is that morphological silvering and actual migration initiation are not one single readiness variable: within a morphology-defined migratory stage, other capture traits and perhaps environmental cues can affect whether departure is observed.

**Not yet supported**: a terminal energetic threshold in FV; a causal physiological control switch; a universal result across waterways; direct escapement improvement.

Conservation relevance: **silver-eel production, telemetry-defined departure, safe passage and actual escapement are different endpoints**. A morphology-only survey cannot automatically substitute for observed initiation or escapement, but the existing six-project data cannot quantify the magnitude of that mismatch in wild population management.

References:
- Durif, C., Dufour, S. & Elie, P. (2005). J Fish Biol 66:1025–1043. https://doi.org/10.1111/j.0022-1112.2005.00662.x
- Sundin, J. et al. (2022). Marine and Coastal Fisheries 14:e10219. https://doi.org/10.1002/mcf2.10219
