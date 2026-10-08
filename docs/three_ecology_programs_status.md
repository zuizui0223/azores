# Three independent ecology programmes — current executable status

These are three separate ecological papers. EOG is provenance/discovery only.

---

## 1. Azores — phase-specific control of eel migration

### Scientific status

**Activation/onset and pooled post-activation speed analyses reproduce exactly. The post-activation project-heterogeneity audit is also complete and does not support strong between-project variation in the Durif-speed coefficient.**

Primary evidence:

**Migration activation**
- initiation Durif OR per FIII -> FIV -> FV increment: **2.08**
- 95% CI **1.56–2.76**
- p approximately **4.2e-7**

**Behavioral onset**
- Cox HR per stage: **1.29**
- 95% CI **1.13–1.47**
- p = **0.00016**

**Post-activation progression**
- whole-route migration-speed ratio per stage: **0.983**
- 95% CI **0.852–1.134**
- p = **0.815**
- frozen median positive inter-station speed audit: ratio **1.001**, 95% CI **0.831–1.204**
- project heterogeneity is unsupported for both progression scales (whole-route Q=2.47, p=0.781; segment-scale Q=2.32, p=0.804)
- simple capture-stage staleness diagnostic unsupported: Durif × log-latency ratio **1.036** (p=0.382); stage-speed ratios among <=1/3/7-day activators **0.942 / 0.953 / 0.963**
- activation-filter diagnostic: FIII initiators are phenotypically selected (length SMD **+0.514**, weight-for-length residual SMD **+0.302**), but same-sample stage-speed changes only **1.042 -> 1.062** after inverse-probability weighting (95% CI for weighted ratio **0.916–1.230**)

Interpretation:
> capture-time silvering readiness is a strong transferable predictor of migration activation and onset, but among eels that cross this stage-dependent activation filter it does not provide a transferable general speed ranking at either whole-route or individual median inter-station scale. Project sign cancellation, simple capture-stage staleness, and selection on the measured canonical activation predictors do not explain the weak progression gradient. Latent readiness selection remains an identification boundary, so this is not a causal estimate that internal-state effects disappear after activation.

Post-activation heterogeneity audit:
- reproducible analysis: `analysis/16_post_initiation_stage_heterogeneity.py`;

- project-specific speed ratios span approximately **0.915–1.272** among the larger systems;
- stage × project interaction: **F(5,397)=1.03, p=0.398**;
- no supported evidence that the pooled near-zero speed effect is created by strong opposite project-specific effects.

Transferability boundary:
- leave-one-project-out robustness shows the pooled activation result is not driven by one project;
- direct project-specific activation fits are not all independently estimable because some project strata approach outcome saturation, so do **not** call this six independent replications.

### Multivariate entry-state transferability result

An activation-trained score combining ordinal Durif stage and continuous
weight-for-length condition now provides the clearest phase test.

Activation-trained weights:
- Durif = **0.756**;
- condition = **0.379**.

Per 1 SD of this frozen entry-state score:
- migration activation OR = **2.23** (95% CI **1.70–2.92**);
- behavioral onset HR = **1.32** (95% CI **1.17–1.49**);
- post-activation whole-route speed ratio = **0.946** (95% CI **0.832–1.076**), partial R² **0.18%**;
- frozen median positive inter-station speed ratio = **1.028** (95% CI **0.869–1.215**), partial R² **0.026%**.

Project-held-out coefficient training gives the same boundary:
- cross-fitted activation OR **1.97** (95% CI **1.53–2.53**);
- cross-fitted onset HR **1.26** (95% CI **1.12–1.42**);
- whole-route speed ratio **0.948** (95% CI **0.836–1.075**);
- frozen segment-speed ratio **1.013** (95% CI **0.860–1.192**);
- both Durif and condition weights remain positive in all six training folds.

This removes held-out-project outcomes from score-weight estimation, while
remaining a post-hoc within-programme robustness test rather than external validation.

Exact-link realized transit-speed audit (corrected expert-eligible cohort, FWL numerical equivalence PASS):
- **17,792** positive segment rows;
- **418** eels;
- **244** directed receiver pairs;
- project-held-out entry-state speed ratio **0.962/SD**;
- 95% CI **0.883–1.048**, p **0.372**;
- weighted partial R² **0.0382%**;
- pair-support sensitivities: **0.956** (>=3 fish) and **0.999** (>=10 fish);
- leave-one-project-out ratio range **0.933–1.013**.

