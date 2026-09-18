# Jev 接入与工程实践

> 检索时点：**2026-09-18** ｜ 配套：[《TypeSafe 全景与 System One》](./TypeSafe全景与System-One.md)
> **口径**：原生以 [docs.typesafe.ai/api](https://docs.typesafe.ai/api) 为准；OpenRouter 以 [Jev Latest](https://openrouter.ai/~typesafe/jev-latest) / [Jev 1.13](https://openrouter.ai/typesafe/jev-1.13) 模型页为准。两套 **不是 Chat Completions**。
> 配套 notebook：[Jev原语与置信度门闩演示.ipynb](./Jev原语与置信度门闩演示.ipynb)（页面示例：payouts 工单 + noul/choice/score；有 `OPENROUTER_API_KEY` 才打 `POST /api/alpha/decisions`）。

---

## 1. 先认渠道，再抄 SDK

Jev 同时出现在四条管道上，**模型 ID 字符串不一样**，协议也不都叫同一个名字：

| 渠道 | 模型 ID | 端点 | 协议 | 鉴权 |
|------|---------|------|------|------|
| **TypeSafe 原生** | `jev-latest` / `jev-1.13.0` / `jev-preview` | `POST https://api.typesafe.ai/v1/systemone` | System One | `Authorization: Bearer $TYPESAFE_API_KEY` |
| **OpenRouter** | `~typesafe/jev-latest`（浮动）· `typesafe/jev-1.13`（钉版本） | `POST https://openrouter.ai/api/alpha/decisions` | **Decisions API**（alpha） | OpenRouter key；可选 `HTTP-Referer` / `X-OpenRouter-Title` |
| **Cloudflare Workers AI** | `typesafe/jev` | `env.AI.run('typesafe/jev', …)` 或 REST run | Workers AI | Cloudflare 账号 |
| **Vercel AI Gateway** | `typesafe-ai/jev` `社区` | AI SDK `experimental_evaluate` | Gateway | `AI_GATEWAY_API_KEY` |

价格三条公开管道都写 **$0.042 / M 输入、输出 $0**。原生另有 250k tok/s · 1200 RPM（动态）；OpenRouter / Cloudflare 限流以各平台为准。

**第一坑：OpenRouter 厂商页 FAQ 仍写「OpenAI 兼容、打 `/api/v1`」。Jev 的模型页写的是 Decisions API，且「This model does not generate text」。不要把 `~typesafe/jev-latest` 丢进 Chat Completions 客户端指望它聊天。**

---

## 2. 一次调用长什么样

所有渠道同一套语义：一份 `state` + 一组命名问题 → 同名 `answers`。

### 2.1 原生 HTTP

```http
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer $TYPESAFE_API_KEY
Content-Type: application/json
```

```json
{
  "model": "jev-latest",
  "state": {
    "ticket_message": "Help! My payouts have been failing for 3 days.",
    "refund_policy": "Duplicate charges are eligible for a refund."
  },
  "questions": {
    "is_urgent": {
      "type": "noul",
      "instructions": "Does `ticket_message` convey urgency?",
      "criteria": {
        "true": "Explicitly time-sensitive",
        "false": "No urgency expressed"
      }
    },
    "department": {
      "type": "choice",
      "instructions": "Which team should handle `ticket_message`?",
      "criteria": {
        "billing": "Payments, invoicing, refunds",
        "technical": "Bugs, outages, integrations",
        "sales": "Pricing, upgrades, new accounts"
      }
    },
    "frustration": {
      "type": "score",
      "instructions": "How frustrated is the customer in `ticket_message`?",
      "criteria": ["Calm", "Frustrated", "Very angry"]
    }
  }
}
```

典型响应（数字随输入变；结构以官方为准）：

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "is_urgent": { "type": "noul", "noul": 0.95 },
    "department": {
      "type": "choice",
      "choice": "billing",
      "confidence": 0.80,
      "probabilities": { "billing": 0.87, "technical": 0.13, "sales": 0.0 }
    },
    "frustration": {
      "type": "score",
      "score": 1.04,
      "confidence": 0.94,
      "legend": { "0": "Calm", "1": "Frustrated", "2": "Very angry" },
      "probabilities": { "0": 0.0, "1": 0.96, "2": 0.04 }
    }
  },
  "usage": { "input_tokens": 426, "output_tokens": 73 }
}
```

要点：

- 响应里的 `model` 是**实际回答的版本化 ID**。用了 `jev-latest` 也要把它记进业务日志。
- 问题 key 只给你的代码用，**不送给底层模型**。判断必须写全在 `instructions`。
- `GET https://api.typesafe.ai/v1/models` 目前列出的是**别名**；`jev-1.13.0` 即使不在列表里也可以钉。

