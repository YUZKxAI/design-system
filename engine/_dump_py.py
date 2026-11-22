#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dump the Python engine's output for a fixed matrix, for the JS parity test."""
import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import generate as g  # noqa: E402

SEEDS = ["#2455B4", "#E5484D", "#10B981", "#7C3AED", "#F5B800",
         "#FF0000", "#00FFFF", "#FFFF00", "#000080", "#808080", "#000000", "#FFFFFF"]
MOODS = sorted(g.MOODS)

out = {}
for s in SEEDS:
    for m in MOODS:
        res, notes = g.generate(s, m)
        key = "%s|%s" % (s.lower(), m)
        if res is None:
            out[key] = {"rejected": notes}
            continue
        out[key] = {
            "brand": res["brand"],
            "semantic": res["semantic"],
            "status": res["status"],
            "darkStatus": res["darkStatus"],
            "chart": res["chart"],
            "chartDark": res["chartDark"],
            "form": res["form"],
            "ok": res["ok"],
        }

json.dump(out, sys.stdout, ensure_ascii=False, indent=1, sort_keys=True)
