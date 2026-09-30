# Analysis programme

## Publication target

This repository does **not** aim to publish a re-analysis of the Azores eel paper.

Azores is a seed system for the cross-system **memory–propagation regime programme**:

> predictive memory can arise from local persistence, shared forcing, observation-process memory, or actual propagation; history-based forecast gain alone does not identify which source generated it.

See [general-principle programme](../docs/general_principle_program.md).

## Phase 0 — seed-system diagnosis only

Run:

```bash
python analysis/01_receiver_state_diagnostic.py
```

This checks the published zero-between-receiver-movement constraint, same-receiver detection gaps, whole-array weekly state, and the documented station-4 failure boundary.

These results are **not the paper endpoint**. Their purpose is to estimate which corner of the general regime map Azores occupies and to derive plausible process timescales.

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
