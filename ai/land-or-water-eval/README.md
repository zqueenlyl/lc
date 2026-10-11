# Land or Water? — 世界模型探针

复刻 Karpathy 转发的那个无参考评测：给模型一串文本经纬度，问它「陆地还是水域？」，
把答案铺回网格成像，用 Natural Earth 真实陆地多边形打分。

## 为什么这个评测有意思

不需要标注数据、不需要判分模型、不需要工具。它直接探测模型权重里**隐式重建的地球**——
训练语料里的地理信息在压缩进参数后，还剩多少空间保真度。

## 目录

```
run_eval.py                    主入口（单模型 / 多模型对比 / 列出状态 / 生成模板）
analyze.py                     误差分解（纬度带 / 误差簇）
make_report.py                 生成 outputs/report.html
models.json                    模型注册表：探针类型、模型名、凭据环境变量、模式、注意事项
lowe/grid.py                   采样网格
lowe/truth.py                  真值：点在 Natural Earth 50m 陆多边形内
lowe/probe.py                  模型探针（mock / file / openai / anthropic）
lowe/registry.py               读 models.json，解析凭据，缺凭据就跳过 —— 绝不伪造预测
lowe/report.py                 打分 + 单模型三栏图 + 多模型对比图
predictions/hy4.intervals.json hy4 的预测（按纬度带的陆地经度区间）
predictions/hy3.intervals.json hy3 的空白模板，待填充
predictions/runs/              每次运行的预测缓存
data/ne_50m_land.shp           Natural Earth 50m 陆地（457 KB）
```

## 用法

```bash
PY=/Users/wzq1/.workbuddy/binaries/python/envs/default/bin/python

# 1) 退化基线：永远回答「陆地」
$PY run_eval.py --probe mock

# 2) 复现 hy4 的结果（读缓存预测，不调 API）
$PY run_eval.py --probe file --path predictions/hy4.intervals.json --name hy4

# 3) 跑真实模型 —— 任意 OpenAI 兼容端点
OPENAI_API_KEY=sk-... OPENAI_BASE_URL=https://api.deepseek.com/v1 \
  $PY run_eval.py --probe openai --model deepseek-chat --batch 40 --workers 8

# 4) Anthropic 官方
ANTHROPIC_API_KEY=sk-ant-... \
  $PY run_eval.py --probe anthropic --model claude-sonnet-4-5 --batch 40 --workers 8

# 5) 报告
$PY make_report.py

# 6) 多模型对比
$PY run_eval.py --list-models                 # 当前哪些模型可跑、哪些缺凭据
$PY run_eval.py --models all                  # 跑全部可跑的，出 leaderboard_4deg.png
$PY run_eval.py --models hy4,deepseek-v4.1-flash,baseline
$PY run_eval.py --emit-template hy3           # 给还没接入的模型生成空白预测模板
```

新增模型只需往 `models.json` 里加一条，不用改代码：

```json
{ "id": "my-model", "label": "My Model", "probe": "openai",
  "model": "my-model-id", "base_url": "https://.../v1",
  "api_key_env": "MY_API_KEY", "mode": "api" }
```

## 参数

| 参数 | 说明 |
|---|---|
| `--step 4` | 网格步长。4° → 4050 点；2° → 16020 点（原版密度）；6° → 1800 点（冒烟） |
| `--batch 40` | 每次 API 请求塞多少个坐标。批量越大越省钱，但会引入跨点上下文 |
| `--workers 8` | 并发请求数 |
| `--limit N` | 只跑前 N 个点，快速验证接线 |

## 三个关键设计

**批量提问。** 逐点提问 4050 次既慢又贵。默认把 40 个坐标塞进一次请求，让模型输出一串
`L`/`W`。这偏离了原版的逐点独立提问 —— 批量模式下模型能看到邻居，成绩会被抬高。
要严格可比就用 `--batch 1`。

**真值不是二元的。** 「陆地」用 Natural Earth 陆多边形判定，湖算陆地（NE 的 land 层不挖湖），
里海算水域（多边形里有洞，`lowe/truth.py` 用 even-odd 填充规则正确处理）。

**退化基线。** 全猜陆地在这个网格上就有 33.1%。任何低于它的成绩说明模型比瞎猜更差 ——
原图里 Haiku 4.5 的 81.3% 放到这个基准下才有意义。

## 已跑出的结果（4° 网格，4050 点）

| 模型 | 模式 | 准确率 | 陆地召回 | 水域召回 | 错误点 |
|---|---|---|---|---|---|
| hy4 | 批量回忆 * | 93.3% | 96.8% | 91.6% | 272 |
| baseline（全猜陆地） | 退化基线 | 33.1% | 100% | 0% | — |
| deepseek-v4.1-flash | API 逐点 | 待跑（缺 `DEEPSEEK_API_KEY`） | | | |
| deepseek-v4.1-pro | API 逐点 | 见下方警告 | | | |
| hy3 | API 逐点 | 待跑（缺 `HY3_BASE_URL` + `HY3_API_KEY`） | | | |

hy4 的错误是**单向**的：229 个点把水域判成陆地，只有 43 个点反向。误差集中在 60°N 以北的
北冰洋沿岸（喀拉海、拉普捷夫海）和南极边缘的冰架分界 —— 也就是训练语料里描述最少、
且本身界限模糊的地方。

## DeepSeek 侧的两个事实（2026-10 核实）

1. **正确模型名是 `deepseek-flash`。** V4.1-Flash 于 2026-09-10 发布并上线 API，官方文档写的是
   「Set your model to `deepseek-flash`」。`deepseek-v4-flash` 只是兼容别名，已被路由到 V4.1-Flash。
2. **V4.1-Pro 还没发布，`pro` 这一行现在跑不出差异。** V4-Pro 已于 2026-09-14 12:00 退役，
   此后所有 `deepseek-v4-pro` 请求被**静默路由到 V4.1-Flash 并按 Flash 单价计费**，
   直到 V4.1-Pro 上线。所以同时注册 flash 和 pro 两条，在真机上是同一个模型、同一份结果 ——
   画进对比图就是假对比。`models.json` 里给这条标了 `caveat`，运行时会在控制台打印出来。

## 未跑通的模型怎么补

| 模型 | 缺什么 | 补法 |
|---|---|---|
| DeepSeek V4.1 Flash | API key | `export DEEPSEEK_API_KEY=sk-...` 然后 `--models deepseek-v4.1-flash` |
| hy3 | 内部 base url + key | `export HY3_BASE_URL=... HY3_API_KEY=...`；若 hy3 只能走对话不能走 API，用 `--emit-template hy3` 出模板，让 hy3 在会话里自己填 |

## 已知限制

- `predictions/hy4.intervals.json` 是一次性批量回忆的产物（按纬度带回忆陆地经度区间），
  不是 4050 次独立提问。要拿严格可比的数字请用 `--probe openai` / `--probe anthropic`。
- 50m 分辨率的真值对小于 4° 的岛屿（夏威夷、佛得角、马尔代夫）不敏感，这些点的对错
  不应过度解读。
- 等距圆柱网格在极地严重过采样：南极洲在 4050 个点里占了 270 个，会拉高整体准确率。