The source segment-speed field contains nonphysical extreme values (candidate
maximum **3752 m/s**). A post-hoc, externally motivated quality audit using
upper screens of 2.5/5/10 m/s removes **63.1/58.6/53.0%** of candidate rows but
leaves ratios **0.942/0.944/0.941**, all null-compatible. Thus the exact-link
null is robust to gross speed artifacts, while absolute source segment-speed
values should not be read as swimming capacity. The filtered negative point estimates have p≈0.07–0.08 and 95% intervals including one.

Interpretation:

> **the multivariate capture state that predicts entry into migration is not a
> general motor-performance score after activation.**

This is now stronger than the Durif-only attenuation result because adding a
second continuous capture-state dimension does not restore a transferable
generic speed ranking.

Canonical artifact:
- `results/entry_state_score_transferability_v1.json`
- `results/cross_project_entry_state_score_v1.json`
- `results/within_link_entry_state_speed_v1.json`
- `results/within_link_speed_quality_sensitivity_v1.json`
- `results/within_link_fwl_numerical_audit_v1.json`
- `docs/ENTRY_STATE_SCORE_TRANSFERABILITY_2026_10_07.md`

### Body-state phase-turnover diagnostic

A new post-hoc body-state programme adds a second pre-movement axis beyond the ordinal Durif label.

Across three frozen weight-for-length definitions:

- activation OR per 1 SD condition = **1.438–1.460**;
- onset HR per 1 SD condition = **1.148–1.153**;
- both directions remain positive in every leave-one-project-out fit under all three definitions;
- Durif × condition interactions are unsupported.

Among activated eels, however:

- whole-route speed condition ratio = **0.896–0.925** per SD, with all six leave-one-project-out estimates below one under all three definitions, but full-cohort 95% intervals include one;
- the previously frozen median positive inter-station speed endpoint gives condition ratios only **1.049–1.050**, with no negative gradient;
- decomposition of whole-route speed gives distance ratios **1.019–1.025** but elapsed-time ratios **1.108–1.138** per SD condition;
- elapsed-time estimates are >1 in every leave-one-project-out fit under all three definitions.

Interpretation:

> **better capture body state predicts entry into migration, but the later whole-route pattern is associated with longer elapsed migration time rather than slower positive transit speed.**

This is compatible with additional waiting/staging or passage selectivity, and is directionally consistent with independent Dutch barrier studies in which better-conditioned eels accumulate more missed passage opportunities. It is **not** yet a causal sign reversal: the post-activation cohort is selected, elapsed time is not direct stop time, and the condition proxies reuse morphometrics that also contribute to Durif classification.

Current status: **MULTIVARIATE_ENTRY_GATE_SUPPORTED / BARRIER_SELECTIVITY_MECHANISM_UNSUPPORTED**.

The independent Dutch arrival-defined tests do **not** support the specific
asset-protection/barrier-selectivity mechanism. After first barrier arrival,
condition is unrelated to missed openings or delay at both EZ and CL, and the
CL condition × duration interaction is near zero. The Europe-wide elapsed-time
pattern therefore remains descriptive and should not be interpreted as general
condition-dependent barrier waiting.

Canonical artifacts:
- `results/multivariate_readiness_gate_diagnostic_v1.json`
- `results/body_condition_onset_diagnostic_v1.json`
- `results/body_condition_metric_robustness_v1.json`
- `results/body_condition_post_activation_speed_v1.json`
- `results/body_condition_segment_progression_v1.json`
- `results/body_condition_whole_route_decomposition_v1.json`
- `docs/CONDITION_PHASE_REVERSAL_HYPOTHESIS_2026_10_07.md`

### Endpoint boundary

The upstream terminal-positive file is not a validated binary success/failure variable.

Therefore:
- terminal-set OR **1.15** is secondary sensitivity only;
- former initiation/terminal OR-ratio **1.81** is secondary sensitivity only;
- non-membership is not biological migration failure;
- no escapement probability is estimated here.

### Canonical artifacts

Manuscript:
- `manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V3.md`

Numeric/interpretation:
- `results/phase_control_canonical_v2.json`
- `manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V2.json`
- `manuscript/MANUSCRIPT_QC_V2.json` — **PASS**

