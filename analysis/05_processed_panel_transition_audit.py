#!/usr/bin/env python3
"""Audit source-study processed eel tracks for state-dependent mobility gating.

Uses the public source repository's migration flags unchanged. Initial
physiological stage is grouped from Durif-style labels:
  growth/resident: I, FI, FII
  premigrant: FIII
  morphologically migratory: FIV, FV, MII, generic "silver"

The target is not to rediscover silver migration. It is to identify individuals
initially in growth/premigrant states that later enter the source study's
movement-defined migration state, and whether that contrast spans different
landscape opportunity classes.
"""
from __future__ import annotations
import argparse,csv,json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

TRUE={"true","1","t","yes","y"}
STAGE_GROUP={
    "i":"growth","fi":"growth","fii":"growth",
    "fiii":"premigrant",
    "fiv":"morph_migrant","fv":"morph_migrant","mii":"morph_migrant",
    "silver":"morph_migrant",
    "na":"unknown","":"unknown",
}

def read(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def norm(x):return (x or "").strip().lower()
def pb(x):return norm(x) in TRUE
def pt(x):
    v=(x or "").strip().replace("Z","+00:00")
    if not v:return None
    for fmt in (None,"%Y-%m-%d %H:%M:%S","%Y-%m-%d","%d/%m/%Y %H:%M","%d/%m/%Y"):
        try:return datetime.fromisoformat(v) if fmt is None else datetime.strptime(v,fmt)
        except:pass
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-repo",default="external/eel-meta-analysis")
    ap.add_argument("--out",default="analysis/results/processed_panel_transition_audit.json")
    args=ap.parse_args()
    root=Path(args.source_repo)
    meta_rows=read(root/"data/interim/eel_meta_data.csv")
    wrs_rows=read(root/"data/external/eels_wrs.csv")

    meta_by_tag=defaultdict(list);wrs_by_tag=defaultdict(list)
    for r in meta_rows:
        tag=(r.get("acoustic_tag_id") or "").strip()
        if tag:meta_by_tag[tag].append(r)
    for r in wrs_rows:
        tag=(r.get("acoustic_tag_id") or "").strip()
        if tag:wrs_by_tag[tag].append(r)

    tracks=defaultdict(list);project_by_tag=defaultdict(set)
    for p in sorted((root/"data/interim/migration").glob("migration_*.csv")):
        for r in read(p):
            tag=(r.get("acoustic_tag_id") or "").strip()
            if not tag:continue
            tracks[tag].append(r);project_by_tag[tag].add(norm(r.get("animal_project_code")))

    rows=[];metadata_ambiguous=0;wrs_ambiguous=0
    for tag,tr in tracks.items():
        ms=meta_by_tag.get(tag,[])
        if len(ms)!=1:
            metadata_ambiguous+=1;continue
        m=ms[0];stage_raw=norm(m.get("life_stage"));group=STAGE_GROUP.get(stage_raw,"other")
        tr=sorted(tr,key=lambda r:pt(r.get("arrival")) or datetime.max)
        mig=[i for i,r in enumerate(tr) if pb(r.get("migration"))]
        onset_i=min(mig) if mig else None
        onset=pt(tr[onset_i].get("arrival")) if onset_i is not None else None
        first=pt(tr[0].get("arrival")) if tr else None;last=pt(tr[-1].get("arrival")) if tr else None
        pre_rows=onset_i if onset_i is not None else 0;post_rows=(len(tr)-onset_i) if onset_i is not None else 0
        ws=wrs_by_tag.get(tag,[]);w=ws[0] if len(ws)==1 else {}
        if len(ws)>1:wrs_ambiguous+=1
        rows.append({
            "tag":tag,"source_projects":sorted(project_by_tag[tag]),
            "life_stage_raw":stage_raw,"stage_group":group,
            "has_behavioral_migration":onset_i is not None,
            "pre_rows":pre_rows,"post_rows":post_rows,
            "pre_days":((onset-first).total_seconds()/86400 if onset and first else None),
            "post_days":((last-onset).total_seconds()/86400 if onset and last else None),
            "barrier_number":w.get("barrier_number"),"wrs_impact_score":w.get("wrs_impact_score"),
            "water_body_class":w.get("water_body_class"),
        })

    raw_counts=defaultdict(int);group_counts=defaultdict(int);transition_counts=defaultdict(int);projects=defaultdict(int);eligible=[]
    for r in rows:
        raw_counts[r["life_stage_raw"] or "missing"]+=1;group_counts[r["stage_group"]]+=1
        if r["has_behavioral_migration"]:transition_counts[r["stage_group"]]+=1
        if r["stage_group"] in {"growth","premigrant"} and r["has_behavioral_migration"]:
            eligible.append(r)
            for p in r["source_projects"]:projects[p]+=1

    support={}
    for a,b in [(1,1),(3,3),(5,5),(10,10)]:
        support[f"pre{a}_post{b}"]=sum(r["pre_rows"]>=a and r["post_rows"]>=b for r in eligible)

    classes=sorted({str(r["water_body_class"]) for r in eligible if r["water_body_class"] not in (None,"","NA")})
    wrs_vals=sorted({str(r["wrs_impact_score"]) for r in eligible if r["wrs_impact_score"] not in (None,"")})
    status="GO_STATE_LANDSCAPE_AUDIT" if eligible and len(projects)>=2 and (len(classes)>=2 or len(wrs_vals)>=2) else "LIMITED"

    result={
      "schema":"azores.processed_eel_panel_transition_audit.v2","status":status,
      "stage_definition":{"growth":["I","FI","FII"],"premigrant":["FIII"],"morph_migrant":["FIV","FV","MII","silver"],"basis":"Durif-style silvering stages; movement-defined migration remains the source study's separate classifier"},
      "source_repository":"PieterjanVerhelst/eel-meta-analysis","total_track_tags":len(rows),
      "metadata_ambiguous_or_missing":metadata_ambiguous,"wrs_ambiguous":wrs_ambiguous,
      "life_stage_raw_counts":dict(sorted(raw_counts.items())),"stage_group_counts":dict(sorted(group_counts.items())),
      "behavioral_migration_by_initial_stage_group":dict(sorted(transition_counts.items())),
      "growth_or_premigrant_to_behavioral_migration":len(eligible),"transition_projects":dict(sorted(projects.items())),
      "pre_post_support_counts":support,"eligible_water_body_classes":classes,"eligible_wrs_impact_values_count":len(wrs_vals),
      "eligible_examples":eligible[:40],
      "claim_boundary":"The transition is from physiological state at tagging to later movement-defined migration. It is not a repeated physiological measurement. The novel test is whether landscape opportunity modifies timing/magnitude of movement expression."
    }
    out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,default=str),encoding="utf-8");print(json.dumps(result,indent=2,default=str))

if __name__=="__main__":main()
