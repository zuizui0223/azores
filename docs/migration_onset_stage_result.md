# Algorithm-only onset sensitivity — not the canonical result

This file is retained as a sensitivity/audit record.

The analysis in the original version of this file used classifier-positive migration records before applying the source study's nine expert non-migrant overrides in the 2015 project. It therefore produced slightly different raw stage counts and effect estimates.

The **canonical expert-corrected** activation result is:

| stage | initiated / tracked | rate |
|---|---:|---:|
| FIII | 154/261 | 59.0% |
| FIV | 53/68 | 77.9% |
| FV | 215/246 | 87.4% |

Adjusted activation OR per Durif-stage increment:

**2.08** (95% CI **1.56–2.76**).

Canonical time-to-onset result:

**HR 1.29** (95% CI **1.13–1.47**).

Use `results/phase_control_canonical_v1.json` as the numeric source of truth.

The pre-correction classifier-only result is retained in git history only and must not be used as the headline estimate.
