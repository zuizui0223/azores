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

Interpretation:
> capture-time silvering readiness is a strong transferable predictor of migration activation and onset, but does not provide a transferable general speed advantage at either whole-route or individual median inter-station scale. This is a transferability boundary, not evidence that internal state becomes irrelevant after activation.

Post-activation heterogeneity audit:
- reproducible analysis: `analysis/16_post_initiation_stage_heterogeneity.py`;

- project-specific speed ratios span approximately **0.915–1.272** among the larger systems;
- stage × project interaction: **F(5,397)=1.03, p=0.398**;
- no supported evidence that the pooled near-zero speed effect is created by strong opposite project-specific effects.

Transferability boundary:
- leave-one-project-out robustness shows the pooled activation result is not driven by one project;
- direct project-specific activation fits are not all independently estimable because some project strata approach outcome saturation, so do **not** call this six independent replications.

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

**PASS_SPEED_REPRODUCTION / HETEROGENEITY_AUDIT_COMPLETE:** pooled speed n=418 and ratio 0.983 reproduce exactly; project-specific speed ratios show no supported heterogeneity (Q=2.47, df=5, p=0.781). Mechanistic attribution to route opportunity remains unresolved rather than rescued by a stage × water-body interaction.

### Active independent mechanism extension — Dutch consecutive barriers

The Europe-wide core manuscript is scientifically closed and does **not** depend on this extension. The Dutch system is the highest-value remaining route for strengthening the biological mechanism behind phase-specific control.

Public DANS metadata for DOI `10.17026/LS/WTSUNG` confirms an event-resolved archive containing raw-filtered acoustic detections, receiver metadata, biometrics/outcomes, and passage-event tables (462 pumping-station events; 282 tidal-sluice events).

The primary extension has been redesigned around **arrival-defined risk sets**:

> after an eel has actually reached a barrier, does FIV/FV migratory readiness modify dependence on the duration/strength of subsequent discharge opportunities?

This avoids using the source-defined opportunity table as the primary duration analysis, because event duration contributes to the source eligibility rule.

Current gate:
- retrieve the public DANS files;
- run `analysis/13_dutch_arrival_riskset_gate.py`;
- validate eel-ID, receiver, event-time and passage joins;
- preserve mandatory `release_group × duration` and `body_mass × duration` confounding checks.

Until that gate passes, no Dutch readiness × opportunity effect is estimated.

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
