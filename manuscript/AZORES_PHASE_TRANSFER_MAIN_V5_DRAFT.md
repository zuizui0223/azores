# A multivariate entry state predicts migration activation but not realized transit speed in European eel

**Condensed main-manuscript candidate V5 — author review, not submitted**

**Authors:** [to be completed from actual contributors]

**Affiliations:** [to be completed from actual contributors]

## Abstract

Migration involves at least two different ecological transitions: entering a migratory state and moving through the subsequent route. Yet a phenotype measured before departure is often treated as a general index of migratory performance. We asked whether capture-time silvering and body condition in European eel (*Anguilla anguilla*) predict downstream migration activation and, independently, realized movement speed after activation. We analysed fixed public telemetry products from six European projects, preserving source migration classifications and expert corrections. The study included 575 stage-coded female eel tracks and phase-specific evaluable risk sets. An activation-only multivariate model assigned additional associations to Durif stage (odds ratio, OR, 2.13 per stage, 95% CI 1.60–2.84) and standardized weight-for-length condition (OR 1.46, 1.16–1.83). A score trained only against activation predicted activation (OR 2.23 per SD, 1.70–2.92) and earlier recorded onset (hazard ratio 1.32, 1.17–1.49), but not whole-route speed (speed ratio 0.946, 0.832–1.076) or positive inter-station speed (1.028, 0.869–1.215). This phase boundary persisted when score weights were fitted without the focal project and when movement speed was evaluated within the same directed receiver links. Silvering-stage associations with initiation nevertheless differed among projects after adjusting for release-year margins (exact conditional p=0.00314; sensitive to Albertkanaal). An independent Dutch barrier archive did not support a simple condition-dependent waiting or opening-window mechanism. These developmental secondary analyses identify an important *transferability boundary*: a phenotype that ranks entry into migration need not rank realized progress through a heterogeneous route. Readiness and passage opportunity should therefore be evaluated as distinct ecological and conservation targets.

**Keywords:** *Anguilla anguilla*; silvering; migration activation; movement ecology; habitat connectivity; individual state; telemetry.

## Introduction

Animal migration is a sequential process rather than a single event. An individual must first become ready and express movement; subsequently, its realized progression depends on the opportunities, constraints and risks along a route. These phases can respond to different internal and external factors. Yet a common analytical shortcut is to relate a capture-time physiological or morphological index directly to an aggregate movement outcome and treat the result as general migration performance. Such aggregation risks conflating propensity to initiate, timing of onset, speed after departure and ultimate arrival (Nathan et al. 2008; Winkler et al. 2014).

European eel offers a particularly informative case. During silvering, body shape and appearance change alongside maturation towards spawning migration. The Durif female categories distinguish the premigrant FIII phenotype from more advanced FIV and FV phenotypes (Durif et al. 2005). A positive association between silvering stage and downstream departure is therefore expected, not by itself a conceptual advance. The harder question is whether that same initial phenotype continues to rank movement once the eel has crossed the behavioral entry threshold. For eel, transit can also depend on discharge opportunities, physical barriers, detection coverage and route characteristics; none is reducible to capture-time silvering.

Two hypotheses generate distinct predictions. Under a **general-performance hypothesis**, capture-time silvering and condition jointly rank both initiation and subsequent realized speed. Under a **phase-specific entry hypothesis**, capture-time phenotype predicts whether and when downstream migration becomes behaviorally expressed but may carry little transferable information about speed among individuals that have already entered the migratory phase. A third, context-dependent hypothesis predicts that even the relation between silvering and entry may vary across river projects. These are observational predictions, not claims that the measured phenotype causes a migration decision.

We tested these predictions using processed telemetry records underlying a Europe-wide eel synthesis (Verhelst et al. 2025). To avoid treating a model trained separately for each endpoint as a different biological phenotype, we fitted one multivariate *entry-state score* using classified activation alone and then applied its weights unchanged to onset and two post-activation speed endpoints. We repeated score training with each project held out. We separately checked exact directed receiver links, classification uncertainty and an independent Dutch barrier archive. Our aim was to determine what a capture-time phenotype can and cannot tell us about the successive ecological phases of seaward migration.

## Methods

### Source cohort, states and ethical scope

