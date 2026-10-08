# A multivariate entry state predicts migration activation but not realized transit speed in European eel

**Manuscript draft V4 — multivariate entry-state revision**

**Authors:** [to be completed]

**Affiliations:** [to be completed]

## Abstract

Animal migration requires both entry into a migratory state and subsequent progression through a heterogeneous route, but capture-time phenotype is often treated as a general measure of movement performance. We tested whether the internal state that predicts entry into seaward migration in European eel (*Anguilla anguilla*) remains predictive after migration has begun. We analysed public telemetry products from six European projects with female Durif stages FIII–FV and a common movement-based migration classification.

Ordinal Durif stage strongly predicted migration activation and onset. In a multivariate activation model, each Durif-stage increment increased activation odds 2.13-fold (95% CI 1.60–2.84), while a continuous weight-for-length condition measure retained an additional 1.46-fold effect per SD (1.16–1.83). We therefore trained an **entry-state score** from these two capture predictors using activation only. Per SD, this frozen score predicted migration activation strongly (OR 2.23, 95% CI 1.70–2.92) and transferred to earlier behavioral onset (HR 1.32, 95% CI 1.17–1.49; 418 events).

The same score did not transfer as a general progression-speed ranking after activation. Among 418 activated eels, its whole-route speed ratio was 0.946 per SD (95% CI 0.832–1.076; p=0.396; partial R²=0.18%). For the independently frozen per-eel median positive inter-station speed endpoint (n=411), the ratio was 1.028 (0.869–1.215; p=0.750; partial R²=0.026%). Durif stage alone showed the same boundary: strong activation/onset effects but no transferable whole-route speed gradient.

A project-held-out robustness analysis preserved this boundary. When the Durif and condition weights were re-estimated while withholding each project in turn, the cross-fitted score still predicted activation (OR 1.97 per SD, 95% CI 1.53–2.53) and onset (HR 1.26, 1.12–1.42), but not whole-route speed (ratio 0.948, 0.836–1.075) or frozen inter-station speed (1.013, 0.860–1.192).

A separate project-held-out discrimination test asked whether condition added predictive ranking beyond Durif, body length and release timing. Within release-year strata, AUC increased from **0.610 to 0.643**, but improvement was positive in only four of six projects; project-resampling uncertainty included zero. A stricter five-project subset with direct eye and fin measurements showed that condition increased AUC from **0.716 to 0.741** after continuous morphology was included, but the project-bootstrap 95% interval for this **+0.024** increment (−0.015 to +0.066) also included zero. A separate timing decomposition found that condition added **+0.033 AUC** for onset by day 30 and **+0.081** for eventual migration classification in a common 475-eel cohort scored with the same held-out models. However, this cohort retained all 422 source initiators but excluded 100 of 153 source noninitiators: random, project-year-stratified thinning of these negative labels generated a mean added AUC of **+0.084** (20,000 resamples), so the larger selected-cohort value did not require selective retention by phenotype. Among 422 initiators, condition improved ranking of onset order by only **+0.0015 C-index**. This cautions against equating onset-hazard association with faster onset among animals that initiate. Moreover, the greater eventual AUC increment after 90-day selection was explained algebraically by shifts in river-specific comparison weights; stratified random exclusion of the same number of noninitiators reproduced its magnitude. An exact-link audit likewise found essentially no realized transit-speed gradient. Comparing 17,792 positive movement segments from 418 eels within 244 identical directed receiver links, while giving each eel equal total weight, yielded a speed ratio of 0.962 per SD of the project-held-out entry-state score (95% CI 0.883–1.048; p=0.372). The source segment-speed field contained grossly implausible values, but post-hoc external-plausibility screens at 2.5, 5 and 10 m s\(^{-1}\) left the ratio at 0.941–0.944 with all intervals spanning one.

We also used an independent Dutch public archive to test a candidate mechanism for the weak post-activation relationship. After reconstructing duration-independent barrier risk sets from observed arrival times and opening-event timestamps, better body condition did not predict more post-arrival missed opportunities, longer barrier delay, or stronger selection for longer opening windows. Thus a general condition-dependent barrier-selectivity mechanism was not supported.

These results identify a **phase-specific transferability boundary** in migratory phenotype: capture state strongly ranks the transition into migration and its timing, but the same multivariate entry state is not a general ranking of subsequent movement speed. Migration readiness should therefore be treated as an entry-state property rather than a universal progression-speed score.

**Keywords:** *Anguilla anguilla*; animal movement; migration; silvering; Durif stage; body condition; internal state; telemetry; phase-specific control; movement ecology

## Introduction

Animal movement emerges from a dynamic interaction between internal motivation, the capacity to move and navigate, and the external environment through which movement is realised (Nathan et al. 2008). For migration, that interaction unfolds sequentially. An animal must first enter a migratory state, then move through a route whose hydrology, barriers, habitat geometry and temporal windows of opportunity can permit, delay or prevent further progress. Nevertheless, migration is often analysed using a single endpoint such as departure, speed, arrival or final success. Pooling these phases can obscure whether the same biological variables control the decision to begin moving and the fate of movement after it has begun.

This distinction is already implicit in movement theory. Internal state, navigation capacity and motion capacity are separate components of the movement-ecology framework, while physiological reviews emphasize that body condition can influence both switches between movement modes and movement efficiency (Winkler et al. 2014; Goossens et al. 2020). Across taxa, better body condition is often associated with faster or more efficient integrated migration, creating a natural expectation that a phenotype predicting migratory departure should also predict subsequent movement performance. Some telemetry studies make that coupling explicit: in red knots, capture condition was associated with departure decisions, faster ground speed and shorter stopovers (Duijns et al. 2017), while energetic state influenced both migration initiation and migration speed in brown trout in age- and scale-dependent ways (Shry et al. 2019). Whether such cross-phase coupling holds when the **same capture phenotype is followed across successive migration phases** remains less clear.

European eel (*Anguilla anguilla*) offers an unusually informative system in which to separate these phases. The continental growth phase ends with silvering, a coordinated suite of morphological and physiological changes associated with preparation for the oceanic spawning migration. Durif et al. (2005) classified females into growth, pre-migrant and migrating stages; FIII represents a pre-migrant state, whereas FIV and FV represent progressively silvered migrating states. Because this stage is measured from the animal rather than inferred from its later telemetry path, it provides an internal-state axis that can be compared with subsequent realised movement.

At the same time, downstream migration takes place through strongly heterogeneous landscapes. Eels may move through free-flowing river reaches, canals, navigation structures, pumps, weirs, hydropower facilities and tidal sluices. Flow, rainfall, darkness and lunar conditions can alter migration timing, while water-regulating structures can impose substantial delay or restrict passage (Verhelst et al. 2025; Huisman et al. 2023; van Rijn et al. 2026). The Europe-wide biotelemetry synthesis of Verhelst et al. (2025), which combined 2,306 tagged eels from 18 water bodies, showed both broad geographic pattern and substantial within-system plasticity in seaward migration. It also developed a common movement-based classifier to harmonise migration identification across heterogeneous telemetry projects.

These features allow a more specific question than whether internal state and external environment both matter. We ask **whether the phenotype that predicts entry into migration is also a general measure of subsequent movement performance**. Durif stage provides a biologically interpretable axis of silvering, but it is ordinal and compresses multiple morphometric changes into discrete classes. We therefore also asked whether continuous weight-for-length state retains information beyond the Durif label.

This produces a stronger phase test than a Durif-only comparison. If capture phenotype represents a general progression-quality axis, then a multivariate state vector that strongly predicts migration activation should also rank movement speed after activation. In contrast, if capture phenotype primarily represents readiness to enter the migratory mode, the same state vector should transfer from activation to behavioral onset but need not transfer to generic post-activation speed.

We first quantified the independent contributions of ordinal Durif stage and continuous capture condition to migration activation. We then froze their activation-derived coefficients as an **entry-state score** and transferred that score, without re-optimizing its weights, to three downstream responses: time to behavioral onset, whole-route migration speed and a separately frozen individual median positive inter-station speed endpoint.

Finally, we used the public archive from a Dutch consecutive-barrier study as an independent mechanism test. We reconstructed passage-event risk sets after observed barrier arrival without using event duration to define eligibility, then tested whether better-conditioned eels preferentially used longer opening windows or accumulated more post-arrival waiting. This test was allowed to falsify, rather than merely corroborate, the proposed mechanism.

We predicted that (1) Durif stage and capture condition would additively predict entry into migration, (2) an activation-trained entry-state score would predict both activation and onset, and (3) the same score would show little transferable association with generic movement speed after activation. We treated the Dutch barrier-selectivity hypothesis as a separate mechanistic prediction rather than a requirement for the core phase-transferability result.

