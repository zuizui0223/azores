# From the EOG result to ecological tests

## Status

This document converts the already-observed EOG result into **post-hoc ecological hypotheses** and explicit next tests.

The EOG result is not a mechanism test. Analyses using the same Azores telemetry are exploratory mechanism diagnosis. Independent confirmation requires a new population, stream, time series, or external telemetry dataset.

## 1. What the EOG result actually says

The frozen Azores endpoint was receiver-week observed detection.

The conventional arm already included season, receiver coordinates, receiver active days, network degree at three frozen scales, release-anchor abundance/distance/exposure, previous-week detection, time since last detection, cumulative previous detections, previous-week detected-receiver count, neighbouring previous-source counts/exposures, and cumulative global detections.

Adding the unchanged EOG world-support summary improved held-out macro log loss from **0.1422727 to 0.1322871** (about **7.0%**), with the augmented arm better in **5/5** held-out blocks.

Therefore the defensible empirical statement is:

> A sequentially updated spatial-history state contained held-out information about future receiver-week detection that was not fully redundant with the already-rich conventional predictor.

It is not evidence that any frozen EOG world was the true movement process.

## 2. The crucial ecological constraint: no observed between-receiver movement

The source study tracked 36 yellow-stage European eels for one year. After the published false-positive exclusions, **none of the eels was detected at more than one receiver, and detections were always at the receiver nearest the release location**.

The published study therefore already establishes extremely restricted movement and high local site fidelity. The EOG endpoint itself explicitly forbade between-receiver movement as the target because that outcome was already known.

This changes the interpretation of the EOG gain:

> **The additional information cannot be read as evidence of receiver-to-receiver dispersal. It must arise from temporal structure in which fixed local pools/tags are detectable, active, or jointly changing state.**

The new ecological question is consequently not "why do eels move among pools?" but:

> **Why does detectability/activity within strongly resident pools have memory and system-level temporal structure?**

## 3. First explanation to test: observation-state memory

### H-A1 — persistent residence + time-varying observation

An eel may remain in the same pool throughout the study while its probability of being detected changes because of microhabitat use, activity, acoustic propagation, receiver performance, or temporary detection gaps.

This can generate long temporal runs of presence/absence at a fixed receiver without any movement among receivers.

**Predictions**

- tag-level detections repeatedly disappear and return at the same receiver;
- an explicit latent-residence + detection model produces high residence persistence but time-varying observation probability;
- after receiver/tag observation heterogeneity is represented, much of the EOG-derived residual history signal shrinks.

## 4. A known receiver-failure test comes before biological interpretation

The source paper reports that **station 4 (ETN station `151 FLO CRUZ`) ceased producing detections after 24 July 2022 because of sediment burial that prevented data retrieval**.

This matters because the EOG conventional baseline used deployment-derived active-day effort. If the deployment record continued to classify station 4 as active after burial, late receiver-week zeros can be observation failures rather than ecological non-detections.

### H-A0 — receiver-failure artifact

**Prediction A0.1:** censoring station 4 after 2022-07-24 changes the apparent temporal-memory signal.

**Prediction A0.2:** if a large share of the residual gain disappears after this correction, the EOG gain was partly an observation-system diagnostic rather than an eel-behaviour signal.

### Mandatory order

This test is first. Do **not** interpret temporal memory biologically until the station-4 boundary and all comparable receiver-operability issues are audited.

## 5. Biological explanation after receiver audit: hydrological synchrony

The study stream is rain-fed and can experience strong flash-flood events. Eels do not need to move among receivers for hydrology to change detection/activity simultaneously across pools.

### H-A2 — shared hydrological state

Rainfall/flow may alter:

- eel activity within a pool;
- refuge use and distance from the receiver;
- acoustic propagation;
- local water depth/turbulence;
- the probability that several receivers detect their resident eels during the same week.

This produces a network-level temporal state without dispersal.

**Predictions**

- receiver-week detections covary across spatially separated pools after same-receiver history is controlled;
- shared covariance is concentrated around hydrological events;
- adding frozen rainfall/flow covariates reduces the residual cross-pool state signal;
- same-pool persistence remains high because no between-receiver movement is required.

## 6. Residual local-state memory

### H-A3 — stable local activity regimes

Even after receiver operation and hydrology are controlled, individual pools may occupy persistent high-activity/high-detectability or low-activity/low-detectability regimes because of local refugia, depth, food, density, competition, or microhabitat.

**Predictions**

- receiver/tag random effects and latent temporal states remain strong after hydrology;
- local state persistence exceeds what season and shared weather alone generate;
- neighbouring-pool state adds little once shared hydrology is included.

This is potentially the genuinely new ecological signal left by EOG.

## 7. Model ladder

Primary unit: tag × week where possible.  
Secondary unit: receiver × week for direct comparability with EOG.

### M0 — published-style temporal/effort baseline

- week/season;
- receiver identity/position;
- recorded active effort.

### M0b — audited observation baseline

M0 plus:

- known receiver-operability boundaries;
- station 4 censored after 2022-07-24;
- any other documented receiver failure.

**Primary first contrast:** M0b vs M0.

### M1 — local observation memory

M0b plus:

- same-tag previous detection;
- time since last detection;
- cumulative tag/local detections;
- receiver/tag random effects or latent observation state.

### M2 — shared temporal state

M1 plus:

- common week effect;
- cross-pool synchrony summary.

### M3 — hydrology

M2 plus frozen hydrological covariates and, if supported, local-memory × hydrology interactions.

### M4 — latent residence + observation

A state-space model in which residence remains fixed/highly persistent and acoustic detection is explicitly time varying.

## 8. Decision logic

### If M0b removes most of the signal

Interpretation:

> a known receiver-operability problem contributed substantially to the EOG gain.

This is an observation-system result, not eel ecology.

### If M1 explains the remaining signal

Interpretation:

> EOG mostly captured persistent within-pool activity/detection memory in resident eels.

### If M2 is important but M3 removes it

Interpretation:

> apparent network information is largely shared hydrological forcing across resident pools.

### If M3 still leaves strong local state persistence

Interpretation:

> pools or individuals have persistent local activity regimes not explained by season, receiver operation, or measured hydrology.

That becomes the main ecological mechanism target.

## 9. What is not the immediate target

The attractive broader idea that small island-stream geometry **compresses realised yellow-eel movement** remains useful, but it cannot explain the EOG residual within this dataset because no valid between-receiver movement was observed.

Treat movement compression as a later comparative project requiring independent telemetry systems spanning streams, rivers, lakes, or estuaries.

## 10. Independence and claim rules

- Same-Azores mechanism analysis is exploratory because the response was already opened in EOG.
- Receiver-week non-detection is not biological absence.
- Do not infer movement from a support-state predictor when the observed animals did not switch receivers.
- Known receiver failures must be handled before biological interpretation.
- Independent confirmation requires a new stream/population/period or external telemetry dataset.

## 11. Scientific question carried forward

> **In a strongly resident island-stream eel population, is temporal predictability primarily an observation-system phenomenon, shared hydrological synchrony, or persistent local activity state?**

This is the primary ecological target of the Azores repository.
