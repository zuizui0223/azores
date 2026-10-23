# Supplementary Methods and Results — Azores V5 migration phase paper

**Author-review scientific draft, 2026-10-23.** This is a populated supplementary evidence document and not a final journal-formatted supplement. All scientific subsections between source markers are verbatim from the original V4, including original section headings; source context and endpoint definitions are not silently reinterpreted.

**Source:** `manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md`, Git blob SHA `e69df3be25abb06eab2b0d709f6c782a7a4c82aa`. **Main paper:** [V5 manuscript](AZORES_PHASE_TRANSFER_MAIN_V5_DRAFT.md); [supplement allocation plan](AZORES_V5_SUPPLEMENT_EVIDENCE_MAP.md). The extracted source passages are developmental secondary analyses, not response-blind registered hypotheses.

## S1. Original source, sample flow and observational endpoint definitions

Source cohort and classification boundaries; no non-evaluable source fish are coded as nonmigrants.

<!-- V4_SOURCE_BEGIN: Data provenance and study scope -->
### Data provenance and study scope

We used openly available processed telemetry products and metadata from the Europe-wide European eel biotelemetry synthesis of Verhelst et al. (2025). The source synthesis assembled data from 18 water bodies in nine countries and included 2,306 tagged eels tracked using acoustic telemetry or the Nedap Trail System. Our analysis did not attempt to reproduce the entire continental meta-analysis. Instead, we selected the subset for which three conditions were simultaneously met:

1. an exact female Durif stage of FIII, FIV or FV was recorded at capture;
2. a public project-level migration table generated with the common source classifier was available; and
3. body length and release date were available for the prespecified adjustment models.

Six projects met these criteria: Warnow, Leopoldkanaal, Albertkanaal, the Scheldt-related 2015 phd_verhelst_eel project, Grote Nete and ESGL.

We treated the source data-processing decisions as fixed provenance. We did not re-tune the movement classifier, reconstruct alternative trajectories, or alter source-project expert judgements after inspecting our endpoints.
<!-- V4_SOURCE_END: Data provenance and study scope -->

<!-- V4_SOURCE_BEGIN: Sample-flow and quality boundary -->
### Sample-flow and quality boundary

Within the six focal projects, 603 metadata records had primary female stages FIII–FV before applying the source project's cleaned migration-table availability. The public migration tables contained 575 evaluable stage-coded tracks.

We did not classify metadata individuals absent from the cleaned migration tables as non-migrants. An audit of the upstream cleaning code showed that 27 of the 28 absent individuals had been explicitly removed for reasons including taxonomic mismatch, translocation, implausible or short tracks, or source-defined track quality. The remaining individual had only a release record and no post-release detection in the cleaned residency data. These individuals were therefore outside the evaluable movement universe.

The source processing also identified nine classifier-positive eels from the 2015 project as non-migratory by expert judgement. We preserved these nine corrections unchanged in all primary initiation and phase analyses. Algorithm-only results before those expert corrections were retained as sensitivity analyses but were not used for the manuscript's primary estimates.
<!-- V4_SOURCE_END: Sample-flow and quality boundary -->

<!-- V4_SOURCE_BEGIN: Durif stage -->
### Durif stage

We treated female Durif stage as an ordinal internal-state predictor:

\[
\mathrm{FIII}=0,\qquad \mathrm{FIV}=1,\qquad \mathrm{FV}=2.
\]

This ordering follows the biological silvering framework in which FIII is pre-migrant and FIV–FV are migrating stages (Durif et al. 2005). FII, MII, coarse silver labels and records with missing life stage were excluded from the primary ordinal comparison rather than pooled post hoc.
<!-- V4_SOURCE_END: Durif stage -->

<!-- V4_SOURCE_BEGIN: Source migration classification -->
### Source migration classification

We inherited the migration-classification algorithm from the source analysis. In brief, the source workflow identified sustained downstream migration using a minimum distance threshold of 4 km and a migration-speed threshold of 0.01 m s\(^{-1}\), with an additional smoothing criterion to avoid identifying stationary periods as migration starts. Once downstream migration was identified, the source migration interval extended from the first qualifying downstream segment to the furthest downstream distance reached.

For the binary initiation analysis, an individual was considered initiated if the source workflow identified qualifying downstream migration, after applying the nine fixed expert corrections. We refer to this as **migration activation** or **classified migration initiation** rather than the unobserved physiological instant at which the animal decided to migrate.
<!-- V4_SOURCE_END: Source migration classification -->

<!-- V4_SOURCE_BEGIN: Gate 1: migration-initiation model -->
### Gate 1: migration-initiation model

The binary Gate-1 endpoint was whether an evaluable track initiated classified downstream migration.

We fitted a logistic model with project × release-year fixed effects. Within each project-year stratum, body length was centred and scaled per 100 mm, and release date was centred and scaled per 100 days. The primary predictor was ordinal Durif stage.

Conceptually:

\[
\operatorname{logit}\{P(\mathrm{initiation})\}
=
\alpha_{\mathrm{project\times year}}
+\beta_L L
+\beta_T T
+\beta_D D,
\]

where \(D\) is the FIII–FIV–FV ordinal score.

Only strata containing outcome variation and at least two Durif stages contributed to coefficient estimation.

We also conducted an explicitly **post-hoc heterogeneity test** distinct from the primary ordinal, covariate-adjusted activation coefficient. The comparison was restricted to FIII versus FV (507 source-classified fish) and used all six projects, including stage-by-outcome separated project tables. Exact conditional inference first fixed stage counts and initiation counts within project. A stricter test also conditioned separately on every project × release-year margin, convolved their noncentral hypergeometric count distributions and tested one shared FV-versus-FIII odds ratio across projects using an enumerated likelihood-ratio distribution. We report exploratory leave-one-project-out tests to assess dependence on one source context. The contrast is an association of source-classified initiation labels, not an estimate of a physiological stage effect or a causal river modifier. The verified result and frozen executable contract are retained in `analysis/results/silvering_stage_project_year_heterogeneity_exact.json` and `analysis/contracts/silvering_stage_project_year_heterogeneity_exact_v1.json`.
<!-- V4_SOURCE_END: Gate 1: migration-initiation model -->

<!-- V4_SOURCE_BEGIN: Time to migration onset -->
### Time to migration onset

To avoid reducing activation timing to an arbitrary fixed-day threshold, we also fitted a stratified Cox proportional-hazards model. Individuals were followed from release to the distance-threshold crossing time (time_first_dist_to_use) attached to the first row with downstream_migration = TRUE; non-initiators were censored at their last available telemetry observation. We did not use the arrival time of the first broader migration = TRUE interval row as the onset clock.

The Cox model used separate baseline hazards for project × release-year strata and the same covariates as the initiation model: within-stratum body length per 100 mm, within-stratum release timing per 100 days and ordinal Durif stage. Tied event times were handled with the Breslow approximation.

The time-to-event dataset contained 570 individuals and 418 onset events across 13 project-year strata. We evaluated project dependence by repeating the stage estimate after omitting each source project in turn.
<!-- V4_SOURCE_END: Time to migration onset -->

## S2. Silvering morphometrics and continuous capture-state measurement

