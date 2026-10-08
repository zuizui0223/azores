# Does the silvering-stage association with classified migration onset vary among rivers?

**Evidence status (2026-10-08):** unstratified six-project finite-sample exact conditional test PASSED in [GitHub Actions run 37770796620](https://github.com/zuizui0223/azores/actions/runs/37770796620). A separate release-year-stratified exact analysis has been specified and implemented; the release-year result is not yet confirmed.

## Why this matters

The source six-project panel contains 575 stage-eligible eels. Durif silvering is positively associated with source-classified downstream migration in the pooled model (activation stage OR approximately 2.08). That average does **not** determine whether the direction or magnitude of the association is constant across river contexts.

Earlier post-hoc analysis used four projects with individually estimable stage slopes and found Q=4.14 (p=0.246), but **two projects containing quasi-separated initiation tables were excluded** from the heterogeneity summary. A heterogeneity test that drops separated cells can miss the strongest departures from a common effect. It is not appropriate to treat p=0.246 for that restricted subset as proof that all six projects share the same stage coefficient.

## Six-project FIII/FV source counts

| Project | FIII classified starts / eels | FV classified starts / eels |
|---|---:|---:|
| 2011 Warnow | 61/86 | 23/28 |
| 2012 Leopoldkanaal | 21/45 | 24/28 |
| 2013 Albertkanaal | 26/26 | 105/117 |
| 2015 Verhelst | 34/67 | 33/36 |
| 2019 Grotenete | 6/11 | 25/25 |
| ESGL | 6/26 | 5/12 |

The two separated source tables (Albertkanaal FIII=26/26 and Grotenete FV=25/25) are retained rather than discarded.

## Exact conditional question and result

We fixed each project's FIII/FV sample sizes and **total** source-classified initiators. Under a *common* FV-versus-FIII odds ratio across all six projects, each possible number of FV initiators follows a noncentral hypergeometric distribution. Conditioning additionally on the **total FV initiators across projects (215)** removes that common odds ratio as a nuisance parameter.

Full enumeration of the **156,690 permissible joint project tables** therefore gives a finite-sample exact conditional test of homogeneous silvering odds without requiring a normal approximation or dropping separated projects.

- Fitted common conditional FV-versus-FIII odds ratio: **3.5508**.
- Likelihood-ratio statistic comparing one common odds ratio with six project-specific odds ratios: **26.1699**.
- **Exact conditional p = 0.00014104**.
- Independent parametric bootstrap with 10,000 null replicates and common-odds refitting: **0** statistics as extreme, plus-one p **0.00009999**.
- Python synthetic checks passed; a separately implemented JavaScript exact enumeration agreed to numerical precision.

These results reject a **single common FV/FIII source-label association across all six projects**, conditional on the sampled project margins and the model's independent-fish assumption. It does not require estimating infinite project-specific logistic coefficients as finite Wald effects.

## Robustness and unresolved confounding

An exploratory exact omission calculation gives a positive heterogeneity signal after excluding any one project; excluding Albertkanaal yields p approximately **0.0448** (five projects). The repository's updated CI calculation of all leave-one-project-out exact tails is pending, so those omission tails are secondary until reproduced.

**Critically, different release years may be mixed within projects.** A separate analysis conditions on every project × release-year table before comparing project-specific silvering odds. See:
- `analysis/contracts/silvering_stage_project_year_heterogeneity_exact_v1.json`
- `analysis/54_silvering_stage_project_year_heterogeneity_exact.py`
- `.github/workflows/silvering-stage-project-year-heterogeneity-exact.yml`

Do not promote a claim of river-specific stage biology until this stricter temporal composition check is completed.

## What is — and is not — identified

**Identified observational pattern:** a common FV/FIII *telemetry-classified initiation odds ratio* is a poor description of all six source cohorts.

**Not identified:** that river discharge, tidal constraints, barriers, energy reserves or any ecological cue causes the variation. This is not a controlled river manipulation. Project-specific cohort selection, follow-up duration, upstream tagging methods and acoustic observation opportunities are confounded with waterways.

The result does not overwrite the previously valid result that all **four individually estimable adjusted project stage slopes were positive**; those tests used a restricted four-project estimand and an ordinal per-stage slope rather than this six-project exact FIII/FV contrast. Both statements can be true.

The key inferential distinction:
- Pooled stage effect: stronger source-classified activation at advanced silvering in the tagged sample.
- Between-river homogeneity: **not supported** by the six-project exact test.
- Biological mechanism and management consequences: **not yet determined**.

## Ecological and conservation implications

A uniform maturity-to-migration conversion factor across rivers is not empirically justified by this particular observational panel. It is safer to report separately: production of morphologically silver eels, individually classified downstream movement, duration/coverage of receiver observation, safe barrier passage and actual escapement.

One may **hypothesize** that external cues and river structure modify readiness-to-departure conversion, but reliable identification requires repeated environments under matched fish observation coverage, project-year-balanced measurement, and time-aligned flow/tide and independent passage events.

## Reproduction

- [Numerical result](../results/silvering_stage_project_heterogeneity_exact_v1.json)
- [Python exact and bootstrap implementation](../analysis/53_silvering_stage_project_heterogeneity_exact.py)
- [Frozen contract](../analysis/contracts/silvering_stage_project_heterogeneity_exact_v1.json)
- [No-network synthetic checks](../analysis/tests/test_silvering_stage_project_heterogeneity_exact.py)
- [Successful Actions run](https://github.com/zuizui0223/azores/actions/runs/37770796620)
