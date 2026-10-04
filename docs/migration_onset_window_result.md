# Developmental result: Durif stage predicts migration initiation across fixed windows

## Why this analysis

The earlier Europe-wide result used the published successful-migrant endpoint.

That endpoint mixes at least two ecological processes:

1. whether an eel begins directed migration;
2. whether it later progresses successfully through the monitored landscape.

To isolate the first process, the public per-project migration tables were reconstructed for all primary-stage projects with available migration files.

## Data reconstruction

Primary stages:

- FIII
- FIV
- FV

Projects:

- 2011 Warnow
- 2012 Leopoldkanaal
- 2013 Albertkanaal
- 2015 phd_verhelst_eel
- 2019 Grotenete
- ESGL

The large Leopoldkanaal, Albertkanaal and 2015 files were retrieved through Git blob access because the GitHub contents API truncates/omits large file bodies.

The upstream source's nine active expert exclusions for the 2015 project were respected.

After those exclusions, **566** FIII/FIV/FV tags were represented in the migration tables.

## Raw initiation pattern

Across represented tags:

| Stage | n | Ever initiated migration | Rate |
|---|---:|---:|---:|
| FIII | 254 | 154 | 60.6% |
| FIV | 67 | 53 | 79.1% |
| FV | 245 | 215 | 87.8% |

Among initiators, raw median release-to-onset latency was:

- FIII: **4.95 d**
- FIV: **0.27 d**
- FV: **0.69 d**

These raw latencies are descriptive only because release timing and follow-up vary strongly among projects and stages.

## Fixed-window sensitivity

To reduce dependence on unequal total follow-up, initiation was redefined at fixed post-release windows.

A non-initiator was eligible only if its observed tracking record extended at least to the end of the tested window. An initiator remained eligible if the migration event occurred inside the window.

Each model included:

- project × release-year fixed effects;
- body length centered within project-year, per 100 mm;
- release timing centered within project-year, per 100 d;
- ordinal Durif score FIII=0, FIV=1, FV=2.

### Results

| Window | Stage OR per increment | 95% CI | p |
|---|---:|---:|---:|
| 7 d | **1.51** | 1.16–1.97 | 0.0025 |
| 30 d | **1.50** | 1.14–1.99 | 0.0043 |
| 60 d | **1.70** | 1.28–2.24 | 0.00021 |
| 90 d | **1.89** | 1.39–2.57 | 0.000050 |

The direction is therefore stable from the first week through three months.

## Biological interpretation

The developmental result now separates two statements.

### Supported developmental statement 1

> **More advanced capture-time Durif stage is associated with a higher probability of initiating directed migration.**

This association is already visible in the first 7–30 days after release and persists at longer windows.

### Supported developmental statement 2

> **Internal migratory readiness is not only associated with eventual successful migration; it is associated with the release of movement itself.**

This makes the biological interpretation substantially stronger than a final-escapement-only result.

## What remains unresolved

The data still do not establish **why the strength of the stage effect differs among systems**.

Possible modifiers include:

- hydrological opportunity;
- barriers;
- tidal versus regulated passage;
- release context;
- tracking geometry.

That is the motivation for the Dutch consecutive-barrier confirmation study.

## Evidence boundary

This is still developmental evidence.

The fixed windows were compared after the broad stage hypothesis had already been motivated and outcome data had been inspected. Therefore:

- do not promote one window as a preregistered primary endpoint;
- report the full window series;
- use an independent system for confirmation of state-dependent landscape gating.
