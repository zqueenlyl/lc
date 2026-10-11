#!/usr/bin/env python3
"""Run the Land-or-Water eval against every model the WorkBuddy picker exposes.

STATUS (2026-10-10): BLOCKED — not yet runnable from inside a live session.

  The bundled `codebuddy` CLI (v2.156.0) lists every model we want
  (hy4-preview-ioa, hy3-ioa, echo, glm-5.3-ioa, glm-5.3-flash-ioa,
  glm-5.3-flashx, glm-5.2-ioa, kimi-k3-ioa, deepseek-v4.1-flash, ...), but:

    1. `codebuddy -p --model <id>` hangs at startup (only a [CliMemWatch]
       heartbeat line, never advances). Root cause: a single-instance lock
       (SingletonSocket) — this CLI detects the running WorkBuddy app and
       tries to delegate via IPC instead of booting its own runtime.
    2. The local gateway (CODEBUDDY_SERVICE_PROXY_URL, Bearer =
       CODEBUDDY_GATEWAY_PASSWORD) DOES accept POST /api/v1/runs, but every
       run is bound to the CURRENT conversation's activeSessionId and shows
       busy=true / runStatus=tool_executing forever — it cannot spin up an
       independent session, and it inherits this session's model rather than
       switching. Nested calls also hit RATE_LIMITED.

  So a model cannot be driven programmatically while this conversation is
  alive. Two ways to actually run the matrix:
    A. From a plain shell OUTSIDE WorkBuddy (no single-instance lock), run
       `codebuddy -p --model <id>` per model. This script already does that.
    B. Manually: switch model in the picker, ask each one for the grid, save
       the reply to predictions/runs/cli_<id>.txt, then score with
       `python score_dump.py --id <id>`.

When run from a real shell, each model gets ONE call returning the full
45 x 90 grid, so every model faces an identical task and the results are
mutually comparable.

  python run_all_models.py                  # all models
  python run_all_models.py --only hy3-ioa,echo
  python run_all_models.py --list
"""

import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

from lowe.grid import build_grid
from lowe.report import render_leaderboard, score
from lowe.truth import LandTruth

CBC = "/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/cli/bin/codebuddy"
HERE = os.path.dirname(os.path.abspath(__file__))
SHP = os.path.join(HERE, "data", "ne_50m_land.shp")
SCRATCH = "/tmp/lowq"

# id -> display label. Order follows the WorkBuddy model picker.
MODELS = [
    ("hy4-preview-ioa", "Hy4 preview"),
    ("hy3-ioa", "Hy3"),
    ("echo", "Echo"),
    ("glm-5.3-ioa", "GLM-5.3"),
    ("glm-5.3-flash-ioa", "GLM-5.3-Flash"),
    ("glm-5.3-flashx", "GLM-5.3-FlashX"),
    ("glm-5.2-ioa", "GLM-5.2"),
    ("kimi-k3-ioa", "Kimi K3"),
    ("kimi-k2.8-preview", "Kimi K2.8 preview"),
    ("minimax-m3-ioa", "MiniMax M3"),
    ("deepseek-v4.1-flash", "DeepSeek V4.1 Flash"),
    ("deepseek-v4-pro-ioa", "DeepSeek V4-Pro (ioa)"),
]

STEP = 4
N_LAT, N_LON = 45, 90

PROMPT = f"""You are a geography oracle. Answer from memory only.

Task: for a {STEP}-degree global grid, decide whether each point is land or water.

Grid layout: {N_LAT} rows x {N_LON} columns.
- Row 1 is latitude 88N, each next row is {STEP} degrees further south, row {N_LAT} is 88S.
- Within a row, column 1 is longitude 180W, each next column is {STEP} degrees further east, column {N_LON} is 176E.

Answer L for land. Answer W for water (ocean, sea, gulf, bay, strait, large lake).
Ice sheets and ice shelves count as land.

Output format: EXACTLY {N_LAT} lines. Each line must be the latitude number
(88 down to -88), one space, then {N_LON} characters each being L or W.
No latitude letter suffix. No explanation. No markdown code fences. No blank lines.

Begin now with the line for 88."""


def _run_cli(model, prompt, timeout):
    env = dict(os.environ)
    env.setdefault("CI", "1")
    # After the 2026-10-10 app update only codebuddy-lite-wb.mjs survives in
    # dist/; the headless and full bundles were removed. Force the lite-wb
    # bundle so the wrapper script does not fall through to the missing
    # ../dist/codebuddy and crash with MODULE_NOT_FOUND.
    env["CODEBUDDY_FORCE_LITE_WB_BUNDLE"] = "1"
    env.pop("CODEBUDDY_FORCE_HEADLESS_BUNDLE", None)
    p = subprocess.run(
        [CBC, "-p", "--model", model, "--tools", "", "--no-session-persistence",
         "--max-turns", "1", prompt],
        cwd=SCRATCH, capture_output=True, text=True, timeout=timeout, env=env,
    )
    return p.stdout + "\n" + p.stderr


