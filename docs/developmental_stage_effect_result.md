# Superseded developmental analysis

This file is retained only for provenance.

The earlier analysis treated all FIII/FIV/FV metadata records as the denominator for the published successful-migrant endpoint. Source-code audit showed that the source workflow separates two sequential processes:

1. migration activation among evaluable processed tracks;
2. sea escapement among animals that activated migration.

The current canonical result is therefore the two-phase analysis:

- activation: OR **2.08** per Durif-stage increment, 95% CI **1.56–2.76**;
- completion after activation: OR **1.15**, 95% CI **0.83–1.59**;
- direct initiation/completion OR ratio: **1.81**, 95% CI **1.15–2.84**, p = **0.0099**.

Use:
- `results/phase_control_canonical_v1.json`
- `docs/phase_stage_interaction_result.md`
- `analysis/09_durif_migration_initiation.py`
- `analysis/11_phase_stage_interaction.py`

Do not cite the former metadata-denominator odds ratios as current evidence.
