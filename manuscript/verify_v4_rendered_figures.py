#!/usr/bin/env python3
"""Fail-closed source-numeric integrity checks for the four V4 manuscript SVGs.

This checks numerical identity and basic XML parsing, not aesthetic rendering,
author sign-off, references, journal formatting or biological causal validity.
"""
from __future__ import annotations

import json
import math
import pathlib
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manuscript/FIGURE_DATA_CONTRACT_V4.json"
FIG_DIR = ROOT / "manuscript/rendered_figures_v4"
NS = {"s": "http://www.w3.org/2000/svg"}


def equal(a, b, label):
    if isinstance(a, float) or isinstance(b, float):
        if not math.isclose(float(a), float(b), rel_tol=1e-11, abs_tol=1e-12):
            raise ValueError(f"{label}: {a} vs {b}")
    elif a != b:
        raise ValueError(f"{label}: {a} vs {b}")


def elements(name, selector):
    root = ET.parse(FIG_DIR / name).getroot()
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        raise ValueError(name + ": not SVG")
    return root.findall(".//s:g[@data-" + selector + "]", NS)


def main():
    src = json.loads(SOURCE.read_text(encoding="utf-8"))["main_figures"]
    expected = [
        ("Activation classification", src["figure1"]["multivariate_activation_n"]),
        ("Behavioral onset", src["figure1"]["onset_n"]),
        ("Whole-route speed", src["figure1"]["whole_route_speed_n"]),
        ("Inter-station transit", src["figure1"]["segment_speed_n"]),
    ]
    n = elements("Figure1.svg", "endpoint")
    equal(len(n), 4, "figure1 endpoint rows")
    for g, (lab, count) in zip(n, expected):
        equal(g.get("data-endpoint"), lab, "figure1 endpoint")
        equal(int(g.get("data-n")), count, "figure1 count")
    f = src["figure2"]
    stages = elements("Figure2.svg", "stage")
    equal(len(stages), len(f["activation_by_stage"]), "figure2 stage rows")
    for g, row in zip(stages, f["activation_by_stage"]):
        for k, v in [("stage", row["stage"]), ("count", row["initiated"]), ("n", row["tracked"]), ("rate", row["rate"])]:
            equal(g.get("data-" + k) if k == "stage" else float(g.get("data-" + k)), v, "figure2 stage " + k)
    fits = elements("Figure2.svg", "term")
    equal(len(fits), len(f["multivariate_activation"]), "figure2 fitted effects")
    for g, row in zip(fits, f["multivariate_activation"]):
        equal(g.get("data-term"), row["term"], "figure2 term")
        for k, v in [("estimate", row["estimate"]), ("lo", row["lo"]), ("hi", row["hi"])]:
            equal(float(g.get("data-" + k)), v, "figure2 " + k)
    rows = elements("Figure3.svg", "phase")
    equal(len(rows), len(src["figure3"]["entry_state_transfer"]), "figure3 phase count")
    for g, row in zip(rows, src["figure3"]["entry_state_transfer"]):
        equal(g.get("data-phase"), row["phase"], "figure3 phase label")
        for k in ("estimate", "lo", "hi"):
            equal(float(g.get("data-" + k)), row[k], "figure3 " + k)
    waiting = elements("Figure4.svg", "barrier")
    equal(len(waiting), 4, "figure4 waiting rows")
    for g, row in zip(waiting, src["figure4"]["waiting_associations"]):
        for k, v in [("barrier", row["barrier"]), ("response", row["response"]), ("r", row["r"]), ("p", row["p_permutation"]), ("n", row["n"])]:
            equal(g.get("data-" + k) if k in ("barrier", "response") else float(g.get("data-" + k)), v, "figure4 " + k)
    text4 = (FIG_DIR / "Figure4.svg").read_text(encoding="utf-8")
    cl = src["figure4"]["matched_choice_CL"]
    if f"{abs(cl['beta_condition_x_duration']):.3f}" not in text4 or f"{cl['p_permutation']:.3f}" not in text4:
        raise ValueError("Figure4 matched CL beta or permutation p not displayed")
    for path in FIG_DIR.glob("Figure*.svg"):
        t = path.read_text(encoding="utf-8")
        if "not " not in t.lower() and "source" not in t.lower():
            raise ValueError(path.name + ": missing scope annotation")
    print(json.dumps({
        "status": "PASS_V4_FIGURE_SOURCE_NUMERIC_INTEGRITY",
        "source": str(SOURCE.relative_to(ROOT)),
        "figures": [f"manuscript/rendered_figures_v4/Figure{i}.svg" for i in range(1, 5)],
        "audited_numeric_groups": 4 + 3 + 2 + 4 + 4,
        "scope": "Source numeric identity and SVG XML parsing only; not visual or final-author review."
    }, indent=2))


if __name__ == "__main__":
    main()