def parse_grid(text):
    """Return list of 45 strings of 90 L/W chars, or None."""
    text = re.sub(r"```[a-z]*", "", text)
    strict = re.compile(r"^\s*[-+]?\d{1,3}\s*[°]?\s*([LWlw]{"
                        + str(N_LON) + r"})\s*$")
    rows = [m.group(1).upper() for m in (strict.match(l) for l in text.splitlines()) if m]
    if len(rows) == N_LAT:
        return rows

    loose = []
    for line in text.splitlines():
        letters = re.findall(r"[LWlw]", line)
        if len(letters) >= N_LON:
            loose.append("".join(letters[:N_LON]).upper())
    if len(loose) >= N_LAT:
        return loose[:N_LAT]
    return None


def run_model(model, label, timeout, retries=2):
    for attempt in range(retries):
        try:
            raw = _run_cli(model, PROMPT, timeout)
        except subprocess.TimeoutExpired:
            print(f"  [{model}] timeout after {timeout}s")
            continue
        grid = parse_grid(raw)
        if grid:
            return grid, raw
        tail = raw.strip().splitlines()[-4:]
        print(f"  [{model}] attempt {attempt + 1}: unparseable. tail: {tail}")
    return None, raw if "raw" in dir() else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated model ids")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()

    if args.list:
        for mid, label in MODELS:
            print(f"{mid:<24} {label}")
        return 0

    models = MODELS
    if args.only:
        want = {x.strip() for x in args.only.split(",")}
        models = [(m, l) for m, l in MODELS if m in want]
        if not models:
            print(f"no known model in: {args.only}")
            return 1

    os.makedirs(SCRATCH, exist_ok=True)
    out_dir = os.path.join(HERE, "outputs")
    cache_dir = os.path.join(HERE, "predictions", "runs")
    os.makedirs(cache_dir, exist_ok=True)

    lats, lons = build_grid(STEP)
    assert len(lats) == N_LAT and len(lons) == N_LON
    pts = [(la, lo) for la in lats for lo in lons]
    truth = LandTruth(SHP).is_land(pts)

    results, rows = [], []
    lock_n = [0]

    def work(item):
        mid, label = item
        print(f"[start] {mid} ({label})")
        grid, raw = run_model(mid, label, args.timeout)
        with open(os.path.join(cache_dir, f"cli_{mid}.txt"), "w") as f:
            f.write(raw)
        if grid is None:
            print(f"[fail ] {mid}")
            return {"id": mid, "label": label, "status": "failed", "mode": "grid-recall"}
        pred = [c for row in grid for c in row]
        s = score(pred, truth)
        arr = np.asarray([c == "L" for c in pred]).reshape(N_LAT, N_LON)
        print(f"[ok   ] {mid}  accuracy {s['accuracy'] * 100:.1f}%")
        return {"id": mid, "label": label, "status": "ok", "mode": "grid-recall",
                "acc": s["accuracy"], "land_recall": s["land_recall"],
                "water_recall": s["water_recall"], "pred": arr,
                "errors": s["n"] - int(round(s["accuracy"] * s["n"]))}

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for r in ex.map(work, models):
            if r["status"] == "ok":
                results.append(r)
            rows.append(r)

    if not results:
        print("no model produced a parseable grid")
        return 1

    results.sort(key=lambda r: -r["acc"])
    png = os.path.join(out_dir, f"leaderboard_all_{STEP}deg.png")
    render_leaderboard(results, lats, lons, STEP, LandTruth(SHP).shapes, png,
                       skipped=[r["label"] for r in rows if r["status"] != "ok"])
    print(f"figure -> {png}")

    with open(os.path.join(out_dir, "leaderboard_all.json"), "w") as f:
        json.dump({"step": STEP, "n_points": len(pts),
                   "baseline_all_land": float(truth.mean()),
                   "rows": [{k: v for k, v in r.items() if k != "pred"} for r in rows]}, f, indent=2)

    print()
    print(f"{'model':<24}{'accuracy':>10}{'land':>9}{'water':>9}{'errors':>8}")
    for r in results:
        print(f"{r['label']:<24}{r['acc'] * 100:>9.1f}%{r['land_recall'] * 100:>8.1f}%"
              f"{r['water_recall'] * 100:>8.1f}%{r['errors']:>8}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