Figures:
- `manuscript/FIGURE_PLAN_V2.md`
- `manuscript/FIGURE_CAPTIONS_V2.md`
- `manuscript/FIGURE_DATA_CONTRACT_V2.json`
- `manuscript/FIGURE_QC_V2.json` — **PASS**
- `manuscript/figure_data_v2/`
- `manuscript/rendered_figures_v2/Figure1.svg` through `Figure4.svg`
- `manuscript/RENDERED_FIGURE_QC_V2.json` — **PASS_REFERENCE_RENDER**

Older V1 completion-centred figure specifications and simplified initiation scripts are explicitly superseded/fail-closed.

### Remaining non-scientific submission inputs

- author/affiliation/contribution fields;
- target-journal formatting;
- source-study ethics wording check;
- release/archive.

**PASS_SPEED_REPRODUCTION / PROGRESSION_FALSIFICATION_AUDITS_COMPLETE:** pooled speed n=418 and ratio 0.983 reproduce exactly; project-specific speed ratios show no supported heterogeneity (Q=2.47, df=5, p=0.781); the finer-scale and stage-staleness audits do not uncover a hidden general stage gradient; measured activation selection is real but IPW does not restore one. Latent selection and route-specific mechanism remain unresolved.

### Active independent mechanism extension — Dutch consecutive barriers

The Europe-wide core manuscript remains scientifically separable from this extension. The Dutch system is an event-level mechanism candidate, not a clean independent confirmation: its source opportunity definition is duration-dependent, Durif stage is associated with release cohort, and stage/body mass are partly non-identifiable at the tidal sluice.

Public DANS metadata for DOI `10.17026/LS/WTSUNG` confirms an event-resolved archive containing raw-filtered acoustic detections, receiver metadata, biometrics/outcomes, and passage-event tables (462 pumping-station events; 282 tidal-sluice events).

The primary extension has been redesigned around **arrival-defined risk sets**:

> after an eel has actually reached a barrier, does FIV/FV migratory readiness modify dependence on the duration/strength of subsequent discharge opportunities?

This avoids using the source-defined opportunity table as the primary duration analysis, because event duration contributes to the source eligibility rule.

Current Dutch status:
- all 15 DANS files were publicly materialized;
- duration-independent arrival-defined risk sets were reconstructed;
- informative strict-start choice sets: EZ **14 fish** (FIII 2), CL **15 fish** (FIII 4);
- condition-dependent preference for longer windows is unsupported;
- arrival-defined condition vs missed events and barrier delay is unsupported at both barriers;
- readiness × duration remains low-information because FIII representation is small.

The Dutch extension therefore functions primarily as a **falsification** of the
specific condition-dependent passage-selectivity mechanism, not as positive
confirmation of an internal-to-external handoff.

---

## 2. Louisiana — hydrological buffering inside resident home ranges

### Scientific status

**Analysis closed for drafting. Canonical figure data materialized. Reference Figure 1–5 SVG render QC PASS.**

Primary independent Lake Erie result:
- **190** valid matched events;
- **10** birds;
- **10/10** positive SRI;
- median SRI **0.886**;
- exact sign-test p **0.00098**.

Temporal retention:
- 10/10 positive;
- median **0.658**.

Availability coupling:
- observed slope **0.162**;
- pseudo-used null median **1.001**;
- coupling reduction **83.8%**;
- 10/10 birds below own null median.

Buffering limit:
- **9/10** retain positive buffering under top-quartile local mismatch;
- median extreme retention **0.629**.

Post-hoc local state-portfolio mechanism:
- **173** events with both intended random plots;
- heterogeneity coefficient **-0.0431** versus matched pseudo-used null median **+0.2617**;
- Monte Carlo **p = 0.000020**;
- stronger mismatch x heterogeneity interaction unsupported (**p = 0.753**).

Interpretation:
> repeated realised microhabitat use strongly dampens temporal hydrological variation experienced by resident King Rails relative to local time-matched availability, and fine-scale hydrological heterogeneity is compatible with providing a local portfolio of alternative states for that buffering.

Boundary:
- coordinate-to-event join remains unresolved;
- do not claim measured geographic displacement caused the buffering.

### Manuscript status

Canonical manuscript:
- `manuscript/LOUIS_HYDROLOGICAL_BUFFERING_MANUSCRIPT_V1.md`

Numeric contract:
- `manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V2.json`

Submission QC:
- logical equivalent of `validation/validate_manuscript_v1.py`: **PASS**
- no control-character / LaTeX corruption;
- all canonical sample-flow and SRI/coupling values present;
- coordinate-linkage boundary explicit;
- no EOG wording;
- no forbidden causal claims;
- Brewer source citation, Zenodo DOI and References section present.