Measurement and coarse-classification dependence are explicit; no direct lipid/endocrine assay is available.

<!-- V4_SOURCE_BEGIN: Capture condition and activation-trained entry-state score -->
### Capture condition and activation-trained entry-state score

We derived a continuous capture condition proxy from body mass and length. Across the six focal projects, log body mass was regressed on log body length, project and capture Durif stage. The residual was standardized to one SD. This residual should be interpreted as **continuous weight-for-length information beyond the ordinal stage label**, not as an independent physiological energy-reserve measurement, because length and weight also contribute to silvering classification.

We first added this condition term to the activation model together with ordinal Durif stage. Developmental Durif × condition and Durif × length interactions were unsupported, so the multivariate interpretation is additive rather than compensatory.

To test phase transferability directly, we defined an activation-trained score:

\[
R = \hat\beta_D D + \hat\beta_C C,
\]

where \(D\) is ordinal Durif stage and \(C\) is within-stratum centered standardized capture condition. The weights \(\hat\beta_D\) and \(\hat\beta_C\) were estimated **only from the activation model**. The score was then standardized within each analysis sample and transferred without re-fitting the relative stage/condition weights to onset, whole-route speed and the frozen median positive inter-station speed endpoint.

Because the score is developed from the same source panel, this is a post-hoc cross-phase transferability diagnostic rather than prospective validation. Its purpose is not to estimate a latent physiological variable, but to ask whether an empirically activation-relevant capture-state vector behaves like a general progression-speed score.

As a cross-project robustness audit, we repeated coefficient training six times, each time withholding one entire project from the activation model. The Durif and condition weights estimated from the remaining five projects were then applied without outcome-based re-estimation to individuals in the held-out project. We concatenated these project-held-out scores and repeated the activation, onset and two progression-speed tests. This removes held-out-project outcome information from score-weight estimation, although predictor preprocessing remained panel-derived; it is therefore stronger than same-panel weight fitting but is not prospective external validation.
<!-- V4_SOURCE_END: Capture condition and activation-trained entry-state score -->

<!-- V4_SOURCE_BEGIN: Independent assessment of continuous silvering morphometrics -->
### Independent assessment of continuous silvering morphometrics

A newly identified subset of the pinned public metadata includes horizontal and vertical eye diameters and pectoral fin length alongside body mass, length and ordinal Durif class. The measurements occupy `length2`–`length4` in **project-dependent order**, which must be resolved using their accompanying measurement-type labels. One of the six focal projects (Warnow) has no recorded eye/fin measurements, whereas the remaining five have measurements for most eligible individuals. We specified a separate, explicitly post-hoc falsification audit comparing held-out initiation ranking from (i) ordinal stage, length and release date, (ii) those variables plus continuous eye and relative pectoral-fin indices, (iii) those variables plus residual condition, and (iv) those variables plus both morphology and condition. The decisive contrast is model (iv) versus (ii): does weight-for-length information add predictive value after continuous silvering morphology is available? Models use the same complete-morphology sample and project-held-out penalized logistic fits. This audit addresses *whether the ordinal class was simply too coarse*, not whether body mass represents independently measured energy stores (Sundin et al. 2022).
<!-- V4_SOURCE_END: Independent assessment of continuous silvering morphometrics -->

<!-- V4_SOURCE_BEGIN: Continuous silvering morphology did not remove all condition ranking information, but project-level certainty was limited -->
### Continuous silvering morphology did not remove all condition ranking information, but project-level certainty was limited

The pinned metadata retain typed and measured horizontal/vertical eye diameters and pectoral-fin lengths for five of the six focal projects, although measurement columns differ by project. Among the original 575 evaluable tagged fish, **429** had complete morphometrics. After leaving each of these five projects out of model training, **3,272** positive–negative initiation pairs were informative within ten held-out project-year strata.

In this identically sampled subset, the base Durif-stage, length and release-date model achieved AUC **0.706**. Adding the continuous eye index and relative fin length raised AUC to **0.716**. Adding the weight-for-length condition residual *instead* raised AUC to **0.741**. Including **both morphology and condition** yielded AUC **0.741**. Thus the incremental AUC from adding condition **after** continuous morphology was **+0.0244**, whereas adding morphology **after** condition gained only **+0.0003** in the pooled score ranking.

This does not justify interpreting condition as an independent energy-reserve trait. A post-hoc sensitivity varying the preselected L2 regularization penalty from **0.1 to 10** yielded positive condition-after-morphology increments of **+0.0269**, **+0.0244** and **+0.0214**; all corresponding five-project uncertainty intervals contained zero. Thus the pooled effect's direction was not specific to one penalty, whereas project-level portability was still unsupported.

The condition-after-morphology increment was positive in **three of five** held-out projects. Project resampling gave a 95% interval of **−0.0151 to +0.0659**; the gain remained positive under each single-project omission (**+0.0125 to +0.0349**), but it was not reliably positive across independent contexts. Moreover, the five-project subset excludes Warnow and therefore has different case mix from the preceding six-project analysis. In particular, its better baseline AUC (0.706 rather than 0.610) cannot be attributed to continuous morphology; the sample and estimation method also differ.

A stage-conditioned sensitivity on this subset yielded a +0.063 condition-after-morphology AUC increment in FIII (949 pairs) and +0.074 in FV (498 pairs), whereas FIV had only 16 pairs and no stable estimate of additional information. Thus the previously observed FV-over-FIII tendency does not establish a stage-specific energetic checkpoint.
<!-- V4_SOURCE_END: Continuous silvering morphology did not remove all condition ranking information, but project-level certainty was limited -->

## S3. Censoring and potential unobserved activation

Worst-case label reassignments are hypothetical and are not observations of erroneous source classification.

<!-- V4_SOURCE_BEGIN: Sensitivity to unobserved initiation among short-follow-up source noninitiators -->
### Sensitivity to unobserved initiation among short-follow-up source noninitiators

Because source noninitiation is defined by telemetry classification rather than independently verified residence, we performed a post-hoc, explicitly adversarial label-ambiguity sensitivity. Among 575 evaluable eels, 422 had source-classified initiation and 153 had no initiation label; **100 of the 153** lacked 90-day receiver-observation eligibility. We kept both original project-held-out logistic score vectors fixed and considered the hypothetical scenario in which exactly *k* of these 100 source noninitiators had actually initiated without an observable source classification. The remaining 53 noninitiators and all 422 source-classified initiators retained their labels. For each k, an exact rank-pair accounting identity and dynamic program identified the **minimum and maximum** possible additional AUC from the body-condition term across allowed label assignments, holding within-project-year comparisons fixed. The numerical algorithm passed exhaustive synthetic enumeration tests. This evaluates vulnerability to unverified labels, not the probability of hidden initiations; fixed original score weights are not refitted under the hypothetical labels. To locate the source of this vulnerability across ordinal maturation states, a separate exploratory, **stage-restricted** exact optimization allowed hypothetical label changes in FIII **only**, FIV **only** or FV **only**, retaining every other class's classifications and all model scores. Each stage-constrained optimum was checked against the original independent pairwise AUC calculation, with exhaustive small-data tests.

