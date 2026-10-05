#!/usr/bin/env python3
"""DEPRECATED analysis retained in git history.

The former project-fixed final-success workflow used all FIII/FIV/FV metadata individuals as the
denominator for the final successful-migrant endpoint. That denominator was too
broad for the biological question.

Canonical pipeline:
  python analysis/09_durif_migration_initiation.py
  python analysis/10_two_stage_mobility.py
  python analysis/11_phase_stage_interaction.py
  python analysis/13_phase_interaction_lopo.py

Numeric source of truth:
  results/phase_control_canonical_v1.json
"""
raise SystemExit(
    "Deprecated denominator. Run the canonical two-phase migration pipeline; "
    "see analysis/README.md and results/phase_control_canonical_v1.json."
)
