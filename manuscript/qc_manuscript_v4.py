#!/usr/bin/env python3
"""Fail-closed manuscript QC for Azores V4."""
from __future__ import annotations

import json
import re
from pathlib import Path

M = Path("manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md")
C = Path("manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V4.json")
R = Path("results/entry_state_score_transferability_v1.json")
D = Path("results/dutch_condition_choice_test_v1.json")
W = Path("results/dutch_arrival_waiting_diagnostic_v1.json")
X = Path("results/cross_project_entry_state_score_v1.json")
L = Path("results/within_link_entry_state_speed_v1.json")
Q = Path("results/within_link_speed_quality_sensitivity_v1.json")
F = Path("results/within_link_fwl_numerical_audit_v1.json")
FD = Path("manuscript/FIGURE_DATA_CONTRACT_V4.json")
I = Path("results/cross_project_condition_increment_v1.json")
J = Path("results/cross_project_condition_increment_project_robustness_v1.json")
G = Path("results/stage_specific_condition_gate_v1.json")
H = Path("results/stage_gate_context_matched_robustness_v1.json")
CM = Path("results/continuous_morphology_condition_increment_v1.json")
PENALTY = Path("results/continuous_morphology_penalty_sensitivity_v1.json")
SEASON = Path("results/seasonal_condition_interaction_v1.json")
FIXED = Path("results/fixed_followup_condition_increment_v1.json")
PAIRED = Path("results/paired_temporal_endpoint_condition_v1.json")
ENTRANT = Path("results/entrant_onset_latency_discrimination_v1.json")
OBS = Path("results/observability_selection_gate_v1.json")
OBS_MIX = Path("results/observability_project_composition_v1.json")
LABEL_TIP = Path("results/observability_label_ambiguity_tipping_v1.json")
RANDOM_HIDDEN = Path("results/observability_random_hidden_start_sensitivity_v1.json")
RECEIVER_OBS = Path("results/receiver_witness_observability_v1.json")
RECEIVER_TIP = Path("results/receiver_stratified_label_tipping_v1.json")
STAGE_BOUNDS = Path("results/stage_entry_observability_bounds_v1.json")
STAGE_SAMPLE = Path("results/stage_order_dual_uncertainty_v1.json")
STAGE_TIP = Path("results/stage_stratified_hidden_start_tipping_v1.json")

text = M.read_text(encoding="utf-8")
contract = json.loads(C.read_text())
score = json.loads(R.read_text())
dutch = json.loads(D.read_text())
waiting = json.loads(W.read_text())
cross = json.loads(X.read_text())
link = json.loads(L.read_text())
quality = json.loads(Q.read_text())
fwl = json.loads(F.read_text())
figure = json.loads(FD.read_text())
increment = json.loads(I.read_text())
project_robustness = json.loads(J.read_text())
stage_gate = json.loads(G.read_text())
stage_matched = json.loads(H.read_text())
morphology = json.loads(CM.read_text())
penalty = json.loads(PENALTY.read_text())
seasonal = json.loads(SEASON.read_text())
fixed_followup = json.loads(FIXED.read_text())
paired_endpoint = json.loads(PAIRED.read_text())
entrant_latency = json.loads(ENTRANT.read_text())
observability = json.loads(OBS.read_text())
observability_mix = json.loads(OBS_MIX.read_text())
label_tip = json.loads(LABEL_TIP.read_text())
random_hidden = json.loads(RANDOM_HIDDEN.read_text())
receiver_obs = json.loads(RECEIVER_OBS.read_text())
receiver_tip = json.loads(RECEIVER_TIP.read_text())
stage_bounds = json.loads(STAGE_BOUNDS.read_text())
stage_sample = json.loads(STAGE_SAMPLE.read_text())
stage_tipping = json.loads(STAGE_TIP.read_text())

checks = {}

def has(pattern: str) -> bool:
    return re.search(pattern, text, flags=re.I | re.M) is not None

def count_line(line: str) -> int:
    return sum(1 for x in text.splitlines() if x.strip() == line)

# Structure
checks["single_discussion_heading"] = count_line("## Discussion") == 1
checks["single_phase_question_heading"] = count_line("### Why phase-specific analysis changes the ecological question") == 1
checks["single_data_availability_heading"] = count_line("## Data availability") == 1
checks["no_stale_V3_label"] = not has(r"\bV3\b|MANUSCRIPT_V3")
checks["no_pending_dutch_gate"] = not has(r"Until that gate passes|Current gate:\s*|retrieve the public DANS files")

# Correct canonical event count: explicitly prevent old 427 bug.
checks["onset_418"] = has(r"418 onset events|onset events\s*=\s*\*\*418\*\*|418\s+onset events")
checks["no_onset_427"] = not has(r"427 onset events|onset events\s*=\s*427")

# Multivariate score numbers as displayed in V4.
checks["score_activation_OR_2_23"] = has(r"2\.23")
checks["score_onset_HR_1_32"] = has(r"1\.32")
checks["score_whole_speed_0_946"] = has(r"0\.946")
checks["score_segment_speed_1_028"] = has(r"1\.028")
checks["score_partial_r2_whole_018pct"] = has(r"0\.18%")
checks["score_partial_r2_segment_0026pct"] = has(r"0\.026%")
checks["cross_activation_OR_1_97"] = has(r"1\.97")
checks["cross_onset_HR_1_26"] = has(r"1\.26")
checks["cross_whole_speed_0_948"] = has(r"0\.948")
checks["cross_segment_speed_1_013"] = has(r"1\.013")
checks["within_link_ratio_0_962"] = has(r"0\.962")
checks["within_link_ci_0_883_1_048"] = has(r"0\.883") and has(r"1\.048")
checks["within_link_n_segments_17792"] = has(r"17,792")
checks["within_link_n_fish_418"] = has(r"17,792.{0,120}418")
checks["within_link_n_pairs_244"] = has(r"244")
checks["quality_ratios_present"] = has(r"0\.942") and has(r"0\.944") and has(r"0\.941")
checks["quality_boundary_present"] = has(r"3752") and has(r"53\.0") and has(r"63\.1")
checks["within_link_no_superseded_numbers"] = not has(r"18,012|0\.995|0\.00052%")
checks["within_link_weak_negative_quality_boundary"] = has(r"0\.07.{0,8}0\.08")

