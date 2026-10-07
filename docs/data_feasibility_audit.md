# Independent-data feasibility audit

## Current decision

The Europe-wide European eel panel is executable from openly available processed data before downloading the 1.1 GB raw detection table.

Source:
- Verhelst et al. 2025, Fish and Fisheries, DOI 10.1111/faf.12904
- public analysis repository: PieterjanVerhelst/eel-meta-analysis
- raw detections: Zenodo DOI 10.5281/zenodo.15260539

## What is already openly available in the source repository

The public repository contains:

- data/interim/eel_meta_data.csv
- per-project data/interim/migration/*.csv
- per-project residency and speed tables
- data/external/eels_wrs.csv
- data/external/habitats.csv
- station-order and distance information
- the published migration-classification code.

Therefore the first gate does not require downloading the 1.1 GB raw file.

## Life-history-state audit

Public eel_meta_data.csv contains 2,684 individuals across 19 project codes.

life_stage counts:

| stage | n |
|---|---:|
| FII | 17 |
| FIII | 303 |
| FIV | 98 |
| FV | 336 |
| MII | 12 |
| coarse silver | 396 |
| NA | 1,522 |

The exact Durif-coded cohort is therefore **766**, not a clean yellow-versus-silver panel.

This distinction is important. The previous wording that the panel simply contains "yellow + silver records" was too coarse.

## Landscape-overlap audit

All 766 exact Durif-coded animals have rows in the public WRS table.

The three well-replicated female stages span multiple projects and WRS classes:

- FIII: 303 individuals across 7 projects;
- FIV: 98 across 7 projects;
- FV: 336 across 7 projects.

FII is sparse and highly context-confounded:
- n=17;
- 16 are from 2012_leopoldkanaal;
- WRS classes are almost entirely one context.

MII is also sparse (n=12).

Therefore the primary independent analysis should be **FIII/FIV/FV**, with FII and MII as explicit boundary/sensitivity groups.

## Outcome availability already inspected

The public successful_migrants_final_detection.csv was inspected during development.

Successful-tag counts among exact stages:

- FII: 0/17;
- FIII: 106/303;
- FIV: 45/98;
- FV: 116/336;
- MII: 1/12.

These are **not effect estimates**. They are unadjusted counts confounded by project, tracking geometry, season and landscape context, and were seen before protocol freeze.

Do not use the raw proportions as the headline result.

## Current GO

### GO 1 — morphology stage -> later movement

Capture-time Durif stage is independent of the later telemetry movement outcome, so the core state predictor is non-circular.

### GO 2 — stage-dependent landscape resistance

FIII/FIV/FV have sufficient representation across projects and WRS classes to test whether landscape resistance has stage-dependent effects, subject to leave-one-project-out stability.

### HOLD — within-individual yellow-to-silver transition

The current public metadata mostly contain a capture-time stage, not repeated physiological staging of the same individual.

Do not describe the Europe-wide panel as a direct repeated-measures physiological transition experiment.

The movement classifier can identify behavioural onset, but that is an outcome, not an independent state predictor.

## Next executable step

Run the lightweight stage/landscape preflight before any 1.1 GB download:

~~~bash
python analysis/03_stage_landscape_preflight.py
~~~

Only download raw detections if an analysis requires reconstruction beyond the already public migration/residency/speed tables.

## New confirmation candidate — consecutive barriers in one Dutch system

van Rijn et al. (2026) tracked 40 European eels through a pumping station and then a tidal sluice in the same source-to-sea route.

Key properties for the present programme:

- all tagged fish were classified with the Durif silvering index;
- only FIII–FV individuals were retained;
- the same individuals encountered two structurally different barriers;
- discharge and weather conditions were measured at passage opportunities;
- 35/40 passed the pumping station and 27/40 completed seaward passage through the tidal sluice;
- the underlying data are openly archived at DANS, DOI 10.17026/LS/WTSUNG.

The source paper already considered Durif stage as an individual predictor at the pumping station, where it was dropped during model selection. At the tidal sluice, Durif stage was excluded because stage and body mass could not be separated among successful individuals.

Therefore this dataset **does not provide an untouched simple stage-effect test**.

Its value is narrower and more relevant:

> can internal readiness modify how a sequence of different passage opportunities/barriers is experienced within one shared landscape?

Because n=40 and stage/weight are partly confounded, treat this as a confirmation candidate rather than a decisive test.



## 2026-10-07 DANS archive-level feasibility update

Public registry metadata for DANS DOI `10.17026/LS/WTSUNG` (dataset version 1.1) confirms that the archive contains:

- raw-filtered acoustic detections;
- receiver-station metadata;
- individual biometrics and passage outcomes;
- per-event passage-probability data with environmental covariates for **462 pumping-station events** and **282 tidal-sluice events**;
- a full variable codebook.

This closes the archive-level question of whether event-resolved barrier data exist publicly. It does **not** yet prove that the frozen matched-choice table can be reconstructed exactly: eel identifiers, opportunity-event identifiers, durations, chosen events, and biometric joins still need field-level inspection.

Therefore the remaining gate is **file retrieval and schema/join validation**, not absence of event-level public data. Do not treat the Dutch matched-choice test as estimated until `analysis/08_dutch_barrier_confirmation_gate.py` passes on the downloaded archive.