We used the published cleaned project-level movement tables and metadata of Verhelst et al. (2025). The continental source assembled 2,306 tagged eels across 18 water bodies; this secondary analysis selected the six projects with exact female Durif stage FIII, FIV or FV, compatible cleaned movement products, body length and release timing: Warnow, Leopoldkanaal, Albertkanaal, the 2015 Verhelst project, Grote Nete and ESGL. We did not reprocess raw tracks, optimize a new movement classifier or classify individuals absent from cleaned data as nonmigrants.

Of 603 metadata entries with candidate FIII–FV stages, 575 had evaluable cleaned stage-coded tracks. Most of the 28 unmatched entries had explicit source exclusion reasons; one had no post-release detection in the relevant cleaned source. Importantly, nine algorithmically classified migrants in the 2015 project were labelled nonmigratory by source expert assessment. We retained these corrections for all primary analyses. We model the resulting **source-classified downstream migration activation**, not unobserved physiological intent, successful ocean escapement or survival. No animals were newly handled in this secondary analysis.

### Capture phenotype and activation-trained score

Female stage was coded ordinally (FIII=0, FIV=1, FV=2). Continuous capture condition was based on standardized residual log body mass after accounting for log body length, project and Durif stage. Because mass, length and external morphology also contribute to silvering classification, this term represents weight-for-length information *beyond the coarse stage variable*, not direct energetic stores or an independent endocrine assay.

We first modeled activation using stage, condition and source-aligned project/release-year, length and release-date adjustments. Interactions were explored separately and did not support a simple compensatory state model. For transferability, we took the two multivariate coefficients estimated **only from the activation outcome** and defined a linear capture entry score, R = beta_stage × stage + beta_condition × standardized condition. Its relative coefficients were held fixed when moving to the onset and speed endpoints, and the resulting score was scaled to one SD within each evaluable analysis set. The score is an observed activation-associated composite; it is not a validated latent physiological quantity.

The phase comparison uses its own predefined observational risk set for each outcome. The multivariate activation score analysis comprised 525 individuals. Onset comprised 570 individuals, of whom 418 had a classified threshold-crossing event. Whole-route speed comprised 418 activated individuals; the independently frozen individual median positive inter-station speed endpoint comprised 411. An estimate on one endpoint is not interpreted as if the same unit, baseline hazard or biological sample applies unchanged to all other endpoints.

### Onset, progression and transfer robustness

Time to onset was calculated from release to the source distance-threshold crossing attached to the first row where downstream_migration was true, not the first broader migration-interval row. Noninitiators were censored at their last available observation. A Cox model used project × release-year baseline strata and relevant body-length, release-timing and capture-state predictors. It estimates the recorded onset hazard under the source observation process; absence of classification is not a verified failure to migrate.

The primary progression endpoints were the source-defined whole-route speed and the separately frozen within-eel median positive inter-station speed after activation. Because the activation-trained coefficients might fit idiosyncrasies of the six source projects, we re-estimated stage and condition weights in six folds, each withholding one entire project. The learned weights were transferred to the held-out project without refitting them on that project's endpoint labels. Predictor preprocessing retained shared panel elements, so this is **cross-project developmental evaluation**, not fully prospective external validation.

We also checked whether route averaging obscured a capture-state effect on speed. The within-link audit compared 17,792 source-positive movements from 418 eels across 244 directed receiver pairs with at least five unique eels per link. Directed link and project-year effects were controlled; each eel received equal total weight, and uncertainty was clustered by eel. Before final interpretation we identified biologically implausible extreme source ground-speed values (up to 3,752 m s⁻¹); post-hoc screens excluding values above 2.5, 5 and 10 m s⁻¹ were therefore labelled **data-quality sensitivities**, not physiological maximum speeds or a replacement of the frozen primary endpoint.

### Heterogeneity, observational uncertainty and independent mechanism test

The stage–initiation association was examined across six source projects, including exact FIII/FV tables with sparse or separated cells. We ran a conditional exact heterogeneity test and a stricter analysis conditioned separately on 14 project × release-year margins. Leave-one-project-out sensitivity quantified dependence on individual waterways. This analyzes heterogeneity in **observed stage–classified-initiation associations**, not variation in experimentally controlled physiological responses.

