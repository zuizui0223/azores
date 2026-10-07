# Claim–evidence map — phase control V3 / manuscript V4

This map supersedes `docs/CLAIM_EVIDENCE_MAP_PHASE_CONTROL_V2.md` for the V4
multivariate-entry-state manuscript.

| Claim | Evidence | Status | Boundary |
|---|---|---|---|
| Capture-time Durif stage predicts migration activation | OR **2.08** per stage, 95% CI **1.56–2.77** in the canonical stage model | Strong developmental | Expected from silvering biology; not novelty alone |
| Continuous capture body state adds information beyond the ordinal Durif label | Multivariate activation model: condition OR **1.46/SD**, 95% CI **1.16–1.83**; Durif OR **2.13/stage** | Strong developmental | Condition is weight/length-derived and not independent physiology |
| Durif and condition act mainly additively at the entry gate | Durif×condition and Durif×length interaction model: LR p **0.931** | Developmental mechanism diagnostic | Does not exclude nonlinear/unmeasured physiological interactions |
| An activation-trained multivariate score predicts migration entry | Score OR **2.23/SD**, 95% CI **1.70–2.92** | Strong within-panel transferability benchmark | Score trained and evaluated in the same public panel; not prospective validation |
| The same activation-trained score predicts earlier behavioral onset | HR **1.32/SD**, 95% CI **1.17–1.49**, **418** onset events | Strong cross-endpoint transfer | Behavioral classifier onset, not physiological decision time |
| The same entry-state score does not rank generic whole-route speed | Ratio **0.946/SD**, 95% CI **0.832–1.076**, p **0.396**; partial R² **0.18%** | Strong null-compatible transferability boundary | Post-activation population is selected; not proof of zero state effects |
| The weak speed transfer is not an artifact of the whole-route endpoint | Frozen individual median positive inter-station speed ratio **1.028/SD**, 95% CI **0.869–1.215**, p **0.750**; partial R² **0.026%** | Developmental frozen-endpoint audit | Does not exclude reach/event-specific state effects |
| Durif alone shows the same phase boundary | Activation OR **2.08**, onset HR **1.29** vs whole-route speed ratio **0.983** and frozen segment ratio **1.001** | Canonical | Multivariate score is the stronger V4 framing |
| Project sign cancellation does not explain the weak generic stage-speed gradient | whole-route Q **2.47**, p **0.781**; segment Q **2.32**, p **0.804** | Post-hoc heterogeneity audit | Some project-stage cells remain imprecise |
| Simple capture-stage ageing does not explain the result | Durif×log-latency ratio **1.036**, p **0.382**; short-latency ratios remain near/below 1 | Post-hoc diagnostic | No repeated post-release physiology |
| Measured activation selection does not restore a positive speed ranking | stage IPW: **1.042→1.062**; condition IPW: **0.907→0.920** | Post-hoc selection diagnostic | Latent readiness selection remains unidentifiable |
| Better condition is **not** supported as causing greater post-arrival barrier selectivity | Dutch CL condition×duration β **−0.095**, p **0.841**, permutation p **0.849**; EZ near-separated and opposite predicted sign | Independent developmental falsification | EZ conditional model is non-converged/ill-conditioned; do not interpret its large negative coefficient biologically |
| Better condition is **not** associated with more post-arrival missed opportunities or delay in the Dutch system | EZ missed r **0.009**, p **0.960**; delay r **0.072**, p **0.677**. CL missed r **−0.104**, p **0.592**; delay r **−0.182**, p **0.350** | Independent developmental falsification | Eventual passers only; not an estimate of eventual passage probability |
| Terminal positive-set membership is not biological failure | source terminal OR **1.15**, CI **0.83–1.59**, retained only as sensitivity | Endpoint boundary | No escapement probability is estimated |
| Fine-scale post-activation state effects can still exist | River Test 2026 retained silvering stage in a reach-level model | External scope boundary | Different route, endpoint and model; not a replication |

## Primary V4 claim

> **The multivariate capture phenotype that predicts migratory commitment is an
> entry-state indicator, not a transferable general motor-performance score
> across the generic post-activation speed summaries tested here.**

## Claims explicitly rejected

Do not claim that:

- the novelty is simply that more silvered eels migrate;
- the entry-state score is a validated physiological latent variable;
- internal state becomes irrelevant after activation;
- external route conditions causally replace internal state;
- terminal non-membership is migration failure;
- escapement probability is estimated;
- better-conditioned eels generally wait for longer barrier-opening opportunities;
- asset protection explains the phase boundary;
- the Dutch study confirms an internal-to-external control handoff.

## Canonical V4 artifacts

- `manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md`
- `manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V4.json`
- `manuscript/MANUSCRIPT_QC_V4.json`
- `results/entry_state_score_transferability_v1.json`
- `results/phase_control_canonical_v2.json`
- `results/dutch_condition_choice_test_v1.json`
- `results/dutch_arrival_waiting_diagnostic_v1.json`
- `results/body_condition_activation_selection_ipw_v1.json`
