# Analysis programme

## Publication target

This repository does **not** aim to publish a re-analysis of the Flores eel paper.

The primary ecological programme is **state-dependent mobility gating**:

> internal migratory readiness may change how strongly landscape resistance constrains realised movement.

See [general-principle programme](../docs/general_principle_program.md) and [independent test protocol](../docs/independent_test_protocol.md).

## Phase 0 — Flores seed diagnosis only

~~~bash
python analysis/01_receiver_state_diagnostic.py
~~~

Flores is the extreme resident anchor. It is not the evidence base for the general claim.

## Phase 1 — lightweight independent preflight

Do **not** download 1.1 GB first.

Run:

~~~bash
python analysis/03_stage_landscape_preflight.py
~~~

This audits the public processed Europe-wide eel products and tests whether exact capture-time Durif stages have enough cross-project/WRS overlap.

Current design target:

~~~text
FIII / FIV / FV × landscape resistance
~~~

FII and MII remain boundary groups.

## Phase 2 — standardized individual table

~~~bash
python analysis/04_build_stage_landscape_table.py
~~~

This creates:

~~~text
analysis/derived/eel_stage_landscape.csv
~~~

from public upstream metadata, WRS data and the published successful-migrant endpoint.

**Boundary:** aggregate outcome counts were already inspected during development. This panel is developmental independent evidence, not outcome-blind confirmation.

## Phase 3 — model

Primary ecological test:

~~~text
later movement ~ capture Durif stage
               + landscape resistance
               + stage × landscape resistance
               + project/design covariates
~~~

Project-level leave-one-project-out stability is mandatory.

Only reconstruct the 1.1 GB raw detections if onset/progression metrics unavailable in the public processed migration/speed products require it.

## Phase 4 — replication

Use Wolastoq or another independently accessible eel system to test whether state-dependent landscape resistance transfers across water bodies/species.
