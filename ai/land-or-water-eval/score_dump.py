#!/usr/bin/env python3
"""Score a pasted model reply (Path B manual fallback for run_all_models.py).

In a live WorkBuddy session the CLI/gateway cannot drive other models (see
run_all_models.py docstring). So: switch model in the picker, send each one the
grid prompt from run_all_models.PROMPT, paste the reply into
predictions/runs/cli_<model-id>.txt, then run this to score and rebuild the
leaderboard:

  python score_dump.py                 # score every cli_*.txt dump
  python score_dump.py --id hy3-ioa    # score one dump
"""

import argparse
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lowe.grid import build_grid
from lowe.probe import parse_answers
from lowe.report import render_leaderboard, score
from lowe.truth import LandTruth
from run_all_models import MODELS, PROMPT, STEP, parse_grid

HERE = os.path.dirname(os.path.abspath(__file__))
SHP = os.path.join(HERE, "data", "ne_50m_land.shp")
DUMPS = os.path.join(HERE, "predictions", "runs")
LABELS = dict(MODELS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", help="score only this model id")
    ap.add_argument("--out", default=os.path.join(HERE, "outputs"))
    args = ap.parse_args()

    lats, lons = build_grid(STEP)
    pts = [(la, lo) for la in lats for lo in lons]
    truth = LandTruth(SHP).is_land(pts)

    patterns = [os.path.join(DUMPS, f"cli_{args.id}.txt")] if args.id \
        else sorted(glob.glob(os.path.join(DUMPS, "cli_*.txt")))
    if not patterns or not os.path.exists(patterns[0]):
        print(f"no dumps. paste each model's reply to {DUMPS}/cli_<id>.txt first.")
        print(f"the prompt to send them is run_all_models.PROMPT ({len(PROMPT)} chars)")
        return 1

    results, rows = [], []
    for path in patterns:
        mid = os.path.basename(path)[4:-4]
        with open(path) as f:
            raw = f.read()
        grid = parse_grid(raw)
        if not grid:
            n = len(parse_answers(raw, 4050) or [])
            print(f"[skip] {mid}: reply did not parse as a {STEP}-deg grid"
                  f" (found {n} loose L/W answers)")
            rows.append({"id": mid, "label": LABELS.get(mid, mid),
                         "status": "unparseable", "mode": "grid-recall"})
            continue
        pred = [c for row in grid for c in row]
        s = score(pred, truth)
        arr = np.asarray([c == "L" for c in pred]).reshape(len(lats), len(lons))
        results.append({"id": mid, "label": LABELS.get(mid, mid), "pred": arr,
                        "acc": s["accuracy"], "land_recall": s["land_recall"],
                        "water_recall": s["water_recall"], "mode": "grid-recall",
                        "errors": s["n"] - int(round(s["accuracy"] * s["n"]))})
        rows.append({k: v for k, v in results[-1].items() if k != "pred"})
        print(f"[ok] {mid:<22} accuracy {s['accuracy'] * 100:.1f}%")

    if not results:
        print("nothing scored")
        return 1

    results.sort(key=lambda r: -r["acc"])
    png = os.path.join(args.out, f"leaderboard_all_{STEP}deg.png")
    render_leaderboard(results, lats, lons, STEP, LandTruth(SHP).shapes, png,
                       skipped=[r["label"] for r in rows if r.get("status") not in (None, "ok")])
    print(f"figure -> {png}")
    with open(os.path.join(args.out, "leaderboard_all.json"), "w") as f:
        json.dump({"step": STEP, "n_points": len(pts),
                   "baseline_all_land": float(truth.mean()), "rows": rows}, f, indent=2)
    print()
    for r in results:
        print(f"{r['label']:<24}{r['acc'] * 100:>8.1f}%  "
              f"land {r['land_recall'] * 100:>5.1f}%  water {r['water_recall'] * 100:>5.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
