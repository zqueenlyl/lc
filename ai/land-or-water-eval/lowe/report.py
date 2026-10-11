"""Scoring and rendering for the Land-or-Water eval."""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

LAND_C = "#E8DFC8"
WATER_C = "#12263F"
ERR_C = "#E24B4A"
COAST_C = "#6E7A8A"
BG = "#101418"
FG = "#E6E6E6"


def score(pred, truth):
    """pred: list of 'L'/'W'; truth: bool ndarray (True = land)."""
    p = np.asarray([x == "L" for x in pred])
    t = np.asarray(truth, dtype=bool)
    acc = float((p == t).mean())
    land_recall = float(p[t].mean()) if t.any() else float("nan")
    water_recall = float((~p[~t]).mean()) if (~t).any() else float("nan")
    pred_land_rate = float(p.mean())
    true_land_rate = float(t.mean())
    return {
        "n": int(len(t)),
        "accuracy": acc,
        "land_recall": land_recall,
        "water_recall": water_recall,
        "pred_land_rate": pred_land_rate,
        "true_land_rate": true_land_rate,
        "baseline_all_land": true_land_rate,
    }


def _draw(ax, arr, extent, shapes, title, sub, cmap):
    ax.imshow(arr, extent=extent, origin="upper", aspect="auto",
              interpolation="nearest", cmap=cmap, vmin=0, vmax=1)
    for v in shapes:
        ax.plot(v[:, 0], v[:, 1], color=COAST_C, linewidth=0.35, alpha=0.85)
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_xticks([-180, -120, -60, 0, 60, 120, 180])
    ax.set_yticks([-90, -60, -30, 0, 30, 60, 90])
    ax.tick_params(colors="#9AA4B0", labelsize=8)
    for s in ax.spines.values():
        s.set_color("#2A3138")
    ax.set_title(title, color=FG, fontsize=12, pad=6)
    ax.set_xlabel(sub, color="#9AA4B0", fontsize=8, labelpad=2)


def render_leaderboard(results, lats, lons, step, shapes, out_png, skipped=None):
    """results: [{'id','label','pred'(bool 2d),'acc','mode'}] sorted best first."""
    n = len(results)
    if not n:
        return
    cols = 3
    rows = -(-n // cols)
    fig = plt.figure(figsize=(5.5 * cols, 2.9 * rows + 3.7), facecolor=BG)
    gs = fig.add_gridspec(rows + 1, cols, height_ratios=[0.8] + [1.0] * rows,
                          hspace=0.55, wspace=0.08,
                          left=0.135, right=0.985, top=0.845, bottom=0.05)

    ax_bar = fig.add_subplot(gs[0, :])
    labels = [f"{r['label']}{' *' if r['mode'] == 'batch-recall' else ''}" for r in results]
    accs = [r["acc"] * 100 for r in results]
    colors = ["#7F77DD" if r["mode"] == "batch-recall" else "#1D9E75" for r in results]
    ypos = list(range(n))[::-1]
    ax_bar.barh(ypos, accs, color=colors, height=0.62)
    for y, v in zip(ypos, accs):
        ax_bar.text(v + 0.8, y, f"{v:.1f}%", va="center", color=FG, fontsize=9.5)
    ax_bar.set_yticks(ypos)
    ax_bar.set_yticklabels(labels, color=FG, fontsize=9.5)
    ax_bar.set_xlim(0, 108)
    ax_bar.set_facecolor(BG)
    ax_bar.tick_params(colors="#9AA4B0", labelsize=8)
    for s in ax_bar.spines.values():
        s.set_color("#2A3138")
    ax_bar.set_title("accuracy  ·  * = batch-recall, not per-point queries — not comparable",
                     color="#9AA4B0", fontsize=9.5, pad=7)

    cmap = ListedColormap([WATER_C, LAND_C])
    extent = [-180 - step / 2, 180 - step / 2, lats[-1] - step / 2, lats[0] + step / 2]
    for i, r in enumerate(results):
        ax = fig.add_subplot(gs[1 + i // cols, i % cols])
        ax.imshow(r["pred"].astype(int), extent=extent, origin="upper", aspect="auto",
                  interpolation="nearest", cmap=cmap, vmin=0, vmax=1)
        for v in shapes:
            ax.plot(v[:, 0], v[:, 1], color=COAST_C, linewidth=0.3, alpha=0.8)
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#2A3138")
        ax.set_title(f"{r['label']}  ·  {r['acc'] * 100:.1f}%", color=FG, fontsize=11, pad=5)

    fig.text(0.035, 0.935,
             "   ".join(f"{r['label']} {r['acc'] * 100:.1f}%"
                        f"{' *' if r['mode'] == 'batch-recall' else ''}" for r in results),
             color=FG, fontsize=10.5, va="center")
    if skipped:
        fig.text(0.035, 0.898, "not run — no credential: " + ", ".join(skipped),
                 color="#8A94A0", fontsize=8.5, va="center")
    fig.suptitle(f"Land or Water? — model comparison · {int(step)}° grid"
                 f" · {len(lats) * len(lons)} points", color=FG, fontsize=14, y=0.992)
    fig.savefig(out_png, dpi=125, facecolor=BG)
    plt.close(fig)


def render(name, lats, lons, pred, truth, shapes, out_png, step):
    n_lat, n_lon = len(lats), len(lons)
    s = score(pred, truth)
    p = np.asarray([x == "L" for x in pred]).reshape(n_lat, n_lon).astype(int)
    t = np.asarray(truth).reshape(n_lat, n_lon).astype(int)
    err = (p != t).astype(int)
    extent = [-180 - step / 2, 180 - step / 2, lats[-1] - step / 2, lats[0] + step / 2]

    fig, axes = plt.subplots(1, 3, figsize=(16.5, 5.4), facecolor=BG)
    fig.subplots_adjust(left=0.04, right=0.985, top=0.86, bottom=0.09, wspace=0.10)

    land_water = ListedColormap([WATER_C, LAND_C])
    plain = ListedColormap([WATER_C, LAND_C])
    errs = ListedColormap(["#141A20", ERR_C])

    _draw(axes[0], p, extent, shapes, f"{name} — prediction",
          f"land drawn as modelled, {step}° grid, {s['n']} points", land_water)
    _draw(axes[1], t, extent, shapes, "Ground truth",
          "Natural Earth 50m land polygons", plain)
    _draw(axes[2], err, extent, shapes, "Errors",
          f"red = wrong · accuracy {s['accuracy'] * 100:.1f}%", errs)

    fig.suptitle(
        f"Land or Water? · {name} · {s['n']} points · accuracy {s['accuracy'] * 100:.1f}%"
        f" · land recall {s['land_recall'] * 100:.1f}% · water recall {s['water_recall'] * 100:.1f}%"
        f" · all-land baseline {s['baseline_all_land'] * 100:.1f}%",
        color=FG, fontsize=13,
    )
    fig.savefig(out_png, dpi=130, facecolor=BG)
    plt.close(fig)
    return s
