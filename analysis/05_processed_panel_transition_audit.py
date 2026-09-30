#!/usr/bin/env python3
"""Audit processed public eel-meta-analysis outputs for mobility-gating eligibility.

Uses the source study's own public migration classifications. It does NOT
reclassify migration from raw detections.

Goal: count eels tagged as yellow that later contain migration==TRUE records,
quantify pre/post classified track support, and audit WRS/water-body covariate
coverage for a future state x landscape analysis.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

FALSE = {"false","0","f","no","n",""}
TRUE = {"true","1","t","yes","y"}

PROJECT_MAP = {
    "2004_gudena":"2004_gudena",
    "2004_gudena".lower():"2004_gudena",
    "2011_loire":"2011_loire",
    "2011_warnow":"2011_warnow",
    "2013_stour":"2013_stour",
    "2014_frome":"2014_frome",
    "2014_nene":"2014_nene",
    "2017_fremur":"2017_fremur",
    "2019_grotenete":"2019_grotenete",
    "ptn-silver-eel-mondego":"mondego",
    "emmn":"emmn",
    "esgl":"esgl",
    "semp":"semp",
    "noordzeekanaal":"noordzeekanaal",
    "nedap_meuse":"nedap_meuse",
    "2012_leopoldkanaal":"2012_leopoldkanaal",
    "2013_albertkanaal":"2013_albertkanaal",
    "2015_phd_verhelst_eel":"2015_phd_verhelst_eel",
    "dak_markiezaatsmeer":"dak_markiezaatsmeer",
    "dak_superpolder":"dak_superpolder",
}


def norm_project(x: str) -> str:
    k = (x or "").strip().lower()
    return PROJECT_MAP.get(k, k)


def parse_bool(x: str | None):
    v=(x or "").strip().lower()
    if v in TRUE: return True
    if v in FALSE: return False
    return None


def parse_time(x: str | None):
    v=(x or "").strip()
    if not v: return None
    v=v.replace("Z","+00:00")
    for fmt in (None,"%Y-%m-%d %H:%M:%S","%Y-%m-%d","%d/%m/%Y %H:%M","%d/%m/%Y"):
        try:
            return datetime.fromisoformat(v) if fmt is None else datetime.strptime(v,fmt)
        except Exception:
            pass
    return None


def read_csv(path: Path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-repo", default="external/eel-meta-analysis")
    ap.add_argument("--out", default="analysis/results/processed_panel_transition_audit.json")
    args=ap.parse_args()
    root=Path(args.source_repo)
    meta_path=root/"data/interim/eel_meta_data.csv"
    wrs_path=root/"data/external/eels_wrs.csv"
    mig_dir=root/"data/interim/migration"
    if not (meta_path.exists() and wrs_path.exists() and mig_dir.exists()):
        raise SystemExit("required source-repo processed assets are missing")

    meta_rows=read_csv(meta_path)
    wrs_rows=read_csv(wrs_path)

    # Audit tag uniqueness before allowing tag-only fallback joins.
    meta_projects_by_tag=defaultdict(set)
    for r in meta_rows:
        meta_projects_by_tag[(r.get("acoustic_tag_id") or "").strip()].add(
            norm_project(r.get("animal_project_code") or "")
        )
    tag_collisions={k:sorted(v) for k,v in meta_projects_by_tag.items() if k and len(v)>1}

    meta={}
    for r in meta_rows:
        tag=(r.get("acoustic_tag_id") or "").strip()
        proj=norm_project(r.get("animal_project_code") or "")
        meta[(proj,tag)]=r

    wrs_by_key={}
    wrs_by_tag={}
    for r in wrs_rows:
        tag=(r.get("acoustic_tag_id") or "").strip()
        proj=norm_project(r.get("animal_project_code") or "")
        wrs_by_key[(proj,tag)]=r
        if tag:
            wrs_by_tag[tag]=r

    eels={}
    for p in sorted(mig_dir.glob("migration_*.csv")):
        rows=read_csv(p)
        for r in rows:
            tag=(r.get("acoustic_tag_id") or "").strip()
            proj=norm_project(r.get("animal_project_code") or "")
            if not tag:
                continue
            key=(proj,tag)
            d=eels.setdefault(key,{
                "project":proj,"tag":tag,"rows":0,"pre_rows":0,"post_rows":0,
                "first_time":None,"migration_start":None,"last_time":None,
                "source_file":p.name,
            })
            d["rows"]+=1
            when=parse_time(r.get("arrival"))
            if when is not None:
                if d["first_time"] is None or when<d["first_time"]: d["first_time"]=when
                if d["last_time"] is None or when>d["last_time"]: d["last_time"]=when
            mig=parse_bool(r.get("migration"))
            if mig and when is not None and (d["migration_start"] is None or when<d["migration_start"]):
                d["migration_start"]=when

    # second pass so rows before/after start are counted with final onset.
    for p in sorted(mig_dir.glob("migration_*.csv")):
        for r in read_csv(p):
            tag=(r.get("acoustic_tag_id") or "").strip()
            proj=norm_project(r.get("animal_project_code") or "")
            key=(proj,tag)
            if key not in eels: continue
            start=eels[key]["migration_start"]
            when=parse_time(r.get("arrival"))
            if start is None or when is None:
                continue
            if when < start:
                eels[key]["pre_rows"]+=1
            else:
                eels[key]["post_rows"]+=1

    joined=[]
    meta_miss=0
    wrs_miss=0
    for key,d in eels.items():
        m=meta.get(key)
        if m is None and not tag_collisions.get(d["tag"]):
            # some source project recodings differ; unique tag fallback is auditable
            candidates=[r for (p,t),r in meta.items() if t==d["tag"]]
            m=candidates[0] if len(candidates)==1 else None
        if m is None:
            meta_miss+=1
        w=wrs_by_key.get(key)
        if w is None and d["tag"] in wrs_by_tag and not tag_collisions.get(d["tag"]):
            w=wrs_by_tag[d["tag"]]
        if w is None:
            wrs_miss+=1
        stage=((m or {}).get("life_stage") or "").strip().lower()
        first=d["first_time"]; start=d["migration_start"]; last=d["last_time"]
        joined.append({
            "project":d["project"],"tag":d["tag"],"life_stage_at_tagging":stage,
            "has_classified_migration": start is not None,
            "rows":d["rows"],"pre_rows":d["pre_rows"],"post_rows":d["post_rows"],
            "pre_days": ((start-first).total_seconds()/86400 if start and first else None),
            "post_days": ((last-start).total_seconds()/86400 if start and last else None),
            "barrier_number": (w or {}).get("barrier_number"),
            "wrs_impact_score": (w or {}).get("wrs_impact_score"),
            "water_body_class": (w or {}).get("water_body_class"),
        })

    stage_counts=defaultdict(int)
    project_yellow_migrants=defaultdict(int)
    water_classes=set()
    wrs_values=set()
    yellow_migrants=[]
    for r in joined:
        stage_counts[r["life_stage_at_tagging"] or "missing"]+=1
        if r["water_body_class"] not in (None,""): water_classes.add(str(r["water_body_class"]))
        if r["wrs_impact_score"] not in (None,""): wrs_values.add(str(r["wrs_impact_score"]))
        if r["life_stage_at_tagging"]=="yellow" and r["has_classified_migration"]:
            yellow_migrants.append(r)
            project_yellow_migrants[r["project"]]+=1

    support_thresholds={}
    for pre_min,post_min in [(1,1),(3,3),(5,5),(10,10)]:
        support_thresholds[f"pre{pre_min}_post{post_min}"]=sum(
            r["pre_rows"]>=pre_min and r["post_rows"]>=post_min
            for r in yellow_migrants
        )

    projects_with_yellow_switch=[p for p,n in project_yellow_migrants.items() if n>0]
    status = (
        "GO_STATE_LANDSCAPE_AUDIT"
        if yellow_migrants and len(projects_with_yellow_switch)>=2 and len(water_classes)>=2
        else "LIMITED"
    )

    result={
        "schema":"azores.processed_eel_panel_transition_audit.v1",
        "status":status,
        "source_repository":"PieterjanVerhelst/eel-meta-analysis",
        "migration_classification":"source study processed migration flags; not recomputed here",
        "total_migration_panel_eels":len(joined),
        "metadata_join_missing":meta_miss,
        "wrs_join_missing":wrs_miss,
        "tag_collisions_across_projects":tag_collisions,
        "life_stage_counts":dict(sorted(stage_counts.items())),
        "yellow_at_tagging_with_classified_migration":len(yellow_migrants),
        "yellow_switch_projects":dict(sorted(project_yellow_migrants.items())),
        "pre_post_support_counts":support_thresholds,
        "water_body_classes":sorted(water_classes),
        "wrs_impact_values_count":len(wrs_values),
        "yellow_migrant_examples":yellow_migrants[:30],
        "claim_boundary":(
            "A yellow-at-tagging eel with later migration==TRUE supports a within-individual "
            "movement-state transition contrast. The new hypothesis is the interaction with "
            "landscape opportunity, not the existence of silver-eel migration itself."
        )
    }
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,default=str),encoding="utf-8")
    print(json.dumps(result,indent=2,default=str))


if __name__=="__main__":
    main()
