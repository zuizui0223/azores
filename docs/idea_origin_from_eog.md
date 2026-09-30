# Idea origin: ecological questions extracted from EOG

## Purpose

This repository is an independent ecological project about yellow-eel temporal state and detectability in an island-stream system. EOG is retained only as the **hypothesis-generating origin**.

The transfer rule is strict:

- migrate empirical associations and model failures that suggested ecological questions;
- do **not** migrate EOG's Layer A/Layer B product claims;
- do **not** interpret EOG predictive improvement as proof of movement mechanism;
- re-test every ecological hypothesis directly with ecological and observation-process data.

## What EOG actually showed

The fresh Azores endpoint was receiver-week observed detection for European yellow eel (*Anguilla anguilla*) at 10 study receivers.

The conventional predictor already contained season, receiver geometry/effort, release geometry, previous-week detection, time since last detection, cumulative local detections, neighbouring previous-source summaries, and cumulative global detections.

Adding the frozen EOG world-support summary reduced held-out macro log loss from **0.1422727 to 0.1322871** and improved **5/5** held-out blocks.

That is an association only:

> a time-updated system state contained information about future receiver-week detection that was not fully redundant with local history, season and geometry.

## The decisive constraint from the source ecology

The source paper reports that, after false-positive exclusions, **none of the 36 tagged yellow eels was detected at more than one receiver; detections were always at the receiver nearest the release location**.

Therefore the EOG gain cannot be used as evidence that eels moved among receivers.

The correct ecological translation is:

> **why do fixed local pools show persistent and coordinated temporal detection/activity states?**

## Primary hypothesis sequence

### A0 — receiver-operability artifact

The source paper reports that station 4 (`151 FLO CRUZ`) ceased detections after 24 July 2022 because of sediment burial.

First test whether correcting documented receiver operability reduces the apparent temporal-memory signal.

### A1 — persistent residence with time-varying detection/activity

Resident eels may remain in the same pool while acoustic detectability varies through behaviour, microhabitat, receiver conditions, or temporary observation gaps.

Prediction: repeated disappearances/reappearances occur at the same receiver and can be explained by a high-persistence latent residence state plus time-varying detection.

### A2 — shared hydrological synchrony

Rainfall/flow may simultaneously alter eel activity and acoustic detectability across multiple pools without any dispersal.

Prediction: cross-pool temporal covariance weakens after hydrological covariates are added.

### A3 — persistent local activity regimes

If receiver operation and shared hydrology do not remove the signal, pools or individuals may occupy persistent local high/low activity regimes driven by microhabitat, refugia, food, density or competition.

Prediction: strong receiver/tag latent-state persistence remains after observation and hydrological controls.

## What remains later

The broader idea that island-stream geometry compresses realised yellow-eel movement is biologically interesting, but the current Azores dataset cannot identify that comparative relationship by itself.

That hypothesis requires independent telemetry systems across streams, larger rivers, lakes or estuaries and is explicitly a **later comparative project**, not the immediate explanation of the EOG result.

## Current test specification

Canonical documents:

- [EOG result to ecological tests](eog_result_to_ecological_tests.md)
- [analysis order](../analysis/README.md)
- [hypothesis registry](../analysis/hypothesis_registry.json)

## Boundary

The Azores response was already opened in EOG. Same-data mechanism analyses are exploratory diagnosis. Independent confirmation requires a new stream, population, period, or external telemetry dataset.
