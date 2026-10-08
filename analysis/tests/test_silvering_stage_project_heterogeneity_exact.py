#!/usr/bin/env python3
"""No-network exact conditional stage heterogeneity unit tests."""
import importlib.util
from pathlib import Path

SOURCE=Path("analysis/53_silvering_stage_project_heterogeneity_exact.py")
spec=importlib.util.spec_from_file_location("stage_heterogeneity_exact",SOURCE)
m=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(m)

# Near-identical project stage tables are maximally compatible with shared odds.
equal=[
    m.Block("A",10,5,10,5),
    m.Block("B",10,5,10,5),
]
k=[5,5]
theta=m.fit_common(equal,k)
assert abs(theta)<1e-8
assert abs(m.deviance(equal,k,theta))<1e-8
ex=m.exact_conditional(equal,k,theta)
assert ex["admissible_joint_vectors"]==11
assert abs(ex["exact_conditional_p"]-1)<1e-10

# Same pooled stage order, opposite project-specific directions. Zero cells
# must not crash the likelihood supremum computation or the exact test.
reverse=[
    m.Block("A",10,0,10,10),
    m.Block("B",10,10,10,0),
]
y=[10,0]
th=m.fit_common(reverse,y)
assert abs(th)<1e-8
lr=m.deviance(reverse,y,th)
assert lr>10
rv=m.exact_conditional(reverse,y,th)
assert rv["admissible_joint_vectors"]==11
assert 0<rv["exact_conditional_p"]<.02

# Fix all project margins + grand FV successes. The common odds nuisance
# must cancel exactly: changing theta must not change exact conditional p.
for new_th in (-2.0,0.0,1.8):
    alt=m.exact_conditional(reverse,y,new_th)
    assert abs(alt["exact_conditional_p"]-rv["exact_conditional_p"])<1e-10

# Parametric bootstrap uses the same LR and adds one to numerator/denominator.
b=m.parametric_bootstrap(reverse,y,th,100,20261008)
assert b["replicates"]==100
assert b["observed_lr"]==lr
assert 1/101<=b["p_plus_one"]<=1

# Input support conservation for current frozen real counts.
source=m.source_blocks()
assert len(source)==6
assert sum(b.n0 for b in source)==261
assert sum(b.n1 for b in source)==246
assert sum(b.y0 for b in source)==154
assert sum(b.y1 for b in source)==215
print("PASS synthetic exact conditional heterogeneity and cohort checks")
