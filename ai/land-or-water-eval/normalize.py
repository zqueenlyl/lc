#!/usr/bin/env python3
"""Normalize a raw cli_*.txt reply into a strict 45x90 L/W grid.

Models return grids with inconsistent per-line width (86-104 chars) or with
duplicate/missing latitude bands. This tool extracts {latitude: LW-string} from
the latitude-prefixed lines, then rebuilds the canonical 45 rows (88 -> -88,
4-degree steps) each padded/truncated to exactly 90 columns (truncation keeps
the western 90 longitudes; missing bands default to water).

  python normalize.py            # normalize every cli_*.txt in place
  python normalize.py --check    # only report, do not write
"""

import argparse
import glob
import os
import re

N_LAT, N_LON = 45, 90
LAT_START, LAT_STEP = 88, -4
STD_LATS = [LAT_START + i * LAT_STEP for i in range(N_LAT)]  # 88..-88

HERE = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(HERE, "predictions", "runs")

LINE = re.compile(r"^\s*([+-]?\d{1,3})\s*[°]?\s*([LWlw ]+?)(?:\s*$)")


def extract(raw):
    """Return dict {latitude_int: cleaned_LW_string}."""
    bands = {}
    for ln in raw.splitlines():
        m = LINE.match(ln)
        if not m:
            continue
        lat = int(m.group(1))
        letters = re.sub(r"[^LWlw]", "", m.group(2)).upper()
        if not letters:
            continue
        # keep the FIRST occurrence per latitude (avoid duplicate-band noise)
        bands.setdefault(lat, letters)
    return bands


def normalize(raw):
    bands = extract(raw)
    rows = []
    for lat in STD_LATS:
        s = bands.get(lat, "")
        if len(s) > N_LON:
            s = s[:N_LON]
        elif len(s) < N_LON:
            s = s + "W" * (N_LON - len(s))
        rows.append(f"{lat} {''.join(s)}")
    return "\n".join(rows) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(DUMPS, "cli_*.txt")))
    if not files:
        print("no cli_*.txt dumps found")
        return 1

    for path in files:
        mid = os.path.basename(path)[4:-4]
        raw = open(path, encoding="utf-8", errors="ignore").read()
        bands = extract(raw)
        n_have = sum(1 for la in STD_LATS if la in bands)
        widths = sorted({len(v) for v in bands.values()})
        status = "OK" if n_have == N_LAT else f"MISSING({n_have}/45)"
        print(f"{mid:<24} bands={n_have:>2}/45 widths={widths} {status}")
        if args.check:
            continue
        # only rewrite if it parses to (near) a full grid
        if sum(1 for la in STD_LATS if la in bands) >= N_LAT - 2:
            with open(path, "w", encoding="utf-8") as f:
                f.write(normalize(raw))
            print(f"   -> rewrote {mid} as strict 45x90")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