A separate project-held-out analysis tested whether continuous condition added activation discrimination beyond stage, length and release timing. It evaluated positive–negative pairs within held-out project-year strata, reported both fish-conditional and project-resampling uncertainty and considered incomplete tracking of apparent noninitiators. Morphological eye and fin measurements were available in a five-project subset for an additional exploratory adjustment. We treated the resulting extra analyses as supplementary because they do not establish a universally portable or causally distinct condition mechanism.

Finally, the public Dutch consecutive-barrier archive (van Rijn et al. 2026) provided a deliberately independent falsification of one possible post-onset mechanism: better-conditioned eels might choose longer sluice/opening opportunities or tolerate more post-arrival waiting. Risk sets were defined by observed barrier arrival, event start and passage, without using the original event-validity flag when that flag depended on opportunity duration itself. We tested condition-dependent opening-window choice, missed post-arrival events and waiting times. This Dutch archive does not directly replicate the six-project activation-score model.

## Results

### Migration initiation and onset were capture-state dependent

Activation frequencies increased from 154/261 FIII fish (59.0%) to 53/68 FIV (77.9%) and 215/246 FV (87.4%). Adjusted for project-year, length and timing, an ordinal stage increment was associated with initiation odds ratio 2.08 (95% CI 1.56–2.76). Onset analysis also showed an association with advanced stage (hazard ratio 1.29, 1.13–1.47); 418 of 570 eligible eels had source-classified onset.

Stage and continuous capture condition contributed jointly to the activation model. The adjusted stage effect was OR 2.13 per stage (1.60–2.84) and the weight-for-length condition effect was OR 1.46 per SD (1.16–1.83). The continuous term may recover information hidden by coarse silvering stage, but does not identify physiological fat reserves independently of the external traits used to derive Durif categories.

### Activation-trained capture state did not rank generic transit speed

The score estimated only from activation had weights 0.756 for stage and 0.379 for standardized condition. For one SD of the resulting score, the activation odds ratio was 2.23 (1.70–2.92); the onset hazard ratio was 1.32 (1.17–1.49). In contrast, the whole-route speed ratio was 0.946 (0.832–1.076; p=0.396, partial R²=0.18%), and the positive inter-station speed ratio was 1.028 (0.869–1.215; p=0.750, partial R²=0.026%) (Figure 3). The two speed estimates do not support a general positive transfer of activation score, but confidence intervals do not prove an exactly zero effect.

When the entry-score weights were trained without each focal project, the same qualitative boundary remained. The project-held-out score predicted activation (OR 1.97, 1.53–2.53) and onset (hazard ratio 1.26, 1.12–1.42), but neither whole-route speed (ratio 0.948, 0.836–1.075) nor inter-station speed (1.013, 0.860–1.192). The phase distinction was therefore not a trivial consequence of training and evaluating the score's relative weights against activation outcomes from the same waterway.

Within identical directed receiver links, the effect on source-derived transit speed remained near null: ratio 0.962 per SD (0.883–1.048; p=0.372). Gross-speed screens removed 53–63% of candidate positive segment observations, yet the corresponding ratios were 0.941–0.944 and all intervals included one. These screens flag the unreliability of absolute source ground speeds as eel swimming-capacity measurements; they do not rescue a general positive internal-state speed ranking.

### The initiation association varied among rivers

The stricter exact FV/FIII test retaining 507 relevant fish and conditioning on project/release-year margins rejected a common source-classified association across all six projects (likelihood ratio 19.087; exact p=0.003142 across 46,116 admissible configurations). Five of six leave-one-project-out year-adjusted tests remained below p=0.05; excluding Albertkanaal gave p=0.05310. Thus contextual heterogeneity was detectable beyond release-year baseline differences, but strongly influenced by one project. This does not establish that river hydraulics or silvering physiology caused the differences; receiver coverage, classification and source-specific release or tracking choices also vary.

In a separate held-out activation-ranking analysis, adding condition raised within-project-year stratified AUC from 0.610 to 0.643 (+0.0336). Four of six projects had positive increments; the six-project bootstrap interval (−0.0007 to +0.0918) included zero. Continuous eye/fin morphology in a five-project subset did not establish robust condition portability after adjustment. In the observation audit, hypothetical misclassification of only 11 selected short-follow-up source negatives was sufficient under a worst-case selection to erase the added AUC; these are unobserved *possibilities*, not eleven documented missed starts. This constrains the case for a universal extra energetic benefit of body condition.

