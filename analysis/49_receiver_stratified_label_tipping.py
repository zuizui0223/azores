#!/usr/bin/env python3
"""Exact hypothetical hidden-start label bounds stratified by receiver evidence.

Uses 46's proven exact fractional-program dynamic program, but constrains the
set of source noninitiators that may be hypothetically relabeled based on
observed physical-receiver contact / another-fish-afterward witnesses.
"""
from __future__ import annotations

import importlib.util
import json
from collections import defaultdict
from datetime import timedelta
from pathlib import Path

PARENT=Path("analysis/46_observability_label_ambiguity_tipping.py")
WITNESS=Path("analysis/48_receiver_witness_observability.py")
CONTRACT=Path("analysis/contracts/receiver_stratified_hidden_start_tipping_v1.json")
PREV=Path("results/observability_label_ambiguity_tipping_v1.json")
RECEIVER_RESULT=Path("results/receiver_witness_observability_v1.json")
OUTPUT=Path("analysis/results/receiver_stratified_label_tipping.json")


def load(path,name):
    sp=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(sp)
    assert sp.loader is not None
    sp.loader.exec_module(module)
    return module


EXACT=load(PARENT,"exact_parent")
W=load(WITNESS,"receiver_witness_parent")
B=EXACT.BASE


def observation_groups(full:list[dict],candidate_tags:set[str]):
    by_tag=defaultdict(list)
    by_receiver=defaultdict(list)
    for project,filename in B.FILES.items():
        for row in B.fetch(f"{B.RAW}/data/interim/migration/{filename}"):
            station=(row.get("station_name") or "").strip()
            rec=(row.get("receiver_id") or "").strip()
            if not W.physical_receiver(station,rec):
                continue
            arrived=B.dt(row.get("arrival"))
            departed=B.dt(row.get("departure"))
            if arrived is None and departed is None:
                continue
            if arrived is None:arrived=departed
            if departed is None:departed=arrived
            tag=(row.get("acoustic_tag_id") or "").strip()
            key=(project,station,rec)
            by_receiver[key].append((arrived,tag))
            if tag in candidate_tags:
                by_tag[tag].append((key,max(arrived,departed)))
    for events in by_receiver.values():
        events.sort(key=lambda x:x[0])
    meta={r["tag"]:r for r in full}
    groups={
        "zero_real_contact":set(),"any_real_contact":set(),
        "later_same_receiver_90d":set(),"no_later_same_receiver_90d":set(),
        "later_same_receiver_1d":set(),"no_later_same_receiver_1d":set(),
    }
    for tag in sorted(candidate_tags):
        rows=by_tag.get(tag,[])
        if not rows:
            groups["zero_real_contact"].add(tag)
            groups["no_later_same_receiver_90d"].add(tag)
            groups["no_later_same_receiver_1d"].add(tag)
            continue
        groups["any_real_contact"].add(tag)
        receiver,last=max(rows,key=lambda x:x[1])
        info=meta[tag]
        w=W.witness_after(last,info["release"]+timedelta(days=90),tag,by_receiver[receiver])
        if w[90]:
            groups["later_same_receiver_90d"].add(tag)
        else:
            groups["no_later_same_receiver_90d"].add(tag)
        if w[1]:
            groups["later_same_receiver_1d"].add(tag)
        else:
            groups["no_later_same_receiver_1d"].add(tag)
    assert len(groups["zero_real_contact"]) + len(groups["any_real_contact"]) == len(candidate_tags)
    assert len(groups["later_same_receiver_90d"]) + len(groups["no_later_same_receiver_90d"]) == len(candidate_tags)
    assert len(groups["later_same_receiver_1d"]) + len(groups["no_later_same_receiver_1d"]) == len(candidate_tags)
    return groups


def filtered_cells(cells:list[dict],eligible:set[str]):
    return [{**c,"candidates":[q for q in c["candidates"] if q["fish"] in eligible]}
            for c in cells]


