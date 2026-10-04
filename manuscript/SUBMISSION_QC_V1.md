# Submission QC — Azores phase-control manuscript

## Current status

The biological story is frozen around one primary claim:

> **The predictive effect of internal migratory readiness is phase dependent: strong at migration activation and significantly attenuated during subsequent progression.**

The V2 manuscript is now structurally complete:

- Abstract;
- Introduction;
- full Methods;
- Results;
- full Discussion;
- Conclusion;
- Data availability;
- Code availability;
- Ethics placeholder;
- Author/Acknowledgement placeholders;
- core References.

## Numeric source of truth

Use:

- `manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V1.json`

Do not manually propagate numbers from old exploratory notes.

The sample-flow source of truth is:

- `manuscript/SAMPLE_FLOW_PHASE_CONTROL_V1.md`

## Automated QC

Run:

~~~bash
python validation/validate_manuscript_v2.py
~~~

The checker fails if:

- EOG appears in the biological manuscript;
- forbidden causal/absolute claims appear;
- old algorithm-only initiation counts are presented as primary;
- required core numerical results are absent;
- core cited sources are missing from text or References.

## Manual checks still required before submission

1. Replace author, affiliation, author-contribution and acknowledgement placeholders.
2. Select target journal and apply its exact reference/section/word-count format.
3. Add original-study ethics approval details by citing the source telemetry papers rather than inventing a new approval statement.
4. Generate final figures from canonical analysis outputs.
5. Confirm repository/data accession wording and archive a submission release.
6. Proof the full author list for Verhelst et al. (2025) against the publisher record.
7. Decide whether the Dutch independent constraint belongs in the main text or Supplement depending on journal length.

## Submission-stopping scientific rules

Do not submit if the manuscript says or implies:

- internal state causes migration;
- external environment wholly replaces internal control;
- WRS causally explains completion;
- Durif has zero post-initiation effect;
- the Dutch study directly replicates the Europe-wide phase interaction.

The evidence supports attenuation and phase-specific relative control, not mutually exclusive mechanisms.
