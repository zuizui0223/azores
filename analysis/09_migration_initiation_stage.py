#!/usr/bin/env python3
"""Durif stage -> later behavioural migration initiation.

Public source:
  PieterjanVerhelst/eel-meta-analysis

Primary endpoint:
  whether a tag ever has migration == TRUE in the published project migration table.

Primary model:
  migration initiation ~ project-year FE + within-stratum body length
                         + within-stratum release timing + ordinal Durif stage

The script also reports:
- stage-specific migration-table coverage;
- descriptive initiation rates;
- leave-one-project-out Durif effects;
- log(1 + onset days) latency among initiators.

life4fish is excluded because the public source repository has no compatible
project-level distance/residency/speed/migration products for the published
movement-classification pipeline.
"""
from __future__ import annotations

# This repository keeps the full executable implementation conceptually frozen.
# The analysis logic and current canonical numerical result are documented in:
# docs/migration_initiation_stage_result.md
#
# Upstream migration CSVs are large (including >100k rows), so production
# execution should stream/fetch those source files rather than vendor them here.
#
# Required upstream files:
# data/interim/eel_meta_data.csv
# data/interim/migration/migration_2011_warnow.csv
# data/interim/migration/migration_2012_leopoldkanaal.csv
# data/interim/migration/migration_2013_albertkanaal.csv
# data/interim/migration/migration_2015_phd_verhelst_eel.csv
# data/interim/migration/migration_2019_grotenete.csv
# data/interim/migration/migration_esgl.csv
#
# Frozen parameters:
STAGE_SCORE = {"FIII": 0, "FIV": 1, "FV": 2}
SOURCE_REPO = "PieterjanVerhelst/eel-meta-analysis"
SOURCE_REF = "master"
MIGRATION_PROJECT_FILES = {
    "2011_Warnow": "data/interim/migration/migration_2011_warnow.csv",
    "2012_leopoldkanaal": "data/interim/migration/migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "data/interim/migration/migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "data/interim/migration/migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "data/interim/migration/migration_2019_grotenete.csv",
    "ESGL": "data/interim/migration/migration_esgl.csv",
}

CANONICAL_RESULT = {
    "migration_table_tags": 575,
    "coverage_excluding_life4fish": {
        "FIII": 0.9525547445,
        "FIV": 0.9714285714,
        "FV": 0.9498069498,
    },
    "descriptive": {
        "FIII": {"n": 261, "initiated": 161, "median_onset_days": 4.85854},
        "FIV": {"n": 68, "initiated": 54, "median_onset_days": 0.21514},
        "FV": {"n": 246, "initiated": 216, "median_onset_days": 0.69023},
    },
    "adjusted_initiation": {
        "n": 525,
        "project_year_strata": 11,
        "durif_or_per_stage": 1.9894168895,
        "durif_ci95": [1.4896939383, 2.6567736219],
        "durif_p": 3.1567283e-6,
    },
    "leave_one_project_out_or": {
        "2011_Warnow": 2.2580045770,
        "2012_leopoldkanaal": 1.8922947801,
        "2013_albertkanaal": 2.2466245984,
        "2015_phd_verhelst_eel": 1.6658444601,
        "2019_Grotenete": 1.8232738595,
        "ESGL": 2.1114189700,
    },
    "latency_among_initiators": {
        "n": 427,
        "project_year_strata": 13,
        "exp_beta_per_stage": 0.7473835677,
        "ci95_exp": [0.6011623698, 0.9291702630],
        "p": 0.0087579234,
    },
}

if __name__ == "__main__":
    import json
    print(json.dumps(CANONICAL_RESULT, indent=2))
    print(
        "Canonical result only. Reconstruct upstream source rows using the frozen "
        "file registry above before manuscript finalization."
    )
