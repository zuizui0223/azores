# Internal migratory readiness governs activation but attenuates during progression in European eel

**Manuscript draft V2**

**Authors:** [to be completed]

**Affiliations:** [to be completed]

## Abstract

Animal migration requires both readiness to leave and opportunity to progress, yet these components are often analysed as if they were a single movement phenotype. We tested whether the predictive importance of internal migratory state changes across sequential phases of seaward migration in European eel (*Anguilla anguilla*). We analysed public telemetry products from six European projects in which female Durif stages FIII–FV were available together with a common movement-based migration classification. The primary cohort contained 575 individuals after retaining the source processing and expert corrections.

Migration initiation increased from 59.0% in FIII to 77.9% in FIV and 87.4% in FV eels. With project × release-year effects and adjustment for body length and release timing, the odds of initiating migration increased 2.08-fold per Durif-stage increment (95% CI 1.56–2.76). A stratified Cox analysis likewise showed earlier migration onset at more advanced stages (hazard ratio 1.28, 95% CI 1.12–1.45). In contrast, among eels that had initiated migration, Durif stage provided little general predictive information for subsequent completion (odds ratio 1.15, 95% CI 0.83–1.59) or migration speed (multiplicative ratio 0.983, 95% CI 0.852–1.134). A direct stacked two-phase model confirmed that the stage effect was stronger at initiation than at completion (ratio of odds ratios 1.81, 95% CI 1.15–2.84; interaction p = 0.0099). The direction of this attenuation remained unchanged in all leave-one-project-out analyses.

Across the six projects, a coarse water-regulating-structure impact score was unrelated to initiation but negatively aligned with completion after initiation; this project-level comparison is contextual rather than causal. An independent Dutch study of 40 FIII–FV eels crossing a pumping station and tidal sluice provides complementary evidence that post-activation progression is shaped by barrier-specific discharge opportunity, wind, lunar conditions and prior passage experience.

Our results support a sequential view of migration: internal silvering state strongly predicts entry into the migratory movement state, whereas its general predictive advantage attenuates during subsequent progression. This distinction separates the production of migration-ready eels from successful escapement through regulated routes and suggests that the biological controls of migration should be evaluated phase by phase rather than only at a final endpoint.

**Keywords:** *Anguilla anguilla*; animal movement; migration; silvering; Durif stage; telemetry; barrier passage; internal state; movement ecology

---

## Introduction

Animal movement emerges from a dynamic interaction between internal motivation, the capacity to move and navigate, and the external environment through which movement is realised (Nathan et al. 2008). For migration, that interaction unfolds sequentially. An animal must first enter a migratory state, then move through a route whose hydrology, barriers, habitat geometry and temporal windows of opportunity can permit, delay or prevent further progress. Nevertheless, migration is often analysed using a single endpoint such as departure, speed, arrival or final success. Pooling these phases can obscure whether the same biological variables control the decision to begin moving and the fate of movement after it has begun.

European eel (*Anguilla anguilla*) offers an unusually informative system in which to separate these phases. The continental growth phase ends with silvering, a coordinated suite of morphological and physiological changes associated with preparation for the oceanic spawning migration. Durif et al. (2005) classified females into growth, pre-migrant and migrating stages; FIII represents a pre-migrant state, whereas FIV and FV represent progressively silvered migrating states. Because this stage is measured from the animal rather than inferred from its later telemetry path, it provides an internal-state axis that can be compared with subsequent realised movement.

At the same time, downstream migration takes place through strongly heterogeneous landscapes. Eels may move through free-flowing river reaches, canals, navigation structures, pumps, weirs, hydropower facilities and tidal sluices. Flow, rainfall, darkness and lunar conditions can alter migration timing, while water-regulating structures can impose substantial delay or restrict passage (Verhelst et al. 2025; Huisman et al. 2023; van Rijn et al. 2026). The Europe-wide biotelemetry synthesis of Verhelst et al. (2025), which combined 2,306 tagged eels from 18 water bodies, showed both broad geographic pattern and substantial within-system plasticity in seaward migration. It also developed a common movement-based classifier to harmonise migration identification across heterogeneous telemetry projects.

