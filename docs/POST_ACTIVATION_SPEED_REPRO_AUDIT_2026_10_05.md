# Post-activation speed reproducibility audit — resolved 2026-10-06

## Resolution

The apparent reproducibility discrepancy was caused by a GitHub connector retrieval limitation for large CSV files, **not** by missing upstream data.

The ordinary file-content route returned an empty content field for three very large migration CSVs while still returning non-empty Git blob SHAs. Fetching those exact blobs by SHA recovered the full data:

- `migration_2012_leopoldkanaal.csv`: ~5.47 million characters;
- `migration_2013_albertkanaal.csv`: ~29.0 million characters;
- `migration_2015_phd_verhelst_eel.csv`: ~2.94 million characters.

The pinned upstream source remains:

- repository: `PieterjanVerhelst/eel-meta-analysis`
- commit: `59578cb622dddbbba5174b4c51bff0807787385a`

## Independent reconstruction

The current committed logic in `analysis/12_post_initiation_speed.py` was independently reconstructed from the six pinned migration inputs plus `eel_meta_data.csv`.

After expert non-migrant exclusions and the script's project-year eligibility rule:

- valid speed-bearing individuals before the stratum filter: **422**;
- modelled individuals: **418**;
- eligible project-year strata: **13**.

Modelled individuals by project:

- 2011 Warnow: **107**;
- 2012 Leopoldkanaal: **52**;
- 2013 Albertkanaal: **128**;
- 2015 phd_verhelst_eel: **86**;
- 2019 Grotenete: **33**;
- ESGL: **12**.

The independently reconstructed primary coefficient is:

- Durif-stage beta: **-0.0170354672**;
- multiplicative speed ratio: **0.9831088159**;
- 95% CI: **0.8524016314–1.1338586275**.

These reproduce the canonical manuscript values to numerical precision.

## Conclusion

**PASS_POST_ACTIVATION_SPEED_REPRO**

The canonical post-activation speed result is reproducible from the pinned source. The previous temporary STOP was based on mistaking omitted large-file content returned by the connector for zero-byte upstream files.

## Remaining scientific question

Reproducibility is no longer the issue.

The useful next question is biological heterogeneity:

> **Is the weak pooled Durif-stage gradient a genuinely general post-activation pattern, or can the stage effect vary among route/environmental contexts and average toward zero?**

This question is motivated by external evidence that silvering stage can contribute to downstream progression in some systems. It should be tested as a pre-specified project/context heterogeneity analysis rather than by searching for a different pooled endpoint.
