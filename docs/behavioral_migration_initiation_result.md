# Superseded developmental analysis

This file is retained as a provenance pointer only.

The earlier workflow in `analysis/09_behavioral_migration_initiation.py` used the raw `migration=TRUE` state without inheriting the source project's nine fixed 2015 expert non-migrant corrections and treated the first broad migration row as the onset clock.

That is **not** the canonical Azores analysis.

Use instead:

- `analysis/09_durif_migration_initiation.py` — expert-corrected binary activation;
- `analysis/10_migration_onset_cox.py` — threshold-defined behavioral onset;
- `analysis/12_post_initiation_speed.py` — post-activation progression speed;
- `results/phase_control_canonical_v2.json` — current numeric/interpretation source;
- `manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V3.md` — current manuscript.

Canonical activation result:

- FIII: 154/261 = 59.0%
- FIV: 53/68 = 77.9%
- FV: 215/246 = 87.4%
- adjusted OR/stage: 2.08, 95% CI 1.56–2.76.

Do not cite the older 161/54/216 counts or the first-`migration=TRUE` arrival latency as the current biological result.