These features allow a more specific question than whether internal state and external environment both matter. We ask whether **the predictive importance of internal migratory readiness changes after migration has been activated**. If silvering primarily regulates readiness to depart, then FIII→FIV→FV should strongly predict whether and when directed downstream migration begins. If subsequent progression is increasingly constrained by route-specific opportunity, the same Durif-stage gradient should weaken for post-initiation speed and completion.

A comparison of significance across separate models would not be sufficient to demonstrate such a phase difference. We therefore directly estimated the same ordinal Durif effect at two sequential gates—migration initiation and completion conditional on initiation—and tested the difference between those coefficients using individual-clustered uncertainty. We complemented this test with time-to-onset and post-initiation speed analyses, a project-level route-resistance diagnostic, and an independent published Dutch consecutive-barrier study.

We predicted that (1) advanced Durif stage would increase both the probability and rate of migration activation, but (2) its general predictive effect would be significantly attenuated after activation. This phase-specific prediction reframes migration as a sequence of ecological filters rather than a single movement outcome.

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

To avoid reducing activation timing to an arbitrary fixed-day threshold, we also fitted a stratified Cox proportional-hazards model. Individuals were followed from release to the first source-classified migration onset; non-initiators were censored at their last available telemetry observation.

The Cox model used separate baseline hazards for project × release-year strata and the same covariates as the initiation model: within-stratum body length per 100 mm, within-stratum release timing per 100 days and ordinal Durif stage. Tied event times were handled with the Breslow approximation.

The time-to-event dataset contained 570 individuals and 418 onset events across 13 project-year strata. We evaluated project dependence by repeating the stage estimate after omitting each source project in turn.

### Gate 2: completion conditional on initiation

To isolate progression from activation, the Gate-2 analysis included only eels classified as having initiated migration under the expert-corrected source definition. The endpoint was membership in the source study's published successful-migrant set.

We used the same project × release-year structure, within-stratum body-length adjustment, within-stratum release-timing adjustment and ordinal Durif coding as in Gate 1. This analysis therefore asked whether silvering stage continued to provide a general advantage **after the animal had already entered the migratory state**.

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

### Direct phase-interaction test

The principal test compared the Durif coefficient directly between migration phases.

Each tracked individual contributed one initiation row. Individuals that initiated migration contributed a second row for completion. We then fitted a stacked logistic model with phase-specific project × release-year intercepts and phase-specific coefficients for body length, release timing and Durif stage.

Because an initiating individual could contribute observations to both phases, uncertainty was estimated with a sandwich covariance clustered by individual tag.

The principal contrast was

\[
\Delta \beta_D
=
\beta_{D,\mathrm{initiation}}
-
\beta_{D,\mathrm{completion}},
\]

reported equivalently as the ratio

\[
\frac{\mathrm{OR}_{\mathrm{initiation}}}
{\mathrm{OR}_{\mathrm{completion}}}.
\]

A ratio above one indicates stronger Durif-stage control at initiation than after initiation. Robustness was assessed by repeating the full phase interaction after leaving out each project.

### Project-level route-context diagnostic

To ask whether broad route context aligned differently with the two gates, we used the source study's water-regulating-structure (WRS) impact score. For each of the six projects we calculated the median WRS impact among focal stage-coded individuals and compared it with migration initiation and completion among initiators.

Associations were summarized by Spearman rank correlation. With only six projects, two-sided exact permutation p-values were calculated by enumerating all 6! assignments.

This analysis was explicitly treated as **contextual bridge evidence**, not causal inference: WRS intensity is strongly confounded with project identity, hydrology, barrier type, telemetry design and endpoint observability.

### Independent Dutch consecutive-barrier evidence

We used the published results of van Rijn, Kuipers and Huisman (2026) as an independent ecological constraint on the Gate-2 interpretation. Their study tracked 40 FIII–FV European eels through a pumping station, a lake and a tidal sluice. Thirty-five passed the pumping station and 27 completed seaward passage; mean cumulative barrier delay was approximately 34 days.

