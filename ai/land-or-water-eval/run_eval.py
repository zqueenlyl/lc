#!/usr/bin/env python3
"""Land or Water? — a reference-free world-model eval.

Single model
  python run_eval.py --probe mock
  python run_eval.py --probe file --path predictions/hy4.intervals.json --name hy4
  OPENAI_API_KEY=sk-... OPENAI_BASE_URL=https://api.deepseek.com/v1 \
      python run_eval.py --probe openai --model deepseek-chat --batch 40 --workers 8
  ANTHROPIC_API_KEY=sk-ant-... python run_eval.py --probe anthropic --model claude-sonnet-4-5

Model comparison (uses models.json)
  python run_eval.py --models all              # run every runnable model
  python run_eval.py --models hy4,deepseek-v4.1-flash,deepseek-v4.1-pro,hy3,baseline
  python run_eval.py --list-models             # show what is runnable right now
  python run_eval.py --emit-template hy3       # blank template for a model to self-report
"""

import argparse
import json
import os
import sys

import numpy as np

from lowe.grid import build_grid, grid_points
from lowe.probe import make_probe
from lowe.registry import load_registry, resolve
from lowe.report import render, render_leaderboard, score
from lowe.truth import LandTruth

HERE = os.path.dirname(os.path.abspath(__file__))
SHP = os.path.join(HERE, "data", "ne_50m_land.shp")
REGISTRY = os.path.join(HERE, "models.json")