# Contract/result identity.
checks["score_schema"] = score.get("schema") == "azores.entry_state_score_transferability.v1"
checks["score_onset_events_result_418"] = score["score_transfer"]["onset"]["events"] == 418
checks["score_activation_exact"] = abs(score["score_transfer"]["activation"]["effect"]["odds_ratio"] - contract["entry_state_score"]["activation"]["or_per_sd"]) < 1e-9
checks["score_onset_exact"] = abs(score["score_transfer"]["onset"]["effect"]["hazard_ratio"] - contract["entry_state_score"]["onset"]["hr_per_sd"]) < 1e-9
checks["score_whole_speed_exact"] = abs(score["score_transfer"]["whole_route_speed"]["effect"]["ratio"] - contract["entry_state_score"]["whole_route_speed"]["ratio_per_sd"]) < 1e-9
checks["score_segment_speed_exact"] = abs(score["score_transfer"]["frozen_median_positive_interstation_speed"]["effect"]["ratio"] - contract["entry_state_score"]["frozen_segment_speed"]["ratio_per_sd"]) < 1e-9
checks["cross_schema"] = cross.get("schema") == "azores.cross_project_entry_state_score.v1"
checks["cross_activation_exact"] = abs(cross["crossfitted_transfer"]["activation"]["effect"]["odds_ratio"] - contract["cross_project_entry_state"]["activation"]["or_per_sd"]) < 1e-9
checks["cross_onset_exact"] = abs(cross["crossfitted_transfer"]["onset"]["effect"]["hazard_ratio"] - contract["cross_project_entry_state"]["onset"]["hr_per_sd"]) < 1e-9
checks["cross_whole_speed_exact"] = abs(cross["crossfitted_transfer"]["whole_route_speed"]["effect"]["ratio"] - contract["cross_project_entry_state"]["whole_route_speed"]["ratio_per_sd"]) < 1e-9
checks["cross_segment_speed_exact"] = abs(cross["crossfitted_transfer"]["frozen_median_positive_interstation_speed"]["effect"]["ratio"] - contract["cross_project_entry_state"]["frozen_segment_speed"]["ratio_per_sd"]) < 1e-9
checks["cross_weight_signs_positive"] = bool(cross["weight_stability"]["stage_beta_all_positive"] and cross["weight_stability"]["condition_beta_all_positive"])
checks["within_link_schema"] = link.get("schema") == "azores.within_link_entry_state_speed.v1"
checks["within_link_ratio_exact"] = abs(link["primary"]["entry_state_effect"]["speed_ratio_per_1sd_score"] - contract["within_link_entry_state"]["primary"]["ratio_per_sd"]) < 1e-9
checks["within_link_ci_exact"] = all(abs(a-b) < 1e-9 for a,b in zip(link["primary"]["entry_state_effect"]["ci95"], contract["within_link_entry_state"]["primary"]["ci95"]))
checks["within_link_sample_exact"] = link["primary"]["n_segment_rows"] == contract["within_link_entry_state"]["primary"]["n_segment_rows"] and link["primary"]["n_fish"] == contract["within_link_entry_state"]["primary"]["n_fish"] and link["primary"]["n_pairs"] == contract["within_link_entry_state"]["primary"]["n_directed_pairs"]
checks["within_link_status_null"] = link.get("status") == "NO_SUPPORTED_WITHIN_LINK_ENTRY_STATE_SPEED_GRADIENT"
checks["within_link_expert_correction"] = link.get("expert_non_migrant_segment_rows") == 0 and link.get("canonical_expert_non_migrant_count") == 9
checks["within_link_canonical_initiator_universe"] = link.get("raw_candidate_fish") == 422
checks["quality_uses_corrected_primary"] = quality.get("frozen_primary_reference", {}).get("n_fish") == link.get("primary", {}).get("n_fish") and abs(quality.get("frozen_primary_reference", {}).get("ratio", 0) - link.get("primary", {}).get("entry_state_effect", {}).get("speed_ratio_per_1sd_score", 999)) < 1e-9
checks["quality_schema"] = quality.get("schema") == "azores.within_link_speed_quality_sensitivity.v1"
checks["quality_status_robust"] = quality.get("status") == "WITHIN_LINK_NULL_ROBUST_TO_GROSS_SPEED_ARTIFACT_SCREEN"
checks["quality_2_5_exact"] = abs(quality["threshold_results"]["2.5"]["primary_model_after_quality_cut"]["entry_state_effect"]["speed_ratio_per_1sd_score"] - contract["within_link_entry_state"]["source_speed_quality_boundary"]["posthoc_upper_screen_results"]["2.5"]["ratio_per_sd"]) < 1e-9
checks["quality_5_exact"] = abs(quality["threshold_results"]["5.0"]["primary_model_after_quality_cut"]["entry_state_effect"]["speed_ratio_per_1sd_score"] - contract["within_link_entry_state"]["source_speed_quality_boundary"]["posthoc_upper_screen_results"]["5.0"]["ratio_per_sd"]) < 1e-9
checks["quality_10_exact"] = abs(quality["threshold_results"]["10.0"]["primary_model_after_quality_cut"]["entry_state_effect"]["speed_ratio_per_1sd_score"] - contract["within_link_entry_state"]["source_speed_quality_boundary"]["posthoc_upper_screen_results"]["10.0"]["ratio_per_sd"]) < 1e-9
checks["fwl_equivalence_pass"] = fwl.get("status") == "PASS_FWL_NUMERICAL_EQUIVALENCE"
checks["fwl_primary_agreement"] = fwl["primary_all_positive_source_speeds"]["absolute_beta_difference"] < 1e-8 and fwl["primary_all_positive_source_speeds"]["absolute_se_difference"] < 5e-4
checks["fwl_primary_sample_match"] = fwl["primary_all_positive_source_speeds"]["n_rows"] == link["primary"]["n_segment_rows"] and fwl["primary_all_positive_source_speeds"]["n_fish"] == link["primary"]["n_fish"]
checks["figure3_corrected_link"] = figure["main_figures"]["figure3"]["exact_link_transit"]["n_segment_rows"] == link["primary"]["n_segment_rows"] and abs(figure["main_figures"]["figure3"]["exact_link_transit"]["ratio_per_sd"] - link["primary"]["entry_state_effect"]["speed_ratio_per_1sd_score"]) < 1e-9
checks["figure3_quality_sensitivity"] = figure["main_figures"]["figure3"]["speed_quality_sensitivity"]["all_intervals_include_one"] is True