### A proposed condition-dependent barrier opportunity mechanism was unsupported

Arrival-defined Dutch tests did not support the prediction that better condition led to more missed opening events, longer post-arrival delay or stronger choice of longer opening windows. At the tidal sluice, the condition × opening duration interaction was −0.095 (permutation p=0.849; n=15 informative fish). Pumping-station matched-choice estimation was unstable and was not assigned a biological sign. Broader waiting measures had permutation p-values 0.35–0.96, with small samples. These findings constrain one proposed mechanism; they neither show that external opportunities are irrelevant nor provide a direct replication of the Europe-wide effect (Figure 4).

## Discussion

The main ecological conclusion is a **phase-specific transferability boundary**, not a claim that silvering affects whether an eel migrates. The latter is expected from the biology of the Durif classification. What is informative is that an activation-trained multivariate phenotype also ranked the recorded onset transition, but explained negligible additional variation in general post-activation speed summaries. The same pattern occurred under project-held-out weight estimation and within-link route control. A capture-time state associated with migration entry is therefore not automatically a general ranking of realized progression quality.

This need not imply two mutually exclusive causal systems. Physiological state can remain relevant after departure even when a particular measured capture-stage/condition score transfers poorly. An eel may change its physiological state after release, and post-activation speed is measured only among eels selected through a stage-dependent initiation filter. Neither the original capture records nor the public telemetry provide repeated silvering measurements at true behavioral onset. Movement opportunity, individual energetics, hydraulics, barrier passage and imperfect observation can all shape realized progression. The current analysis identifies which predictions fail to transfer, not which alternative route driver is causally responsible.

The multivariate result is also more nuanced than a simple independent-energy story. A weight-for-length residual increased activation association after coarse ordinal stage adjustment, but stage assignment already uses related external morphometrics. In a subset with continuous eye and fin measurements, the remaining conditional activation-ranking benefit of weight-for-length was positive in the pooled comparison but heterogeneous across projects. Its practical prediction value under incomplete observation was sensitive to the assumed pattern of missed initiations. We therefore interpret continuous condition as *additional information in capture phenotype*, not a demonstrated metabolic reserve or a biologically universal threshold.

The river-level heterogeneity provides an additional positive ecological pattern. After holding release-year baseline structure fixed, the FV/FIII initiation relationship was not uniform across projects. This is compatible with environmental context modifying whether silvering is expressed as observable downstream migration, but it is not a hydrological mechanism test: observed associations could also be altered by receiver deployment, fish selection and source-specific classification. Future research could pair physiological maturation with measured discharge, barrier operations and receiver detection to distinguish ecological opportunity from observation-process heterogeneity. One influential project limits how strongly a general modifier can be inferred from this six-context dataset.

The Dutch data illustrate the value of separating a mechanistic prediction from general ecological plausibility. Movement must occur through openings and barriers, yet the specific hypothesis that better-conditioned eels favor longer opportunities or wait longer once at the barrier was unsupported. Other opportunity mechanisms—such as threshold-triggered discharge responses, avoidance of high-risk routes, learning or energetic fatigue—remain possible and would require better time-aligned environmental and behavioral data.

The management distinction is direct, but conditional. Producing migration-ready silver eels and ensuring usable passage opportunities are related yet different targets. Growth habitats and maturation affect the pool of fish that can initiate; barrier management, bypasses and safe discharge windows may affect what becomes possible after departure. Our data do not estimate biological escapement or demonstrate that any particular intervention improves survival. They instead caution against assessing both transitions by a single capture-time readiness score.

### Limitations

All results are developmental secondary analyses of public, processed, nonrandomized source products. Classified activation reflects monitoring geometry and thresholds as well as animal behavior. Speed fields include extreme artifacts, and post-hoc quality screens can assess but not retroactively repair their original measurement process. Initiation-dependent speed analyses condition on eels that entered movement; unmeasured selection is not removed by measured-propensity corrections. With only six partly heterogeneous projects, inference about cross-river portability is limited, while the independent Dutch dataset has sparse stage and choice information. Odds, onset-hazard and speed ratios describe different responses and are not quantitatively interchangeable causal coefficients.

The underlying six-project program is not six independent prospective biological replications. Nor does a near-null speed result prove no internal-state effects. The stronger claim—that capture phenotype is an entry-state indicator, not a universally transferable realized-transit-speed predictor—is the scope warranted here.

