# Analysis programme

## Canonical ecological mainline

The current Azores paper is **not** a site-fidelity re-analysis and not an EOG validation paper.

The primary ecological result is phase specific:

> **Capture-time silvering readiness strongly predicts migration activation, but its predictive effect is significantly attenuated after migration has begun.**

The current source of truth is pinned to:

- upstream repository: `PieterjanVerhelst/eel-meta-analysis`
- upstream commit: `59578cb622dddbbba5174b4c51bff0807787385a`
- primary stages: FIII/FIV/FV

## Canonical pipeline

### 1. Gate 1 — binary migration activation

~~~bash
python analysis/09_durif_migration_initiation.py
~~~

Expert-corrected primary result:

- FIII: **154/261 = 59.0%**
- FIV: **53/68 = 77.9%**
- FV: **215/246 = 87.4%**
- adjusted OR per stage: **2.08**
- 95% CI: **1.56–2.76**
- p ≈ **4.2e-7**

The source-study nine 2015 expert non-migrant corrections are inherited unchanged.

### 2. Gate 1 timing — threshold-defined onset

~~~bash
python analysis/10_migration_onset_cox.py
~~~

The canonical clock is `time_first_dist_to_use` on the first `downstream_migration = TRUE` row.

Current result:

- HR per stage: **1.29**
- 95% CI: **1.13–1.47**
- p = **0.00016**

This is supportive timing evidence, not the main novelty.

### 3. Direct phase interaction

~~~bash
python analysis/11_phase_stage_interaction.py
python analysis/13_phase_interaction_lopo.py
~~~

Clustered stacked continuation-ratio result:

- initiation OR/stage: **2.08**
- completion OR/stage: **1.15**
- ratio of stage ORs: **1.81**
- 95% CI: **1.15–2.84**
- direct phase interaction p = **0.0099**

LOPO:

- direction preserved in **6/6** project deletions;
- OR-ratio range **1.55–2.13**;
- **5/6** deletions remain p < 0.05.

This is the primary developmental evidence.

### 4. Gate 2 — sea escapement conditional on activation

~~~bash
python analysis/10_two_stage_mobility.py
~~~

The upstream `identify_escapement_success.R` defines success as **successful escapement to the sea** with project-specific terminal station/distance rules.

Among initiators:

- adjusted OR/stage: **1.15**
- 95% CI: **0.83–1.59**
- p = **0.412**

Do not call this "no internal effect"; call it attenuation relative to Gate 1.

### 5. Independent post-activation response — migration speed

~~~bash
python analysis/12_post_initiation_speed.py
~~~

- adjusted speed ratio/stage: **0.983**
- 95% CI: **0.852–1.134**
- p = **0.815**

Thus the post-activation attenuation is not unique to the binary escapement endpoint.

### 6. External-context bridge

~~~bash
python analysis/11_project_context_gate.py
~~~

Across six project contexts:

- WRS vs initiation: rho **0.029**, exact p **0.983**
- WRS vs completion: rho **-0.928**, exact p **0.022**

This is **context evidence only**, because WRS, project, route, hydrology, telemetry geometry and observability are confounded.

### 7. Independent confirmation target

The Dutch pump -> tidal-sluice system is the active within-route confirmation target.

After obtaining DANS DOI `10.17026/LS/WTSUNG`:

~~~bash
python analysis/08_dutch_barrier_confirmation_gate.py --data-dir <downloaded_DANS_directory>
~~~

The confirmation question is:

> once migration has activated, do barrier-specific passage opportunities explain progression better than residual Durif-stage differences?

Return NON-IDENTIFIABLE rather than dropping body mass or regrouping Durif stages if the predictor structure is confounded.

## Interpretation boundary

The paper may claim:

> **the predictive association of internal migratory readiness is phase dependent and significantly weaker after migration activation.**

It may not yet claim:

- WRS causally causes the attenuation;
- external factors wholly replace internal control;
- Durif stage has zero post-initiation effect;
- the Dutch study directly replicates the Europe-wide interaction.

## Historical analyses

Older stage-effect, fixed-window and exploratory files remain for audit trail. They are not the numeric source of truth.

Use:
- `manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V1.json`
- `docs/phase_stage_interaction_result.md`
- `docs/CLAIM_EVIDENCE_MAP_PHASE_CONTROL_V1.md`
for current manuscript numbers and claims.
