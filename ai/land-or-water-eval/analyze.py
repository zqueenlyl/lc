#!/usr/bin/env python3
"""Error breakdown for a cached Land-or-Water prediction."""

import json
import os
import sys

import numpy as np

from lowe.grid import build_grid, grid_points
from lowe.truth import LandTruth

HERE = os.path.dirname(os.path.abspath(__file__))
SHP = os.path.join(HERE, "data", "ne_50m_land.shp")


def load_intervals(path):
    with open(path) as f:
        data = json.load(f)
    return {float(k): v for k, v in data["grid"].items()}


def predict(pts, intervals):
    out = []
    for lat, lon in pts:
        land = any(min(a, b) <= lon <= max(a, b) for a, b in intervals.get(round(lat, 6), []))
        out.append(land)
    return np.asarray(out, dtype=bool)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "predictions", "hy4.json")
    step = 4.0
    lats, lons = build_grid(step)
    pts = grid_points(lats, lons)
    truth = LandTruth(SHP).is_land(pts)
    pred = predict(pts, load_intervals(path))

    lat_arr = np.asarray([p[0] for p in pts])
    lon_arr = np.asarray([p[1] for p in pts])
    wrong = pred != truth

    print(f"total {len(pts)}  accuracy {(~wrong).mean() * 100:.2f}%")
    print(f"errors: {wrong.sum()}  (predicted land but water: {(pred & ~truth).sum()},"
          f" predicted water but land: {(~pred & truth).sum()})")
    print()
    print("accuracy by 20-degree latitude band")
    for lo in range(80, -100, -20):
        sel = (lat_arr <= lo) & (lat_arr > lo - 20)
        if sel.sum():
            print(f"  {lo:>4} .. {lo - 20:>4}   n={sel.sum():>4}  acc={(~wrong[sel]).mean() * 100:6.1f}%"
                  f"  truth-land={truth[sel].mean() * 100:5.1f}%  pred-land={pred[sel].mean() * 100:5.1f}%")

    print()
    print("largest error clusters (4x4 deg cells, grouped)")
    cells = {}
    for (la, lo), w, tt, pp in zip(pts, wrong, truth, pred):
        if not w:
            continue
        key = (int(la // 12) * 12, int(lo // 12) * 12)
        c = cells.setdefault(key, {"n": 0, "over": 0, "under": 0})
        c["n"] += 1
        if pp and not tt:
            c["over"] += 1
        else:
            c["under"] += 1
    for (la, lo), c in sorted(cells.items(), key=lambda kv: -kv[1]["n"])[:15]:
        kind = "over-land" if c["over"] >= c["under"] else "under-land"
        print(f"  lat {la:>4}..{la + 12:>4}  lon {lo:>4}..{lo + 12:>4}   {c['n']:>3} errs"
              f"  ({c['over']} over / {c['under']} under)  {kind}")


if __name__ == "__main__":
    main()
