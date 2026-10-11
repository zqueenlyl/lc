#!/usr/bin/env python3
"""Build outputs/report.html from a cached interval prediction."""

import base64
import html
import json
import os
import subprocess
import sys

import numpy as np

from lowe.grid import build_grid, grid_points
from lowe.truth import LandTruth

HERE = os.path.dirname(os.path.abspath(__file__))
SHP = os.path.join(HERE, "data", "ne_50m_land.shp")
PY = sys.executable


def predict(pts, intervals):
    out = []
    for lat, lon in pts:
        out.append(any(min(a, b) <= lon <= max(a, b) for a, b in intervals.get(round(lat, 6), [])))
    return np.asarray(out, dtype=bool)


def main():
    name = "hy4"
    path = os.path.join(HERE, "predictions", f"{name}.intervals.json")
    with open(path) as f:
        intervals = {float(k): v for k, v in json.load(f)["grid"].items()}

    step = 4.0
    lats, lons = build_grid(step)
    pts = grid_points(lats, lons)
    truth = LandTruth(SHP).is_land(pts)
    pred = predict(pts, intervals)
    wrong = pred != truth

    acc = float((~wrong).mean())
    over = int((pred & ~truth).sum())
    under = int((~pred & truth).sum())
    land_recall = float(pred[truth].mean())
    water_recall = float((~pred[~truth]).mean())
    base = float(truth.mean())

    bands = []
    lat_arr = np.asarray([p[0] for p in pts])
    for lo in range(80, -100, -20):
        sel = (lat_arr <= lo) & (lat_arr > lo - 20)
        if sel.sum():
            bands.append((f"{lo}° .. {lo - 20}°", int(sel.sum()),
                          float((~wrong[sel]).mean()), float(truth[sel].mean()),
                          float(pred[sel].mean())))

    png = os.path.join(HERE, "outputs", f"{name}_{int(step)}deg.png")
    with open(png, "rb") as f:
        img = base64.b64encode(f.read()).decode()

    lb_png_path = os.path.join(HERE, "outputs", f"leaderboard_{int(step)}deg.png")
    lb_json_path = os.path.join(HERE, "outputs", "leaderboard.json")
    lb_img, lb_rows_html, lb_note = "", "", ""
    if os.path.exists(lb_json_path) and os.path.exists(lb_png_path):
        with open(lb_png_path, "rb") as f:
            lb_img = base64.b64encode(f.read()).decode()
        with open(lb_json_path) as f:
            lb = json.load(f)
        for r in sorted(lb["rows"], key=lambda x: -x.get("accuracy", -1)):
            if r["status"] == "ok":
                mark = " *" if r["mode"] == "batch-recall" else ""
                lb_rows_html += (
                    f"<tr><td>{html.escape(r['label'])}{mark}</td><td>{r['mode']}</td>"
                    f"<td class='n'>{r['accuracy'] * 100:.1f}%</td>"
                    f"<td class='n'>{r['land_recall'] * 100:.1f}%</td>"
                    f"<td class='n'>{r['water_recall'] * 100:.1f}%</td>"
                    f"<td class='n'>{r['errors']}</td></tr>")
            else:
                lb_rows_html += (
                    f"<tr class='skip'><td>{html.escape(r['label'])}</td><td>{r['mode']}</td>"
                    f"<td class='n'>—</td><td class='n'>—</td><td class='n'>—</td>"
                    f"<td class='n'>{r['status']}</td></tr>")
        lb_note = (f"全猜陆地基线 {lb['baseline_all_land'] * 100:.1f}%，"
                   f"{lb['n_points']} 个点，{int(lb['step'])}° 网格。")

    log = subprocess.run([PY, os.path.join(HERE, "analyze.py"), path],
                         capture_output=True, text=True).stdout

    rows = "".join(
        f"<tr><td>{b}</td><td class='n'>{n}</td><td class='n'>{a * 100:.1f}%</td>"
        f"<td class='n'>{t * 100:.1f}%</td><td class='n'>{p * 100:.1f}%</td>"
        f"<td class='n {'warn' if a < 0.92 else ''}'>{'低' if a < 0.92 else '正常'}</td></tr>"
        for b, n, a, t, p in bands
    )

    lb_section = ""
    if lb_img:
        lb_section = f"""
<h2>模型对比</h2>
<img src="data:image/png;base64,{lb_img}" alt="model comparison">
<p style="color:#8A94A0;font-size:13px;margin-top:10px">{lb_note}</p>
<table>
  <thead><tr><th>模型</th><th>模式</th><th class="n">准确率</th>
  <th class="n">陆地召回</th><th class="n">水域召回</th><th class="n">错误点 / 状态</th></tr></thead>
  <tbody>{lb_rows_html}</tbody>
</table>
<div class="note">
<b>* 标记的行不可直接比较。</b>hy4 是批量回忆（按纬度带回忆陆地经度区间，一次成型），
其余模型是逐点独立提问。批量模式下模型能看到相邻坐标、空间一致性会自我修正，成绩系统性偏高。
要让两者可比，把 hy4 也改成逐点 API 调用，或对 DeepSeek / hy3 用 <code>--batch 1</code> 跑。
</div>
"""
    doc = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>Land or Water? · {name}</title>