---

## Methods

### Data provenance and study scope

We used openly available processed telemetry products and metadata from the Europe-wide European eel biotelemetry synthesis of Verhelst et al. (2025). The source synthesis assembled data from 18 water bodies in nine countries and included 2,306 tagged eels tracked using acoustic telemetry or the Nedap Trail System. Our analysis did not attempt to reproduce the entire continental meta-analysis. Instead, we selected the subset for which three conditions were simultaneously met:

1. an exact female Durif stage of FIII, FIV or FV was recorded at capture;
2. a public project-level migration table generated with the common source classifier was available; and
3. body length and release date were available for the prespecified adjustment models.

Six projects met these criteria: Warnow, Leopoldkanaal, Albertkanaal, the Scheldt-related 2015 phd_verhelst_eel project, Grote Nete and ESGL.

We treated the source data-processing decisions as fixed provenance. We did not re-tune the movement classifier, reconstruct alternative trajectories, or alter source-project expert judgements after inspecting our endpoints.

### Sample-flow and quality boundary

Within the six focal projects, 603 metadata records had primary female stages FIII–FV before applying the source project's cleaned migration-table availability. The public migration tables contained 575 evaluable stage-coded tracks.

We did not classify metadata individuals absent from the cleaned migration tables as non-migrants. An audit of the upstream cleaning code showed that 27 of the 28 absent individuals had been explicitly removed for reasons including taxonomic mismatch, translocation, implausible or short tracks, or source-defined track quality. The remaining individual had only a release record and no post-release detection in the cleaned residency data. These individuals were therefore outside the evaluable movement universe.

The source processing also identified nine classifier-positive eels from the 2015 project as non-migratory by expert judgement. We preserved these nine corrections unchanged in all primary initiation and phase analyses. Algorithm-only results before those expert corrections were retained as sensitivity analyses but were not used for the manuscript's primary estimates.

### Durif stage

We treated female Durif stage as an ordinal internal-state predictor:

\[
\mathrm{FIII}=0,\qquad \mathrm{FIV}=1,\qquad \mathrm{FV}=2.
\]

This ordering follows the biological silvering framework in which FIII is pre-migrant and FIV–FV are migrating stages (Durif et al. 2005). FII, MII, coarse silver labels and records with missing life stage were excluded from the primary ordinal comparison rather than pooled post hoc.

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

### Incremental information from body condition in project-held-out initiation ranking

In a separate exploratory test specified before inspecting the AUC comparison, we tested whether adding continuous capture condition improved activation ranking beyond Durif stage, length and release timing in completely held-out projects. For each held-out project, we fitted two nested logistic activation models on the other five projects, using the canonical nine-fish expert correction: the base model included project-year intercepts, centered length, centered release timing and ordinal Durif stage; the expanded model also included the allometric weight-for-length residual. Neither model fitted coefficients using held-out outcomes. We evaluated pairwise initiator/non-initiator concordance **within held-out project-year strata**, pooling positive–negative pairs to form a stratified AUC, since project-specific absolute-risk intercepts were not transportable. A 500-replicate within-stratum, within-outcome fish bootstrap with frozen training coefficients estimated conditional evaluation uncertainty, not uncertainty from training six independent models. A second, explicitly post-result exploratory audit resampled the **six projects**, computed leave-one-project-out pooled AUC differences and performed a 64-configuration paired sign-flip diagnostic. These latter tests assess between-project heterogeneity rather than treating 6,914 fish pairs as independent projects.

### Sensitivity to unobserved initiation among short-follow-up source noninitiators

Because source noninitiation is defined by telemetry classification rather than independently verified residence, we performed a post-hoc, explicitly adversarial label-ambiguity sensitivity. Among 575 evaluable eels, 422 had source-classified initiation and 153 had no initiation label; **100 of the 153** lacked 90-day receiver-observation eligibility. We kept both original project-held-out logistic score vectors fixed and considered the hypothetical scenario in which exactly *k* of these 100 source noninitiators had actually initiated without an observable source classification. The remaining 53 noninitiators and all 422 source-classified initiators retained their labels. For each k, an exact rank-pair accounting identity and dynamic program identified the **minimum and maximum** possible additional AUC from the body-condition term across allowed label assignments, holding within-project-year comparisons fixed. The numerical algorithm passed exhaustive synthetic enumeration tests. This evaluates vulnerability to unverified labels, not the probability of hidden initiations; fixed original score weights are not refitted under the hypothetical labels.

### Horizon-controlled initiation and onset order among detected entrants

Following the initial project-held-out condition AUC findings, we froze three further exploratory analyses of the distinction between *ever starting migration* and *how soon a participating eel starts*. First, for post-release horizons of **7, 30, 60 and 90 days**, an eel counted as an early detected event if its canonical migration-onset timestamp fell before the horizon; a no-event control required a receiver arrival at or after that same horizon. The latter rule establishes a later observation, **not continuous tracking**. Baseline and condition-augmented initiation models were trained separately for each eligible horizon population, always withholding the focal project, to measure the sensitivity of outcome-specific predictive utility to observed follow-up. This changes both training weights and case mix, and therefore cannot establish a biological sign reversal by itself.

Second, we used one **common population of 475 eels eligible at day 90** and two project-held-out models trained **only for eventual activation on the original 575 eels**. This selection retains **all 422 source-classified initiators** but only **53 of 153 source-classified noninitiators**; the other **100** lacked the requisite horizon documentation. Thus the common cohort is held constant *across horizon labels* but is not a representative or randomly selected subset of the original panel. We therefore used an exact decomposition of the change in pooled AUC gain between the original 575-fish population and this 475-fish subset into (i) changes in project-level positive–negative pair weights and (ii) within-project AUC changes, keeping original project-held-out scores frozen. As a second post-hoc observation-process sensitivity, we performed **20,000** random draws retaining all 422 initiators and the *observed number* of 90-day-eligible source noninitiators within each project-year, but randomizing which noninitiators remained. We also tested whether the existing scores rank 90-day observability among source noninitiators. These are checks on follow-up selection, not corrected survival estimates or causal mechanisms. With scores frozen, we successively classified onset by 7/30/60/90 days or eventual source initiation, evaluating within-project-year AUC at each horizon. We compared the added condition information for eventual versus day-30 initiation across the four projects having both mixed-outcome endpoint sets using an equal-project paired contrast, project resampling (10,000 repetitions) and an exploratory exact sign-flip test. Within the same population we separately compared early entrants (≤30 days), later entrants (>30 days) and those never classified as initiators. These groups are retrospective telemetry categories, not biological success/failure labels.

Because the common 90-day eligibility filter retained source initiators and removed mostly source noninitiators, we performed a separate **post-hoc observation-selection negative control** after inspecting the apparent endpoint dependence. We kept every original held-out score and eventual-initiation label fixed across all **575** source eels, verified that all 422 source initiators survived the 90-day selection, then independently drew **20,000** score-blind sets of noninitiators. Within each project × release-year stratum, each draw retained exactly the observed number of 90-day-eligible source noninitiators and all source initiators. We recalculated the pair-weighted within-stratum AUC gain from adding condition. The resulting conditional retention distribution measures the gain expected solely from thinning the source noninitiator class with the observed project-year composition, not from an additional energetic or causal receiver-retention mechanism.

Finally, among all source-classified initiators with nonnegative, reconstructable release-to-onset latencies, we evaluated **continuous onset-order concordance** within project-year: for each two initiators with distinct onset delays, did the same frozen score rank the earlier initiator higher? We compared stage, stage+condition, and nested stage/length/release-time models with and without condition, including a sensitivity excluding onset within the first post-release day. This analysis **conditions on initiation** and does not causally decompose the Cox onset hazard into latent physiological decisions.

### Independent assessment of continuous silvering morphometrics

A newly identified subset of the pinned public metadata includes horizontal and vertical eye diameters and pectoral fin length alongside body mass, length and ordinal Durif class. The measurements occupy `length2`–`length4` in **project-dependent order**, which must be resolved using their accompanying measurement-type labels. One of the six focal projects (Warnow) has no recorded eye/fin measurements, whereas the remaining five have measurements for most eligible individuals. We specified a separate, explicitly post-hoc falsification audit comparing held-out initiation ranking from (i) ordinal stage, length and release date, (ii) those variables plus continuous eye and relative pectoral-fin indices, (iii) those variables plus residual condition, and (iv) those variables plus both morphology and condition. The decisive contrast is model (iv) versus (ii): does weight-for-length information add predictive value after continuous silvering morphology is available? Models use the same complete-morphology sample and project-held-out penalized logistic fits. This audit addresses *whether the ordinal class was simply too coarse*, not whether body mass represents independently measured energy stores (Sundin et al. 2022).