### Remaining non-scientific submission inputs

- author/affiliation/contribution fields;
- target-journal formatting;
- source ethics wording verification;
- submission release/archive.

**The local-heterogeneity mechanism decomposition is complete and a bird-level robustness audit is now frozen. Do not add more Lake Erie post-hoc metrics unless an authoritative coordinate-event linkage or genuinely new response dimension becomes available.**

### Published Godwit boundary

The Senegal Delta Black-tailed Godwit system is retained as an opposite-scale ecological boundary rather than an SRI replication: seasonal movement is associated with habitat-state replacement/resource tracking rather than strict state retention. Louisiana therefore asks the broader question **when local movement buffers experienced environmental variation and when animals must switch or relocate to a different resource state**.

---

## 3. Tampa — buffered persistence under quantitative degradation

### Scientific status

Retrospective ecology is closed.

Supported:
- recorded occurrence can remain stable while frequency, abundance, blade length, shoot density or composition deteriorate;
- external Zostera panel reproduces broad binary–quantitative state decoupling.

Mechanism remains prospective.

### Decisive prospective test

**Four-bay rhizome TNC sampling first; within-meadow state augmentation is the decisive primary inference.**

Planning frame:
- Old Tampa Bay: 8 recent positive nodes
- Middle Tampa Bay: 11
- Lower Tampa Bay: 14
- Boca Ciega Bay: 8
- planning total: **41**

Confirmatory gate:
- >=36 analyzable nodes total;
- >=6 analyzable nodes per bay;
- >=3 valid cores/node;
- one <=28-day campaign;
- paired baseline within +/-14 days;
- one frozen HPLC workflow.

The paper-level TNC hierarchy is frozen before outcome access: the within-node anchor test is decisive; the four-bay cross-node TNC model is supportive/generalization only and cannot rescue an unsupported within-node result.

A second, independent high-novelty branch is also frozen for **history-linked functional insurance**. A response-independent preflight identified 18 Old+Middle Tampa Bay meadows containing both a current alternative-seagrass point with documented prior Thalassia loss and a nearby >=3-year persistent-Thalassia comparator; all 18 pairs are within 100 m (median 25 m, maximum 75 m). The future primary compares synchronized measured hydrodynamic attenuation within each matched meadow. A null/overlapping interval is not treated as functional equivalence.

### Software/readiness status

Authoritative pilot path:

~~~text
raw response-independent pilot records
 -> validation/build_tnc_v2_method_pilot_summary.py
 -> field/tnc_v2_method_pilot_candidate.json
 -> validation/validate_tnc_v2_method_pilot.py
 -> PASS_METHOD_PILOT
 -> apply selected values to field/tnc_v2_precollection_freeze.json
 -> validation/validate_tnc_v2_baseline.py
~~~

The following templates already exist:
- `field/tnc_v2_raw_pilot_metadata.json`
- `field/tnc_v2_hplc_matrix_pilot.json`
- `field/tnc_v2_tissue_class_pilot.csv`
- `field/tnc_v2_core_geometry_pilot.csv`
- `field/tnc_v2_offset_pilot.csv`
- `field/tnc_v2_preservation_pilot.csv`

### Current hard stop

**STOP_RESOURCE_FREEZE_INCOMPLETE**

The unresolved values are physical field/laboratory facts, not analytical choices:

1. campaign start date;
2. campaign end date;
3. selected horizontal-rhizome tissue class;
4. minimum perpendicular transect offset;
5. selected core diameter;
6. selected core depth;
7. maximum collection-to-preservation time;
8. preservation method;
9. final four-bay node/date/resource manifests;
10. optional forcing modules must be explicitly confirmatory or disabled.

These values cannot be inferred from existing retrospective data and must not be fabricated.

### Single next external input

The next scientifically valid input is:

> **response-independent TNC method/field pilot measurements entered into the existing pilot files.**

Once those values exist, the repository already contains the builder, validator and fail-closed transition into the outcome-bearing four-bay campaign.

---

# Active order

1. **Azores:** core manuscript scientifically QC-passed; independent Dutch barrier-mechanism extension remains active pending archive retrieval/schema validation.
2. **Louisiana:** manuscript scientifically QC-passed; submission formatting only.
3. **Tampa:** active science blocker is the physical TNC method/field pilot.

## Hard boundary

Do not restart exploratory analyses in Azores or Louisiana merely because Tampa is waiting on external field/laboratory input.

The target remains three independent ecological papers.