To distinguish the fragility of the *incremental continuous-state predictor* from that of the *ordinal silvering-class contrast*, we separately calculated exact, post-hoc partial-identification intervals for source-classified initiation proportions. All 422 classified initiators and 53 noninitiators satisfying the day-90 observation criterion were held fixed; the remaining 100 short-follow-up source-negative labels were allowed to be counterfactually reclassified in any configuration. For each stage and project, the sharp scenario-conditional interval is classified initiators divided by evaluable fish through classified initiators plus short-follow-up negatives divided by evaluable fish. We then compared FV and FIII rates in the pooled cohort and separately for each project, averaged the project-specific bounds under fixed equal-project and minimum-stage-sample weights, and calculated by integer arithmetic how many additional longer-observed FIII negative labels would have to be wrong to erase the pooled ordering. These are **logical observation-error sensitivity bounds**, not biological initiation probabilities, confidence intervals or estimates of actual missed departures.

To prevent finite-sample logical robustness from being confused with population inference, we conducted two exploratory resampling audits of the *lower and upper endpoints themselves*, leaving the hypothetical relabeling rules fixed. First, 10,000 resamples drew fish with replacement from the three observed source-outcome categories within each project × stage while fixing each project × stage sample size. Second, 10,000 resamples drew six entire project count tables with replacement to assess heterogeneity across waterways. We reported percentile variation of each bound endpoint, not confidence intervals for true physiological initiation. Both resampling procedures used a pre-specified deterministic random sequence and preserve the distinction between label uncertainty, within-project fish sampling and between-project context variation.
<!-- V4_SOURCE_END: Sensitivity to unobserved initiation among short-follow-up source noninitiators -->

<!-- V4_SOURCE_BEGIN: The additional condition ranking was sensitive to hypothetical hidden initiation -->
### The additional condition ranking was sensitive to hypothetical hidden initiation

A direct observation-process sensitivity found that among the **100** source-classified noninitiators without 90-day receiver support, reclassifying an **adversarially selected 11** as hypothetical undetected initiators was sufficient to move the frozen-score added AUC from **+0.0336** to approximately **−0.00016**. The exact envelope still required at least **11** such flips to reach a nonpositive increment: 10 flips gave a minimum **+0.00191**, whereas 15 could give **−0.00784**. At the eleven-fish tipping assignment, eight labels came from Warnow and one each from Leopoldkanaal, Albertkanaal and Verhelst. Other admissible 11-fish assignments can leave or enlarge the score advantage; this is a **worst-case label-contamination bound**, not a finding that eleven misclassifications occurred. It does not bound performance after retraining the models on revised labels and does not establish the actual frequency of missed migration. Nevertheless, the apparently useful continuous-state increment depends materially on distinguishing genuine noninitiation from incomplete observation. A separate post-hoc scenario audit asked whether the adversarial eleven-label tipping represented typical hypothetical missed starts. With frozen scores and exactly eleven short-follow-up source-negative labels reassigned, **10,000** uniformly selected sets had a median AUC increment of **+0.0337** (assignment 95% range **+0.0231 to +0.0446**), while a deliberately score-disagreement-enriched 3:1 selection scenario yielded **+0.0262** (**+0.0158 to +0.0374**); neither produced a nonpositive increment in 10,000 draws. The score-disagreement scenario yielded nonpositive increments in **3.25%** of 30-label draws and **23.3%** of 50-label draws. These are conditional what-if distributions under unverified assignment assumptions, not a true detection-error model. Strikingly, flipping **all 100** ambiguous negatives produces a positive increment of **+0.0683**, since relabeling also changes the composition of informative pairs. Thus the *pattern* of missed observation, not only a hypothetical rate, determines the claimed predictor advantage. In the new stage-restricted exact audit, **16 of 70** candidate FIII noninitiation labels could be chosen to nullify the original +0.0336 AUC increment, whereas **neither changing only FIV labels (13 candidates) nor only FV labels (17 candidates) could nullify it**, even with every candidate changed. At a common budget of 11 hypothetical changes, the most adverse AUC increments were still **+0.0064** for FIII only, **+0.0250** for FIV only and **+0.0212** for FV only; combining stages allowed the previous zero-crossing at 11. Notably, changing all 70 FIII short-followup negatives increased the pooled increment again to **+0.0622**: the exact location and composition of hypothetical misclassification matters more than a monotonic number of errors. This does **not** establish that FIII fish were actually misclassified or that FIII physiology causes the predictive advantage. A source-pinned physical-receiver inventory then showed that **24 of 100** short-follow-up source noninitiators had no recorded physical-receiver encounter beyond synthetic release rows, whereas **76** had at least one actual receiver encounter. Among those 76, **70** had a later detection of a *different* fish at their last known receiver within 90 days (58 within one day), indicating receiver activity at the later event but neither continuous receiver uptime nor the focal eel's residence. Restricting exact hypothetical label reassignments to the **24 receiver-unobserved fish** could **not** erase the condition AUC increment, even if all 24 were relabeled. Restricting them to the **76 with real receiver contacts** required **13** adversarial relabelings, and the original unrestricted 11-fish tipping assignment included **9 previously receiver-detected fish and 2 virtual-only fish**. The robustness boundary is therefore not simply an absence of any physical contact: the endpoint also depends on unresolved fates after partial detection. None of these counterfactual classifications establishes actual hidden initiation, mortality, tag failure or a physiological gate.
<!-- V4_SOURCE_END: The additional condition ranking was sensitive to hypothetical hidden initiation -->

<!-- V4_SOURCE_BEGIN: The pooled FV–FIII initiation ordering survived limited observability ambiguity, but was not consistent across rivers -->
### The pooled FV–FIII initiation ordering survived limited observability ambiguity, but was not consistent across rivers

Among the **100** source noninitiators without day-90 follow-up, **70** were FIII, **13** FIV and **17** FV. If any subset of only these records represented unseen initiation, the *pooled* source-classified initiation-rate intervals would be **59.0–85.8%** for FIII and **87.4–94.3%** for FV. Thus the minimum FV-minus-FIII difference remains **+1.57 percentage points**, even if every short-follow-up FIII negative was a hidden start. But this pooled ordering does not generalize across project contexts: the equal-project mean difference interval is **−6.84 to +38.67 percentage points**, two projects have strictly positive FV-minus-FIII bounds, one has a strictly negative bound and three remain indeterminate. Moreover, if the **37 longer-observed FIII source negatives** are not treated as definitive noninitiators, hypothetically relabeling only **five** of them in addition to all 70 short-follow-up FIII negatives would erase the pooled ordering. These numbers are exact *conditional bounds*, not observed hidden migration, continuous receiver operation or physiological reversals. More importantly, **the positive 1.57-point empirical lower bound is not a sampling-uncertainty guarantee**. When we additionally resampled classified starts, short-followup negatives and longer-observed negatives within each project × stage, the *lower bound endpoint* varied between **−3.91 and +6.87 percentage points** over its exploratory 95% percentile interval; resampling the six whole projects yielded **−16.65 to +17.96 points**. These are descriptive bootstrap endpoint ranges under explicit sampling assumptions, not confidence intervals for a causal silvering effect. Thus the source-sample ordering is robust only in a restricted logical sense; it is neither universally observed across rivers nor statistically guaranteed for new populations. The better-known ordinal silvering association is less sensitive than the incremental condition AUC to the narrowly defined 100-label worst-case scenario, but no universal stage effect or true biological absence is identified.
<!-- V4_SOURCE_END: The pooled FV–FIII initiation ordering survived limited observability ambiguity, but was not consistent across rivers -->