### Within-link realized transit-speed audit

To test whether the weak progression signal was created by averaging across unlike routes, we froze a developmental within-link audit before inspecting its coefficient. An initial implementation was subsequently corrected to exclude the nine pre-existing expert-classified 2015 non-migrants, consistent with the canonical activated cohort. We used the project-held-out entry-state score and source positive `speed_m_s` values only when both the current and immediately preceding rows for an eel were classified `migration = TRUE` and the station identity changed. Each directed receiver-to-receiver pair was treated as a fixed route link. The primary model required at least five unique eels per directed pair, included directed-pair and project × release-year fixed effects plus body length and release timing, weighted segment rows so that each eel contributed total weight one, and used fish-clustered sandwich standard errors. Pair-support thresholds of three and ten eels, unweighted segment rows and leave-one-project-out fits were frozen sensitivities.

The source `speed_m_s` field is a last-detection-to-first-detection ground-speed calculation and, after the frozen primary was run, was found to contain biologically impossible values. We therefore registered an explicitly post-hoc data-quality sensitivity rather than changing the primary endpoint. A laboratory sample of female European silver eels showed mean Ucrit 0.94 m s\(^{-1}\) and Uopt 0.64 m s\(^{-1}\) (Tudorache et al. 2015), but these sustained-swimming measurements are not universal maxima for field-derived ground speeds. The broad swimming-performance database of Katopodis and Gervais (2016) also does not establish a verified 2.26 m s\(^{-1}\) maximum for this source field. Accordingly, we treated 2.5, 5 and 10 m s\(^{-1}\) as explicitly heuristic, increasingly permissive gross-artifact screens, not species-specific physical cutoffs. The same primary model was re-fitted at each cutoff as post-hoc sensitivity, and the all-positive-speed analysis remains the frozen primary.

### Source migration classification

We inherited the migration-classification algorithm from the source analysis. In brief, the source workflow identified sustained downstream migration using a minimum distance threshold of 4 km and a migration-speed threshold of 0.01 m s\(^{-1}\), with an additional smoothing criterion to avoid identifying stationary periods as migration starts. Once downstream migration was identified, the source migration interval extended from the first qualifying downstream segment to the furthest downstream distance reached.

For the binary initiation analysis, an individual was considered initiated if the source workflow identified qualifying downstream migration, after applying the nine fixed expert corrections. We refer to this as **migration activation** or **classified migration initiation** rather than the unobserved physiological instant at which the animal decided to migrate.

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

### Time to migration onset

To avoid reducing activation timing to an arbitrary fixed-day threshold, we also fitted a stratified Cox proportional-hazards model. Individuals were followed from release to the distance-threshold crossing time (time_first_dist_to_use) attached to the first row with downstream_migration = TRUE; non-initiators were censored at their last available telemetry observation. We did not use the arrival time of the first broader migration = TRUE interval row as the onset clock.

The Cox model used separate baseline hazards for project × release-year strata and the same covariates as the initiation model: within-stratum body length per 100 mm, within-stratum release timing per 100 days and ordinal Durif stage. Tied event times were handled with the Breslow approximation.

The time-to-event dataset contained 570 individuals and 418 onset events across 13 project-year strata. We evaluated project dependence by repeating the stage estimate after omitting each source project in turn.

### Terminal positive-set membership sensitivity

The source workflow created a file of eels positively observed at project-specific terminal/sea endpoints using water-body-specific station or distance rules.

The Europe-wide source paper explicitly did not analyse escapement success rate because interpreting non-observation at these endpoints would require additional assumptions about fishing, terminal detection loss, release position and study-specific monitoring geometry.

We therefore retained terminal-set membership only as a **secondary sensitivity endpoint** among activated eels. Its complement was not interpreted as validated biological failure.

The sensitivity model used the same project × release-year structure, within-stratum body-length adjustment, within-stratum release-timing adjustment and ordinal Durif coding as the activation model.

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

### Progression falsification and selection diagnostics

Because a weak stage-speed coefficient could arise for several reasons other than a genuine phase difference, we ran three developmental diagnostics after the primary result was known.

First, we tested whether the pooled coefficient concealed strong opposing project effects and repeated progression at the individual median positive inter-station speed scale. Second, we tested a capture-stage-staleness alternative by fitting a Durif × release-to-activation-latency interaction and by re-estimating the stage-speed coefficient among eels activating within 1, 3 and 7 days.

Third, we audited selection induced by conditioning on activation. We compared initiators and non-initiators within capture stage on body length and a descriptive log-weight residual after length, project and stage adjustment. We then fitted the canonical initiation model to obtain individual fitted activation probabilities. Among speed-bearing initiators with estimable propensities, we refitted the same stage-speed model using inverse-probability weights (1/hat p_i). This weighting is a selection diagnostic only: speed is undefined for non-initiators, so the analysis cannot identify counterfactual post-activation speed for animals that never crossed the activation gate.

### Terminal-endpoint phase contrast — sensitivity only

For audit continuity, we retained the previously developed stacked initiation-versus-terminal-membership model with individual-clustered uncertainty.

Because the second binary response is observability dependent, this contrast is not used as the principal test of phase-specific control in V4.

Its role is limited to asking whether the direction of the stage association differs when the same positive terminal-set definition is used across projects. It must not be interpreted as a direct comparison of biological initiation probability with biological failure probability.

### Project-level route-context diagnostic

To ask whether broad route context aligned differently with the two gates, we used the source study's water-regulating-structure (WRS) impact score. For each of the six projects we calculated the median WRS impact among focal stage-coded individuals and compared it with migration initiation and completion among initiators.

Associations were summarized by Spearman rank correlation. With only six projects, two-sided exact permutation p-values were calculated by enumerating all 6! assignments.

This analysis was explicitly treated as **contextual bridge evidence**, not causal inference: WRS intensity is strongly confounded with project identity, hydrology, barrier type, telemetry design and endpoint observability.

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

### Evidence class

All Europe-wide analyses are secondary analyses of public data and were developed after inspection of source outcomes. They are therefore described as **developmental independent evidence**, not preregistered or response-blind confirmation. The Dutch archive provides independent developmental falsification of a proposed condition-dependent passage-selectivity mechanism; it does not constitute a direct replication of the Europe-wide phase model.

---

## Results

### Advanced Durif stage strongly predicted migration activation

The final evaluable cohort comprised 575 FIII–FV females with compatible cleaned migration tracks. Expert-corrected initiation increased monotonically with silvering stage: 154 of 261 FIII eels (59.0%), 53 of 68 FIV eels (77.9%) and 215 of 246 FV eels (87.4%) initiated classified downstream migration.

After project × release-year adjustment and control for within-stratum body length and release timing, each one-stage increase in Durif classification was associated with a 2.08-fold increase in the odds of migration initiation (95% CI 1.56–2.76; p = 4.2×10\(^{-7}\)).

### More advanced stage predicted earlier migration onset

The time-to-event analysis contained 570 individuals and 418 migration-onset events. Each FIII→FIV→FV increment increased the instantaneous migration-onset rate by 28% (HR 1.29, 95% CI 1.13–1.47; p = 0.00016).

The stage HR remained above one in every leave-one-project-out analysis, ranging from 1.09 to 1.52. Omitting the 2015 project produced the weakest and least precise estimate, with the 95% interval crossing one. Thus, the average onset association was positive but not fully project-independent in precision.

### Continuous body state added information beyond ordinal silvering stage

In the activation model with both capture-state terms, the Durif effect remained strong (OR 2.13 per stage, 95% CI 1.60–2.84; p=2.8×10\(^{-7}\)) and standardized weight-for-length condition contributed independently (OR 1.46 per SD, 95% CI 1.16–1.83; p=0.00105). Adding the two terms jointly improved the activation model by LR χ²=39.01 with 2 df (p=3.4×10\(^{-9}\)).

The condition effect was robust to three alternative weight-for-length definitions and remained positive in every leave-one-project-out fit. A simple compensatory model was not supported: Durif × condition and Durif × length interactions did not improve activation prediction.

### An activation-trained entry-state score transferred to onset but not realized transit speed

The activation-derived score assigned weights 0.756 to ordinal Durif stage and 0.379 to standardized capture condition. Per 1 SD, this frozen score increased migration-activation odds 2.23-fold (95% CI 1.70–2.92; p=5.1×10\(^{-9}\)).