We did not re-fit this study to search for a Durif effect. Instead, we used its published barrier-specific results to evaluate whether post-activation progression was consistent with external opportunity and route-history effects. The study reported associations with discharge-event duration, wind, lunar illumination, body or movement traits and prior barrier experience. Durif stage did not remain a generic pumping-station predictor and was not separately identifiable from body mass at the tidal sluice.

### Evidence class

All Europe-wide analyses are secondary analyses of public data and were developed after inspection of source outcomes. They are therefore described as **developmental independent evidence**, not preregistered or response-blind confirmation. The Dutch study provides independent published ecological corroboration but does not constitute a direct replication of the phase-interaction model.

---

## Results

### Advanced Durif stage strongly predicted migration activation

The final evaluable cohort comprised 575 FIII–FV females with compatible cleaned migration tracks. Expert-corrected initiation increased monotonically with silvering stage: 154 of 261 FIII eels (59.0%), 53 of 68 FIV eels (77.9%) and 215 of 246 FV eels (87.4%) initiated classified downstream migration.

After project × release-year adjustment and control for within-stratum body length and release timing, each one-stage increase in Durif classification was associated with a 2.08-fold increase in the odds of migration initiation (95% CI 1.56–2.76; p = 4.2×10\(^{-7}\)).

### More advanced stage predicted earlier migration onset

The time-to-event analysis contained 570 individuals and 418 migration-onset events. Each FIII→FIV→FV increment increased the instantaneous migration-onset rate by 28% (HR 1.28, 95% CI 1.12–1.45; p = 0.00022).

The stage HR remained above one in every leave-one-project-out analysis, ranging from 1.10 to 1.47. Omitting the 2015 project produced the weakest and least precise estimate, with the 95% interval crossing one. Thus, the average onset association was positive but not fully project-independent in precision.

### Durif stage provided little general completion advantage after initiation

Once migration had been activated, the general Durif gradient weakened markedly. In the conditional completion model, the adjusted odds ratio per stage increment was 1.15 (95% CI 0.83–1.59; p = 0.412).

Thus, a more advanced capture-time silvering stage did not translate into a clear project-independent increase in the probability of reaching the source study's successful-migrant endpoint once an eel had already entered the migration state.

### Post-initiation migration speed showed no general Durif gradient

Among 418 initiated eels retained in informative project-year strata, median migration speeds were 0.0229 m s\(^{-1}\) for FIII, 0.0232 m s\(^{-1}\) for FIV and 0.0245 m s\(^{-1}\) for FV.

After adjustment, the multiplicative change in migration speed per Durif-stage increment was 0.983 (95% CI 0.852–1.134; p = 0.815). The attenuation of the internal-stage signal therefore was not specific to the binary completion endpoint.

### Direct phase comparison confirmed attenuation of the stage effect

The stacked phase model contained 575 individuals, 910 phase observations and 22 informative phase × project-year strata.

The cluster-robust stage effect at initiation was OR 2.08 per Durif increment (95% CI 1.55–2.77), whereas the corresponding completion effect was OR 1.15 (95% CI 0.81–1.62).

The ratio of stage odds ratios was 1.81 (95% CI 1.15–2.84; p = 0.0099), directly demonstrating stronger Durif control at initiation.

All six leave-one-project-out estimates retained a ratio above one (range 1.55–2.13). Five of six remained below p = 0.05; omitting the 2015 project reduced precision (OR ratio 1.55, 95% CI 0.94–2.56; p = 0.083). The attenuation was therefore directionally robust, although formal precision depended partly on the 2015 system.

### Route context aligned with Gate 2 rather than Gate 1

Across six project contexts, median WRS impact was essentially unrelated to migration initiation (Spearman \(\rho=0.029\), exact p = 0.983).

In contrast, median WRS impact was negatively associated with completion after initiation (\(\rho=-0.928\), exact p = 0.022). The negative relationship remained strong when individual projects were removed and also persisted after standardization to a common FIII/FIV/FV stage composition.