## S4. Held-out condition information, project portability and onset timing

Conditional held-out risk sets and project-level uncertainty are retained, including the changing follow-up composition.

<!-- V4_SOURCE_BEGIN: Incremental information from body condition in project-held-out initiation ranking -->
### Incremental information from body condition in project-held-out initiation ranking

In a separate exploratory test specified before inspecting the AUC comparison, we tested whether adding continuous capture condition improved activation ranking beyond Durif stage, length and release timing in completely held-out projects. For each held-out project, we fitted two nested logistic activation models on the other five projects, using the canonical nine-fish expert correction: the base model included project-year intercepts, centered length, centered release timing and ordinal Durif stage; the expanded model also included the allometric weight-for-length residual. Neither model fitted coefficients using held-out outcomes. We evaluated pairwise initiator/non-initiator concordance **within held-out project-year strata**, pooling positive–negative pairs to form a stratified AUC, since project-specific absolute-risk intercepts were not transportable. A 500-replicate within-stratum, within-outcome fish bootstrap with frozen training coefficients estimated conditional evaluation uncertainty, not uncertainty from training six independent models. A second, explicitly post-result exploratory audit resampled the **six projects**, computed leave-one-project-out pooled AUC differences and performed a 64-configuration paired sign-flip diagnostic. These latter tests assess between-project heterogeneity rather than treating 6,914 fish pairs as independent projects.
<!-- V4_SOURCE_END: Incremental information from body condition in project-held-out initiation ranking -->

<!-- V4_SOURCE_BEGIN: Horizon-controlled initiation and onset order among detected entrants -->
### Horizon-controlled initiation and onset order among detected entrants

Following the initial project-held-out condition AUC findings, we froze three further exploratory analyses of the distinction between *ever starting migration* and *how soon a participating eel starts*. First, for post-release horizons of **7, 30, 60 and 90 days**, an eel counted as an early detected event if its canonical migration-onset timestamp fell before the horizon; a no-event control required a receiver arrival at or after that same horizon. The latter rule establishes a later observation, **not continuous tracking**. Baseline and condition-augmented initiation models were trained separately for each eligible horizon population, always withholding the focal project, to measure the sensitivity of outcome-specific predictive utility to observed follow-up. This changes both training weights and case mix, and therefore cannot establish a biological sign reversal by itself.

Second, we used one **common population of 475 eels eligible at day 90** and two project-held-out models trained **only for eventual activation on the original 575 eels**. This selection retains **all 422 source-classified initiators** but only **53 of 153 source-classified noninitiators**; the other **100** lacked the requisite horizon documentation. Thus the common cohort is held constant *across horizon labels* but is not a representative or randomly selected subset of the original panel. We therefore used an exact decomposition of the change in pooled AUC gain between the original 575-fish population and this 475-fish subset into (i) changes in project-level positive–negative pair weights and (ii) within-project AUC changes, keeping original project-held-out scores frozen. As a second post-hoc observation-process sensitivity, we performed **20,000** random draws retaining all 422 initiators and the *observed number* of 90-day-eligible source noninitiators within each project-year, but randomizing which noninitiators remained. We also tested whether the existing scores rank 90-day observability among source noninitiators. These are checks on follow-up selection, not corrected survival estimates or causal mechanisms. With scores frozen, we successively classified onset by 7/30/60/90 days or eventual source initiation, evaluating within-project-year AUC at each horizon. We compared the added condition information for eventual versus day-30 initiation across the four projects having both mixed-outcome endpoint sets using an equal-project paired contrast, project resampling (10,000 repetitions) and an exploratory exact sign-flip test. Within the same population we separately compared early entrants (≤30 days), later entrants (>30 days) and those never classified as initiators. These groups are retrospective telemetry categories, not biological success/failure labels.

Because the common 90-day eligibility filter retained source initiators and removed mostly source noninitiators, we performed a separate **post-hoc observation-selection negative control** after inspecting the apparent endpoint dependence. We kept every original held-out score and eventual-initiation label fixed across all **575** source eels, verified that all 422 source initiators survived the 90-day selection, then independently drew **20,000** score-blind sets of noninitiators. Within each project × release-year stratum, each draw retained exactly the observed number of 90-day-eligible source noninitiators and all source initiators. We recalculated the pair-weighted within-stratum AUC gain from adding condition. The resulting conditional retention distribution measures the gain expected solely from thinning the source noninitiator class with the observed project-year composition, not from an additional energetic or causal receiver-retention mechanism.

Finally, among all source-classified initiators with nonnegative, reconstructable release-to-onset latencies, we evaluated **continuous onset-order concordance** within project-year: for each two initiators with distinct onset delays, did the same frozen score rank the earlier initiator higher? We compared stage, stage+condition, and nested stage/length/release-time models with and without condition, including a sensitivity excluding onset within the first post-release day. This analysis **conditions on initiation** and does not causally decompose the Cox onset hazard into latent physiological decisions.
<!-- V4_SOURCE_END: Horizon-controlled initiation and onset order among detected entrants -->

<!-- V4_SOURCE_BEGIN: Body condition supplied additional activation information beyond silvering stage, but its benefit varied among projects -->
### Body condition supplied additional activation information beyond silvering stage, but its benefit varied among projects

The six-project held-out initiation-ranking test used **575 evaluable eels** and **6,914 initiator/non-initiator pairs** across 12 informative project-year strata. A base model using Durif stage, body length and release timing achieved stratified AUC **0.610**. Adding continuous capture condition raised AUC to **0.643**, an increment of **0.0336**; its fixed-training fish-level conditional bootstrap interval was **0.0021–0.0644**. When comparisons were restricted to **3,199 pairs of eels of the same Durif stage**, AUC increased from **0.480 to 0.555**. This stage-controlled comparison shows why a continuous body-state axis can contain information masked by a coarse maturation classification, although it does not isolate an energetic mechanism.

The increment was positive in **four of six** held-out projects and negative in two. The pooled increment remained positive when any single project was removed (range **0.0136–0.0632**). However, the **six-project cluster bootstrap** gave a 95% interval of **−0.0007 to 0.0918** for the pooled pair-weighted increment; an exploratory two-sided project sign-flip test was **p=0.1875**. The 2012 Leopoldkanaal and 2013 Albertkanaal cohorts had the strongest positive increments (respectively +0.109 and +0.103), whereas ESGL was −0.065. Thus continuous condition **can improve held-out ranking in this panel**, but consistent improvement across independent rivers has **not** been established. This is neither a prospective validation nor a measure of ultimate escapement success.
<!-- V4_SOURCE_END: Body condition supplied additional activation information beyond silvering stage, but its benefit varied among projects -->