Transferred without re-fitting its relative weights to the onset model, the same score predicted earlier behavioral expression of migration (HR 1.32, 95% CI 1.17–1.49; p=6.9×10\(^{-6}\); 418 onset events).

The score did not transfer as a generic speed ranking. Among 418 activated eels, the whole-route speed ratio per SD was 0.946 (95% CI 0.832–1.076; p=0.396), with partial R²=0.0018. For the separately frozen median positive inter-station speed endpoint (n=411), the ratio was 1.028 (95% CI 0.869–1.215; p=0.750), with partial R²=0.00026.

The same phase boundary survived project-held-out coefficient training. Across the six leave-one-project-out training folds, both activation-derived weights remained positive (Durif beta range 0.563–0.892; condition beta range 0.213–0.497). Pooling scores whose weights were learned without the focal project's outcomes, the cross-fitted score still predicted activation (OR 1.97 per SD, 95% CI 1.53–2.53; p=1.3×10\(^{-7}\)) and earlier onset (HR 1.26, 95% CI 1.12–1.42; p=0.00014), while remaining weak for whole-route speed (ratio 0.948, 95% CI 0.836–1.075; p=0.408; partial R²=0.17%) and frozen inter-station speed (ratio 1.013, 95% CI 0.860–1.192; p=0.879; partial R²=0.006%). Thus the boundary is not explained simply by estimating the entry-state weights using outcomes from the same project to which they are applied.

### Body condition supplied additional activation information beyond silvering stage, but its benefit varied among projects

The six-project held-out initiation-ranking test used **575 evaluable eels** and **6,914 initiator/non-initiator pairs** across 12 informative project-year strata. A base model using Durif stage, body length and release timing achieved stratified AUC **0.610**. Adding continuous capture condition raised AUC to **0.643**, an increment of **0.0336**; its fixed-training fish-level conditional bootstrap interval was **0.0021–0.0644**. When comparisons were restricted to **3,199 pairs of eels of the same Durif stage**, AUC increased from **0.480 to 0.555**. This stage-controlled comparison shows why a continuous body-state axis can contain information masked by a coarse maturation classification, although it does not isolate an energetic mechanism.

The increment was positive in **four of six** held-out projects and negative in two. The pooled increment remained positive when any single project was removed (range **0.0136–0.0632**). However, the **six-project cluster bootstrap** gave a 95% interval of **−0.0007 to 0.0918** for the pooled pair-weighted increment; an exploratory two-sided project sign-flip test was **p=0.1875**. The 2012 Leopoldkanaal and 2013 Albertkanaal cohorts had the strongest positive increments (respectively +0.109 and +0.103), whereas ESGL was −0.065. Thus continuous condition **can improve held-out ranking in this panel**, but consistent improvement across independent rivers has **not** been established. This is neither a prospective validation nor a measure of ultimate escapement success.

### The additional condition ranking was sensitive to hypothetical hidden initiation

A direct observation-process sensitivity found that among the **100** source-classified noninitiators without 90-day receiver support, reclassifying an **adversarially selected 11** as hypothetical undetected initiators was sufficient to move the frozen-score added AUC from **+0.0336** to approximately **−0.00016**. The exact envelope still required at least **11** such flips to reach a nonpositive increment: 10 flips gave a minimum **+0.00191**, whereas 15 could give **−0.00784**. At the eleven-fish tipping assignment, eight labels came from Warnow and one each from Leopoldkanaal, Albertkanaal and Verhelst. Other admissible 11-fish assignments can leave or enlarge the score advantage; this is a **worst-case label-contamination bound**, not a finding that eleven misclassifications occurred. It does not bound performance after retraining the models on revised labels and does not establish the actual frequency of missed migration. Nevertheless, the apparently useful continuous-state increment depends materially on distinguishing genuine noninitiation from incomplete observation.

### Continuous silvering morphology did not remove all condition ranking information, but project-level certainty was limited

The pinned metadata retain typed and measured horizontal/vertical eye diameters and pectoral-fin lengths for five of the six focal projects, although measurement columns differ by project. Among the original 575 evaluable tagged fish, **429** had complete morphometrics. After leaving each of these five projects out of model training, **3,272** positive–negative initiation pairs were informative within ten held-out project-year strata.

In this identically sampled subset, the base Durif-stage, length and release-date model achieved AUC **0.706**. Adding the continuous eye index and relative fin length raised AUC to **0.716**. Adding the weight-for-length condition residual *instead* raised AUC to **0.741**. Including **both morphology and condition** yielded AUC **0.741**. Thus the incremental AUC from adding condition **after** continuous morphology was **+0.0244**, whereas adding morphology **after** condition gained only **+0.0003** in the pooled score ranking.

This does not justify interpreting condition as an independent energy-reserve trait. A post-hoc sensitivity varying the preselected L2 regularization penalty from **0.1 to 10** yielded positive condition-after-morphology increments of **+0.0269**, **+0.0244** and **+0.0214**; all corresponding five-project uncertainty intervals contained zero. Thus the pooled effect's direction was not specific to one penalty, whereas project-level portability was still unsupported.

The condition-after-morphology increment was positive in **three of five** held-out projects. Project resampling gave a 95% interval of **−0.0151 to +0.0659**; the gain remained positive under each single-project omission (**+0.0125 to +0.0349**), but it was not reliably positive across independent contexts. Moreover, the five-project subset excludes Warnow and therefore has different case mix from the preceding six-project analysis. In particular, its better baseline AUC (0.706 rather than 0.610) cannot be attributed to continuous morphology; the sample and estimation method also differ.

A stage-conditioned sensitivity on this subset yielded a +0.063 condition-after-morphology AUC increment in FIII (949 pairs) and +0.074 in FV (498 pairs), whereas FIV had only 16 pairs and no stable estimate of additional information. Thus the previously observed FV-over-FIII tendency does not establish a stage-specific energetic checkpoint.

### Readiness information concerned observed migration participation more than onset order

When both outcome definitions and models were retrained in separate horizon-eligible populations, adding condition changed held-out AUC by **−0.0263** at 7 days (n=496), **−0.0291** at 30 days (n=484), **−0.0226** at 60 days (n=478), and **+0.0021** at 90 days (n=475). The negative increments do not imply that greater body condition delays migration: the training outcome and set of tracked animals differed at every horizon, and five informative projects gave a 30-day exact sign-flip p=0.0625 despite a project-bootstrap interval below zero.

A more direct endpoint comparison kept **475 eels** and both held-out model scores unchanged. Because all **422** eventual source initiators survived the day-90 eligibility selection while **100/153** source noninitiators were excluded, the eventual-endpoint AUC in these 475 eels should not be equated with the separate 575-fish AUC, nor interpreted as evidence of differential physiology without an observability audit. Added condition AUC increased with the length of the observed endpoint: **+0.0077** by day 7, **+0.0329** by day 30, **+0.0460** by day 60, **+0.0549** by day 90, and **+0.0807** for eventual source-defined migration initiation. The equal-project mean contrast of eventual versus day-30 added AUC was **+0.0431** across **four** informative projects (project-bootstrap 95% CI **+0.0164 to +0.0697**; exact paired two-sided sign-flip **p=0.125**). Among this same cohort, **299** eels began within 30 days, **123** began later and **53** had no source-classified initiation. Condition added similar information for distinguishing early versus never classified (AUC increment **+0.0832**) and late versus never classified (**+0.0756**), but little for distinguishing early versus late initiators (**+0.0089**). The horizon signal is consequently compatible with the changing composition of an apparent noninitiator group, not demonstrated physiological waiting by high-condition fish. In particular, the larger eventual AUC increment in the day-90-selected subset is conditional on an asymmetric follow-up filter. The additional condition AUC for *the same eventual initiation label* rose from **+0.0336** in all 575 eels to **+0.0807** after the 90-day selection (difference **+0.0471**). An exact project-level accounting identity attributed **+0.0515** to the changed weights of project-specific initiator/noninitiator pairs and **−0.0044** to the within-project changes. The Warnow project's share of informative pairs dropped from **52.6% to 5.2%** while Leopoldkanaal increased from **21.1% to 53.4%**. Under 20,000 project-year-stratified *random* retentions of the same number of noninitiators, the mean expected AUC increment was **+0.0844** (95% random-retention range **+0.0606 to +0.1083**), with the observed +0.0807 unexceptional (two-sided deviation probability **0.764**). Among noninitiators alone, added condition AUC for ranking 90-day receiver observability was only **+0.0092** over 326 comparison pairs, and its signs differed among projects. Thus the inflated selected-subset condition signal did not require unusually phenotype-related retention beyond the project-year composition effect. Importantly, the 100 excluded source noninitiators had a median final receiver arrival **0.52 days** after release, compared with **549 days** among the 53 retained records; these are last-detection spans, *not continuous monitoring coverage*, and neither group is a confirmed biological nonmigrant.