# Project-held-out AUC increment and project-level uncertainty.
delta = increment["primary_pairwise_auc"]["delta_auc_condition_above_stage_length_timing"]
incr_contract = contract["heldout_condition_increment"]
checks["condition_increment_schema"] = increment.get("schema") == "azores.cross_project_condition_increment.v1"
checks["condition_increment_n_projects"] = increment["n_projects"] == 6 and increment["n_source_evaluable"] == 575
checks["condition_increment_auc_exact"] = abs(delta - incr_contract["incremental_auc"]) < 1e-10
checks["condition_increment_auc_baseline_exact"] = abs(increment["primary_pairwise_auc"]["auc"]["score_base"] - incr_contract["base_auc"]) < 1e-10
checks["condition_increment_auc_plus_exact"] = abs(increment["primary_pairwise_auc"]["auc"]["score_plus"] - incr_contract["expanded_auc"]) < 1e-10
checks["condition_increment_pairs_exact"] = increment["primary_pairwise_auc"]["n_positive_negative_pairs"] == incr_contract["initiator_noninitiator_pairs"] == 6914
checks["condition_increment_stage_control"] = increment["secondary_same_stage_pairwise_auc"]["n_positive_negative_pairs"] == incr_contract["same_stage_pairs"] == 3199
checks["condition_increment_4_of_6"] = increment["primary_pairwise_auc"]["project_deltas_positive"] == incr_contract["n_projects_positive"] == 4
checks["condition_project_robustness_schema"] = project_robustness.get("schema") == "azores.cross_project_condition_increment_project_robustness.v1"
checks["condition_project_ci_includes_zero"] = project_robustness["project_cluster_bootstrap"]["pair_weighted_gain_ci95"][0] < 0 < project_robustness["project_cluster_bootstrap"]["pair_weighted_gain_ci95"][1]
checks["condition_project_ci_exact"] = all(abs(x-y)<1e-10 for x,y in zip(project_robustness["project_cluster_bootstrap"]["pair_weighted_gain_ci95"], incr_contract["project_cluster_bootstrap_ci95"]))
checks["condition_project_leave_one_out"] = min(p["delta_auc"] for p in project_robustness["leave_one_project_out"]) > 0
checks["condition_project_signed_test"] = abs(project_robustness["exploratory_exact_sign_flip"]["weighted"]["two_sided"] - 0.1875) < 1e-10
checks["condition_figure_contract_matches"] = abs(figure["supplementary"]["heldout_condition_increment"]["delta_auc"] - delta) < 1e-10
checks["condition_auc_reported"] = has(r"0\.610") and has(r"0\.643") and has(r"0\.0336")
checks["condition_project_uncertainty_reported"] = has(r"0\.0007") and has(r"0\.0918") and has(r"four of six") and has(r"p=0\.1875")

