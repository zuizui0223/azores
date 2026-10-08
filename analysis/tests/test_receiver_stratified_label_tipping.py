#!/usr/bin/env python3
"""Exhaustive synthetic equivalence for candidate-constrained exact tipping."""
from __future__ import annotations

import importlib.util
from itertools import combinations
from pathlib import Path

path=Path("analysis/49_receiver_stratified_label_tipping.py")
sp=importlib.util.spec_from_file_location("constrained_tipping",path)
m=importlib.util.module_from_spec(sp)
assert sp.loader is not None
sp.loader.exec_module(m)

rows=[]
for i,(p,y,b,z) in enumerate([
 ("A",1,.7,.6),("A",1,.1,.5),
 ("A",0,.2,.4),("A",0,.4,.1),
 ("B",1,.7,.7),("B",1,.2,.8),
 ("B",0,.1,.4),("B",0,.5,.2),
]):
 rows.append({"fish":f"eel_{i}","project":p,"stratum":p+"::2020",
              "initiated":y,"stage":"FIII","score_base":b,"score_plus":z,
              "score_stage_only":0.0,"score_stage_condition":z})
eligible={"eel_0","eel_1","eel_4","eel_5","eel_7"}
cells,n0,d0=m.EXACT.build_cells(rows,eligible)
candidates={r["fish"] for r in rows if not r["initiated"] and r["fish"] not in eligible}
assert candidates=={"eel_2","eel_3","eel_6"}
for permitted in [{"eel_2"},{"eel_3","eel_6"},candidates]:
 filtered=m.filtered_cells(cells,permitted)
 assert sum(len(c["candidates"]) for c in filtered)==len(permitted)
 for k in range(len(permitted)+1):
  estimated=m.EXACT.envelope(filtered,n0,d0,k,+1)["ratio"]
  direct=[]
  for subset in combinations(sorted(permitted),k):
   rr=[{**r,"initiated":int(r["initiated"] or r["fish"] in subset)} for r in rows]
   direct.append(m.EXACT.INC.summarize(m.EXACT.INC.evaluate_groups(rr),False)["delta_auc_condition_above_stage_length_timing"])
  assert abs(estimated-min(direct))<1e-10,(permitted,k,estimated,min(direct))
 print("PASS subgroup constrained exact tipping",len(permitted))