The 90-day filter's composition was an important source of amplification. It retained **all 422** source-defined eventual initiators but only **53 of 153** source noninitiators; the remaining **100** had insufficient observation support, not verified failure or inactivity. The same held-out-score condition AUC increment rose from **+0.0336** in all 575 fish to **+0.0807** in the selected 475. Yet under **20,000 random, project-year-stratified draws** retaining exactly the same number of noninitiators per stratum, the expected increment was **+0.0844** (95% random-retention envelope **+0.0606 to +0.1083**). The observed **+0.0807** lay within that envelope (upper-tail probability **0.625**). Thus the increased selected-subset AUC gain did **not** require preferential retention of high- or low-condition noninitiators within project-year strata. Among source noninitiators, retained records had a median last-observation interval of **549 days**, versus **0.52 days** for excluded records; this contrast flags profound differences in recorded follow-up, not continuous tracking or a biological survival contrast. The positive classification AUC in the selected subset cannot therefore be promoted as evidence that capture condition becomes physiologically more important over time.

Directly examining the order of observed onset among **422 initiated eels** gave **10,756** informative within-project-year onset-order pairs. Baseline stage/length/release-time concordance was **0.5446** and became **0.5461** after adding condition, an increment of **+0.0015** (six-project bootstrap 95% CI **−0.0237 to +0.0202**, exploratory project sign-flip **p=0.9375**). Excluding starts within 24 hours left 291 initiators and reduced the incremental concordance to **−0.0086**. Stage-specific median detected onset delays among entrants were 7.21 days (FIII) and 2.14 days (FIV and FV), but median differences do not identify individual energetic readiness or distinguish hydraulic cue timing. Capture condition therefore provided much more information about *membership of the initiating group* than about *onset ordering within that selected group*.

### Entry state did not rank realized speed within identical route links

The exact-link audit retained 17,792 positive segment rows from 418 eels across 244 directed station pairs with at least five unique fish per pair. With each eel contributing total weight one, the project-held-out entry-state score had a within-link speed ratio of **0.962 per SD** (95% CI **0.883–1.048**; p=**0.372**) and weighted partial R² of **0.0003815** (approximately **0.0382%**).

The result was insensitive to the prespecified pair-support threshold: ratios were **0.956** for at least three fish per link and **0.999** for at least ten. Leave-one-project-out estimates ranged from **0.933 to 1.013**, crossing both sides of one. Thus the absence of a positive speed ranking is not explained by pooling eels across different receiver-to-receiver geometries.

The raw source segment-speed field nevertheless had a serious quality boundary: the frozen primary candidate rows included values up to **3752 m s\(^{-1}\)**. The first implementation accidentally included nine fixed expert-classified non-migrants; all within-link estimates now reported use the corrected 422-eel candidate migratory universe, with 418 eels retained after the link-support filter. Externally motivated post-hoc screens therefore removed speeds above 2.5, 5 or 10 m s\(^{-1}\), which removed **63.1%**, **58.6%** and **53.0%** of candidate segment rows, respectively. Despite this large data-quality correction, the fish-equal within-link ratios remained **0.942**, **0.944** and **0.941**, with all 95% intervals spanning one. All three post-hoc filtered point estimates are negative, with p approximately 0.07–0.08, although none of their 95% intervals excludes one. Thus these estimates do not establish a negative speed gradient, nor do they establish a precisely zero effect. The near-null primary finding is robust to grossly implausible source-speed artifacts, although the raw segment-speed field should not be treated as a direct physiological swimming measurement. A separate Frisch–Waugh–Lovell SVD absorption analysis reproduced the corrected fixed-effects coefficient within 4×10\(^{-14}\), supporting numerical stability despite high-dimensional nuisance collinearity.

Thus a capture-state vector optimized only for entry into migration retained information about **when** migration began but essentially no general information about **how fast** activated eels progressed under either generic speed summary or within identical receiver-to-receiver links.

### Terminal positive-set membership showed a weak general stage gradient

Among activated eels, ordinal Durif stage showed a weak association with membership in the source study's project-specific terminal positive set (adjusted OR 1.15, 95% CI 0.83–1.59; p = 0.412).

Because non-membership can reflect censoring, fishing, detection loss and route-specific monitoring geometry, this result is reported as a sensitivity analysis rather than as an estimate of migration completion probability.

### Post-initiation migration speed showed no general Durif gradient

Among 418 initiated eels retained in informative project-year strata, median migration speeds were 0.0229 m s\(^{-1}\) for FIII, 0.0232 m s\(^{-1}\) for FIV and 0.0245 m s\(^{-1}\) for FV.

After adjustment, the multiplicative change in migration speed per Durif-stage increment was 0.983 (95% CI 0.852–1.134; p = 0.815). This continuous progression result does not require terminal non-observations to be classified as biological failures.

### Terminal-endpoint phase contrast was directionally consistent but sensitivity-only

The stacked sensitivity model yielded a larger stage coefficient for activation than for terminal positive-set membership (OR ratio 1.81, 95% CI 1.15–2.84; p = 0.0099), with the same direction in all six leave-one-project-out analyses.

This contrast is retained for reproducibility but is not manuscript-primary because the terminal binary response does not provide a validated failure state.

The independent post-activation speed analysis provides the primary progression evidence without requiring that assumption.

### Project-level route context was associated with terminal positive-set membership, not activation

Across six project contexts, median WRS impact was essentially unrelated to migration activation (Spearman \(\rho=0.029\), exact p = 0.983).

Median WRS impact was negatively associated with terminal positive-set membership among activated eels (\(\rho=-0.928\), exact p = 0.022).

Because the terminal response is observability dependent and only six non-randomized project contexts are available, this is contextual bridge evidence only. It is not interpreted as a WRS effect on biological completion probability.

### Arrival-defined Dutch tests did not support condition-dependent barrier selectivity

The Dutch public archive allowed the proposed passage-selectivity mechanism to be tested after observed barrier arrival rather than through the source duration-dependent opportunity definition.

At the tidal sluice, the condition × duration interaction was near zero (β=−0.095; p=0.841; permutation p=0.849). At the pumping station, the fitted interaction was strongly negative, opposite to the positive preregistered prediction, but the model was near-separated and non-converged with enormous uncertainty and therefore was not interpreted as a biological negative effect.

The broader arrival-defined waiting analysis likewise showed no evidence that better-conditioned eels waited through more opening events after reaching a barrier. At the pumping station, condition was unrelated to missed post-arrival events (Spearman r=0.009; permutation p=0.960) or delay to passage (r=0.072; p=0.677). At the tidal sluice, the corresponding associations were r=−0.104 (p=0.592) and r=−0.182 (p=0.350). Adjusting for body mass, readiness, arrival calendar time and release group did not reveal hidden positive associations.

Thus the independent Dutch analysis **did not support the specific prediction** that higher capture condition generally favours longer opening windows or greater post-arrival waiting. Given the small number of informative matched-choice fish and the unstable pumping-station model, this should not be interpreted as proving the mechanism impossible.

---

## Discussion

### Migration is a sequence of ecological filters, but entry state is not a progression-speed score

Our central result is not simply that more silvered eels migrate. FIII is explicitly a pre-migrant Durif stage and FIV/FV are migrating stages, so that qualitative relationship is built into the biology of silvering.

The informative result is the **transferability boundary**. Ordinal Durif stage and continuous weight-for-length state both carried information about entry into migration. When their activation-derived contributions were compressed into one score, that score strongly predicted whether migration became behaviorally expressed and when onset occurred. Yet it explained only 0.18% of residual variation in whole-route speed and 0.026% in the frozen positive inter-station speed summary.

This directly rejects the simple interpretation of capture-time readiness as a universal realized-progression-quality axis. The phenotype that makes an eel more likely to enter the migratory mode is not, in these data, a general ranking of how fast activated animals move through heterogeneous routes.

The additional continuous-morphology analysis sharpens the interpretation, but not into a physiological proof: after eye and pectoral-fin measurements were available, weight-for-length still increased the pooled held-out initiation AUC by +0.0244. The between-project interval nevertheless encompassed zero, and adding morphology to the condition-based model yielded essentially no pooled gain. The data are therefore consistent with several explanations, including stage categorization losing continuous mass information, genuine individual body-state variation, or study-specific covariation. They cannot isolate fat reserves, hormones or a causal readiness threshold.