# Complete-morphology replication of the condition increment.
mc = contract["continuous_morphology_condition_increment"]
fig_m = figure["supplementary"]["continuous_silvering_morphology"]
checks["continuous_morphology_schema"] = morphology.get("schema") == "azores.continuous_morphology_condition_increment.v1"
checks["continuous_morphology_n"] = morphology["n_complete_morphology_evaluable"] == mc["n_morphology_complete"] == 429
checks["continuous_morphology_projects"] = morphology["n_eligible_projects"] == mc["n_projects"] == 5 and "2011_Warnow" not in morphology["eligible_projects"]
checks["continuous_morphology_n_pairs"] = morphology["primary"]["n_pairs"] == mc["n_positive_negative_pairs"] == 3272
checks["continuous_morphology_auc_identity"] = all(abs(morphology["primary"]["auc"][key] - mc["auc"][key]) < 1e-10 for key in ("base","morph","condition","full"))
checks["continuous_morphology_condition_increment"] = abs(morphology["primary"]["deltas"]["condition_after_morph"] - mc["delta_auc"]["condition_after_morph"]) < 1e-10
checks["continuous_morphology_ci_spans_zero"] = morphology["project_uncertainty"]["project_bootstrap"]["ci95"][0] < 0 < morphology["project_uncertainty"]["project_bootstrap"]["ci95"][1]
checks["continuous_morphology_project_signs"] = morphology["project_uncertainty"]["n_positive_project_deltas"] == mc["n_project_delta_positive"] == 3
checks["continuous_morphology_figure"] = abs(fig_m["delta_auc"]["condition_after_morph"]-mc["delta_auc"]["condition_after_morph"]) < 1e-10
checks["continuous_morphology_manuscript"] = has(r"429") and has(r"3,272") and has(r"0\.0244") and has(r"0\.0003") and has(r"0\.0659")
checks["continuous_morphology_no_energy_proof"] = has(r"cannot isolate fat reserves") and has(r"not justify interpreting condition as an independent energy-reserve trait")
checks["stage_schema"] = stage_gate.get("schema") == "azores.stage_specific_condition_gate.v1"
checks["stage_n_fish"] = stage_gate["n_evaluable_fish"] == 575 and stage_gate["n_informative_same_stage_pairs"] == 3199
checks["stage_FV_FIII_finite"] = stage_gate["stage"]["FV"]["delta_auc"] > stage_gate["stage"]["FIII"]["delta_auc"]
checks["stage_matched_schema"] = stage_matched.get("schema") == "azores.stage_gate_context_matched_robustness.v1"
checks["stage_matched_contexts"] = stage_matched["full"]["n_contexts"] == 5 and stage_matched["full"]["n_projects"] == 4
checks["stage_matched_uncertainty"] = stage_matched["exploratory_exact_project_signflip_two_sided_p"] == 0.25
checks["penalty_schema"] = penalty.get("schema") == "azores.continuous_morphology_penalty_sensitivity.v1"
checks["penalty_three_strengths"] = sorted(penalty.get("sweep",{}).keys()) == ["0.1","1.0","10.0"]
checks["penalty_frozen_lambda_exact"] = abs(penalty["sweep"]["1.0"]["delta_auc"]["condition_after_morph"] - morphology["primary"]["deltas"]["condition_after_morph"]) < 1e-10
checks["penalty_all_positive"] = penalty["all_increment_signs_positive"] is True and all(x["delta_auc"]["condition_after_morph"]>0 for x in penalty["sweep"].values())
checks["penalty_all_project_ci_overlap_zero"] = penalty["all_project_resample_cis_include_zero"] is True and all(x["project_ci95"][0] < 0 < x["project_ci95"][1] for x in penalty["sweep"].values())
checks["penalty_contract_consistency"] = all(abs(penalty["sweep"][k]["delta_auc"]["condition_after_morph"]-contract["continuous_morphology_penalty_sensitivity"]["condition_after_morph_delta_by_lambda"][k]) < 1e-10 for k in ("0.1","1.0","10.0"))
checks["penalty_manuscript_reporting"] = has(r"0\.0269") and has(r"0\.0244") and has(r"0\.0214")





# Temporal endpoint evidence: guard against retroactive promotion of apparent
# short-horizon sign reversals or overstatement of entrant-only timing.
temp = contract["temporal_entry_decomposition"]
tcommon = temp["common_cohort_fixed_score"]
tlat = temp["entrant_latency"]
checks["temporal_season_schema"] = seasonal.get("schema") == "azores.seasonal_condition_interaction.v1"
checks["temporal_season_not_supported"] = seasonal.get("status") == "NO_GENERAL_HELDOUT_SEASONAL_CONDITION_INTERACTION_SUPPORT"
checks["temporal_season_delta_exact"] = abs(seasonal["primary"]["delta_auc"] - temp["seasonal_interaction"]["delta"]) < 1e-10
checks["temporal_fixed_schema"] = fixed_followup.get("schema") == "azores.fixed_followup_condition_increment.v1"
checks["temporal_fixed_primary_negative"] = abs(fixed_followup["windows"]["30"]["pairwise_auc"]["delta_auc_condition_above_stage_length_timing"] - temp["fixed_window_retrained"]["30"]["condition_auc_delta"]) < 1e-10
checks["temporal_fixed_retention"] = fixed_followup["windows"]["90"]["cohort"]["n_included"] == 475 and fixed_followup["windows"]["90"]["cohort"]["n_excluded_early_tracking_end"] == 100
checks["temporal_paired_schema"] = paired_endpoint.get("schema") == "azores.paired_temporal_endpoint_condition.v1"
checks["temporal_paired_475"] = paired_endpoint["n_common_fish"] == tcommon["n"] == 475
checks["temporal_paired_event_counts"] = paired_endpoint["endpoint_auc_with_fixed_scores"]["30"]["n_event"] == tcommon["by_horizon"]["30"]["events"] == 299 and paired_endpoint["endpoint_auc_with_fixed_scores"]["eventual"]["n_event"] == tcommon["by_horizon"]["eventual"]["events"] == 422
checks["temporal_paired_horizon_exact"] = all(abs(paired_endpoint["endpoint_auc_with_fixed_scores"][key]["delta_auc_condition_above_stage_length_timing"] - tcommon["by_horizon"][key]["condition_delta_auc"]) < 1e-10 for key in ("7","30","60","90","eventual"))
checks["temporal_paired_4projects"] = paired_endpoint["paired_eventual_minus_30day"]["n_projects"] == 4
checks["temporal_paired_project_signflip"] = abs(paired_endpoint["paired_eventual_minus_30day"]["signflip_two_sided_p"] - tcommon["paired_project_signflip_p"]) < 1e-10 and tcommon["paired_project_signflip_p"] == 0.125
checks["temporal_paired_ci_exact"] = all(abs(x-y)<1e-10 for x,y in zip(paired_endpoint["paired_eventual_minus_30day"]["project_boot_ci95"],tcommon["paired_project_boot_ci95"]))
checks["temporal_three_categories"] = paired_endpoint["early_late_never"]["group_counts"] == {"early_le_30":299,"late_gt_30":123,"no_detected_initiation":53}
checks["temporal_entrant_schema"] = entrant_latency.get("schema") == "azores.entrant_onset_latency_discrimination.v1"
checks["temporal_entrant_n"] = entrant_latency["n_initiators_with_valid_onset"] == tlat["n"] == 422 and entrant_latency["primary"]["n_pairs"] == tlat["pairs"] == 10756
checks["temporal_entrant_delta_exact"] = abs(entrant_latency["primary"]["condition_delta"] - tlat["condition_increment"]) < 1e-10
checks["temporal_entrant_ci_spans_zero"] = tlat["project_boot_ci95"][0] < 0 < tlat["project_boot_ci95"][1]
checks["temporal_entrant_exclusion"] = entrant_latency["sensitivity_excluding_day0_to1"]["n_entrants"] == tlat["n_excluding_1_day"] == 291
checks["temporal_figure_matches"] = figure["supplementary"]["temporal_entry_decomposition"]["common_cohort"]["n"] == tcommon["n"] and figure["supplementary"]["temporal_entry_decomposition"]["conditional_latency"]["pairs"] == tlat["pairs"]
checks["temporal_manuscript_results"] = has(r"10,756") and has(r"0\.5461") and has(r"0\.0329") and has(r"0\.0807") and has(r"0\.125")
checks["temporal_no_migration_delay_claim"] = not has(r"high(?:er)?[- ]condition eels (?:deliberately )?wait longer|proved? that (?:better|high)[- ]condition eels delay")