### 2.2 OpenRouter Decisions API

用户给的入口：[https://openrouter.ai/~typesafe/jev-latest](https://openrouter.ai/~typesafe/jev-latest)

```python
import json, os, requests

resp = requests.post(
    "https://openrouter.ai/api/alpha/decisions",
    headers={
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your.app",      # 可选，榜单归因
        "X-OpenRouter-Title": "your-app",        # 可选
    },
    data=json.dumps({
        "model": "~typesafe/jev-latest",
        "state": "Help! My payouts have been failing for 3 days.",
        "questions": {
            "is_urgent": {
                "type": "noul",
                "instructions": "Does this message convey urgency?",
                "criteria": {
                    "true": "Explicitly time-sensitive",
                    "false": "No urgency expressed",
                },
            },
            "department": {
                "type": "choice",
                "instructions": "Which team should handle this?",
                "criteria": {
                    "billing": "Payments, invoicing, refunds",
                    "technical": "Bugs, outages, integrations",
                    "sales": "Pricing, upgrades, new accounts",
                },
            },
            "frustration": {
                "type": "score",
                "instructions": "How frustrated is the customer?",
                "criteria": ["Calm", "Frustrated", "Very angry"],
            },
        },
    }),
)
print(resp.json())
```

钉版本把 `model` 换成 `typesafe/jev-1.13`（**没有** `~` 前缀）。`~typesafe/jev-latest` 的 `~` 是 OpenRouter 的「永远指向家族最新」写法。

OpenRouter 模型页示例有把 noul 的 `true`/`false`、choice 的选项**摊到问题对象顶层**的渲染；官方 schema 是 `criteria` 嵌套。上线前用一条真实请求核对，不要只抄页面折叠后的伪代码。

OpenRouter 标价与原生相同；上下文在 OpenRouter 侧只公示 **32,000**。官方 Models 页是「整请求 64k / state+最长问题 32k」。跨渠道不要假设窗口一样大。

### 2.3 Python / JS SDK（原生）

```bash
pip install typesafe-sdk          # Python ≥ 3.10，读 TYPESAFE_API_KEY
# 或: uv add typesafe-sdk
```

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

client = TypeSafeClient()  # 默认 jev-latest

ticket = "Hi, I've been trying to connect my Stripe account for 3 days..."

response = client.system_one(
    state=ticket,
    questions={
        "department": Choice(
            instructions="Which team should handle this",
            criteria={
                "billing": "Payment or subscription issues",
                "technical": "Bugs or integration problems",
                "sales": "Pricing or account questions",
            },
        ),
        "frustration": Score(
            instructions="How frustrated the customer appears",
            criteria=[
                "Calm, just stating facts",
                "Frustrated but civil",
                "Very angry, strong language",
            ],
        ),
        "is_urgent": Noul(
            instructions="The message conveys urgency or time-sensitivity",
        ),
    },
)

if response.answers["is_urgent"].noul > 0.9:
    page_on_call()
```

JS：`@typesafe-ai/sdk` 的 `TypeSafeClient` + `choice()` / `noul()` / `score()`。SDK 默认对 `429` / `529` 做退避，并尊重 `retry-after`。裸 HTTP 要自己做指数退避。

钉版本：`TypeSafeClient(model="jev-1.13.0")`，或每次 `system_one(..., model="jev-1.13.0")`。阈值一旦按某版调过，**别跟着 `jev-latest` 漂**。

### 2.4 Cloudflare / Vercel

Cloudflare Workers AI 把同一份 payload 交给 `typesafe/jev`。响应示例与原生同构（`model` 仍报 `jev-1.13.0`）。

Vercel AI Gateway 模型 ID 为 `typesafe-ai/jev`（`社区`：Flavio Copes 文，价同 $0.042/M）。AI SDK **7.0.105+** 有 `experimental_evaluate`。Gateway 的 `zeroDataRetention` 是 Vercel Pro/Enterprise 选项，**不等于** TypeSafe 原生 ZDR（原生只对企业客户宣传）。请求仍会到 Vercel 再打到 TypeSafe。

---

## 3. 请求怎么写才稳

### 3.1 state：内容；questions：判断

| 形状 | 什么时候用 |
|------|------------|
| 字符串 | 单段文本、一条消息 |
| 对象 | 默认首选：票据 + 订单 + 政策各占字段 |
| 数组 | 对话轮次、记录序列 |

Jev **只吃文本**。图/音/视频先转写或抽字段。英语最好；中文能跑，官方说准确率较差——生产前用自己的语料画校准曲线，不要直接搬英文阈值。

指向对象里某一处时，在 `instructions` 里写反引号路径：`` Does `ticket.messages[0].text` request a refund? ``

### 3.2 一条问题只问一件事

坏：`Analyze this message and determine the best course of action`  
好：分别问「是否要退款」「政策是否覆盖」「愤怒程度」，代码里组合。

同一请求里的问题**互不看见对方的答案**。只有「第二枪的 state / 选项依赖第一枪」时才串行（官方三个例外：技能短名单精读、结构恢复、层级分类）。其余全部扇出，用不到的答案在代码里丢掉。加问题几乎不增加延迟，只多付问题文本那点输入 token。

Choice 把完整选项都给（最多 255），不要自己先截短名单；盖不全就加 `other`。选项相近时，用对象而不是一句话描述「是什么 / 不是什么 / 例子」。

Score 档位写情景。模型看不到档位编号，也看不到「比上一档更严重」这种邻档关系。

### 3.3 置信度怎么变成控制流

Noul：直接对 `noul` 设阈值（退款意愿 > 0.9 自动过，< 0.5 人工）。

Choice / Score：先看 `confidence` 再看点估计。官方起手三档：

```python
action = response.answers["action"]
if action.confidence < 0.5:
    route_to_human()
elif action.choice == "check_balance":
    show_balance()                          # 低风险，中等置信也可以
elif action.choice == "approve_transfer":
    if action.confidence > 0.9:
        confirm_then_execute()
    else:
        ask_user_to_confirm()               # 高风险抬门槛
```

**0.5 / 0.9 不是官方魔法数**，是示例。用自己的数据标定。Noul 的阈值不能原样搬到 Choice 的 `probabilities["yes"]`——官方 jaggedness 给过反例：同一句话 Noul=0.22 而 Choice `no`=0.99。

### 3.4 四种官方模式（名字可当设计词汇）

| 模式 | 做什么 |
|------|--------|
| Speculative fan-out | 一次打出所有可能用到的问题，代码决定读哪几条 |
| Confidence-gated routing | 答案告诉你「是什么」，confidence 告诉你「敢不敢自动做」 |
| Composite scoring | 多个原子 Score，权重在代码里；改优先级改系数，不改提示 |
| Intent routing | Jev 分流：确定性逻辑 / 专用 LLM / 人 |

Agent 环境可装官方 skill：`claude plugin marketplace add typesafe-ai/skills` 然后 `claude plugin install typesafe@typesafe-ai`；其它 agent：`npx skills add typesafe-ai/skills --skill typesafe-ai`。skill 的核心提醒就是：**别养成一问一枪**。

---

## 4. 错误、限流、成本

| HTTP | 含义 | 处理 |
|------|------|------|
| 401 | key 无效 | 换密钥 |
| 422 | body 校验失败（缺字段、问题畸形） | 读 body 里的字段路径 |
| 429 | 超限流 | 退避；SDK 默认会做 |
| 529 | 服务过载 | 同样退避，不要立刻重打 |

粗算：一封工单 + 三条问题大约几百输入 token。按 $0.042/M，**一千次调用大约几分钱**。官方 Doom 量级 10 QPS ≈ $7/小时，说明实时扇出也负担得起，但不要把它理解成「生成模型也这个价」——生成模型输出按 token 另计，Jev 输出免费是因为它几乎不吐文本。

计费只收输入。响应里仍有 `output_tokens`，OpenRouter / 原生都可能回，**单价是 0**。不要用输出 token 做成本预警主指标。

---

## 5. 工程坑清单

1. **接错协议。** Chat Completions / Responses / Messages 都不是 Jev。OpenRouter 走 `/api/alpha/decisions`；原生走 `/v1/systemone`。
2. **渠道 ID 互不通用。** `jev-latest` ≠ `~typesafe/jev-latest` ≠ `typesafe/jev` ≠ `typesafe-ai/jev`。路由表要分渠道写。
3. **别名会漂。** 响应永远带版本化 `model`。阈值、黄金集、回归都钉 `jev-1.13.0`。
4. **OpenRouter 窗口公示 32k，官方 64k/32k 双预算。** 大 state + 多问题先按更紧的那条设计。
5. **OpenRouter 厂商 FAQ 与模型页打架。** FAQ 说 OpenAI 兼容；模型页说不生成文本。以模型页 + 一次实测为准。
6. **问题互相独立。** 不要指望同一枪里后一个问题读到前一个答案。
7. **Noul 没有 confidence。** 靠近 0.5 自己当不确定；不要去 answers 里找该字段。
8. **算术恒等不成立。** `P(退款) + P(非退款)` 不必为 1；Noul 与 yes/no Choice 不可互换阈值。
9. **别让 Jev 数数、比日期、算 hex。** 抽取可以问它，比较在代码里。
10. **state 当数据，不当可信指令。** 1.13 默认不把 state 当敌对输入；注入可以撬答案。护栏场景要把准则写死，并在边角集上回归。
11. **中文阈值单独标定。** 官方：英语最佳，CJK 较差。
12. **不能微调。** 领域知识进 `state`，边界进 `criteria`。想学客户分布，官方建议把 Jev 概率当特征喂给下游经典模型（AutoResearch cookbook）。
13. **候补名单。** 原生仍是 early access；等不了就走 OpenRouter / Cloudflare / Vercel（可用性以当时账户为准）。
14. **Coding agent 容易一问一枪。** 装官方 skill，或在仓库里写死「同一 state 必须合并请求」。

---

## 6. 最小落地顺序

1. 选渠道：有 TypeSafe key 用原生 SDK；只有 OpenRouter key 用 Decisions API。
2. 把业务判断拆成 Noul / Choice / Score，state 只放事实。
3. 用 50～100 条真实样本画 `noul` / `confidence` 直方图，再定自动 / 人审 / 升级 LLM 的阈值。
4. 日志记：`model` 版本、问题 ID、点估计、全分布、`usage.input_tokens`、你实际走的分支。
5. 黄金集锁版本；`jev-latest` 只用于探索，不用于生产阈值。

---

## 7. 参考来源

- [TypeSafe API](https://docs.typesafe.ai/api) · [Quick start](https://docs.typesafe.ai/introduction/quickstart) · [Models](https://docs.typesafe.ai/models) · [State](https://docs.typesafe.ai/concepts/state)
- [Patterns](https://docs.typesafe.ai/patterns)（fan-out / confidence-routing / composite-scoring / intent-routing）
- [OpenRouter · ~typesafe/jev-latest](https://openrouter.ai/~typesafe/jev-latest) · [typesafe/jev-1.13](https://openrouter.ai/typesafe/jev-1.13)
- [Cloudflare · typesafe/jev](https://developers.cloudflare.com/ai/models/typesafe/jev/)
- Python SDK：`typesafe-sdk`（`system_one`）；JS：`@typesafe-ai/sdk`
- Agent skill：[typesafe-ai/skills](https://github.com/typesafe-ai/skills)
- 社区：[Flavio Copes · Jev deep dive](https://flaviocopes.com/jev/)（Vercel Gateway / AI SDK）

全景、原语、锯齿：[《TypeSafe 全景与 System One》](./TypeSafe全景与System-One.md)

配套 notebook：[Jev原语与置信度门闩演示.ipynb](./Jev原语与置信度门闩演示.ipynb)