The added out-of-project discrimination test clarifies that this result is more than a redundant Durif-stage predictor. Within the same ordinal stage, a continuous capture-condition axis sometimes improves ranking of which eels initiate migration. Nevertheless, the advantage varies substantially among river projects and the between-project uncertainty includes zero. The ecological possibility is a context-dependent **readiness threshold** within silvering categories, not a universal energy-to-speed conversion. The available projects do not allow us to distinguish hydraulic gating, energetic reserves, variation in migration cues or project-specific tagging and observation biases as causes of that context dependence.

The exact-link result makes that boundary harder to attribute to route aggregation. Even after conditioning on the same directed receiver-to-receiver link, using project-held-out score weights, giving each fish equal total weight and clustering uncertainty by fish, the corrected speed ratio was 0.962 per SD; the score explained only 0.038% of the remaining weighted log-speed variation. The result also survived removing the many grossly implausible source segment-speed values using externally motivated thresholds. Accordingly, the observed separation is between **entry-state information** and **realized transit-speed ranking**, not merely between an individual trait and a coarse whole-route average.

That result is not the default prediction from the broad condition–movement literature. Goossens et al. (2020) synthesize many systems in which higher condition is associated with more efficient migration and, when integrated over an entire trajectory, faster travel and earlier arrival. Our eel result instead shows strong condition information at the transition into migration but almost no transferable information in positive inter-station speed. The difference is therefore not simply “condition matters” versus “condition does not matter”; it is **which component of movement the condition signal describes**.

This uncoupling contrasts with systems in which individual state carries forward from a departure decision into faster travel. For example, high-condition red knots both selected migration timing differently and attained higher ground speeds, while experimental and telemetry work in brown trout linked energetic state to migration initiation and speed, although with strong age and spatial-scale dependence (Duijns et al. 2017; Shry et al. 2019). The eel result therefore supports treating migratory commitment and displacement performance as empirically separable state-dependent traits rather than assuming one scalar “migration quality” phenotype.

The distinction is important because movement sequences contain different ecological filters. Entry depends on internal preparation and motivation. Progression after entry can still depend on physiology, but it is additionally conditioned by hydrology, route geometry, temporal activity schedules, barriers and local opportunity. A final movement endpoint can merge those filters and obscure which measured phenotype is informative at which transition.

The independent Dutch analysis strengthened this conclusion by failing to support a tempting mechanistic shortcut. Better-conditioned fish did not generally wait for longer opening windows after arrival. Thus the phase boundary should not be replaced with a universal asset-protection or barrier-selectivity story.

### Entry into migration is multivariate rather than purely ordinal

Durif stages provide a biologically meaningful silvering axis, but they compress continuous morphology into discrete categories. The additional positive condition coefficient shows that the ordinal label does not exhaust capture-state information relevant to behavioral activation.

The absence of Durif × condition compensation is also informative. The data do not support a simple architecture in which high condition specifically rescues low-stage FIII animals. Instead, stage and weight-for-length state contribute approximately additively to the probability of activation.

This motivates interpreting capture phenotype as a **multivariate entry gate** rather than as one linear silvering ruler. The activation-trained score operationalizes that gate without claiming that it is a direct endocrine or energetic measurement.

Selection remains an important boundary because post-activation speed is only observed for entrants. However, inverse-probability weighting that included condition in the measured activation process shifted the condition-speed ratio only from 0.907 to 0.920. Likewise, the earlier Durif-specific selection audit did not restore a general stage-speed gradient. Measured entry selection therefore does not explain the loss of a positive generic speed ranking, although unmeasured readiness selection cannot be removed from these observational data.

The label-ambiguity calculation provides a second reason not to interpret the initiation classifier as a purely physiological switch. A cohort with unchanged capture phenotypes and model coefficients can lose its apparent incremental body-state ranking if a small, carefully selected subset of short-follow-up controls actually initiated without detection. This is an exact **sensitivity** result, not evidence of actual misclassification: the assignment is deliberately adversarial, and the true movement histories are not identifiable from the available receiver records. It strengthens the case for explicit detection opportunity in validation datasets rather than for yet another fitted readiness index.

### Migration-entry propensity and its temporal scheduling are not equivalent

The interpretation of an apparent readiness-to-time relationship depends critically on which animals can be observed. Selecting the 90-day traceable subset retains all source initiators but excludes 100/153 source noninitiation records, strongly changing project contribution to the AUC. The rise in the eventual-entry condition increment within the selected sample is almost entirely explained by project-pair weighting, and a matched random negative-retention null reproduces it. This **rules out using that particular AUC rise as evidence that a physiological readiness gate strengthens over elapsed time**. It does not demonstrate that river discharge, biological state or true time-to-departure plays no ecological role; those variables were not directly measured as individual cue–response trajectories.


The time-horizon checks sharpen what the earlier onset Cox hazard represents. Both a higher probability of **ever being classified as an initiator during surveillance** and a tendency toward **earlier detected onset** can affect an observed hazard; a positive hazard ratio is not automatically evidence that body state determines the scheduling of movement *among entrants*. In the source data, the same project-held-out phenotype had predictive value for observed participation in migration, but condition scarcely improved within-project-year ordering of onset times among the 422 animals that entered the migratory classification. The distinction survived removing release-day detections.

A strong counterexample to interpreting the cumulative AUC pattern biologically comes from the **observation-selection audit**. Holding the initiation labels, scores and all positive eels fixed while randomly retaining project-year-specific numbers of noninitiators reproduced the high (+0.081) selected-cohort AUC increment; its observed value was not unusual against the random-retention distribution. Hence the **growth in apparent condition information over increasing observation horizons is not evidence for a delayed energetic checkpoint**. It arises in part from changing endpoint composition and an asymmetric observability gate. This does not negate the separate, direct empirical finding that condition adds little to ranking onset times *within the classified migratory group*. Both claims remain subject to small independent-project samples, imperfect detections and selection on initiators.

The potential separation between physiological readiness and environmental migration cues is **not a novel ecological hypothesis by itself**. In two long-term European eel monitoring rivers, Sandlund et al. (2017) distinguished conditions acting in the months before migration from daily triggers of movement among ready eels, including water-level and nocturnal conditions. Arevalo et al. (2021) likewise showed that the combined thermal and flow environment affects preferred silver-eel migration opportunities, including preferential migration at roughly 10–20 °C with high discharge in those two systems. Both published studies analysed Imsa and Burrishoole, so they are related prior evidence, not independent broad-scale replications of an entry/scheduling mechanism. Our incremental contribution is specifically the **same fitted, project-held-out capture-state phenotype evaluated across onset classification, common-cohort endpoint horizons, conditional onset order and realized transit speed**, with explicit receiver-observation and project-dependence boundaries. We cannot assign environmental cause because the necessary eel-specific time-aligned flow and temperature covariates are missing from this pooled telemetry programme.

This could mean that the capture phenotype contributes to crossing an entry threshold while start time for committed eels is comparatively conditioned by environmental opportunity. **However, the present observations do not measure cue exposure** and cannot identify this as the causal explanation. The cumulative endpoint result also depends on receiver observation: 100 eels did not meet day-90 eligibility, early events and non-events had asymmetric follow-up rules, and the 53 day-90-eligible eventual noninitiators are not confirmed failed or surviving residents. The smaller sample of independent projects and initiation-selection bias limit the generality of the contrast. A testable biological follow-up would distinguish repeated physiological readiness from time-resolved hydraulic/temperature opportunities and tag-detection coverage; the current data support an empirical separation of predictions, not a proven control handoff.

### Internal readiness predicts activation but not transferable realized transit speed

The post-initiation speed result differed sharply from the activation result. Durif stage strongly predicted whether and when migration became active, but showed no general gradient in the source-defined **whole-migration** speed response after activation (ratio 0.983 per stage, 95% CI 0.852–1.134).

A developmental project-level audit did not indicate that this pooled near-null was merely produced by strong opposing water-body effects. Project-specific stage-speed ratios ranged from 0.915 to 1.272, but Cochran's Q was 2.47 with 5 df (p = 0.78). A separately frozen individual-level audit using median positive inter-station transit speed gave the same qualitative result (ratio 1.001 per stage, 95% CI 0.831–1.204), with no supported among-project heterogeneity at that scale either (Q = 2.32, p = 0.80). The weak transferable stage signal is therefore not specific to the whole-route elapsed-speed summary used in the primary analysis.

