# Silvering readiness predicts migration activation but not generic post-activation speed in European eel

**Manuscript draft V3 — corrected after terminal-endpoint audit**

**Authors:** [to be completed]

**Affiliations:** [to be completed]

## Abstract

Animal migration requires both readiness to leave and opportunity to progress, yet these components are often compressed into one movement phenotype. We tested whether capture-time migratory readiness predicts different parts of seaward migration in European eel (*Anguilla anguilla*). We analysed public telemetry products from six European projects in which female Durif stages FIII–FV were available together with a common movement-based migration classification. The primary cohort contained 575 evaluable stage-coded individuals after retaining the source processing and expert corrections.

Migration activation increased from 59.0% in FIII to 77.9% in FIV and 87.4% in FV eels. With project × release-year effects and adjustment for body length and release timing, the odds of activating migration increased 2.08-fold per Durif-stage increment (95% CI 1.56–2.76). A stratified Cox analysis likewise showed earlier behavioral onset at more advanced stages (hazard ratio 1.29, 95% CI 1.13–1.47). In contrast, among activated eels, the source-defined migration-speed response showed no general Durif gradient (multiplicative ratio 0.983 per stage, 95% CI 0.852–1.134; p = 0.815).

The source study also provides a set of eels positively observed at project-specific terminal/sea endpoints. Because the source meta-analysis explicitly did not estimate escapement success rate, we treat terminal-set membership and its initiation-versus-terminal stage contrast as sensitivity analyses only; non-membership is not interpreted as biological failure.

The source Europe-wide study reported substantial water-body-specific variation in migration speed and effects of tidal and water-regulating-structure context. An independent Dutch study of 40 FIII–FV eels crossing a pumping station and tidal sluice further shows that post-activation progression can depend on barrier-specific passage opportunities and route history.

Our results support a phase-resolved view of eel migration: silvering readiness strongly predicts whether and when directed movement becomes behaviorally expressed, whereas the same morphological readiness gradient does not translate into a generic speed advantage once migration is active. This separates the production of migration-ready eels from the route conditions governing subsequent progression without requiring unobserved terminal outcomes to be labelled as failures.

**Keywords:** *Anguilla anguilla*; animal movement; migration; silvering; Durif stage; telemetry; barrier passage; internal state; movement ecology

## Introduction

Animal movement emerges from a dynamic interaction between internal motivation, the capacity to move and navigate, and the external environment through which movement is realised (Nathan et al. 2008). For migration, that interaction unfolds sequentially. An animal must first enter a migratory state, then move through a route whose hydrology, barriers, habitat geometry and temporal windows of opportunity can permit, delay or prevent further progress. Nevertheless, migration is often analysed using a single endpoint such as departure, speed, arrival or final success. Pooling these phases can obscure whether the same biological variables control the decision to begin moving and the fate of movement after it has begun.

European eel (*Anguilla anguilla*) offers an unusually informative system in which to separate these phases. The continental growth phase ends with silvering, a coordinated suite of morphological and physiological changes associated with preparation for the oceanic spawning migration. Durif et al. (2005) classified females into growth, pre-migrant and migrating stages; FIII represents a pre-migrant state, whereas FIV and FV represent progressively silvered migrating states. Because this stage is measured from the animal rather than inferred from its later telemetry path, it provides an internal-state axis that can be compared with subsequent realised movement.

At the same time, downstream migration takes place through strongly heterogeneous landscapes. Eels may move through free-flowing river reaches, canals, navigation structures, pumps, weirs, hydropower facilities and tidal sluices. Flow, rainfall, darkness and lunar conditions can alter migration timing, while water-regulating structures can impose substantial delay or restrict passage (Verhelst et al. 2025; Huisman et al. 2023; van Rijn et al. 2026). The Europe-wide biotelemetry synthesis of Verhelst et al. (2025), which combined 2,306 tagged eels from 18 water bodies, showed both broad geographic pattern and substantial within-system plasticity in seaward migration. It also developed a common movement-based classifier to harmonise migration identification across heterogeneous telemetry projects.

These features allow a more specific question than whether internal state and external environment both matter. We ask **which part of realised migration is most strongly associated with internal migratory readiness**. If silvering primarily regulates readiness to depart, then FIII→FIV→FV should strongly predict whether and when directed downstream migration begins. If subsequent progression is increasingly shaped by route-specific opportunity, the same Durif-stage gradient need not persist in post-initiation migration speed.

We therefore analysed migration activation, time to threshold-defined behavioral onset and post-initiation migration speed using the same capture-time Durif axis. We retained the source study's project-specific terminal positive set only as a sensitivity endpoint because its complement cannot be assumed to represent biological failure. We complemented the primary analyses with route-context diagnostics and an independent published Dutch consecutive-barrier study.

We predicted that (1) advanced Durif stage would increase the probability and rate of migration activation, and (2) no comparable general Durif gradient would remain in migration speed after activation. This phase-resolved prediction distinguishes activation from progression without relying on a binary escapement-rate estimate.

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