def _grid(step, limit):
    lats, lons = build_grid(step)
    pts = grid_points(lats, lons)
    if limit:
        pts = pts[:limit]
        lats = lats[: -(-len(pts) // len(lons))]
    return lats, lons, pts


def _sanitize(name):
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in name)


def cmd_emit_template(name, step):
    lats, _ = build_grid(step)
    path = os.path.join(HERE, "predictions", f"{name}.intervals.json")
    if os.path.exists(path):
        print(f"already exists, refusing to overwrite: {path}")
        return 1
    with open(path, "w") as f:
        json.dump({"_note": f"{name}: fill each latitude with the longitude intervals you "
                            f"recall as LAND, then run "
                            f"--probe file --path predictions/{name}.intervals.json",
                   "grid": {str(la): [] for la in lats}}, f, indent=2)
    print(f"template -> {path}")
    return 0


def cmd_list_models():
    reg = load_registry(REGISTRY)
    print(f"{'id':<22} {'probe':<10} {'mode':<14} status")
    for e in reg:
        probe, reason, label, mode = resolve(e, HERE)
        status = "runnable" if probe is not None else f"SKIP — {reason}"
        print(f"{e['id']:<22} {e['probe']:<10} {mode:<14} {status}")
        if e.get("caveat"):
            print(f"{'':<22} {'':<10} {'':<14} ! {e['caveat']}")
    return 0


def cmd_compare(ids, step, batch, workers, out_dir, limit):
    full = load_registry(REGISTRY)
    if ids != ["all"]:
        wanted = [i.strip() for i in ids]
        reg = [e for e in full if e["id"] in wanted]
        missing = [i for i in wanted if i not in {e["id"] for e in full}]
        if missing:
            print(f"unknown model id(s): {', '.join(missing)}")
            print(f"known: {', '.join(e['id'] for e in full)}")
            return 1
    else:
        reg = full

    lats, lons, pts = _grid(step, limit)
    print(f"grid: {len(lats)} lat x {len(lons)} lon = {len(pts)} points")
    truth = LandTruth(SHP)
    t = truth.is_land(pts)

    results, rows = [], []
    for e in reg:
        for key in ("note", "caveat"):
            if e.get(key):
                print(f"[{key}] {e['id']}: {e[key]}")
        probe, reason, label, mode = resolve(e, HERE, batch=batch, workers=workers)
        if probe is None:
            print(f"[skip] {e['id']}: {reason}")
            rows.append({"id": e["id"], "label": label, "status": "skipped",
                         "reason": reason, "mode": mode})
            continue
        print(f"[run ] {e['id']} ({probe.name}) ...")
        try:
            pred = probe.predict(pts)
        except Exception as exc:
            print(f"[fail] {e['id']}: {exc}")
            rows.append({"id": e["id"], "label": label, "status": "failed",
                         "reason": str(exc), "mode": mode})
            continue
        s = score(pred, t)
        arr = np.asarray([x == "L" for x in pred]).reshape(len(lats), len(lons))
        results.append({"id": e["id"], "label": label, "pred": arr,
                        "acc": s["accuracy"], "mode": mode})
        rows.append({"id": e["id"], "label": label, "status": "ok", "mode": mode,
                     "accuracy": s["accuracy"], "land_recall": s["land_recall"],
                     "water_recall": s["water_recall"],
                     "errors": s["n"] - int(round(s["accuracy"] * s["n"]))})
        print(f"       accuracy {s['accuracy'] * 100:.1f}%")

        cache_dir = os.path.join(HERE, "predictions", "runs")
        os.makedirs(cache_dir, exist_ok=True)
        with open(os.path.join(cache_dir, f"{_sanitize(e['id'])}.json"), "w") as f:
            json.dump({"id": e["id"], "step": step, "predictions": pred}, f)

    if not results:
        print("no model produced a result")
        return 1

    results.sort(key=lambda r: -r["acc"])
    os.makedirs(out_dir, exist_ok=True)
    png = os.path.join(out_dir, f"leaderboard_{int(step)}deg.png")
    skipped = [r["label"] for r in rows if r["status"] != "ok"]
    render_leaderboard(results, lats, lons, step, truth.shapes, png, skipped=skipped)
    print(f"figure -> {png}")

    lb = os.path.join(out_dir, "leaderboard.json")
    with open(lb, "w") as f:
        json.dump({"step": step, "n_points": len(pts),
                   "baseline_all_land": float(t.mean()), "rows": rows}, f, indent=2)
    print(f"leaderboard -> {lb}")

    print()
    print(f"{'model':<24}{'mode':<15}{'accuracy':>10}{'land':>9}{'water':>9}")
    for r in results:
        rr = next(x for x in rows if x["id"] == r["id"])
        print(f"{r['label']:<24}{r['mode']:<15}{r['acc'] * 100:>9.1f}%"
              f"{rr['land_recall'] * 100:>8.1f}%{rr['water_recall'] * 100:>8.1f}%")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", type=float, default=4.0)
    ap.add_argument("--probe", help="mock | file | openai | anthropic")
    ap.add_argument("--models", help="comma-separated ids from models.json, or 'all'")
    ap.add_argument("--list-models", action="store_true")
    ap.add_argument("--emit-template", metavar="NAME")
    ap.add_argument("--path", help="prediction file (probe=file)")
    ap.add_argument("--name")
    ap.add_argument("--model")
    ap.add_argument("--batch", type=int, default=40)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default=os.path.join(HERE, "outputs"))
    args = ap.parse_args()

    if args.emit_template:
        return cmd_emit_template(args.emit_template, args.step)
    if args.list_models:
        return cmd_list_models()
    if args.models:
        return cmd_compare(args.models.split(","), args.step, args.batch,
                           args.workers, args.out, args.limit)

    lats, lons, pts = _grid(args.step, args.limit)
    print(f"grid: {len(lats)} lat x {len(lons)} lon = {len(pts)} points")
    truth = LandTruth(SHP)
    t = truth.is_land(pts)

    probe = make_probe(args.probe or "mock", path=args.path, model=args.model,
                       batch=args.batch, workers=args.workers)
    name = args.name or probe.name
    print(f"probe: {probe.name}")
    pred = probe.predict(pts)

    s = score(pred, t)
    print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v)
                      for k, v in s.items()}, indent=2))

    os.makedirs(args.out, exist_ok=True)
    png = os.path.join(args.out, f"{_sanitize(name)}_{int(args.step)}deg.png")
    render(name, lats, lons, pred, t, truth.shapes, png, args.step)
    print(f"figure -> {png}")

    cache_dir = os.path.join(HERE, "predictions", "runs")
    os.makedirs(cache_dir, exist_ok=True)
    cache = os.path.join(cache_dir, f"{_sanitize(name)}.json")
    with open(cache, "w") as f:
        json.dump({"name": name, "step": args.step, "predictions": pred}, f)
    print(f"cached -> {cache}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