def exact_subgroup(cells:list[dict],num0:float,den0:int,k11:int=11):
    n=sum(len(c["candidates"]) for c in cells)
    tipping=EXACT.first_tipping(cells,num0,den0,n) if n else None
    res={
        "candidate_count":n,
        "first_k_with_nonpositive_gain":tipping,
        "k11_admissible":n>=k11,
        "at_k11":None,
        "at_first_tipping":None,
    }
    if n>=k11:
        r=EXACT.envelope(cells,num0,den0,k11,+1)
        res["at_k11"]={"minimum_auc_gain":r["ratio"],
                       "n_comparison_pairs_after_flip":r["n_informative_pairs_after_flip"],
                       "hypothetical_flips_by_project":r["flips_by_project"]}
    if tipping is not None:
        r=EXACT.envelope(cells,num0,den0,tipping,+1)
        res["at_first_tipping"]={"minimum_auc_gain":r["ratio"],
                                  "n_comparison_pairs_after_flip":r["n_informative_pairs_after_flip"],
                                  "hypothetical_flips_by_project":r["flips_by_project"]}
    return res


def main():
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    prev=json.loads(PREV.read_text(encoding="utf-8"))
    documented=json.loads(RECEIVER_RESULT.read_text(encoding="utf-8"))
    full=B.load()
    eligible,_=EXACT.FIX.horizon_filter(full,90)
    eligible_tags={r["tag"] for r in eligible}
    candidates={r["tag"] for r in full if not r["initiated"] and r["tag"] not in eligible_tags}
    assert len(full)==575 and len(candidates)==100
    scored,_=EXACT.PAIRED.train_scores_once(full)
    cells,num0,den0=EXACT.build_cells(scored,eligible_tags)
    assert len(candidates)==sum(len(c["candidates"]) for c in cells)==100
    assert den0==6914 and abs(num0/den0-prev["frozen_original_auc_gain"])<1e-10
    groups=observation_groups(full,candidates)
    assert len(groups["zero_real_contact"])==documented["cohorts"]["short_followup_source_noninitiator"]["n_fish_without_any_real_receiver_contact"]
    assert len(groups["any_real_contact"])==documented["cohorts"]["short_followup_source_noninitiator"]["n_fish_with_real_receiver_contact"]
    assert len(groups["later_same_receiver_90d"])==documented["cohorts"]["short_followup_source_noninitiator"]["has_later_other_fish_detection_same_receiver"]["90"]["n_positive"]
    assert len(groups["later_same_receiver_1d"])==documented["cohorts"]["short_followup_source_noninitiator"]["has_later_other_fish_detection_same_receiver"]["1"]["n_positive"]
    results={key:exact_subgroup(filtered_cells(cells,tags),num0,den0) for key,tags in sorted(groups.items())}
    original_tags=set(prev["tipping_witness"]["witness_tags"])
    assert len(original_tags)==prev["first_k_with_nonpositive_exact_minimum"]==11
    original_composition={
        k:len(tags & original_tags) for k,tags in groups.items()
    }
    result={
        "schema":"azores.receiver_stratified_label_tipping.v1",
        "evidence_class":contract["evidence_class"],
        "contract":str(CONTRACT),
        "source_tipping_result":str(PREV),
        "source_receiver_inventory":str(RECEIVER_RESULT),
        "source_fish":575,
        "source_ambiguous_noninitiators":100,
        "frozen_original_auc_increment":num0/den0,
        "unrestricted_first_nonpositive_k":prev["first_k_with_nonpositive_exact_minimum"],
        "observed_receiver_evidence_groups":results,
        "original_adversarial_11_fish_group_composition":original_composition,
        "status":"EXACT_RECEIVER_CONSTRAINED_LABEL_SENSITIVITY",
        "interpretation_boundary":contract["interpretation_boundary"],
    }
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