Because this comparison contains only six non-randomized project contexts, it cannot identify a causal WRS effect. Its role is narrower: the same broad external-context descriptor aligned with progression or completion but not activation.

### An independent consecutive-barrier system showed barrier-specific post-activation control

In the independent Dutch study, 35 of 40 tagged FIII–FV eels passed a pumping station and 27 completed seaward passage through a subsequent tidal sluice, accumulating approximately 34 days of mean barrier delay (van Rijn et al. 2026).

Published analyses identified barrier-specific predictors rather than a common monotonic Durif-stage effect. Pump passage was associated with discharge opportunity and wind, whereas tidal-sluice passage was associated with lunar illumination; previous pumping-station passage experience also predicted faster subsequent sluice passage. Durif stage was dropped from the pumping-station individual model and was non-identifiable from body mass in the tidal-sluice analysis.

These results do not replicate our phase interaction statistically, but they independently constrain its interpretation: once migration is active, progression through a real route can be strongly shaped by barrier-specific opportunity and prior route experience.

---

## Discussion

### Migration is a sequence of ecological filters

Our central result is not simply that silvering predicts eel migration. That relationship is expected from the biological meaning of the Durif framework. The new result is that the predictive strength of the same internal-state axis is **phase dependent**.

Advanced FIII→FIV→FV stage strongly predicted whether classified downstream migration began and was associated with earlier onset. Once migration had begun, however, the same stage gradient did not provide a clear general advantage for either migration speed or final completion. The direct clustered phase comparison showed that the stage coefficient itself was significantly larger at initiation than at completion.

This distinction matters because a final migration-success endpoint compresses several processes into one number. A successful migrant must be ready to leave, initiate movement, encounter suitable hydrological windows, negotiate barriers, avoid excessive delay and remain observable through the endpoint. A predictor can therefore appear to explain migration success because it acts strongly at only one of these filters. Decomposing the sequence exposes where its information is concentrated.

### Silvering readiness primarily predicts entry into movement

Durif stages were developed to distinguish resident, pre-migrant and migrating eel phenotypes (Durif et al. 2005). Our initiation result therefore should not be presented as the discovery that silver eels migrate. Instead, it validates capture-time Durif stage as an informative, movement-independent readiness axis within the public multi-project telemetry panel and establishes a Gate-1 benchmark against which post-initiation effects can be compared.

The association remained after project-year stratification, body-length adjustment and release-timing adjustment. More advanced stage also predicted a higher onset hazard without imposing a fixed onset window. Because the same predictor and ordinal coding were carried into Gate 2, attenuation cannot be attributed merely to switching from one biological readiness measure to another.

The result is consistent with the movement-ecology view that internal state governs motivation or readiness to move (Nathan et al. 2008), but adds a temporal qualification: the informational value of internal readiness need not remain constant throughout a movement path.

### Internal-state control attenuates during progression

The post-initiation results were strikingly different. Neither completion nor migration speed showed a comparable general Durif gradient. Importantly, our conclusion does not rest on one model being significant and another not. The stacked analysis directly estimated the difference between phase-specific stage coefficients and supported stronger Durif control at initiation.

We therefore interpret the result as an **attenuation of relative internal-state control**, not as disappearance of internal effects. Individual traits can still influence barrier approach, swimming performance or persistence after departure, and external conditions can also affect activation. The supported claim is that the general, transferable Durif-stage advantage is concentrated more strongly at the activation gate.

This phase dependence provides a more mechanistic reading of heterogeneity in the Europe-wide source data. Verhelst et al. (2025) reported large variation in migration phenology and speed within and among water bodies, with water-regulating structures and tidal context contributing to that heterogeneity. Our decomposition suggests that one reason a single continental movement model can remain heterogeneous is that different systems act most strongly after the readiness filter has already been passed.

### Route opportunity increasingly filters realised migration