### Terminal-endpoint phase contrast — sensitivity only

For audit continuity, we retained the previously developed stacked initiation-versus-terminal-membership model with individual-clustered uncertainty.

Because the second binary response is observability dependent, this contrast is not used as the principal test of phase-specific control in V3.

Its role is limited to asking whether the direction of the stage association differs when the same positive terminal-set definition is used across projects. It must not be interpreted as a direct comparison of biological initiation probability with biological failure probability.

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

The time-to-event analysis contained 570 individuals and 418 migration-onset events. Each FIII→FIV→FV increment increased the instantaneous migration-onset rate by 28% (HR 1.29, 95% CI 1.13–1.47; p = 0.00016).

The stage HR remained above one in every leave-one-project-out analysis, ranging from 1.09 to 1.52. Omitting the 2015 project produced the weakest and least precise estimate, with the 95% interval crossing one. Thus, the average onset association was positive but not fully project-independent in precision.

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

### An independent consecutive-barrier system showed barrier-specific post-activation control

In the independent Dutch study, 35 of 40 tagged FIII–FV eels passed a pumping station and 27 completed seaward passage through a subsequent tidal sluice, accumulating approximately 34 days of mean barrier delay (van Rijn et al. 2026).

Published analyses identified barrier-specific predictors rather than a common monotonic Durif-stage effect. Pump passage was associated with discharge opportunity and wind, whereas tidal-sluice passage was associated with lunar illumination; previous pumping-station passage experience also predicted faster subsequent sluice passage. Durif stage was dropped from the pumping-station individual model and was non-identifiable from body mass in the tidal-sluice analysis.

These results do not replicate our phase interaction statistically, but they independently constrain its interpretation: once migration is active, progression through a real route can be strongly shaped by barrier-specific opportunity and prior route experience.

---

## Discussion

### Migration is a sequence of ecological filters

Our central result is not simply that silvering predicts eel migration. That relationship is expected from the biological meaning of the Durif framework.

The informative pattern is phase resolved. Advanced FIII→FIV→FV stage strongly predicted whether classified downstream migration began and was associated with earlier onset. Once migration had begun, however, the same stage gradient was absent from the source-defined migration-speed response.

This distinction matters because a final endpoint can compress several processes into one number: readiness to leave, movement activation, hydrological opportunity, barrier passage, delay, route choice and terminal observability. Analysing activation and progression separately exposes where a measured internal-state variable actually carries information.

The terminal positive-set sensitivity analysis points in the same qualitative direction, but it is not required for the main inference because non-membership is not a validated failure state.

### Silvering readiness primarily predicts entry into movement

Durif stages were developed to distinguish resident, pre-migrant and migrating eel phenotypes (Durif et al. 2005). Our activation result therefore should not be presented as the discovery that silver eels migrate.

Instead, the multi-project analysis establishes a robust benchmark: capture-time Durif stage predicts later behavioral migration activation even after project-year, body-length and release-timing adjustment. The time-to-onset analysis provides an independent temporal expression of the same readiness gradient.

That benchmark is useful because the same stage variable then shows little generic association with migration speed among activated eels. The contrast is therefore not created by changing the biological readiness measure; it arises because the response phase changes.

This is consistent with movement-ecology theory in which internal state contributes to movement motivation, while leaving open which external and individual factors govern progression after movement is active.

### Internal readiness predicts activation but not generic progression speed

The post-initiation speed result differed sharply from the activation result. Durif stage strongly predicted whether and when migration became active, but showed no general gradient in the source-defined **whole-migration** speed response after activation (ratio 0.983 per stage, 95% CI 0.852–1.134).

A developmental project-level audit did not indicate that this pooled near-null was merely produced by strong opposing water-body effects. Project-specific stage-speed ratios ranged from 0.915 to 1.272, but Cochran's Q was 2.47 with 5 df (p = 0.78). The broad-scale result is therefore compatible with a weak transferable Durif gradient in whole-route speed across these six systems.

That broad-scale result does **not** imply that internal readiness ceases to matter once movement starts. Moyo et al. (2026) followed silver eels in the River Test after downstream movement had already begun and modelled progression at the river-reach scale. Silvering stage was retained together with temperature, barrier, flow and lunar variables; removing silvering stage worsened model fit. Thus a readiness signal can be detectable for finer-grained progression even when it is weak in a pooled whole-migration metric.

We therefore interpret the evidence as **scale- and context-sensitive persistence of internal-state information**: Durif readiness is strongly and transferably associated with activation, while its post-activation contribution is weak at the whole-route scale used here but can reappear at finer spatial or temporal scales.

This does not demonstrate that external conditions causally replace internal state. Individual traits can still influence movement after departure, and external conditions can also influence activation. The result instead identifies where the transferable Durif signal is strongest and motivates a sharper progression question: at what spatial and temporal scale does internal readiness remain visible, and when is it masked by route opportunity and environmental forcing?

