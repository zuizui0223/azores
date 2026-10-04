# Manuscript sample-flow contract — Azores phase-control paper

## Primary analytic universe

| Step | n | Rule |
|---|---:|---|
| FIII/FIV/FV metadata in six focal projects before cleaned-track availability | 603 | Exact female Durif stage and focal project |
| Cleaned/evaluable project-level migration tracks | **575** | Present in inherited public migration tables |
| Metadata-stage records absent from cleaned movement universe | 28 | **Not** recoded as non-migrants |
| Of the 28 absent: explicitly removed by upstream cleaning | 27 | Taxonomic/translocation/track-quality/source rules |
| Remaining absent track | 1 | A69-1601-26517: release record only, no post-release detection |
| Algorithm-positive tracks before 2015 expert correction | 431 | Sensitivity only |
| Source expert-corrected migration initiators | **422** | Primary initiation definition |
| FIII initiators | 154 / 261 | 59.0% |
| FIV initiators | 53 / 68 | 77.9% |
| FV initiators | 215 / 246 | 87.4% |

## Analysis-specific effective n

| Analysis | n | Events / rows | Why n differs |
|---|---:|---:|---|
| Binary migration initiation | 575 tracked universe; informative strata subset in fitted model | binary | Project-year strata require outcome variation and >=2 stages |
| Cox migration onset | **570** | **418 onset events** | Requires valid follow-up from release to onset or last telemetry row |
| Conditional completion | 422 initiators before informative-stratum filtering | binary completion | Only initiated eels; fitted model requires informative project-year strata |
| Post-initiation speed | **418 modelled** | continuous speed | Requires valid positive migration distance/time and informative strata |
| Direct phase interaction | **575 individuals** | **910 stacked rows** | One initiation row per individual + one completion row for eligible initiators; 22 informative phase × project-year strata |

## Nine fixed 2015 expert non-migrant corrections

These source-study judgements are inherited unchanged:

- A69-1601-52624
- A69-1601-57478
- A69-1601-52630
- A69-1601-52658
- A69-1601-52650
- A69-1601-52652
- A69-1601-57465
- A69-1601-52665
- A69-1602-30335

They remain in the tracked universe but are treated as non-initiators in the primary expert-corrected analysis.

## Hard reporting rules

- Never use 603 as the tracked analysis n.
- Never recode the 28 absent cleaned tracks as non-migrants.
- Never report the pre-expert-correction counts 161/54/216 as primary.
- Primary initiation counts are 154/53/215.
- Distinguish 422 expert-corrected initiators from 418 Cox onset events and 418 speed-modelled initiators.
- Do not imply that different effective n values are contradictory; they correspond to different endpoint-specific eligibility requirements.
