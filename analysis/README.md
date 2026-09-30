# Analysis programme

## Publication target

This repository does **not** aim to publish a re-analysis of the Azores eel paper.

Azores is a seed system for the cross-system **memory–propagation regime programme**:

> predictive memory can arise from local persistence, shared forcing, observation-process memory, or actual propagation; history-based forecast gain alone does not identify which source generated it.

See [general-principle programme](../docs/general_principle_program.md).

## Phase 0 — seed-system diagnosis only

Azores is an especially useful anchor because the source paper reports **zero valid between-receiver movements among the retained yellow eels**, while EOG still found held-out value in a spatial-history representation. The immediate task is therefore to explain memory **without invoking propagation**.

### Phase 0A — published receiver-state diagnostic

Run:

```bash
python analysis/01_receiver_state_diagnostic.py
```

This checks:

- the zero-between-receiver-movement constraint;
- weekly receiver-state persistence;
- same-receiver detection gaps;
- the documented 151 FLO CRUZ failure boundary.

### Phase 0B — receiver operability audit

Run:

```bash
python analysis/02_receiver_operability_audit.py
```

This compares the published 2022-07-24 station-4 failure against the exact deployment-derived effort rule used by EOG.

Decision:

- if deployment metadata still marks station 151 eligible after failure, treat those late zeros as potentially contaminated by observation-system failure;
- if no post-failure EOG-eligible weeks exist, this specific artifact is ruled out.

### Phase 0C — individual persistence and locality screen

Run:

```bash
python analysis/run_residency_screen.py
```

This tests whether detection memory is stronger:

- within an individual through time;
- among co-resident eels sharing a receiver;
- than among eels occupying different receivers.

Current exploratory screen shows strong individual weekly persistence and stronger same-receiver than different-receiver covariance. That local covariance still does not distinguish shared pool ecology from shared receiver detectability.

## Phase 0 decision target

The seed-system question is:

> **Is Azores predictive memory primarily local biological state, shared observation state, or an external/common temporal driver?**

Only after observation-operability effects are cleared should hydrology or other external forcing be introduced.

These results are **not the paper endpoint**. Their purpose is to estimate which corner of the general regime map Azores occupies and derive plausible process timescales.

## Phase 1 — known-truth regime benchmark

Before broad empirical synthesis, construct simulated systems with known truth spanning:

- persistence without propagation;
- shared forcing without propagation;
- observation-memory / imperfect-detection artifacts;
- genuine directional propagation;
- mixed regimes.

Vary observation interval relative to process timescales and test whether the proposed scale ratios recover the correct memory source.

## Phase 2 — independent cross-system panel

Add independent systems spanning the same regimes. For every system estimate the same quantities:

1. gain from lagged history beyond current environment;
2. same-site persistence contribution;
3. shared-forcing contribution;
4. observation-process contribution;
5. residual directional propagation contribution;
6. sensitivity of all contributions to temporal re-binning.

## Phase 3 — comparative principle

Test whether systems cluster by the proposed scale ratios better than by taxon or ecosystem label.

Azores is one anchor point, not the evidence base.