Verhelst et al. (2025) independently reported substantial variation in migration phenology and speed among water bodies, with tidal context and water-regulating structures contributing to that heterogeneity. The independent Dutch consecutive-barrier study provides a direct route for testing barrier-specific opportunity variables within one shared landscape, while the River Test result shows that fine-scale progression need not be independent of silvering state.

### Route opportunity is the next target after activation

The current Europe-wide reanalysis does not itself identify the external variable that controls post-activation progression.

What it shows is a scale-dependent gap: Durif stage strongly predicts activation, but does not provide a general whole-route speed gradient across the six-project analysis. The source meta-analysis independently found that migration speed varies with tidal context, water-regulating structures and water-body-specific hydrology, while Moyo et al. (2026) shows that silvering stage can still contribute to reach-level progression within one river.

Independent barrier studies provide more direct ecological candidates. Passage through tidal sluices can depend on discharge dynamics, and individual eels can experience substantial delay after reaching migration obstacles. At hydropower and pumping structures, route choice and passage performance vary with local flow and operational conditions.

Most directly, van Rijn et al. (2026) followed FIII–FV eels through a pumping station and a subsequent tidal sluice. Barrier-specific passage was associated with different opportunity and history variables, and no single monotonic Durif-stage coefficient dominated both structures.

Together, these findings motivate the next test rather than closing it:

> **once migration is active, at what spatial and temporal scales does internal readiness still contribute to progression, and when do route-specific hydrological and barrier opportunities dominate the observed movement rate?**

The project-level WRS-versus-terminal-membership correlation is retained only as sensitivity/context because the terminal response is observability dependent and the six projects are not exchangeable.

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

First, these are secondary developmental analyses of public data, not preregistered tests. Source outcomes were inspected during programme development.

Second, migration activation is an algorithmic telemetry classification rather than a directly observed physiological decision time. We inherited the source thresholds and expert corrections to avoid outcome-driven redefinition.

Third, the source projects differ in hydrology, barriers, telemetry design and monitoring extent. Project-year adjustment controls baseline differences but does not make route contexts exchangeable.

Fourth, the terminal positive set is not a validated binary escapement-success variable. The source meta-analysis explicitly avoided estimating escapement success rate because non-observation can reflect fishing, detection loss, release geometry and other study-specific processes. Terminal-set analyses and the former stacked phase OR-ratio are therefore sensitivity results only.

Fifth, a weak general Durif effect on post-activation whole-migration speed does not prove that internal traits cease to matter. A project-level heterogeneity audit found no evidence that the pooled near-null was simple cancellation among the six source systems, but that audit remains developmental and several project-specific stage contrasts are imprecise. The River Test study further shows that silvering stage can contribute to finer-scale post-activation progression.

Finally, the Dutch consecutive-barrier and River Test studies constrain the interpretation but are not formal replications of the Europe-wide model. Their main value is to identify the spatial and temporal scales, and the route-opportunity variables, at which a stronger within-landscape confirmation should be conducted.

### Conclusion

Capture-time silvering stage strongly predicted whether and when European eels entered classified downstream migration, but the same Durif gradient did not predict **whole-migration** speed after activation across the six-project analysis.

The most defensible synthesis is therefore phase- and scale-specific:

> **internal migratory readiness is highly informative at the gate into migration; after activation, its detectable contribution depends on the scale at which progression is measured and on the route and environmental context through which movement is realised.**

This conclusion does not depend on treating every eel absent from a terminal receiver set as a biological failure.

Separating activation from progression sharpens both movement ecology and conservation: producing migration-ready silver eels and providing physical opportunities for those eels to progress through fragmented river networks are related, but empirically distinct, problems.

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

Moyo, S., Britton, J. R., Major, T., Wright, R. M., Moore, A., Ives, M., Davies, P., Hall, A. E., Stamp, T., Sheehan, E. V., & Bašić, T. (2026). Initial marine movements of silver European eels *Anguilla anguilla* following their emigration from an English chalk stream. *Hydrobiologia*. https://doi.org/10.1007/s10750-026-06406-6

van Rijn, J., Kuipers, H. J., & Huisman, J. B. J. (2026). Seaward migration of European Eel through consecutive migration barriers: passage at a pumping station and tidal sluice. *Canadian Journal of Fisheries and Aquatic Sciences*, **83**, 1–14. https://doi.org/10.1139/cjfas-2025-0359

Verhelst, P., Righton, D., Aarestrup, K., Almeida, P. R., Bašić, T., Bolland, J. D., Carter, L., Coeck, J., Costa, J. L., Dainys, J., Davidsen, J. G., Domingos, I., Dorow, M., Feunteun, E., Frankowski, J., Griffioen, A. B., Monteiro, R. M., Moore, A., Oldoni, D., et al. (2025). The seaward migration of European eel at a continental scale: a Europe-wide biotelemetry meta-analysis. *Fish and Fisheries*, **26**, 651–668. https://doi.org/10.1111/faf.12904