<!-- V4_SOURCE_BEGIN: Readiness information concerned observed migration participation more than onset order -->
### Readiness information concerned observed migration participation more than onset order

When both outcome definitions and models were retrained in separate horizon-eligible populations, adding condition changed held-out AUC by **−0.0263** at 7 days (n=496), **−0.0291** at 30 days (n=484), **−0.0226** at 60 days (n=478), and **+0.0021** at 90 days (n=475). The negative increments do not imply that greater body condition delays migration: the training outcome and set of tracked animals differed at every horizon, and five informative projects gave a 30-day exact sign-flip p=0.0625 despite a project-bootstrap interval below zero.

A more direct endpoint comparison kept **475 eels** and both held-out model scores unchanged. Because all **422** eventual source initiators survived the day-90 eligibility selection while **100/153** source noninitiators were excluded, the eventual-endpoint AUC in these 475 eels should not be equated with the separate 575-fish AUC, nor interpreted as evidence of differential physiology without an observability audit. Added condition AUC increased with the length of the observed endpoint: **+0.0077** by day 7, **+0.0329** by day 30, **+0.0460** by day 60, **+0.0549** by day 90, and **+0.0807** for eventual source-defined migration initiation. The equal-project mean contrast of eventual versus day-30 added AUC was **+0.0431** across **four** informative projects (project-bootstrap 95% CI **+0.0164 to +0.0697**; exact paired two-sided sign-flip **p=0.125**). Among this same cohort, **299** eels began within 30 days, **123** began later and **53** had no source-classified initiation. Condition added similar information for distinguishing early versus never classified (AUC increment **+0.0832**) and late versus never classified (**+0.0756**), but little for distinguishing early versus late initiators (**+0.0089**). The horizon signal is consequently compatible with the changing composition of an apparent noninitiator group, not demonstrated physiological waiting by high-condition fish. In particular, the larger eventual AUC increment in the day-90-selected subset is conditional on an asymmetric follow-up filter. The additional condition AUC for *the same eventual initiation label* rose from **+0.0336** in all 575 eels to **+0.0807** after the 90-day selection (difference **+0.0471**). An exact project-level accounting identity attributed **+0.0515** to the changed weights of project-specific initiator/noninitiator pairs and **−0.0044** to the within-project changes. The Warnow project's share of informative pairs dropped from **52.6% to 5.2%** while Leopoldkanaal increased from **21.1% to 53.4%**. Under 20,000 project-year-stratified *random* retentions of the same number of noninitiators, the mean expected AUC increment was **+0.0844** (95% random-retention range **+0.0606 to +0.1083**), with the observed +0.0807 unexceptional (two-sided deviation probability **0.764**). Among noninitiators alone, added condition AUC for ranking 90-day receiver observability was only **+0.0092** over 326 comparison pairs, and its signs differed among projects. Thus the inflated selected-subset condition signal did not require unusually phenotype-related retention beyond the project-year composition effect. Importantly, the 100 excluded source noninitiators had a median final receiver arrival **0.52 days** after release, compared with **549 days** among the 53 retained records; these are last-detection spans, *not continuous monitoring coverage*, and neither group is a confirmed biological nonmigrant.

The 90-day filter's composition was an important source of amplification. It retained **all 422** source-defined eventual initiators but only **53 of 153** source noninitiators; the remaining **100** had insufficient observation support, not verified failure or inactivity. The same held-out-score condition AUC increment rose from **+0.0336** in all 575 fish to **+0.0807** in the selected 475. Yet under **20,000 random, project-year-stratified draws** retaining exactly the same number of noninitiators per stratum, the expected increment was **+0.0844** (95% random-retention envelope **+0.0606 to +0.1083**). The observed **+0.0807** lay within that envelope (upper-tail probability **0.625**). Thus the increased selected-subset AUC gain did **not** require preferential retention of high- or low-condition noninitiators within project-year strata. Among source noninitiators, retained records had a median last-observation interval of **549 days**, versus **0.52 days** for excluded records; this contrast flags profound differences in recorded follow-up, not continuous tracking or a biological survival contrast. The positive classification AUC in the selected subset cannot therefore be promoted as evidence that capture condition becomes physiologically more important over time.

Directly examining the order of observed onset among **422 initiated eels** gave **10,756** informative within-project-year onset-order pairs. Baseline stage/length/release-time concordance was **0.5446** and became **0.5461** after adding condition, an increment of **+0.0015** (six-project bootstrap 95% CI **−0.0237 to +0.0202**, exploratory project sign-flip **p=0.9375**). Excluding starts within 24 hours left 291 initiators and reduced the incremental concordance to **−0.0086**. Stage-specific median detected onset delays among entrants were 7.21 days (FIII) and 2.14 days (FIV and FV), but median differences do not identify individual energetic readiness or distinguish hydraulic cue timing. Capture condition therefore provided much more information about *membership of the initiating group* than about *onset ordering within that selected group*.
<!-- V4_SOURCE_END: Readiness information concerned observed migration participation more than onset order -->

## S5. Transit-speed reliability and conditional progression endpoints

Retains the original observational progression cohort and severe source ground-speed limitations; no speed null is an equivalence test.

<!-- V4_SOURCE_BEGIN: Within-link realized transit-speed audit -->
### Within-link realized transit-speed audit

To test whether the weak progression signal was created by averaging across unlike routes, we froze a developmental within-link audit before inspecting its coefficient. An initial implementation was subsequently corrected to exclude the nine pre-existing expert-classified 2015 non-migrants, consistent with the canonical activated cohort. We used the project-held-out entry-state score and source positive `speed_m_s` values only when both the current and immediately preceding rows for an eel were classified `migration = TRUE` and the station identity changed. Each directed receiver-to-receiver pair was treated as a fixed route link. The primary model required at least five unique eels per directed pair, included directed-pair and project × release-year fixed effects plus body length and release timing, weighted segment rows so that each eel contributed total weight one, and used fish-clustered sandwich standard errors. Pair-support thresholds of three and ten eels, unweighted segment rows and leave-one-project-out fits were frozen sensitivities.

The source `speed_m_s` field is a last-detection-to-first-detection ground-speed calculation and, after the frozen primary was run, was found to contain biologically impossible values. We therefore registered an explicitly post-hoc data-quality sensitivity rather than changing the primary endpoint. A laboratory sample of female European silver eels showed mean Ucrit 0.94 m s\(^{-1}\) and Uopt 0.64 m s\(^{-1}\) (Tudorache et al. 2015), but these sustained-swimming measurements are not universal maxima for field-derived ground speeds. The broad swimming-performance database of Katopodis and Gervais (2016) also does not establish a verified 2.26 m s\(^{-1}\) maximum for this source field. Accordingly, we treated 2.5, 5 and 10 m s\(^{-1}\) as explicitly heuristic, increasingly permissive gross-artifact screens, not species-specific physical cutoffs. The same primary model was re-fitted at each cutoff as post-hoc sensitivity, and the all-positive-speed analysis remains the frozen primary.
<!-- V4_SOURCE_END: Within-link realized transit-speed audit -->

<!-- V4_SOURCE_BEGIN: Post-initiation migration speed -->
### Post-initiation migration speed