# 90-day observability gate: freeze the project-composition, permutation and
# descriptive follow-up denominators rather than promote a stronger timing effect.
oc = contract["observability_selection_gate"]
oe = observability["cohort"]
om = observability_mix["exact_decomposition"]
ar = observability["random_negative_retention"]
null = ar["conditional_random_retention"]
checks["observability_schema"] = observability.get("schema") == "azores.observability_selection_gate.v1"
checks["observability_mix_schema"] = observability_mix.get("schema") == "azores.observability_project_composition.v1"
checks["observability_n"] = oe["n_initiators"] == oc["source_initiators"] == 422 and oe["n_source_noninitiators"] == oc["source_noninitiators"] == 153
checks["observability_asymmetric_retention"] = oe["n_excluded_initiators"] == oc["excluded_initiators"] == 0 and oe["n_excluded_noninitiators"] == oc["early_followup_excluded"] == 100 and oe["n_retained_noninitiators"] == oc["retained_noninitiators"] == 53
checks["observability_full_auc"] = abs(observability_mix["auc_condition_increment"]["full"] - oc["full_eventual_auc_gain"]) < 1e-10
checks["observability_selected_auc"] = abs(ar["observed_selected_delta"] - oc["day90_selected_eventual_auc_gain"]) < 1e-10
checks["observability_exact_weight_identity"] = abs(om["identity_residual"]) < 1e-10 and abs(om["project_pair_weight_rebalancing"] - oc["project_weight_composition_term"]) < 1e-10 and abs(om["within_project_changes_and_project_year_mix"] - oc["within_project_changes_term"]) < 1e-10
checks["observability_random_retention_count"] = null["resamples"] == oc["null_retention"]["n_replicates"] == 20000
checks["observability_random_retention_same_auc"] = abs(null["mean_delta"] - oc["null_retention"]["mean_auc_gain"]) < 1e-10 and abs(ar["observed_selected_delta"] - oc["null_retention"]["observed_delta"]) < 1e-10
checks["observability_random_retention_ci"] = null["ci95"][0] < ar["observed_selected_delta"] < null["ci95"][1] and abs(null["two_sided_distance_from_mean_probability"] - oc["null_retention"]["two_sided_distance_from_mean_p"]) < 1e-10
checks["observability_no_phenotype_retention_claim"] = ar["status"] == "OBSERVED_RETENTION_WITHIN_STRATIFIED_RANDOM_THINNING_ENVELOPE"
checks["observability_source_negative_control"] = abs(observability["negative_control"]["auc_within_project_year"]["delta_auc_condition_above_stage_length_timing"] - oc["negative_control"]["delta_auc_condition"]) < 1e-10
checks["observability_followup_medians"] = abs(observability["noninitiator_condition_and_followup_medians"]["excluded"]["median_last_observation_days"] - oc["source_noninitiator_last_receiver_arrival_days"]["excluded_median"]) < 1e-10 and abs(observability["noninitiator_condition_and_followup_medians"]["retained"]["median_last_observation_days"] - oc["source_noninitiator_last_receiver_arrival_days"]["selected_median"]) < 1e-10
checks["observability_figure_data"] = abs(figure["supplementary"]["observation_process_gate"]["project_weight_rebalance_component"] - om["project_pair_weight_rebalancing"]) < 1e-10
checks["observability_in_manuscript"] = has(r"0\.0515") and has(r"0\.0044") and has(r"0\.0844") and has(r"0\.764") and has(r"100/153")
checks["observability_no_phenotype_time_strengthening"] = not has(r"condition gains? (?:more |stronger )?physiological influence over (?:elapsed )?time|time makes condition more biologically important")


checks["title_realized_transit_speed"] = text.startswith("# A multivariate entry state predicts migration activation but not realized transit speed in European eel")
checks["new_refs_present"] = "Tudorache, C." in text and "Katopodis, C." in text

# Dutch falsification language and numbers.
checks["dutch_falsification_heading"] = has(r"did not support condition-dependent barrier selectivity|falsified the specific prediction")
checks["dutch_CL_beta"] = has(r"β\s*=\s*[−-]0\.095")
checks["dutch_CL_p"] = has(r"p\s*=\s*0\.841")
checks["dutch_CL_perm_p"] = has(r"permutation p\s*=\s*0\.849")
checks["dutch_EZ_missed_null"] = has(r"r\s*=\s*0\.009.*p\s*=\s*0\.960")
checks["dutch_CL_missed_null"] = has(r"r\s*=\s*[−-]0\.104.*p\s*=\s*0\.592")
checks["dutch_choice_schema"] = dutch.get("schema") == "azores.dutch_condition_choice_test.v1"
checks["dutch_waiting_schema"] = waiting.get("schema") == "azores.dutch_arrival_waiting_diagnostic.v1"