<style>
  :root {{ color-scheme: dark; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:#0E1116; color:#E6E9ED;
         font: 400 14px/1.7 -apple-system, "SF Pro Text", "PingFang SC", "Microsoft YaHei", sans-serif; }}
  .wrap {{ max-width: 1180px; margin: 0 auto; padding: 40px 28px 72px; }}
  h1 {{ font-size: 24px; font-weight: 500; margin: 0 0 6px; letter-spacing:.2px; }}
  h2 {{ font-size: 16px; font-weight: 500; margin: 40px 0 12px; color:#E6E9ED; }}
  .sub {{ color:#8A94A0; font-size: 13px; margin-bottom: 28px; }}
  .cards {{ display:grid; grid-template-columns: repeat(5, 1fr); gap:12px; margin: 24px 0 8px; }}
  .card {{ background:#161B22; border:1px solid #232A33; border-radius:12px; padding:14px 16px; }}
  .card .k {{ font-size:12px; color:#8A94A0; }}
  .card .v {{ font-size:24px; font-weight:500; margin-top:4px; font-variant-numeric: tabular-nums; }}
  .card .v.small {{ font-size:17px; padding-top:5px; }}
  .accent {{ color:#7FD1A0; }} .warn {{ color:#E8A23C; }} .bad {{ color:#E24B4A; }}
  img {{ width:100%; border-radius:12px; border:1px solid #232A33; display:block; margin-top:8px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; margin-top:8px;
           font-variant-numeric: tabular-nums; }}
  th, td {{ text-align:left; padding:8px 10px; border-bottom:1px solid #1E242C; }}
  th {{ color:#8A94A0; font-weight:400; font-size:12px; }}
  td.n, th.n {{ text-align:right; }}
  tr:last-child td {{ border-bottom:none; }}
  tr.skip td {{ color:#5F6B78; }}
  code {{ background:#1B2129; padding:1px 6px; border-radius:5px; font-size:12.5px;
          font-family: ui-monospace, "SF Mono", Menlo, monospace; }}
  pre {{ background:#161B22; border:1px solid #232A33; border-radius:12px; padding:14px 16px;
         overflow:auto; font-size:12.5px; line-height:1.6;
         font-family: ui-monospace, "SF Mono", Menlo, monospace; color:#C8D0D8; }}
  .note {{ background:#161B22; border:1px solid #232A33; border-left:2px solid #E8A23C;
           border-radius:8px; padding:14px 18px; margin-top:12px; font-size:13.5px; color:#C8D0D8; }}
  ul {{ padding-left: 20px; margin: 8px 0; }}
  li {{ margin: 4px 0; }}
</style></head><body><div class="wrap">
<h1>Land or Water? — 世界模型探针</h1>
<div class="sub">模型：<code>{name}</code> · 网格 {int(step)}° · {len(pts)} 个坐标点 · 基准真值：Natural Earth 50m 陆地多边形</div>

<div class="cards">
  <div class="card"><div class="k">准确率</div><div class="v accent">{acc * 100:.1f}%</div></div>
  <div class="card"><div class="k">陆地召回</div><div class="v">{land_recall * 100:.1f}%</div></div>
  <div class="card"><div class="k">水域召回</div><div class="v">{water_recall * 100:.1f}%</div></div>
  <div class="card"><div class="k">全猜陆地基线</div><div class="v small">{base * 100:.1f}%</div></div>
  <div class="card"><div class="k">错误点</div><div class="v small">{int(wrong.sum())}</div></div>
</div>

<img src="data:image/png;base64,{img}" alt="Land or Water eval result">
{lb_section}
<h2>误差结构</h2>
<ul>
  <li><span class="bad">{over}</span> 个点把水域判成陆地，仅 <span class="warn">{under}</span> 个点把陆地判成水域 —— 单向偏置明显，模型倾向于回答"陆地"。</li>
  <li>预测陆地占比 {pred.mean() * 100:.1f}%，真值 {base * 100:.1f}%，系统性高估约 {(pred.mean() - base) * 100:.1f} 个百分点。</li>
  <li>误差集中在 60°N 以北的北冰洋沿岸（喀拉海、拉普捷夫海、加拿大北极群岛的狭窄水道），以及南极洲边缘的冰架/海域分界。</li>
</ul>

<table>
  <thead><tr><th>纬度带</th><th class="n">样本</th><th class="n">准确率</th>
  <th class="n">真值陆地占比</th><th class="n">预测陆地占比</th><th class="n">判定</th></tr></thead>
  <tbody>{rows}</tbody>
</table>

<h2>方法</h2>
<ol>
  <li>按 {int(step)}° 步长在全球铺网格，得到 {len(pts)} 个 <code>(lat, lon)</code> 文本坐标。</li>
  <li>询问模型"这个坐标是陆地还是水域"，不给图、不给工具、不给上下文。</li>
  <li>把答案重新铺回网格成像；用 Natural Earth 50m 陆地多边形做点在多边形内判定，得到打分基准。</li>
  <li>同时计算"全猜陆地"退化基线 —— 任何低于 {base * 100:.1f}% 的成绩说明模型比瞎猜还差。</li>
</ol>
<p style="color:#8A94A0;font-size:13px">结果对应网格点的标签，不是对 4050 次独立提问的统计；独立逐点提问（无跨点上下文）通常会更难。</p>

<h2>复现</h2>
<pre>python run_eval.py --probe mock                      # 全猜陆地基线
python run_eval.py --probe file \\
    --path predictions/{name}.intervals.json --name {name}

# 换成真实模型（OpenAI 兼容，任意厂商）
OPENAI_API_KEY=sk-... OPENAI_BASE_URL=https://api.deepseek.com/v1 \\
    python run_eval.py --probe openai --model deepseek-chat --batch 40 --workers 8

# Anthropic 官方
ANTHROPIC_API_KEY=sk-ant-... python run_eval.py --probe anthropic \\
    --model claude-sonnet-4-5 --batch 40 --workers 8</pre>

<div class="note">
<b>注意</b>：{name} 这次是「一次性批量回忆」模式——按纬度带回忆陆地经度区间，而非逐点独立提问。
批量模式下模型能看到相邻坐标，空间一致性会被"自我修正"，成绩通常高于真正逐点提问。
要拿到严格可比的数字，请用 <code>--probe openai</code> / <code>--probe anthropic</code> 跑一次真·独立查询。
</div>
</div></body></html>"""

    out = os.path.join(HERE, "outputs", "report.html")
    with open(out, "w") as f:
        f.write(doc)
    print(out)
    print(log)


if __name__ == "__main__":
    main()
