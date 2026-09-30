# Analysis order

The EOG result is used only to generate ecological hypotheses.

## Stage 1 — observation audit

Run:

```bash
python analysis/01_receiver_state_diagnostic.py
```

This checks:

- the published zero-between-receiver-movement constraint;
- same-receiver detection gaps and persistence;
- whole-array weekly state;
- the known station 4 / `151 FLO CRUZ` failure boundary.

**Stop rule:** do not interpret EOG's residual history signal as biology until known receiver-operability problems are audited.

## Stage 2 — local memory versus shared synchrony

Fit the model ladder frozen in `hypothesis_registry.json`:

`M0 -> M0b -> M1 -> M2 -> M3 -> M4`.

Hydrological covariates must be chosen/frozen before using them to explain the detection sequence.

## Stage 3 — independent confirmation

Same-Azores mechanism analysis is exploratory. Confirmation requires an independent stream/population/period or external telemetry dataset.
