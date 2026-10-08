#!/usr/bin/env python3
"""Receiver-event inventory for source noninitiation and short follow-up.

Real contact means a source event at a named physical receiver. Another fish
detected subsequently on that receiver proves activity only at THAT moment;
it does NOT prove continuous operation, that the focal fish remained in range,
or that the focal fish was actually capable of moving.
"""
from __future__ import annotations

import importlib.util
import json
from bisect import bisect_right
from collections import Counter, defaultdict
from datetime import timedelta
from pathlib import Path

import numpy as np

PARENT=Path("analysis/45_observability_selection_gate.py")
CONTRACT=Path("analysis/contracts/receiver_witness_observability_v1.json")
OUTPUT=Path("analysis/results/receiver_witness_observability.json")
WINDOWS=(1,7,30,90)


def load_parent():
    spec=importlib.util.spec_from_file_location("obs_source",PARENT)
    m=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


OBS=load_parent()
B=OBS.BASE


def physical_receiver(station:str,receiver:str) -> bool:
    station=str(station or "").strip().lower()
    receiver=str(receiver or "").strip().lower()
    return bool(station and receiver and
                receiver not in {"none","na","n/a","nan","null"} and
                not station.startswith("rel_") and
                not station.startswith("release"))


def summary(records:list[dict],name:str):
    stages=Counter(r["stage"] for r in records)
    with_contact=[r for r in records if r["n_real_rows"]>0]
    def med(values):
        values=[x for x in values if x is not None]
        return float(np.median(values)) if values else None
    return {
        "group":name,
        "n_fish":len(records),
        "n_fish_without_any_real_receiver_contact":len(records)-len(with_contact),
        "n_fish_with_real_receiver_contact":len(with_contact),
        "fraction_fish_with_real_receiver_contact":len(with_contact)/len(records) if records else None,
        "stage_counts":dict(sorted(stages.items())),
        "number_real_receiver_rows":{"total":sum(r["n_real_rows"] for r in records),
                                     "median":med([r["n_real_rows"] for r in records])},
        "unique_real_receivers_median":med([r["n_unique_receivers"] for r in records]),
        "last_real_receiver_day_since_release_median":med([r["days_last_real_since_release"] for r in with_contact]),
        "has_later_other_fish_detection_same_receiver":{
            str(k):{
                "n_positive":sum(bool(r["witness"].get(k)) for r in with_contact),
                "n_known_last_receiver":len(with_contact),
                "fraction_positive_given_real_contact":(
                    sum(bool(r["witness"].get(k)) for r in with_contact)/len(with_contact) if with_contact else None
                )
            } for k in WINDOWS
        },
    }


def witness_after(last_time,cutoff,tag,receiver_events):
    if last_time is None or not receiver_events or cutoff <= last_time:
        return {k:False for k in WINDOWS}
    times=[x[0] for x in receiver_events]
    j=bisect_right(times,last_time)
    witness={k:False for k in WINDOWS}
    for time,other in receiver_events[j:]:
        if time>cutoff:break
        if other==tag:continue
        delta=(time-last_time).total_seconds()/86400
        for days in WINDOWS:
            if 0 < delta <= days:
                witness[days]=True
        if all(witness.values()):break
    return witness


def main():
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    full=B.load()
    eligible,_=OBS.FIX.horizon_filter(full,90)
    eligible_tags={r["tag"] for r in eligible}
    focal={r["tag"]:r for r in full}
    assert len(full)==575
    short={r["tag"] for r in full if not r["initiated"] and r["tag"] not in eligible_tags}
    supported={r["tag"] for r in full if not r["initiated"] and r["tag"] in eligible_tags}
    started={r["tag"] for r in full if r["initiated"]}
    assert (len(short),len(supported),len(started))==(100,53,422)
    assert len(short|supported|started)==575

    per_fish=defaultdict(list)
    by_receiver=defaultdict(list)
    nonphysical_rows=0
    source_real_rows=0
    # Include physical-receiver records from all source study fish, even when
    # they do not satisfy the FIII/FIV/FV cohort, as external operation witnesses.
    for project,filename in B.FILES.items():
        for row in B.fetch(f"{B.RAW}/data/interim/migration/{filename}"):
            tag=(row.get("acoustic_tag_id") or "").strip()
            station=(row.get("station_name") or "").strip()
            receiver=(row.get("receiver_id") or "").strip()
            if not physical_receiver(station,receiver):
                nonphysical_rows+=1
                continue
            arrival=B.dt(row.get("arrival"))
            depart=B.dt(row.get("departure"))
            if arrival is None and depart is None:
                continue
            if arrival is None:arrival=depart
            if depart is None:depart=arrival
            last=max(arrival,depart)
            key=(project,station,receiver)
            by_receiver[key].append((arrival,tag))
            source_real_rows+=1
            if tag in focal and focal[tag]["project"]==project:
                per_fish[tag].append({"receiver":key,"arrival":arrival,"last":last})

    for key in by_receiver:
        by_receiver[key].sort(key=lambda x:x[0])

    records=[]
    for tag,r in focal.items():
        encounters=per_fish.get(tag,[])
        if encounters:
            last=max(encounters,key=lambda x:x["last"])
            last_time=last["last"]
            witness=witness_after(last_time,r["release"]+timedelta(days=90),tag,by_receiver[last["receiver"]])
            days_last_real=(last_time-r["release"]).total_seconds()/86400
        else:
            witness={k:False for k in WINDOWS}
            days_last_real=None
        records.append({
            "project":r["project"],
            "stage":r["stage"],
            "cohort":("source_initiator" if tag in started else
                      "short_followup_source_noninitiator" if tag in short else
                      "day90_supported_source_noninitiator"),
            "n_real_rows":len(encounters),
            "n_unique_receivers":len({x["receiver"] for x in encounters}),
            "days_last_real_since_release":days_last_real,
            "witness":witness,
        })

    cohorts=sorted({r["cohort"] for r in records})
    result={
        "schema":"azores.receiver_witness_observability.v1",
        "evidence_class":"post_hoc_source_receiver_event_inventory_for_observation_gate",
        "contract":str(CONTRACT),
        "source_commit":B.PINNED,
        "source":{
            "focal_fish":len(full),
            "physical_receiver_events_across_all_source_fish":source_real_rows,
            "nonphysical_virtual_or_missing_receiver_rows":nonphysical_rows,
            "receiver_station_keys":len(by_receiver),
            "has_receiver_deployment_and_recovery_times":False,
            "receiver_metadata_limit":"interim and raw deployments.csv list coordinates but no deploy/recovery dates for these six projects"
        },
        "cohorts":{c:summary([r for r in records if r["cohort"]==c],c) for c in cohorts},
        "by_project_short_followup":{
            p:summary([r for r in records if r["cohort"]=="short_followup_source_noninitiator" and r["project"]==p],p)
            for p in sorted(B.FILES)
        },
        "by_stage_short_followup":{
            stage:summary([r for r in records if r["cohort"]=="short_followup_source_noninitiator" and r["stage"]==stage],stage)
            for stage in sorted(B.STAGE)
        },
        "status":"RECEIVER_EVENT_EVIDENCE_INVENTORIED_NOT_RECEIVER_EFFORT_ESTIMATED",
        "interpretation_boundary":contract["checks"]
    }
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