# Interpretation boundaries.
checks["terminal_sensitivity_only"] = has(r"terminal.*sensitivity")
checks["nonmembership_not_failure"] = has(r"non-membership.*not.*(?:biological )?failure|complement.*not.*validated.*failure")
checks["no_escapement_claim"] = not has(r"we estimate(?:d)? escapement probability|escapement probability was")
checks["entry_not_progression_speed_claim"] = has(r"entry-state indicator.*not.*(?:transferable )?general progression-speed score|entry state is not a progression-speed score")
checks["no_asset_protection_support"] = not has(r"(support(?:s|ed)?|confirm(?:s|ed)?)\s+(?:a\s+)?(?:general\s+)?asset[- ]protection")
checks["no_dutch_handoff_confirmation"] = not has(r"Dutch.{0,100}(confirm(?:s|ed|ation)|support(?:s|ed)).{0,100}(handoff|internal-to-external)")

# Reference requirements.
for key in ["Durif, C.", "Nathan, R.", "Verhelst, P.", "Huisman, J. B. J.", "van Rijn, J.", "Lennox, R. J.", "Moyo, S."]:
    checks[f"ref::{key}"] = key in text

# Exact fixed-score sensitivity to hypothetical initiation misclassification.
lt = contract["observability_label_ambiguity_tipping"]
tc = label_tip["cohort"]
checks["label_tip_schema"] = label_tip.get("schema") == "azores.observability_label_ambiguity_tipping.v1"
checks["label_tip_evidence_class"] = label_tip.get("status") == "AUC_INCREMENT_SENSITIVE_TO_HYPOTHETICAL_UNOBSERVED_INITIATION"
checks["label_tip_sample"] = tc["source_fish"] == 575 and tc["source_initiators"] == lt["n_initiators"] == 422 and tc["source_noninitiators"] == lt["n_noninitiators"] == 153
checks["label_tip_short_followup"] = tc["short_followup_source_noninitiators_potentially_ambiguous"] == lt["n_shortfollowup_potentially_ambiguous"] == 100 and tc["long_observed_source_noninitiators_frozen_negative"] == lt["n_fixed_adequately_observed_noninitiators"] == 53
checks["label_tip_correct_frozen_baseline"] = abs(label_tip["frozen_original_auc_gain"] - incr_contract["incremental_auc"]) < 1e-10 and abs(label_tip["frozen_original_auc_gain"] - lt["baseline_delta_auc"]) < 1e-10
checks["label_tip_exact_tipping"] = label_tip["first_k_with_nonpositive_exact_minimum"] == lt["exact_first_nonpositive_k"] == 11 and abs(label_tip["tipping_witness"]["ratio"] - lt["first_nonpositive_delta_auc"]) < 1e-10
checks["label_tip_10_positive_15_nonpositive"] = label_tip["exact_minimum_at_k"]["10"]["ratio"] > 0 and label_tip["exact_minimum_at_k"]["15"]["ratio"] < 0
checks["label_tip_11_projects"] = label_tip["tipping_witness"]["flips_by_project"] == lt["tipping_flips_by_project"]
checks["label_tip_figure_data"] = figure["supplementary"]["observation_process_gate"]["label_ambiguity_bound"]["first_k_with_nonpositive_worst_case_auc_gain"] == label_tip["first_k_with_nonpositive_exact_minimum"] and abs(figure["supplementary"]["observation_process_gate"]["label_ambiguity_bound"]["worst_case_auc_gain_at_tipping"] - label_tip["tipping_witness"]["ratio"]) < 1e-10
checks["label_tip_manuscript_scope"] = has(r"adversarially selected 11") and has(r"worst-case label-contamination") and has(r"not a finding that eleven misclassifications occurred")
checks["label_tip_not_promoted_biology"] = not has(r"(?:observed|confirmed|proved) (?:eleven|11) (?:hidden|missed|false-negative) (?:migration|initiations)")

# The exact 11-fish vulnerability and a conditional random-assignment model
# answer different questions. Freeze that distinction in the manuscript.
rh = contract["observability_random_hidden_start_sensitivity"]
rfig = figure["supplementary"]["observation_process_gate"]["conditional_hidden_start_assignment"]
checks["random_hidden_schema"] = random_hidden.get("schema") == "azores.observability_random_hidden_start_sensitivity.v1"
checks["random_hidden_source_population"] = random_hidden["population"]["source_fish"] == 575 and random_hidden["population"]["hypothetically_relabelable_negative_fish"] == 100 and random_hidden["population"]["baseline_pairs"] == 6914
checks["random_hidden_exact_tipping_preserved"] = random_hidden["exact_adversarial_tipping_k"] == label_tip["first_k_with_nonpositive_exact_minimum"] == rh["exact_worst_case_tipping_k"] == 11
checks["random_hidden_baseline"] = abs(random_hidden["original_auc_increment"] - rh["baseline_auc_gain"]) < 1e-10
checks["random_hidden_scenario_count"] = len(random_hidden["scenarios"]) == 3 and all(len(v) == 10 for v in random_hidden["scenarios"].values())
checks["random_hidden_frozen_training"] = random_hidden["evidence_class"] == "post_hoc_scenario_sensitivity_after_exact_11_label_tipping"
checks["random_hidden_conditional_samples"] = random_hidden["monte_carlo_replications"] == rh["conditional_repetitions"] == 10000
for scenario,contract_key in [("uniform","uniform"),("stage_FV_x3","FV_enriched"),("adverse_disagreement_x3","score_disagreement_enriched")]:
    row = next(x for x in random_hidden["scenarios"][scenario] if x["k"] == 11)
    saved = rh["k11"][contract_key]
    checks["random_hidden_11_" + contract_key] = abs(row["median_auc_increment"] - saved["median"]) < 1e-10 and all(abs(a-b) < 1e-10 for a,b in zip(row["ci95_assignment"], saved["interval95"])) and row["fraction_nonpositive"] == 0 and saved["nonpositive_draws"] == 0
