#!/usr/bin/env python3
"""Exhaustive network-free validation of random hidden-start AUC formula."""
from __future__ import annotations

import importlib.util
from itertools import combinations
from pathlib import Path

SOURCE=Path("analysis/47_observability_random_hidden_start_sensitivity.py")
spec=importlib.util.spec_from_file_location("random_hidden",SOURCE)
m=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(m)

# Deterministic two-stratum fixture, including fixed non-initiator.
rows=[]
for i,(project,y,base,plus,stage) in enumerate([
    ("A",1,.7,.5,"FIII"),("A",1,.1,.3,"FV"),
    ("A",0,.2,.35,"FIII"),("A",0,.5,.1,"FV"),
    ("B",1,.8,.7,"FIII"),("B",1,.3,.6,"FV"),
    ("B",0,.2,.4,"FV"),("B",0,.5,.3,"FIII"),
]):
    rows.append({"fish":f"f{i}","project":project,"stratum":project+"::2020",
                 "initiated":y,"stage":stage,
                 "score_base":base,"score_plus":plus,
                 "score_stage_only":float(stage=="FV"),
                 "score_stage_condition":plus})
eligible={r["fish"] for r in rows if r["initiated"] or r["fish"]=="f7"}
cells,num0,den0=m.P.build_cells(rows,eligible)
tab=m.candidate_table if False else None
# Small synthetic group bypasses full-panel candidate count assertion.
indices=[];impact=[];stages=[];tags=[]
for i,cell in enumerate(cells):
    for c in cell["candidates"]:
        tags.append(c["fish"]);indices.append(i);impact.append(c["row_impact"])
        stages.append(next(r["stage"] for r in rows if r["fish"]==c["fish"]))
import numpy as np
tab={"tags":tags,"index":np.asarray(indices,int),"impact":np.asarray(impact,float),"stages":stages}

for k in range(len(tags)+1):
    for subset in combinations(range(len(tags)),k):
        chosen=np.asarray(subset,dtype=int)
        fast,pairs=m.auc_after_flip(cells,num0,den0,tab,chosen)
        flips={tags[i] for i in chosen}
        rr=[{**r,"initiated":int(r["initiated"] or r["fish"] in flips)} for r in rows]
        direct=m.P.INC.summarize(m.P.INC.evaluate_groups(rr),False)
        assert abs(fast-direct["delta_auc_condition_above_stage_length_timing"])<1e-10,(k,subset,fast,direct)
        assert pairs==direct["n_positive_negative_pairs"]
for scenario in ["uniform","stage_FV_x3","adverse_disagreement_x3"]:
    weights=m.draw_weights(tab,scenario)
    assert np.all(weights>0)
    assert abs(np.sum(weights)-1)<1e-12
    sims=m.simulate(cells,num0,den0,tab,[0,1,2,len(tags)],[scenario],nrep=50,seed=13)[scenario]
    assert sims[0]["n_evaluated"]==1
    assert sims[-1]["n_evaluated"]==1
    assert all(0<=r["fraction_nonpositive"]<=1 for r in sims)
print("PASS exhaustive random-label formula and conditional assignment scenarios")