As a continuous progression metric independent of the binary completion endpoint, we reproduced the source study's overall migration-speed definition. For each expert-corrected initiated individual, speed was calculated over source migration rows as:

\[
\mathrm{speed}
=
\frac{
\max(\mathrm{distance\ to\ source})
-\min(\mathrm{distance\ to\ source})
}{
\max(\mathrm{departure})
-\min(\mathrm{arrival})
}.
\]

We modelled log migration speed with project × release-year fixed effects, within-stratum body length, within-stratum release timing and ordinal Durif stage. Informative project-year strata were required to contain at least eight initiated individuals and at least two Durif stages.
<!-- V4_SOURCE_END: Post-initiation migration speed -->

<!-- V4_SOURCE_BEGIN: Progression falsification and selection diagnostics -->
### Progression falsification and selection diagnostics

Because a weak stage-speed coefficient could arise for several reasons other than a genuine phase difference, we ran three developmental diagnostics after the primary result was known.

First, we tested whether the pooled coefficient concealed strong opposing project effects and repeated progression at the individual median positive inter-station speed scale. Second, we tested a capture-stage-staleness alternative by fitting a Durif × release-to-activation-latency interaction and by re-estimating the stage-speed coefficient among eels activating within 1, 3 and 7 days.

Third, we audited selection induced by conditioning on activation. We compared initiators and non-initiators within capture stage on body length and a descriptive log-weight residual after length, project and stage adjustment. We then fitted the canonical initiation model to obtain individual fitted activation probabilities. Among speed-bearing initiators with estimable propensities, we refitted the same stage-speed model using inverse-probability weights (1/hat p_i). This weighting is a selection diagnostic only: speed is undefined for non-initiators, so the analysis cannot identify counterfactual post-activation speed for animals that never crossed the activation gate.
<!-- V4_SOURCE_END: Progression falsification and selection diagnostics -->

<!-- V4_SOURCE_BEGIN: Terminal positive-set membership sensitivity -->
### Terminal positive-set membership sensitivity

The source workflow created a file of eels positively observed at project-specific terminal/sea endpoints using water-body-specific station or distance rules.

The Europe-wide source paper explicitly did not analyse escapement success rate because interpreting non-observation at these endpoints would require additional assumptions about fishing, terminal detection loss, release position and study-specific monitoring geometry.

We therefore retained terminal-set membership only as a **secondary sensitivity endpoint** among activated eels. Its complement was not interpreted as validated biological failure.

The sensitivity model used the same project × release-year structure, within-stratum body-length adjustment, within-stratum release-timing adjustment and ordinal Durif coding as the activation model.
<!-- V4_SOURCE_END: Terminal positive-set membership sensitivity -->

<!-- V4_SOURCE_BEGIN: Terminal-endpoint phase contrast — sensitivity only -->
### Terminal-endpoint phase contrast — sensitivity only

For audit continuity, we retained the previously developed stacked initiation-versus-terminal-membership model with individual-clustered uncertainty.

Because the second binary response is observability dependent, this contrast is not used as the principal test of phase-specific control in V4.

Its role is limited to asking whether the direction of the stage association differs when the same positive terminal-set definition is used across projects. It must not be interpreted as a direct comparison of biological initiation probability with biological failure probability.
<!-- V4_SOURCE_END: Terminal-endpoint phase contrast — sensitivity only -->

<!-- V4_SOURCE_BEGIN: Entry state did not rank realized speed within identical route links -->
### Entry state did not rank realized speed within identical route links

The exact-link audit retained 17,792 positive segment rows from 418 eels across 244 directed station pairs with at least five unique fish per pair. With each eel contributing total weight one, the project-held-out entry-state score had a within-link speed ratio of **0.962 per SD** (95% CI **0.883–1.048**; p=**0.372**) and weighted partial R² of **0.0003815** (approximately **0.0382%**).

The result was insensitive to the prespecified pair-support threshold: ratios were **0.956** for at least three fish per link and **0.999** for at least ten. Leave-one-project-out estimates ranged from **0.933 to 1.013**, crossing both sides of one. Thus the absence of a positive speed ranking is not explained by pooling eels across different receiver-to-receiver geometries.

The raw source segment-speed field nevertheless had a serious quality boundary: the frozen primary candidate rows included values up to **3752 m s\(^{-1}\)**. The first implementation accidentally included nine fixed expert-classified non-migrants; all within-link estimates now reported use the corrected 422-eel candidate migratory universe, with 418 eels retained after the link-support filter. Externally motivated post-hoc screens therefore removed speeds above 2.5, 5 or 10 m s\(^{-1}\), which removed **63.1%**, **58.6%** and **53.0%** of candidate segment rows, respectively. Despite this large data-quality correction, the fish-equal within-link ratios remained **0.942**, **0.944** and **0.941**, with all 95% intervals spanning one. All three post-hoc filtered point estimates are negative, with p approximately 0.07–0.08, although none of their 95% intervals excludes one. Thus these estimates do not establish a negative speed gradient, nor do they establish a precisely zero effect. The near-null primary finding is robust to grossly implausible source-speed artifacts, although the raw segment-speed field should not be treated as a direct physiological swimming measurement. A separate Frisch–Waugh–Lovell SVD absorption analysis reproduced the corrected fixed-effects coefficient within 4×10\(^{-14}\), supporting numerical stability despite high-dimensional nuisance collinearity.

Thus a capture-state vector optimized only for entry into migration retained information about **when** migration began but essentially no general information about **how fast** activated eels progressed under either generic speed summary or within identical receiver-to-receiver links.
<!-- V4_SOURCE_END: Entry state did not rank realized speed within identical route links -->

<!-- V4_SOURCE_BEGIN: Terminal positive-set membership showed a weak general stage gradient -->
### Terminal positive-set membership showed a weak general stage gradient

Among activated eels, ordinal Durif stage showed a weak association with membership in the source study's project-specific terminal positive set (adjusted OR 1.15, 95% CI 0.83–1.59; p = 0.412).

Because non-membership can reflect censoring, fishing, detection loss and route-specific monitoring geometry, this result is reported as a sensitivity analysis rather than as an estimate of migration completion probability.
<!-- V4_SOURCE_END: Terminal positive-set membership showed a weak general stage gradient -->

<!-- V4_SOURCE_BEGIN: Post-initiation migration speed showed no general Durif gradient -->
### Post-initiation migration speed showed no general Durif gradient

Among 418 initiated eels retained in informative project-year strata, median migration speeds were 0.0229 m s\(^{-1}\) for FIII, 0.0232 m s\(^{-1}\) for FIV and 0.0245 m s\(^{-1}\) for FV.

After adjustment, the multiplicative change in migration speed per Durif-stage increment was 0.983 (95% CI 0.852–1.134; p = 0.815). This continuous progression result does not require terminal non-observations to be classified as biological failures.
<!-- V4_SOURCE_END: Post-initiation migration speed showed no general Durif gradient -->

<!-- V4_SOURCE_BEGIN: Terminal-endpoint phase contrast was directionally consistent but sensitivity-only -->
### Terminal-endpoint phase contrast was directionally consistent but sensitivity-only