checks["random_hidden_rank_adverse_tail"] = all(abs(next(x for x in random_hidden["scenarios"]["adverse_disagreement_x3"] if x["k"] == int(k))["fraction_nonpositive"] - v) < 1e-10 for k,v in rh["score_disagreement_enrichment_nonpositive_fraction_by_k"].items())
checks["random_hidden_all100_nonmonotonic"] = abs(next(x for x in random_hidden["scenarios"]["uniform"] if x["k"] == 100)["mean_auc_increment"] - rh["deterministic_all_100_reclassified_gain"]) < 1e-10 and rh["deterministic_all_100_reclassified_gain"] > rh["baseline_auc_gain"]
checks["random_hidden_figure_match"] = abs(rfig["all_100_reclassified_auc_gain"] - rh["deterministic_all_100_reclassified_gain"]) < 1e-10 and abs(rfig["score_disagreement_nonpositive_at_50"] - rh["score_disagreement_enrichment_nonpositive_fraction_by_k"]["50"]) < 1e-10
checks["random_hidden_reported_as_hypothetical"] = has(r"10,000.{0,8}uniformly selected") and has(r"23\.3%") and has(r"hypothetical") and has(r"not a true detection-error model")

# Physical receiver event evidence is not proof of continuous receiver uptime.
rc = contract["receiver_observability_and_stratified_tipping"]
rf = figure["supplementary"]["observation_process_gate"]["receiver_evidence"]
short = receiver_obs["cohorts"]["short_followup_source_noninitiator"]
supported = receiver_obs["cohorts"]["day90_supported_source_noninitiator"]
groups = receiver_tip["observed_receiver_evidence_groups"]
checks["receiver_obs_schema"] = receiver_obs.get("schema") == "azores.receiver_witness_observability.v1"
checks["receiver_tip_schema"] = receiver_tip.get("schema") == "azores.receiver_stratified_label_tipping.v1"
checks["receiver_source_575"] = receiver_obs["source"]["focal_fish"] == 575 and receiver_tip["source_fish"] == 575
checks["receiver_exact_partition"] = short["n_fish"] == rc["receiver_cohort"]["short_noninitiators"] == 100 and short["n_fish_without_any_real_receiver_contact"] == rc["receiver_cohort"]["virtual_only"] == 24 and short["n_fish_with_real_receiver_contact"] == rc["receiver_cohort"]["any_real"] == 76
checks["receiver_supported_contrast"] = supported["n_fish"] == rc["receiver_cohort"]["day90_noninitiators"] == 53 and supported["number_real_receiver_rows"]["median"] == rc["receiver_cohort"]["day90_median_real_rows"] == 260 and short["number_real_receiver_rows"]["median"] == rc["receiver_cohort"]["median_real_rows"] == 1
checks["receiver_other_tag_point_witness"] = all(short["has_later_other_fish_detection_same_receiver"][str(k)]["n_positive"] == rc["receiver_cohort"][f"later_other_fish_same_receiver_{k}d"] for k in [1,7,90])
checks["receiver_no_fake_uptime"] = receiver_obs["source"]["has_receiver_deployment_and_recovery_times"] is False
checks["receiver_exact_tipping_partition"] = receiver_tip["unrestricted_first_nonpositive_k"] == rc["unrestricted_first_nonpositive_k"] == 11 and receiver_tip["original_adversarial_11_fish_group_composition"]["zero_real_contact"] == rc["original_11_witness_zero_receiver"] == 2 and receiver_tip["original_adversarial_11_fish_group_composition"]["any_real_contact"] == rc["original_11_witness_real_receiver"] == 9
checks["receiver_zero_contact_no_tipping"] = groups["zero_real_contact"]["candidate_count"] == 24 and groups["zero_real_contact"]["first_k_with_nonpositive_gain"] is None
checks["receiver_real_contact_13_tipping"] = groups["any_real_contact"]["candidate_count"] == 76 and groups["any_real_contact"]["first_k_with_nonpositive_gain"] == 13
checks["receiver_later_witness_13_tipping"] = groups["later_same_receiver_90d"]["candidate_count"] == 70 and groups["later_same_receiver_90d"]["first_k_with_nonpositive_gain"] == 13
checks["receiver_1day_witness_17_tipping"] = groups["later_same_receiver_1d"]["candidate_count"] == 58 and groups["later_same_receiver_1d"]["first_k_with_nonpositive_gain"] == 17
checks["receiver_group_figure_consistency"] = rf["virtual_only"] == 24 and rf["with_real_receiver"] == 76 and rf["original_witness_composition"]["with_real"] == 9 and abs(rf["exact_tipping_subgroups"]["any_real_contact"]["minimum_auc_at_k11"] - groups["any_real_contact"]["at_k11"]["minimum_auc_gain"]) < 1e-10
checks["receiver_manuscript_scope"] = has(r"24 of 100") and has(r"76.{0,30}actual receiver") and has(r"70.{0,100}later detection") and has(r"required .{0,20}13") and has(r"9 previously receiver-detected")




