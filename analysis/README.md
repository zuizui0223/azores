# Analysis programme

## Publication target

This repository does **not** aim to publish a re-analysis of the Flores eel paper.

The primary ecological programme is **state-dependent mobility gating**:

> internal life-history state determines motivation to move, while landscape opportunity determines how fully that mobility is expressed.

See [general-principle programme](../docs/general_principle_program.md).

## Phase 0 — Flores seed diagnosis only

```bash
python analysis/01_receiver_state_diagnostic.py
```

Flores is the extreme resident anchor. It is not the evidence base for the general claim.

## Phase 1 — independent Europe-wide panel

Audit the public Zenodo record:

```bash
python analysis/02_fetch_public_comparative_data.py
```

Download only when ready for the ~1.1 GB file:

```bash
python analysis/02_fetch_public_comparative_data.py --download
```

Then gate the raw detection schema:

```bash
python analysis/03_stage_transition_gate.py \
  --detections data/external/silver_eel_meta/raw_detection_data.csv
```

**Hard rule:** detection tracks alone do not establish a yellow-to-silver state transition. The published migration-state classifier/software must be integrated before pre/post mobility-release inference.

## Phase 2 — mobility-release analysis

Primary test:

```text
movement ~ migratory_state
         * landscape_opportunity
         + refuge/context covariates
         + tracking design
         + study/system effects
```

The new biological content is the interaction. A state effect alone is not enough.

## Phase 3 — replication

Use Wolastoq and other independent eel systems to test whether stage × landscape effects transfer across species and water-body types.