The stacked sensitivity model yielded a larger stage coefficient for activation than for terminal positive-set membership (OR ratio 1.81, 95% CI 1.15–2.84; p = 0.0099), with the same direction in all six leave-one-project-out analyses.

This contrast is retained for reproducibility but is not manuscript-primary because the terminal binary response does not provide a validated failure state.

The independent post-activation speed analysis provides the primary progression evidence without requiring that assumption.
<!-- V4_SOURCE_END: Terminal-endpoint phase contrast was directionally consistent but sensitivity-only -->

## S6. Project heterogeneity and route opportunity

Source-project effects are observational, dependent on release-year composition, source receiver coverage and one influential waterway.

<!-- V4_SOURCE_BEGIN: Project-level route-context diagnostic -->
### Project-level route-context diagnostic

To ask whether broad route context aligned differently with the two gates, we used the source study's water-regulating-structure (WRS) impact score. For each of the six projects we calculated the median WRS impact among focal stage-coded individuals and compared it with migration initiation and completion among initiators.

Associations were summarized by Spearman rank correlation. With only six projects, two-sided exact permutation p-values were calculated by enumerating all 6! assignments.

This analysis was explicitly treated as **contextual bridge evidence**, not causal inference: WRS intensity is strongly confounded with project identity, hydrology, barrier type, telemetry design and endpoint observability.
<!-- V4_SOURCE_END: Project-level route-context diagnostic -->

<!-- V4_SOURCE_BEGIN: Year-conditioned silvering associations differed across projects, with one influential river -->
### Year-conditioned silvering associations differed across projects, with one influential river

The six-project exact FV/FIII test rejected a common source-classified initiation association without conditioning on release year (LR 26.170, exact p=0.000141). The stricter analysis conditioned on **14 project × release-year margins** (11 containing informative stage contrasts) across the **507 FIII/FV fish**. It still rejected a single common association (LR **19.087**, exact conditional **p=0.003142** over **46,116** admissible joint configurations). Five of six year-adjusted leave-one-project-out analyses retained p < 0.05, but exclusion of Albertkanaal raised p to **0.05310**. The result therefore establishes observational heterogeneity not explained solely by release-year baseline differences, while the strength of that heterogeneity is materially dependent on Albertkanaal. Year conditioning cannot adjust river-specific receiver coverage, tracking protocols, barrier opportunities, animal selection or unobserved migration; it does not show that water flow or a distinct silvering physiology causes the differences.
<!-- V4_SOURCE_END: Year-conditioned silvering associations differed across projects, with one influential river -->

<!-- V4_SOURCE_BEGIN: Project-level route context was associated with terminal positive-set membership, not activation -->
### Project-level route context was associated with terminal positive-set membership, not activation

Across six project contexts, median WRS impact was essentially unrelated to migration activation (Spearman \(\rho=0.029\), exact p = 0.983).

Median WRS impact was negatively associated with terminal positive-set membership among activated eels (\(\rho=-0.928\), exact p = 0.022).

Because the terminal response is observability dependent and only six non-randomized project contexts are available, this is contextual bridge evidence only. It is not interpreted as a WRS effect on biological completion probability.
<!-- V4_SOURCE_END: Project-level route context was associated with terminal positive-set membership, not activation -->

## S7. Dutch independent barrier opportunity test

Independent Dutch data refute one proposed conditional-opening mechanism only; sparse and nonconvergent estimates are not promoted as biological effects.

<!-- V4_SOURCE_BEGIN: Independent Dutch consecutive-barrier falsification -->
### Independent Dutch consecutive-barrier falsification

We re-analysed the public DANS archive associated with van Rijn, Kuipers and Huisman (2026; DOI 10.17026/LS/WTSUNG). The archive contains raw acoustic detections, receiver metadata, individual biometrics, opening-event tables and a variable codebook.

The source study defined passage-opportunity eligibility partly from whether an eel could physically reach the barrier during an opening event; event duration therefore contributes to the source `valid` flag. Because our mechanism test used opening duration as an exposure, we did **not** use the source valid flag for primary risk-set inclusion.

Instead, for each eel and barrier we used source-derived observed barrier arrival (`SewerArrival`), opening-event start (`Firstquarter`) and confirmed passage time (`PassageTime`). The primary matched choice set contained events satisfying:

\[
\mathrm{arrival} \leq \mathrm{event\ start} \leq \mathrm{passage\ time}.
\]

Event duration (`OutletTimeTotal`) was then used only as a predictor. The pumping-station risk set yielded 14 informative fish (2 FIII, 12 FIV/FV) and the tidal-sluice risk set 15 fish (4 FIII, 11 FIV/FV).

The primary mechanistic prediction was that better capture condition would increase dependence on longer opening windows after barrier arrival. We tested condition × log event duration in eel-stratified conditional choice models. Because the stage composition was sparse, readiness × duration was treated as secondary. We also tested a broader arrival-defined waiting response in all eventual passers: number of non-passage opening events after arrival and elapsed hours from arrival to confirmed passage. Permutation tests were used for the small-sample condition associations.

This Dutch analysis is an independent developmental test of a proposed post-activation mechanism, not a replication of the Europe-wide activation model.
<!-- V4_SOURCE_END: Independent Dutch consecutive-barrier falsification -->

<!-- V4_SOURCE_BEGIN: Arrival-defined Dutch tests did not support condition-dependent barrier selectivity -->
### Arrival-defined Dutch tests did not support condition-dependent barrier selectivity

The Dutch public archive allowed the proposed passage-selectivity mechanism to be tested after observed barrier arrival rather than through the source duration-dependent opportunity definition.

At the tidal sluice, the condition × duration interaction was near zero (β=−0.095; p=0.841; permutation p=0.849). At the pumping station, the fitted interaction was strongly negative, opposite to the positive preregistered prediction, but the model was near-separated and non-converged with enormous uncertainty and therefore was not interpreted as a biological negative effect.

The broader arrival-defined waiting analysis likewise showed no evidence that better-conditioned eels waited through more opening events after reaching a barrier. At the pumping station, condition was unrelated to missed post-arrival events (Spearman r=0.009; permutation p=0.960) or delay to passage (r=0.072; p=0.677). At the tidal sluice, the corresponding associations were r=−0.104 (p=0.592) and r=−0.182 (p=0.350). Adjusting for body mass, readiness, arrival calendar time and release group did not reveal hidden positive associations.

Thus the independent Dutch analysis **did not support the specific prediction** that higher capture condition generally favours longer opening windows or greater post-arrival waiting. Given the small number of informative matched-choice fish and the unstable pumping-station model, this should not be interpreted as proving the mechanism impossible.

---
<!-- V4_SOURCE_END: Arrival-defined Dutch tests did not support condition-dependent barrier selectivity -->

## S8. Reproducibility, evidence class, ethics and limitations

Full V4 evidence classification, source/data/code availability and limitations retained.

<!-- V4_SOURCE_BEGIN: Evidence class -->
### Evidence class

All Europe-wide analyses are secondary analyses of public data and were developed after inspection of source outcomes. They are therefore described as **developmental independent evidence**, not preregistered or response-blind confirmation. The Dutch archive provides independent developmental falsification of a proposed condition-dependent passage-selectivity mechanism; it does not constitute a direct replication of the Europe-wide phase model.

