# Superseded developmental analysis

This file is retained for provenance only.

The earlier analysis used all FIII/FIV/FV metadata individuals as the denominator for the published successful-migrant endpoint. Source-code audit showed that this denominator was too broad: the upstream workflow first filters to individuals/records classified as migratory and only then identifies successful escapement.

The current corrected result separates:

1. migration initiation among exact-stage individuals actually represented in the relevant migration tables;
2. migration completion among those initiators.

See:
- [corrected two-stage result](corrected_two_stage_migration_result.md)
- [analysis/09_two_stage_migration.py](../analysis/09_two_stage_migration.py)

Do not cite the former OR in this file as the current ecological result.