Our project-level WRS result is consistent with this interpretation but must be treated conservatively. Median WRS impact was almost unrelated to initiation, yet strongly negatively ranked with completion after initiation. This contrast persisted under stage standardization and leave-one-project-out checks. However, only six project contexts were available and WRS is entangled with hydrology, structure type, telemetry design and endpoint observability. The project-level correlation therefore cannot establish that WRS caused the Gate-2 pattern.

Independent barrier studies provide more direct ecological context. Passage through tidal sluices can depend on the magnitude and dynamics of discharge events, and individual eels can experience substantial barrier delay even after reaching a migration obstacle (Huisman et al. 2023). At hydropower facilities, passage performance and route choice likewise depend on local flow conditions and available bypass structures (Calles et al. 2021). Most directly, van Rijn et al. (2026) showed that eels already in FIII–FV stages experienced two consecutive barriers whose passage dynamics were associated with different environmental and historical predictors. Their result is important precisely because it does **not** suggest a universal Durif-stage coefficient that simply continues to dominate every downstream step.

Taken together, these findings support a sequential model in which readiness governs entry into directed movement, while post-activation progression is increasingly filtered by the opportunities and constraints encountered along the route.

### Why phase-specific analysis changes the ecological question

The general movement-ecology framework explicitly combines internal state and external factors (Nathan et al. 2008). Our contribution is not to add another factor to that framework, but to show empirically that their relative predictive importance can change across phases of one migration.

This suggests that migration studies should distinguish at least two questions whenever data permit:

1. **Activation:** what determines whether and when the migratory phenotype is expressed?
2. **Progression:** conditional on activation, what determines the rate, delay, route and probability of successful passage?

Those questions need not have the same answer. Pooling them can make a readiness variable look like a general movement driver when it acts principally at departure, or can make a barrier effect appear weak when many tracked animals were never behaviourally committed to movement.

The same logic may apply beyond eels to migratory fish, birds and mammals whenever internal preparation precedes movement through strongly heterogeneous routes. Testing that generality requires data in which internal state is measured independently of the movement outcome and the same individuals can be followed across multiple phases.

### Conservation implications: readiness and escapement are separate bottlenecks

European eel management explicitly targets silver-eel escapement. Under Council Regulation (EC) No 1100/2007, Eel Management Plans aim to permit escapement to sea of at least 40% of the silver-eel biomass relative to estimated pristine conditions.

Our results highlight why the abundance of migration-ready animals and realised escapement should not be treated as interchangeable indicators. Gate 1 concerns whether eels reach and express migratory readiness. Gate 2 concerns whether those already-moving eels can traverse regulated rivers, pumps, sluices and other barriers without prohibitive delay or mortality.

Management actions can therefore target distinct bottlenecks. Measures that improve continental growth conditions or the production of silver eels address the supply of migration-ready individuals. Measures that provide discharge windows, safe bypasses, effective sluice operation and source-to-sea connectivity address progression after migration begins. Evidence from regulated systems shows that operational changes can alter route choice and safe downstream passage, underscoring the management value of distinguishing readiness from passage opportunity.

### Limitations

Several limitations define the scope of inference.

First, the Europe-wide analyses are secondary developmental analyses of public data, not preregistered tests. Source outcomes were inspected during programme development. The phase interaction is therefore evidence for a coherent biological pattern, not untouched prospective confirmation.

Second, migration initiation is an algorithmic telemetry classification rather than a directly observed physiological decision time. We inherited the source thresholds and expert corrections to avoid outcome-driven redefinition, but the onset event still represents the first detected expression of a movement phenotype under the monitoring network.

Third, the six source projects differ in hydrology, barriers, telemetry design and endpoint observability. Project-year adjustment handles baseline differences but does not make route contexts exchangeable. The WRS comparison is consequently bridge evidence only.

Fourth, the Dutch consecutive-barrier study constrains the Gate-2 interpretation but does not reproduce the same phase-interaction analysis. At one barrier Durif was not retained in model selection; at the other it was confounded with body mass. These results are compatible with phase attenuation but are not a formal external replication.

Finally, attenuation of a general Durif effect after initiation does not imply that internal traits cease to matter. The distinction is one of **relative predictive control**, not mutually exclusive mechanisms.

