# runtime · 运行与加速

> **定位**：决定**跑得多快 / 多省 / 本地 / 实时**。
> **口诀**：「讲引擎 / 显存 / 延迟 / 量化 / 实时」→ 归这。

上级索引：[../README.md](../README.md) ｜ 学习地图：[../learning-path.md](../learning-path.md)

## 专题

| 专题 | 一句话 | 入口 |
|---|---|---|
| **本地推理运行时** | llama.cpp / Ollama / LM Studio / MLX：安装、参数、本地 API、实测 | [local-inference/](./local-inference/) |
| **Speculative Decoding** | 小模型草稿 + 大模型一次校验，加速解码 | [speculative-decoding/](./speculative-decoding/) |
| **Voice / Realtime** | 双向音视频流，延迟预算 &lt; 500ms | [voice-realtime/](./voice-realtime/) |

## 三件事的分工

| 专题 | 回答的问题 | 手段 |
|---|---|---|
| local-inference | 「怎么在本机跑起来」 | 引擎选型 / GGUF 量化 / 显存与 KV Cache / 排错 |
| speculative-decoding | 「同样硬件怎么跑更快」 | 解码策略（草稿 + 校验） |
| voice-realtime | 「延迟怎么压到 500ms 内」 | 流式协议 + 端到端语音模型 |

## 原理纵深（按序）

- 推理解码与 KV Cache → [../foundation/transformer/环节10-推理解码与KV缓存详解.md](../foundation/transformer/环节10-推理解码与KV缓存详解.md)
- 服务化与推理引擎（vLLM / SGLang / PagedAttention / 连续批处理） → [../foundation/transformer/环节11-服务化与推理引擎详解.md](../foundation/transformer/环节11-服务化与推理引擎详解.md)

## 相邻大类

- 模型本体 → [../foundation/](../foundation/)
- 上生产 → [../reliability/](../reliability/)