We also examined a biologically plausible predictor-ageing alternative. FIII eels took longer to reach the migration threshold than FIV/FV eels (median 7.21 d versus 2.14–2.15 d), raising the possibility that initially less advanced animals physiologically converged before progression was measured. A post-hoc diagnostic did not support the simple version of that explanation: the Durif × log-latency interaction was not negative (interaction ratio 1.036, p = 0.382), and stage-speed point estimates remained near or below one among animals activating within 1, 3 or 7 d of release (0.942, 0.953 and 0.963, respectively). Because no eel was re-staged at activation, this weakens but cannot exclude physiological convergence.

We separately audited activation-induced selection because post-activation speed is observed only for eels that crossed a stage-dependent entry filter. Measured capture phenotype was indeed selected: for FIII, initiators were on average 39.5 mm longer than non-initiators, with a standardized length difference of 0.514; selection on weight-for-length residual was 0.302. In the 373 speed-bearing initiators for whom canonical initiation propensities were estimable, inverse-probability weighting shifted the stage-speed ratio only from 1.042 (95% CI 0.902–1.205) to 1.062 (0.916–1.230). Measured activation selection therefore did not explain the weak stage-speed gradient, but the principal-stratum problem remains because speed is undefined for non-initiators and unmeasured readiness selection cannot be recovered from these data.

These audits sharpen the boundary rather than converting a null result into proof of no internal effect. Moyo et al. (2026) followed silver eels in the River Test after downstream movement had already begun and retained silvering stage in a reach-level progression model together with temperature, barrier, flow and lunar variables. A post-activation readiness signal can therefore exist in a particular route and endpoint even though a transferable gradient is weak across the six-project panel.

We therefore interpret the evidence as a **phase-specific transferability boundary**: capture-time Durif readiness carries strong, reproducible information about activation and onset across heterogeneous systems, but among eels that cross this stage-dependent activation filter the same capture-stage gradient does not transfer as a general post-activation speed ranking across either of the two progression summaries tested here.

This does not demonstrate that external conditions causally replace internal state. Individual traits can still influence movement after departure, and external conditions can also influence activation. The result instead identifies where the transferable Durif signal is strongest and motivates a sharper progression question: at what spatial and temporal scale does internal readiness remain visible, and when is it masked by route opportunity and environmental forcing?

Verhelst et al. (2025) independently reported substantial variation in migration phenology and speed among water bodies, with tidal context and water-regulating structures contributing to that heterogeneity. The independent Dutch arrival-defined reanalysis did not support a general condition-dependent passage-selectivity mechanism, while the River Test result shows that fine-scale progression need not be independent of silvering state.

### Route opportunity remains relevant, but no single barrier mechanism explains the phase boundary

The Europe-wide analysis does not identify a universal external controller of post-activation progression. The source meta-analysis documents strong water-body variation, and independent studies show that flow, darkness, barriers and local route geometry can affect migration timing and passage. Moyo et al. (2026) further shows that silvering stage can remain informative at a finer reach scale even when no transferable whole-route gradient is detected here.

Our Dutch reanalysis is important precisely because it **did not** deliver the expected positive mechanism. After barrier arrival, better condition did not predict more missed openings, longer delay, or stronger selection for long events. The previously attractive asset-protection explanation should therefore not be promoted as the general reason why capture condition predicts entry more strongly than generic post-activation speed.

The remaining ecological statement is broader and better supported: variables that rank the transition into a migratory state are not guaranteed to rank subsequent progression across routes. Which internal or external variables matter after activation can depend on spatial and temporal scale.

This produces a sharper next question:

> **what state variables remain informative after migratory commitment at specific reaches or decisions, and which components of route opportunity overwrite or mask the capture-state ranking at broader scales?**

That question is compatible with both positive fine-scale stage effects and weak transferable whole-route effects.

### Why phase-specific analysis changes the ecological question

The general movement-ecology framework combines internal state with external conditions. The present analysis adds a temporal qualification: **the same internal-state variable need not retain the same predictive value throughout a movement sequence.**

This suggests two distinct questions whenever data permit:

1. **Activation:** what determines whether and when the migratory phenotype becomes behaviorally expressed?
2. **Progression:** once movement is active, what determines speed, delay, route choice and passage through the landscape?

Those questions need not have the same answer.

Pooling them can make a readiness variable look like a universal movement driver when it acts mainly at activation, or obscure route effects by mixing animals that never entered the movement state with animals already negotiating the landscape.

The same logic is testable beyond eels wherever internal preparation can be measured independently of movement and individuals are followed across heterogeneous routes. It also suggests that apparently conflicting studies can be biologically compatible when one measures whole-route movement and another resolves reach-level or event-level progression.

### Conservation implications: readiness and passage opportunity are distinct management targets

European eel management explicitly seeks successful seaward escapement, but the present reanalysis does not estimate an escapement probability.

The results nevertheless distinguish two management-relevant processes. One concerns whether eels reach and express migration-ready internal states. The other concerns the physical opportunities available once movement is active.

Measures that improve continental growth conditions and production of silver eels address the first process. Measures that provide safe discharge windows, bypasses, effective sluice operation and source-to-sea connectivity address the second.

The distinction is therefore between **production of migration-ready individuals** and **conditions permitting their progression**, not between a measured readiness rate and a measured failure rate.

### Limitations

Several limitations define the scope of inference.

First, these are secondary developmental analyses of public data, not preregistered tests. The 90-day observation audit itself is post-hoc and inherits the source classification. The short final-detection spans of many noninitiators make the migration-entry endpoint partially dependent on observability and source processing; true nondeparture, later departure, receiver dropout and unobserved mortality cannot be discriminated without additional data. Source outcomes were inspected during programme development.

Second, migration activation is an algorithmic telemetry classification rather than a directly observed physiological decision time. We inherited the source thresholds and expert corrections to avoid outcome-driven redefinition.

A key measurement dependency limits physiological interpretation: the Durif silvering index is partly built from body mass, body length, eye diameters and pectoral fins (Durif et al. 2005; Sundin et al. 2022). Accordingly, weight-for-length condition may recover variation lost when a continuous multivariate classification is reduced to FIII/FIV/FV. The pinned source metadata permitted a completed five-project morphology-controlled sensitivity on 429 fish, but do not measure lipid content or endocrine readiness. Its remaining positive pooled condition AUC increment (+0.0244) was heterogeneous and its project-bootstrap interval included zero. The morphological categories describe premigrant FIII and migrating FIV/FV phenotypes, not verified telemetry outcomes. The stronger condition-associated FV ranking, if replicated, cannot by itself be interpreted as an energetic checkpoint.

The post-hoc temporal decomposition does not represent an unbiased migration hazard. In the 90-day negative-control experiment, all 422 source initiators survived selection whereas 100 of the 153 source noninitiators were removed. A score-blind, project-year-stratified negative-label thinning experiment could reproduce the observed selected-cohort condition AUC, so no increased physiological conditional effect is inferred from this selected subset. In its stricter 90-day common-cohort analysis, **100 of 575** original eels lacked the required observation support, while first-onset cases could enter despite earlier loss of tracking. The 53 remaining no-initiation records are not verified never-migrators. The small matched-project sample and selecting only migration initiators for onset-order comparison preclude inferring an individual-level causal delay mechanism.

The incremental held-out AUC analysis also has only six independent project contexts. A further exact sensitivity found that hypothetical false-negative labels among 11/100 source-noninitiators with inadequate 90-day follow-up can erase the frozen-score added AUC under a worst-case assignment. This is a vulnerability bound, not an estimated false-negative rate or a corrected estimate of the biological initiation effect. Its fish-resampling interval treats training weights as fixed, whereas the wider project-resampling interval includes zero. Therefore the AUC gain is evidence of potential additional information in the study panel, not a guarantee of gain in a new river.

Third, the source projects differ in hydrology, barriers, telemetry design and monitoring extent. Project-year adjustment controls baseline differences but does not make route contexts exchangeable.

Fourth, the terminal positive set is not a validated binary escapement-success variable. The source meta-analysis explicitly avoided estimating escapement success rate because non-observation can reflect fishing, detection loss, release geometry and other study-specific processes. Terminal-set analyses and the former stacked phase OR-ratio are therefore sensitivity results only.

Fifth, a weak general Durif effect on post-activation speed does not prove that internal traits cease to matter. Project-specific and finer-scale progression audits did not reveal a hidden transferable stage gradient, and a simple capture-stage-staleness diagnostic was unsupported, but all three are developmental analyses with finite precision. The staleness audit is especially indirect because individuals were staged only at capture rather than repeatedly through migration. The River Test study further shows that silvering stage can contribute to a different, reach-level post-activation progression model.