### Conclusion

European eel migration is better represented as a sequence of filters than as a single movement phenotype. Capture-time silvering stage strongly predicted whether and when downstream migration was activated, but its general predictive advantage attenuated after activation for both migration speed and completion. A direct two-phase comparison confirmed that the same internal-state predictor exerted significantly stronger effects at initiation than during subsequent progression.

The most defensible synthesis is therefore not that control switches completely from the animal to the environment. Rather, **internal readiness is most informative at the gate into migration, after which route-specific ecological opportunity increasingly filters realised movement**. Separating these phases clarifies both movement ecology and conservation: producing migration-ready silver eels and enabling those eels to escape through fragmented river networks are related but distinct biological problems.

---

## Data availability

The primary Europe-wide telemetry products and analysis code are publicly available through the source study repository and associated data release reported by Verhelst et al. (2025). This study uses processed metadata and project-level migration products without modifying the source migration classifier.

The independent Dutch consecutive-barrier evidence is from van Rijn et al. (2026); its associated public data archive is reported under DOI 10.17026/LS/WTSUNG.

## Code availability

All secondary-analysis code, claim boundaries and reproducible analysis definitions for this manuscript are maintained in the zuizui0223/azores repository. Canonical analyses include migration initiation, stratified onset, conditional completion, post-initiation speed, direct phase interaction, leave-one-project-out robustness and the project-context diagnostic.

## Ethics statement

No animals were newly captured or handled for the present secondary analysis. Animal-handling and telemetry approvals belong to the original source studies and should be cited from those publications in the final submission.

## Author contributions

[To be completed.]

## Acknowledgements

[To be completed.]

## References

Calles, O., Elghagen, J., Nyqvist, D., Harbicht, A., & Nilsson, P. A. (2021). Efficient and timely downstream passage solutions for European silver eels at hydropower dams. *Ecological Engineering*, **170**, 106350. https://doi.org/10.1016/j.ecoleng.2021.106350

Council of the European Union. (2007). Council Regulation (EC) No 1100/2007 of 18 September 2007 establishing measures for the recovery of the stock of European eel. *Official Journal of the European Union*, L 248.

Durif, C., Dufour, S., & Elie, P. (2005). The silvering process of *Anguilla anguilla*: a new classification from the yellow resident to the silver migrating stage. *Journal of Fish Biology*, **66**, 1025–1043. https://doi.org/10.1111/j.0022-1112.2005.00662.x

Huisman, J. B. J., Höhne, L., Hanel, R., Kuipers, H., Schollema, P. P., & Nagelkerke, L. (2023). Factors influencing the downstream passage of European silver eels (*Anguilla anguilla*) through a tidal sluice. *Journal of Fish Biology*, **103**, 347–356. https://doi.org/10.1111/jfb.15398

Nathan, R., Getz, W. M., Revilla, E., Holyoak, M., Kadmon, R., Saltz, D., & Smouse, P. E. (2008). A movement ecology paradigm for unifying organismal movement research. *Proceedings of the National Academy of Sciences USA*, **105**, 19052–19059. https://doi.org/10.1073/pnas.0800375105

van Rijn, J., Kuipers, H. J., & Huisman, J. B. J. (2026). Seaward migration of European Eel through consecutive migration barriers: passage at a pumping station and tidal sluice. *Canadian Journal of Fisheries and Aquatic Sciences*, **83**, 1–14. https://doi.org/10.1139/cjfas-2025-0359

Verhelst, P., Righton, D., Aarestrup, K., Almeida, P. R., Bašić, T., Bolland, J. D., Carter, L., Coeck, J., Costa, J. L., Dainys, J., Davidsen, J. G., Domingos, I., Dorow, M., Feunteun, E., Frankowski, J., Griffioen, A. B., Monteiro, R. M., Moore, A., Oldoni, D., et al. (2025). The seaward migration of European eel at a continental scale: a Europe-wide biotelemetry meta-analysis. *Fish and Fisheries*, **26**, 651–668. https://doi.org/10.1111/faf.12904
