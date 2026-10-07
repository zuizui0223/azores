#!/usr/bin/env python3
"""Fetch only the small schema/source files from Dutch DANS archive.

The 41 MB raw detection file (datafile 71836) is intentionally excluded.
Its successful public download and header have already been independently
verified by the full archive audit. This helper accelerates schema/provenance
inspection without repeatedly transferring the raw detections.
"""
from __future__ import annotations
import argparse, hashlib, json, urllib.request
from pathlib import Path

SERVER="https://lifesciences.datastations.nl"
FILES={
  71838:"biometrics_cl.tab",
  71844:"biometrics_ez.tab",
  71841:"calculate_distance_validity.R",
  71834:"codebook.tab",
  71845:"durif_21.tab",
  71848:"figure3_plot.R",
  71837:"mpo_model_cl.R",
  71839:"mpo_model_ez.R",
  71846:"passage_cl.tab",
  71843:"passage_ez.tab",
  71840:"passage_glmm_cl.R",
  71835:"passage_glmm_ez.R",
  71847:"README.txt",
  71842:"station_info.tab",
}

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--out-dir",default="external/dutch_dans_schema")
 ap.add_argument("--manifest",default="analysis/results/dutch_dans_schema_fetch.json")
 a=ap.parse_args()
 root=Path(a.out_dir);root.mkdir(parents=True,exist_ok=True)
 rec=[]
 for fid,name in FILES.items():
  url=f"{SERVER}/api/access/datafile/{fid}?format=original"
  req=urllib.request.Request(url,headers={"User-Agent":"azores-dutch-schema/1.0"})
  with urllib.request.urlopen(req,timeout=180) as r:data=r.read()
  p=root/name;p.write_bytes(data)
  rec.append({"datafile_id":fid,"label":name,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"path":str(p)})
 out={"schema":"azores.dutch_dans_schema_fetch.v1","excluded_raw_detection_datafile":71836,
      "files":rec,"n":len(rec),"status":"PASS_SMALL_SCHEMA_FILES_FETCHED"}
 p=Path(a.manifest);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2))
 print(json.dumps(out,indent=2))

if __name__=="__main__":main()