Sixth, post-activation speed is only defined for animals that entered the classified migratory state. Because activation probability differs strongly among FIII, FIV and FV, conditioning on activation creates a stage-dependent selected population. Observed-trait and inverse-probability diagnostics show that this selection is real but do not recover a strong stage-speed gradient after adjustment for measured activation predictors. They cannot remove selection on unmeasured latent readiness, so the post-activation coefficient is a descriptive ranking among entrants rather than a causal estimate of how a fixed stage effect attenuates in all tagged eels.

Finally, the Dutch consecutive-barrier and River Test studies constrain the interpretation but are not formal replications of the Europe-wide model. Their main value is to test where route-specific progression can retain or lose information from internal readiness. The Dutch reanalysis is retained as an independent falsification of one proposed passage-selectivity mechanism rather than as positive evidence for a universal control handoff.

### Conclusion

European eel migration is better described as a sequence of state-dependent transitions than as one phenotype of “migration performance.”

Capture-time Durif stage and continuous weight-for-length state jointly predicted entry into classified downstream migration. A score trained only on that activation transition also predicted when migration began. The same score, however, explained essentially none of the variation in two generic post-activation speed summaries.

The strongest synthesis is therefore:

> **the multivariate phenotype that predicts migratory commitment is an entry-state indicator, not a transferable general progression-speed score.**

The project-held-out analysis strengthens this interpretation: the entry/onset signal persisted when score weights were learned without the focal project's outcomes, whereas both generic post-activation speed summaries remained near null. This still falls short of external prospective validation because all folds come from the same public multi-project programme and share predictor preprocessing.

The independent Dutch analysis further showed that this boundary should not be explained by a universal condition-dependent preference for stronger barrier-opening opportunities: that specific mechanism was not supported after observed barrier arrival.

This conclusion does not imply that internal state becomes irrelevant after departure. Fine-scale state effects can remain, and route-specific environmental forcing can interact with individual phenotype. Instead, it identifies a scale- and phase-specific limit on what capture phenotype can predict.

For conservation, the implication is straightforward: producing physiologically and behaviorally migration-ready silver eels and enabling safe, timely progression through fragmented routes are related but distinct management problems.

## Data availability

The primary Europe-wide telemetry products and analysis code are publicly available through the source study repository and associated data release reported by Verhelst et al. (2025). This study uses processed metadata and project-level migration products without modifying the source migration classifier.

The independent Dutch consecutive-barrier reanalysis uses the public archive associated with van Rijn et al. (2026), DOI 10.17026/LS/WTSUNG.

## Code availability

All secondary-analysis code, claim boundaries and reproducible analysis definitions for this manuscript are maintained in the zuizui0223/azores repository. Canonical analyses include migration activation, stratified onset, the activation-trained multivariate entry-state score, whole-route and frozen inter-station speed transferability tests, activation-selection diagnostics, and the independent Dutch arrival-defined falsification analysis.

## Ethics statement

No animals were newly captured or handled for the present secondary analysis. Animal-handling and telemetry approvals belong to the original source studies and should be cited from those publications in the final submission.

## Author contributions

[To be completed.]

## Acknowledgements

[To be completed.]

## References

Arevalo, E., Drouineau, H., Tétard, S., Durif, C. M. F., Diserud, O. H., Poole, W. R., & Maire, A. (2021). Joint temporal trends in river thermal and hydrological conditions can threaten the downstream migration of the critically endangered European eel. *Scientific Reports*, **11**, 16927. https://doi.org/10.1038/s41598-021-96302-x

Calles, O., Elghagen, J., Nyqvist, D., Harbicht, A., & Nilsson, P. A. (2021). Efficient and timely downstream passage solutions for European silver eels at hydropower dams. *Ecological Engineering*, **170**, 106350. https://doi.org/10.1016/j.ecoleng.2021.106350

Council of the European Union. (2007). Council Regulation (EC) No 1100/2007 of 18 September 2007 establishing measures for the recovery of the stock of European eel. *Official Journal of the European Union*, L 248.

Duijns, S., Niles, L. J., Dey, A., Aubry, Y., Friis, C., Koch, S., Anderson, A. M., & Smith, P. A. (2017). Body condition explains migratory performance of a long-distance migrant. *Proceedings of the Royal Society B: Biological Sciences*, **284**, 20171374. https://doi.org/10.1098/rspb.2017.1374

Durif, C., Dufour, S., & Elie, P. (2005). The silvering process of *Anguilla anguilla*: a new classification from the yellow resident to the silver migrating stage. *Journal of Fish Biology*, **66**, 1025–1043. https://doi.org/10.1111/j.0022-1112.2005.00662.x

Goossens, S., Wybouw, N., Van Leeuwen, T., & Bonte, D. (2020). The physiology of movement. *Movement Ecology*, **8**, 5. https://doi.org/10.1186/s40462-020-0192-2

Huisman, J. B. J., Höhne, L., Hanel, R., Kuipers, H., Schollema, P. P., & Nagelkerke, L. (2023). Factors influencing the downstream passage of European silver eels (*Anguilla anguilla*) through a tidal sluice. *Journal of Fish Biology*, **103**, 347–356. https://doi.org/10.1111/jfb.15398

Nathan, R., Getz, W. M., Revilla, E., Holyoak, M., Kadmon, R., Saltz, D., & Smouse, P. E. (2008). A movement ecology paradigm for unifying organismal movement research. *Proceedings of the National Academy of Sciences USA*, **105**, 19052–19059. https://doi.org/10.1073/pnas.0800375105

Lennox, R. J., Økland, F., Jonsson, B., Aronsen, T., Austrheim, E., Diserud, O. H., et al. (2018). European eel *Anguilla anguilla* compromise speed for safety in the early marine spawning migration. *ICES Journal of Marine Science*, **75**, 1984–1991. https://doi.org/10.1093/icesjms/fsy104

Moyo, S., Britton, J. R., Major, T., Wright, R. M., Moore, A., Ives, M., Davies, P., Hall, A. E., Stamp, T., Sheehan, E. V., & Bašić, T. (2026). Initial marine movements of silver European eels *Anguilla anguilla* following their emigration from an English chalk stream. *Hydrobiologia*. https://doi.org/10.1007/s10750-026-06406-6

Sandlund, O. T., Diserud, O. H., Poole, R., Bergesen, K., Dillane, M., Rogan, G., Durif, C., Thorstad, E. B., & Vøllestad, L. A. (2017). Timing and pattern of annual silver eel migration in two European watersheds are determined by similar cues. *Ecology and Evolution*, **7**, 5956–5966. https://doi.org/10.1002/ece3.3099

Sundin, J., Persson, J., Wickström, H., Sjöberg, N., Renman, O., & Skoglund, S. (2022). Evaluation of sampling methods for maturation stage determination in the European eel *Anguilla anguilla*. *Marine and Coastal Fisheries*, **14**, e10219. https://doi.org/10.1002/mcf2.10219

Tudorache, C., Burgerhout, E., Brittijn, S., & van den Thillart, G. (2015). Comparison of swimming capacity and energetics of migratory European eel (*Anguilla anguilla*) and New Zealand short-finned eel (*A. australis*). *Frontiers in Physiology*, **6**, 256. https://doi.org/10.3389/fphys.2015.00256

Katopodis, C., & Gervais, R. (2016). *Fish swimming performance database and analyses*. Canadian Science Advisory Secretariat Research Document 2016/002. Fisheries and Oceans Canada.

van Rijn, J., Kuipers, H. J., & Huisman, J. B. J. (2026). Seaward migration of European Eel through consecutive migration barriers: passage at a pumping station and tidal sluice. *Canadian Journal of Fisheries and Aquatic Sciences*, **83**, 1–14. https://doi.org/10.1139/cjfas-2025-0359

Winkler, D. W., Jørgensen, C., Both, C., Houston, A. I., McNamara, J. M., Levey, D. J., Partecke, J., Fudickar, A., Kacelnik, A., Roshier, D., & Piersma, T. (2014). Cues, strategies, and outcomes: how migrating vertebrates track environmental change. *Movement Ecology*, **2**, 10. https://doi.org/10.1186/2051-3933-2-10

Verhelst, P., Righton, D., Aarestrup, K., Almeida, P. R., Bašić, T., Bolland, J. D., Carter, L., Coeck, J., Costa, J. L., Dainys, J., Davidsen, J. G., Domingos, I., Dorow, M., Feunteun, E., Frankowski, J., Griffioen, A. B., Monteiro, R. M., Moore, A., Oldoni, D., et al. (2025). The seaward migration of European eel at a continental scale: a Europe-wide biotelemetry meta-analysis. *Fish and Fisheries*, **26**, 651–668. https://doi.org/10.1111/faf.12904