## Conclusions

European eel migration should be analyzed as a series of ecological transitions rather than a single state of performance. Silvering stage and weight-for-length condition jointly predicted classified entry, and an activation-trained score also ranked onset. That score did not provide a robust general ranking of transit speed, even after project-held-out weighting and within-link comparison. Contextual initiation associations varied among waterways; one proposed condition-dependent barrier-waiting explanation was unsupported. The ecological implication is to distinguish internal **readiness for migration** from opportunities for **progression through the route**, without treating their observational separation as proof of a specific physiological or hydraulic mechanism.

## Figures

- **Figure 1:** Six-project source cohort and phase-specific eligible samples — [V4 source-matched SVG](rendered_figures_v4/Figure1.svg).
- **Figure 2:** Classified stage initiation frequencies and multivariate capture phenotype — [V4 source-matched SVG](rendered_figures_v4/Figure2.svg).
- **Figure 3:** Activation-derived score transferred to onset and two speed endpoints — [V4 source-matched SVG](rendered_figures_v4/Figure3.svg).
- **Figure 4:** Independent Dutch matched barrier opportunity falsification — [V4 source-matched SVG](rendered_figures_v4/Figure4.svg).

## Data, code and ethics

Original eel telemetry products and metadata are from Verhelst et al. (2025); the Dutch opening/detection archive is at DOI 10.17026/LS/WTSUNG. Reanalysis scripts, numeric contracts and original full-length exploratory/sensitivity text are archived in the [azores repository](https://github.com/zuizui0223/azores). No animals were newly captured or handled for the reanalysis. Original animal-care approvals must be documented from each source study before journal submission.

**Author contributions and acknowledgements are not yet populated. This is a scientific main-text candidate, not a certified journal-format submission.** Detailed observational and stage-specific sensitivities remain in [full V4 evidence manuscript](AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md) and must be allocated to the eventual supplement under journal requirements.

## References (core subset, preserved from V4)

Durif, C., Dufour, S., & Elie, P. (2005). The silvering process of *Anguilla anguilla*: a new classification from the yellow resident to the silver migrating stage. *Journal of Fish Biology*, **66**, 1025–1043. https://doi.org/10.1111/j.0022-1112.2005.00662.x

Nathan, R., Getz, W. M., Revilla, E., Holyoak, M., Kadmon, R., Saltz, D., & Smouse, P. E. (2008). A movement ecology paradigm for unifying organismal movement research. *Proceedings of the National Academy of Sciences USA*, **105**, 19052–19059. https://doi.org/10.1073/pnas.0800375105

Tudorache, C., Burgerhout, E., Brittijn, S., & van den Thillart, G. (2015). Comparison of swimming capacity and energetics of migratory European eel (*Anguilla anguilla*) and New Zealand short-finned eel (*A. australis*). *Frontiers in Physiology*, **6**, 256. https://doi.org/10.3389/fphys.2015.00256

van Rijn, J., Kuipers, H. J., & Huisman, J. B. J. (2026). Seaward migration of European Eel through consecutive migration barriers: passage at a pumping station and tidal sluice. *Canadian Journal of Fisheries and Aquatic Sciences*, **83**, 1–14. https://doi.org/10.1139/cjfas-2025-0359

Verhelst, P., Righton, D., Aarestrup, K., Almeida, P. R., Bašić, T., Bolland, J. D., Carter, L., Coeck, J., Costa, J. L., Dainys, J., Davidsen, J. G., Domingos, I., Dorow, M., Feunteun, E., Frankowski, J., Griffioen, A. B., Monteiro, R. M., Moore, A., Oldoni, D., et al. (2025). The seaward migration of European eel at a continental scale: a Europe-wide biotelemetry meta-analysis. *Fish and Fisheries*, **26**, 651–668. https://doi.org/10.1111/faf.12904

Winkler, D. W., Jørgensen, C., Both, C., Houston, A. I., McNamara, J. M., Levey, D. J., Partecke, J., Fudickar, A., Kacelnik, A., Roshier, D., & Piersma, T. (2014). Cues, strategies, and outcomes: how migrating vertebrates track environmental change. *Movement Ecology*, **2**, 10. https://doi.org/10.1186/2051-3933-2-10
