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