# Conditional partial-identification of ordinal silvering contrast under
# source-observation ambiguity. These are not biological stage-rate estimates.
sb = contract["stage_entry_observability_partial_identification"]
stage_figure = figure["supplementary"]["stage_entry_observability_partial_identification"]
stage_project = stage_bounds["project_status_summary"]
checks["stage_observability_source_schema"] = stage_bounds.get("schema") == "azores.stage_entry_observability_bounds.v1"
checks["stage_observability_575_fish"] = sum(v["n"] for v in stage_bounds["stage_bounds"].values()) == 575
checks["stage_observability_100_short_negative"] = sum(v["hypothetically_ambiguous_short_negative"] for v in stage_bounds["stage_bounds"].values()) == 100
checks["stage_observability_53_longer_negative"] = sum(v["longer_observed_negative"] for v in stage_bounds["stage_bounds"].values()) == 53
checks["stage_observability_source_bound_exact"] = all(
    abs(stage_bounds["stage_bounds"][k]["lower_rate"]-sb["stage_rate_bounds"][k]["rate_interval"][0]) < 1e-10
    and abs(stage_bounds["stage_bounds"][k]["upper_rate"]-sb["stage_rate_bounds"][k]["rate_interval"][1]) < 1e-10
    for k in ("FIII","FIV","FV")
)
checks["stage_observability_pooled_positive"] = stage_bounds["fv_minus_fiii_pooled"]["lower"] > 0 and abs(stage_bounds["fv_minus_fiii_pooled"]["lower"]-sb["pooled_fv_minus_fiii_bounds"][0]) < 1e-10
checks["stage_observability_project_uncertainty"] = stage_bounds["equal_project_mean_fv_minus_fiii_bounds"]["lower"] < 0 < stage_bounds["equal_project_mean_fv_minus_fiii_bounds"]["upper"]
checks["stage_observability_project_status"] = stage_project["robust_fv_gt_fiii"] == sb["project_status"]["robust_fv_gt_fiii"] == 2 and stage_project["robust_fv_lt_fiii"] == sb["project_status"]["robust_fv_lt_fiii"] == 1
checks["stage_observability_five_hypothetical_longer_flips"] = stage_bounds["minimum_additional_longer_observed_fiii_negative_relabels_to_erase_fv_over_fiii"]["needed"] == sb["min_additional_longer_observed_fiii_negative_flips_to_erase_pooled_order"] == 5
checks["stage_observability_fig_contract"] = all(abs(x-y)<1e-10 for x,y in zip(stage_figure["pooled_fv_minus_fiii_bounds"], sb["pooled_fv_minus_fiii_bounds"]))
checks["stage_observability_manuscript"] = has(r"85\.8%") and has(r"87\.4%") and has(r"1\.57 percentage points") and has(r"37 longer-observed FIII") and has(r"five")

# Separate sharp bounds in the observed fish from fish/context resampling.
su = contract["stage_order_sampling_uncertainty"]
checks["stage_dual_uncertainty_schema"] = stage_sample.get("schema") == "azores.stage_order_dual_uncertainty.v1"
checks["stage_dual_uncertainty_ref"] = abs(stage_sample["observed"]["pooled_lower"] - stage_bounds["fv_minus_fiii_pooled"]["lower"]) < 1e-12
checks["stage_dual_uncertainty_seed"] = stage_sample.get("n_resamples") == su["n_resamples"] == 10000 and stage_sample.get("seed") == su["seed"] == 20261008
checks["stage_fish_sample_ci_exact"] = all(abs(a-b)<1e-12 for a,b in zip(stage_sample["sampling_variation"]["within_project_fish"]["lower"]["ci95"],su["within_site_fish_lower_endpoint_ci95"]))
checks["stage_project_sample_ci_exact"] = all(abs(a-b)<1e-12 for a,b in zip(stage_sample["sampling_variation"]["project_cluster"]["pooled_lower"]["ci95"],su["project_cluster_lower_endpoint_ci95"]))
checks["stage_dual_ci_cross_zero"] = stage_sample["sampling_variation"]["within_project_fish"]["lower"]["ci95"][0] < 0 < stage_sample["sampling_variation"]["within_project_fish"]["lower"]["ci95"][1] and stage_sample["sampling_variation"]["project_cluster"]["pooled_lower"]["ci95"][0] < 0 < stage_sample["sampling_variation"]["project_cluster"]["pooled_lower"]["ci95"][1]
checks["stage_dual_manuscript"] = has(r"3\.91 and \+6\.87 percentage points") and has(r"16\.65 to \+17\.96 points") and has(r"finite-sample")

st = contract["stage_stratified_hidden_start_tipping"]
checks["stage_restricted_tipping_schema"] = stage_tipping.get("schema") == "azores.stage_stratified_hidden_start_tipping.v1"
checks["stage_restricted_tipping_candidates"] = stage_tipping["n_short_negative_candidates"] == st["n_short_negative_candidates"] == 100
checks["stage_restricted_unrestricted_k"] = stage_tipping["unrestricted_minimum_k"] == st["unrestricted_first_k"] == 11
checks["stage_restricted_all_stage_counts"] = sum(v["candidate_count"] for v in stage_tipping["stage"].values()) == 100
checks["stage_restricted_fiii_k16"] = stage_tipping["stage"]["FIII"]["first_k_with_nonpositive_heldout_condition_auc_gain"] == st["stage"]["FIII"]["first_nonpositive_k"] == 16
checks["stage_restricted_other_stage_null"] = all(stage_tipping["stage"][key]["first_k_with_nonpositive_heldout_condition_auc_gain"] is None for key in ("FIV","FV"))
checks["stage_restricted_ci_recomputed"] = all(
    abs(stage_tipping["stage"][key]["minimum_at_exactly_11_flips"]["minimum_delta_auc"] - st["stage"][key]["minimum_delta_at_11"]) < 1e-10
    for key in ("FIII","FIV","FV")
)
checks["stage_restricted_fiii_nonmonotonic"] = stage_tipping["stage"]["FIII"]["minimum_if_all_stage_candidates_flipped"]["minimum_delta_auc"] > 0.06
checks["stage_restricted_manuscript"] = has(r"16 of 70") and has(r"0\.0064") and has(r"0\.0622") and has(r"neither changing only FIV labels")



failed = [k for k,v in checks.items() if not v]
result = {
    "schema":"azores.manuscript_qc.v4",
    "manuscript":str(M),
    "contract":str(C),
    "status":"PASS" if not failed else "FAIL",
    "checks":checks,
    "failed":failed,
}
Path("manuscript/MANUSCRIPT_QC_V4.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,indent=2))
raise SystemExit(0 if not failed else 1)