---
<!-- V4_SOURCE_END: Evidence class -->

<!-- V4_SOURCE_BEGIN: Data availability -->
## Data availability

The primary Europe-wide telemetry products and analysis code are publicly available through the source study repository and associated data release reported by Verhelst et al. (2025). This study uses processed metadata and project-level migration products without modifying the source migration classifier.

The independent Dutch consecutive-barrier reanalysis uses the public archive associated with van Rijn et al. (2026), DOI 10.17026/LS/WTSUNG.
<!-- V4_SOURCE_END: Data availability -->

<!-- V4_SOURCE_BEGIN: Code availability -->
## Code availability

All secondary-analysis code, claim boundaries and reproducible analysis definitions for this manuscript are maintained in the zuizui0223/azores repository. Canonical analyses include migration activation, stratified onset, the activation-trained multivariate entry-state score, whole-route and frozen inter-station speed transferability tests, activation-selection diagnostics, and the independent Dutch arrival-defined falsification analysis.
<!-- V4_SOURCE_END: Code availability -->

<!-- V4_SOURCE_BEGIN: Ethics statement -->
## Ethics statement

No animals were newly captured or handled for the present secondary analysis. Animal-handling and telemetry approvals belong to the original source studies and should be cited from those publications in the final submission.
<!-- V4_SOURCE_END: Ethics statement -->

<!-- V4_SOURCE_BEGIN: Limitations -->
### Limitations

Several limitations define the scope of inference.

First, these are secondary developmental analyses of public data, not preregistered tests. The 90-day observation audit itself is post-hoc and inherits the source classification. The short final-detection spans of many noninitiators make the migration-entry endpoint partially dependent on observability and source processing; true nondeparture, later departure, receiver dropout and unobserved mortality cannot be discriminated without additional data. Source outcomes were inspected during programme development.

Second, migration activation is an algorithmic telemetry classification rather than a directly observed physiological decision time. We inherited the source thresholds and expert corrections to avoid outcome-driven redefinition.

A key measurement dependency limits physiological interpretation: the Durif silvering index is partly built from body mass, body length, eye diameters and pectoral fins (Durif et al. 2005; Sundin et al. 2022). Accordingly, weight-for-length condition may recover variation lost when a continuous multivariate classification is reduced to FIII/FIV/FV. The pinned source metadata permitted a completed five-project morphology-controlled sensitivity on 429 fish, but do not measure lipid content or endocrine readiness. Its remaining positive pooled condition AUC increment (+0.0244) was heterogeneous and its project-bootstrap interval included zero. The morphological categories describe premigrant FIII and migrating FIV/FV phenotypes, not verified telemetry outcomes. The stronger condition-associated FV ranking, if replicated, cannot by itself be interpreted as an energetic checkpoint.

The post-hoc temporal decomposition does not represent an unbiased migration hazard. In the 90-day negative-control experiment, all 422 source initiators survived selection whereas 100 of the 153 source noninitiators were removed. A score-blind, project-year-stratified negative-label thinning experiment could reproduce the observed selected-cohort condition AUC, so no increased physiological conditional effect is inferred from this selected subset. In its stricter 90-day common-cohort analysis, **100 of 575** original eels lacked the required observation support, while first-onset cases could enter despite earlier loss of tracking. The 53 remaining no-initiation records are not verified never-migrators. The small matched-project sample and selecting only migration initiators for onset-order comparison preclude inferring an individual-level causal delay mechanism.

The incremental held-out AUC analysis also has only six independent project contexts. A further exact sensitivity found that hypothetical false-negative labels among 11/100 source-noninitiators with inadequate 90-day follow-up can erase the frozen-score added AUC under a worst-case assignment. This is a vulnerability bound, not an estimated false-negative rate or a corrected estimate of the biological initiation effect. Its fish-resampling interval treats training weights as fixed, whereas the wider project-resampling interval includes zero. Therefore the AUC gain is evidence of potential additional information in the study panel, not a guarantee of gain in a new river.

Third, the source projects differ in hydrology, barriers, telemetry design and monitoring extent. Project-year adjustment controls baseline differences but does not make route contexts exchangeable. The post-hoc exact year-stratified FV/FIII heterogeneity result is Albertkanaal-sensitive, and its initiation endpoint remains dependent on the source telemetry classification and observation process.

Fourth, the terminal positive set is not a validated binary escapement-success variable. The source meta-analysis explicitly avoided estimating escapement success rate because non-observation can reflect fishing, detection loss, release geometry and other study-specific processes. Terminal-set analyses and the former stacked phase OR-ratio are therefore sensitivity results only.

Fifth, a weak general Durif effect on post-activation speed does not prove that internal traits cease to matter. Project-specific and finer-scale progression audits did not reveal a hidden transferable stage gradient, and a simple capture-stage-staleness diagnostic was unsupported, but all three are developmental analyses with finite precision. The staleness audit is especially indirect because individuals were staged only at capture rather than repeatedly through migration. The River Test study further shows that silvering stage can contribute to a different, reach-level post-activation progression model.

Sixth, post-activation speed is only defined for animals that entered the classified migratory state. Because activation probability differs strongly among FIII, FIV and FV, conditioning on activation creates a stage-dependent selected population. Observed-trait and inverse-probability diagnostics show that this selection is real but do not recover a strong stage-speed gradient after adjustment for measured activation predictors. They cannot remove selection on unmeasured latent readiness, so the post-activation coefficient is a descriptive ranking among entrants rather than a causal estimate of how a fixed stage effect attenuates in all tagged eels.

Finally, the Dutch consecutive-barrier and River Test studies constrain the interpretation but are not formal replications of the Europe-wide model. Their main value is to test where route-specific progression can retain or lose information from internal readiness. The Dutch reanalysis is retained as an independent falsification of one proposed passage-selectivity mechanism rather than as positive evidence for a universal control handoff.
<!-- V4_SOURCE_END: Limitations -->

## Supplementary evidence boundaries and release checks

These sections preserve the original V4 analysis narrative and are not new empirical replications. The primary V5 estimands remain the activation-trained score, onset and two separate conditional speed responses. A near-null measured transit coefficient does not prove zero physiological contribution. Dutch arrival-defined barrier data constrain only the proposed condition-dependent window selection/waiting hypothesis.

- The displayed V4 source sections include post-hoc tests. Do not label their sensitivity rules prospectively registered, and do not present hypothetical missed starts as documented source classification errors.
- Receiver-based downstream migration is a source algorithm classification. Nonclassification is not evidence of death, permanent nonmigration or failed escapement.
- The route WRS/terminal-positive-set project correlation is not a causal river/hydraulic effect.
- Original-source animal ethics approval details and the complete verified full-length reference list require a final author and journal-format review before submission.
- Frozen source numbers: [V4 numeric contract](MANUSCRIPT_NUMERIC_CONTRACT_V4.json) and [V4 figure data](FIGURE_DATA_CONTRACT_V4.json). The original [full V4 references](AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md) remain the bibliographic authority pending verification.
