# Idea origin: ecological questions extracted from EOG

## Purpose

This repository is an independent ecological project about yellow-eel space use in an island stream system. EOG is retained only as the **hypothesis-generating origin** of the project.

The transfer rule is strict:

- migrate empirical associations and model failures that suggested ecological questions;
- do **not** migrate EOG's Layer A/Layer B product claims;
- do **not** interpret EOG predictive improvement as proof of movement mechanism;
- re-test every ecological hypothesis directly with the original ecological data.

## What EOG actually showed

The fresh Azores endpoint was receiver-week observed detection for European yellow eel (*Anguilla anguilla*) at 10 study receivers. The frozen cohort contained 36 yellow eels.

The conventional predictor already contained substantial temporal, spatial and history information, including:

- week and seasonal terms;
- receiver coordinates and active days;
- receiver-network degree at three spatial scales;
- release-anchor abundance, distance and exposure;
- previous-week detection;
- weeks since last detection;
- cumulative previous detections;
- previous-week detected-receiver count;
- neighbouring previous-source counts/exposures;
- cumulative prior global detections.

Adding the EOG world-support summary reduced held-out macro log loss from **0.1422727 to 0.1322871** and improved **5/5** held-out blocks.

This is an **association**, not a mechanism result. It says that a time-updated spatial/history state contained information about future receiver-week detection that was not fully redundant with the already-rich conventional feature set.

It does not show that a particular EOG world was true, that an eel travelled along an inferred path, or that receiver-week detection equals movement.

## Ecological signal carried forward

The key transferred observation is:

> **Future local detection retains information from the recent spatial-history state even after accounting for season, receiver location, release geometry and explicit recent/cumulative detection history.**

That residual association is the starting clue for this repository.

The ecological question is therefore not "Does EOG improve prediction?" It is:

> **What biological process makes local space use history-dependent in a highly migratory fish living in a small island-stream landscape?**

## Hypothesis family generated from that clue

### H1 — Local residence memory

Yellow eels repeatedly use local pools or stream sections, creating a persistent local state. Under this hypothesis, individual identity and recent local occupancy should explain future detections better than a memoryless spatial model.

Prediction: individual-level residence duration and return probability should be high, with strong within-individual temporal autocorrelation.

### H2 — Disturbance-reset memory

Local residence is persistent but can be reset by hydrological disturbance. After a disturbance, prior local state should temporarily lose predictive value, followed by re-localisation.

Prediction: history dependence weakens around high-flow/rainfall events and strengthens again during hydrologically stable periods.

This is a new ecological hypothesis generated from the EOG pattern; it was **not** established by EOG.

### H3 — Landscape movement compression

The species has high life-history migratory capacity, but realised yellow-stage movement may be compressed by the geometry of a short, spatially constrained island freshwater network.

Prediction: realised local movement scale should be small relative to the species' broader migratory capacity and should covary with available stream-network extent, spacing among usable pools, barriers and hydrological connectivity rather than simply body size or elapsed time.

## First causal decomposition to test

The initial analysis should decompose the apparent history signal into:

```text
individual residence / site fidelity
        +
seasonal detectability
        +
release-location legacy
        +
stream-network geometry
        +
hydrological disturbance
        ->
future detection / movement
```

The priority is to determine whether the EOG-derived residual association is primarily:

1. biological memory of local space use;
2. observation/detection memory;
3. geometry imposed by the island stream;
4. disturbance-driven state switching.

## Boundary

The EOG result is provenance for hypothesis generation only. All claims in this repository must be supported by direct ecological analysis of the Azores eel data or independent comparative data.

