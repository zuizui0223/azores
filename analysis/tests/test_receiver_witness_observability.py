#!/usr/bin/env python3
"""No-network receiver operation-witness logic checks."""
from __future__ import annotations

import importlib.util
from datetime import datetime,timedelta
from pathlib import Path

p=Path("analysis/48_receiver_witness_observability.py")
sp=importlib.util.spec_from_file_location("receiver_test",p)
m=importlib.util.module_from_spec(sp)
assert sp.loader is not None
sp.loader.exec_module(m)

assert not m.physical_receiver("rel_warnow","none")
assert not m.physical_receiver("rel_esgl","VR1")
assert not m.physical_receiver("W3","none")
assert not m.physical_receiver("W3","NA")
assert m.physical_receiver("W3","VR2W-112219")

t=datetime(2020,1,1,12,0)
other=[
 (t-timedelta(days=1),"eel_A"),
 (t,"eel_A"),
 (t+timedelta(days=2),"eel_A"),
 (t+timedelta(days=3),"eel_B"),
 (t+timedelta(days=10),"eel_C"),
 (t+timedelta(days=120),"eel_D"),
]
w=m.witness_after(t,t+timedelta(days=90),"eel_A",other)
assert w=={1:False,7:True,30:True,90:True},w
w=m.witness_after(t,t+timedelta(days=2),"eel_A",other)
assert w=={1:False,7:False,30:False,90:False},w
w=m.witness_after(t,t+timedelta(days=90),"eel_B",[])
assert w=={1:False,7:False,30:False,90:False}
print("PASS receiver virtual-station exclusion and strictly later independent-fish witnesses")
