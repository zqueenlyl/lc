# Qwen-Omni 实时接入与工程实践

> 对象：阿里云百炼（DashScope）Qwen-Omni **Realtime** 系列 ｜ 整理时间：2026-09-11
> 一手来源：官方《Python SDK 调用 Qwen-Omni 实时模型接口与参数》《qwen3-omni-flash-realtime 模型信息》
> 说明：本文只写**官方文档明确给出**的接口语义与限制；官方文档内部存在不一致处（如 `turn_detection_threshold` 默认值）会显式指出。成本章节的金额为**基于官方单价 + 官方换算规则的估算**，已标注。

---

## 一、选型决策：先选档位，再写代码

```
要用 Function Calling / 联网搜索 / 语义 VAD / 细粒度音频格式？
├─ 是 → qwen3.5-omni-plus-realtime 或 qwen3.5-omni-flash-realtime
└─ 否 → 需要"口语化输出"？ 
        ├─ 是 → qwen3-omni-flash-realtime
        └─ 否 → qwen-omni-turbo-realtime（注意：生成参数不可调）
```

**为什么第一步就问这个**：`tools`、`enable_search`、`semantic_vad`、`idle_timeout_ms`、`input_audio_config` 这些能力**只在新档位生效**，旧档位不是"参数不生效"，而是**根本不支持**。先定档位能省掉一轮重构。

| 能力 | `qwen3.5-omni-*`-realtime | `qwen3-omni-flash-realtime` | `qwen-omni-turbo-realtime` |
|------|:---:|:---:|:---:|
| `tools`（Function Calling） | ✅ | ❌ | ❌ |
| `enable_search`（与 `tools` 互斥） | ✅ | ❌ | ❌ |
| `semantic_vad` | ✅ | ❌ | ❌ |
| `input_audio_config` / `output_audio_config` | ✅ | ❌ | ❌ |
| `idle_timeout_ms`（仅 server_vad） | ✅ | ❌ | ❌ |
| `smooth_output`（口语化） | ❌ | ✅ | ❌ |
| 生成参数可调 | ✅ | ✅ | ❌ |
| 默认音色 | `Tina` | `Cherry` | `Chelsie` |

---

## 二、连接与会话初始化

| 项 | 值 |
|----|-----|
| SDK | DashScope Python SDK **≥ 1.26.5** |
| 入口类 | `from dashscope.audio.qwen_omni import OmniRealtimeConversation` |
| 回调接口 | `OmniRealtimeCallback`：`on_open()` / `on_event(message)` / `on_close(close_status_code, close_msg)` |
| 端点（北京） | `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime` |
| 端点（新加坡） | `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime` |
| 旧端点 | `wss://dashscope.aliyuncs.com`（北京）、`wss://dashscope-intl.aliyuncs.com`（新加坡）——**仍可用，官方建议迁移到业务空间专属域名**（性能与稳定性更佳） |

> `{WorkspaceId}` 需替换为业务空间 ID。**建议直接上专属域名**，避免后续迁移。

### 2.1 关键方法

| 方法 | 作用 | 注意 |
|------|------|------|
| `connect()` | 建立连接 | 返回"会话已创建"类事件 |
| `update_session(...)` | 更新会话配置 | 服务端校验参数，返回 `session.updated` |
| `append_audio(audio_b64)` | 追加 base64 音频到云端缓冲区 | —— |
| `append_video(video_b64)` | 追加 base64 图片到云端视频缓冲区 | 视频的本质就是**抽帧上传** |
| `clear_appended_audio()` | 清空已接收音频 | 返回 `input_audio_buffer.cleared` |
| `commit()` | 提交缓冲区 | **不触发模型响应**；**缓冲区为空会报错** |
| `create_response(instructions, output_modalities)` | 指示服务端创建响应 | 流式返回 `response.*` 事件 |
| `cancel_response()` | 取消进行中的响应 | **无响应可取消时服务端报错** |
| `create_item(item)` | 发送 `conversation.item.create` | 工具调用场景回传结果（`type="function_call_output"` + `call_id` + `output`） |
| `close()` | 终止任务并关连接 | —— |
| `get_session_id()` / `get_last_response_id()` | 取会话/响应 ID | 用于可观测与问题定位 |

---

## 三、会话配置（`update_session`）

| 分组 | 参数 | 说明 |
|------|------|------|
| 输出 | `output_modalities` | `[TEXT]` 或 `[TEXT, AUDIO]` |
| 输出 | `voice` | 音色，见档位默认值表 |
| 输出 | `instructions` | 系统提示（人设/风格） |
| 音频 | `input_audio_config` / `output_audio_config` | 格式 `pcm` / `wav`；采样率 `8000/16000/24000/48000`；输入默认 16 kHz、输出默认 24 kHz。**仅 3.5 系列** |
| 音频 | `input_audio_format` / `output_audio_format` | 历史兼容字段（默认 `PCM_16000HZ_MONO_16BIT` / `PCM_24000HZ_MONO_16BIT`）。新接入建议改用 `*_config` |
| 语音识别 | `enable_input_audio_transcription` | 是否开启输入音频转写 |
| 语音识别 | `input_audio_transcription_model` | **固定为 `qwen3-asr-flash-realtime`，不支持修改** |
| 轮次 | `enable_turn_detection` | 是否开启服务端 VAD |
| 轮次 | `turn_detection_type` | `server_vad`（默认，声学）/ `semantic_vad`（语义，**仅 3.5 系列**） |
| 搜索 | `enable_search`、`search_options` | 如 `{'enable_source': True}` 返回来源列表。**仅 3.5 系列；与 `tools` 不兼容** |
| 工具 | `tools` | `type="function"` + `function.name/description/parameters`。**仅 3.5 系列**；命中工具调用时模型**不生成音频**，只返回调用参数 |
| 生成 | `temperature` / `top_p` / `top_k` / `max_tokens` / `repetition_penalty` / `presence_penalty` / `seed` / `smooth_output` | turbo 系列**不可调** |

### 3.1 生成参数默认值（官方表）

| 参数 | Qwen3.5-Omni-Realtime | Qwen3-Omni-Flash-Realtime | Qwen-Omni-Turbo-Realtime |
|------|:---:|:---:|:---:|
| `voice` | `Tina` | `Cherry` | `Chelsie` |
| `temperature` | 0.7 | 0.9 | 1.0 |
| `top_p` | 0.8 | 1.0 | 0.01 |
| `top_k` | 20 | 50 | 20 |
| `repetition_penalty` | 1.0 | 1.05 | 1.05 |
| `presence_penalty` | 1.5 | 0.0 | 0.0 |

> `smooth_output`：`True` 口语化 / `False` 书面化 / `None` 自动，**仅 Qwen3-Omni-Flash-Realtime 支持**。

---

## 四、音视频输入的工程约束（硬限制）

### 4.1 图像/视频帧

| 项 | 官方要求 |
|----|----------|
| 格式 | **JPG / JPEG** |
| 分辨率 | 建议 480P 或 720P，**最大 1080P** |
| 单帧体积 | base64 编码后 **≤ 256 KB**（建议原始图片 ≤ 190 KB） |
| 发送频率 | 建议 **1 张/秒**；推荐帧率 **1 fps 或 2 fps** |

**语义**：云端以**音频为时间轴**，图片按**发送时刻**插入音频时间轴——所以"视频理解"= 在正确的时间点插入正确的帧，**采样节奏比单帧画质更影响理解质量**。

### 4.2 音频

| 项 | 官方要求 |
|----|----------|
| 分包 | 按 **100 ms 一包**发送 |
| 格式 | pcm / wav（3.5 档位可配采样率；旧档位用 `PCM_16000HZ_MONO_16BIT` 等常量） |
| 单事件上限 | 关闭 VAD 时由客户端决定每事件音频量，**单事件 ≤ 15 MiB** |

### 4.3 视频开关

可在实时交互中**随时开关视频输入**（不是会话级开关），适合"只在需要时看画面"的成本敏感场景。

---

## 五、VAD 与打断机制

### 5.1 两种模式（由 `enable_turn_detection` 控制）

| 维度 | 开启 VAD（`True`） | 关闭 VAD（Manual） |
|------|---------------------|---------------------|
| 轮次判断 | 云端 VAD 自动判断用户一句话结束 | **自行**判断一轮输入结束 |
| 触发响应 | **自动**调用模型并下发文本+语音 | 手动 `commit()` + `create_response()` |
| 客户端 `commit` | 无需发送 | 必须 |
| 回复期间输入 | **音视频可继续输入**，无需中断 | **必须停止音视频输入**，回复结束才能下一轮 |
| 打断 | 检测到用户说话**立即打断**本轮回复 | 只能通过 `cancel_response()` 主动取消 |
| 适用 | 实时通话、自然对话 | 精确控制时序（如预录素材回放、自动化测试） |

> **关键认知**：关闭 VAD 就等于主动退回**半双工**（回复期间不能输入）。如果目标是"像人一样随时插话"，必须开 VAD，并接受"误判抢话"的调优成本。

### 5.2 VAD 相关参数

| 参数 | 说明 |
|------|------|
| `turn_detection_type` | `server_vad`（默认，基于声学特征）/ `semantic_vad`（基于语义有效性，可过滤无意义语音与背景音；**仅 Qwen3.5-Omni-Realtime 系列**） |
| `turn_detection_threshold` | ∈ [-1.0, 1.0]，越接近 -1 噪音越易被当语音。**文档不一致**：正文写默认 0.5、方法签名默认 0.2 → **建议显式指定** |
| `turn_detection_silence_duration_ms` | 判定"说完"的静音时长，默认 **800**，范围 [200, 6000] |
| `prefix_padding_ms` | 方法签名默认 **300**（把语音起始前的一小段一并纳入） |
| `turn_detection_param` | `{'idle_timeout_ms': N}`：静默超时后主动引导继续对话，范围 [5000, 30000]，**仅 qwen3.5-omni-plus/flash-realtime 且 server_vad 时生效** |

### 5.3 调参经验

| 目标 | 动作 | 副作用 |
|------|------|--------|
| 响应更快 | 调小 `silence_duration_ms` | 用户短暂停顿时误判抢话 |
| 少被打断误伤 | 调大 `silence_duration_ms` | 对话变"卡" |
| 抗背景噪音 | 用 `semantic_vad`（3.5） | 需要新档位 |
| 避免回声自打断 | **戴耳机**（官方建议） | —— |

---

## 六、交互时序（状态机）

```
connect()
  │  ← 会话创建事件
update_session(instructions, voice, output_modalities, VAD 配置…)
  │  ← session.updated
  ├─ append_audio(b64)  ← 100ms/包，持续注入
  ├─ append_video(b64)  ← 1~2 fps，按需注入（可随时开关）
  │
  ├─[开 VAD] 服务端自动判定轮次结束 → 自动推理 → response.* 流式事件
  │
  └─[关 VAD] commit() → create_response() → response.* 流式事件
                                    │
                                    └─ 用户插话 → cancel_response()
  │
  └─[工具调用场景] response.function_call_arguments.done →
       create_item(type="function_call_output", call_id=…, output=…) → 再 create_response()
```

**事件回调要点**：所有服务端事件都从 `on_event(message)` 进来，需按 `type` 分派；`response.*` 为流式增量，需自行拼接（文本增量与音频增量分别累积）。

---

## 七、成本估算与优化杠杆

**官方单价**（`qwen3-omni-flash-realtime`，华北2 北京，原价 / 百万 tokens）：文本输入 2.2 ｜ 音频输入 18.9 ｜ 图片·视频输入 3.9 ｜ 文本输出 8.3（输入仅文本）/ 15.2（输入含多模态）｜ **文本+音频输出 75.1**。

**官方换算规则**：音频 token ≈ `时长(秒) × 12.5`；图片每 `32×32` 像素 = 1 token，单图最少 4、默认上限 **1280**。

### 7.1 估算（本文推算，非官方报价）

| 输入项 | 计算 | 折算 |
|--------|------|------|
| 音频输入 | 60 s × 12.5 = 750 tokens | ≈ **0.014 元/分钟** |
| 语音输出（模型说话） | 60 s × 12.5 = 750 tokens × 75.1 | ≈ **0.056 元/分钟** |
| 视频帧 @720P·1 fps | 900 tokens/帧 × 60 | ≈ **0.21 元/分钟** |
| 视频帧 @720P·2 fps | 同上 ×120 | ≈ **0.42 元/分钟** |
| 视频帧 @1080P·1 fps | 触发 1280 tokens/帧上限 × 60 | ≈ **0.30 元/分钟** |

**结论**：**视频帧是成本主项（占 70%+），音频几乎可忽略**。三个优化杠杆按性价比排序：

1. **降帧率**（2 fps → 1 fps 直接省一半）
2. **按需开关视频**（只在需要看画面时注入帧）
3. **控分辨率**（720P 已够；1080P 反而会撞 token 上限，且更容易超 256KB/帧体积限制，**收益为负**）

> 对比替代方案：智谱 GLM-Realtime 按**分钟**计费（视频档 1.2 元/分钟起），阿里按**帧 token** 计费——后者把"帧率"变成可调的成本旋钮，做成本-体验权衡时更灵活。

---

## 八、坑清单

1. **端到端模型不产出"输入音频的转写"**：文本输出是"对输入的回答"，不是转写。要做字幕/记录必须另开 `enable_input_audio_transcription`（固定 `qwen3-asr-flash-realtime`）。
2. **`tools` 与 `enable_search` 不可同时开启**且仅 3.5 档位支持——想"先搜再答"要走 `enable_search` 或自行编排工具。
3. **`commit()` 在缓冲区为空时会报错**；`cancel_response()` 在无可取消响应时也会报错 → 调用前做状态判断，别裸调。
4. **关闭 VAD 后回复期间必须停输入**，否则语义混乱——这是最容易"看起来能跑、实际答非所问"的坑。
5. **图片必须 JPG/JPEG**，其它格式（PNG/WebP）需自行转码；base64 ≤256KB 是硬限制，**超了直接被拒**。
6. **`turn_detection_threshold` 默认值文档自相矛盾**（0.5 vs 0.2）→ 生产环境**显式指定**，别吃默认值。
7. **开 VAD + 外放 → 回声触发自打断**：官方明确建议戴耳机。
8. **旧档位不能改 `temperature` 等生成参数**（turbo 系列），别把"调参无效"当 bug 排查。
9. **`input_audio_config` 只在 3.5 档位生效**，旧档位静默沿用 legacy 字段——迁移时音频采样率不会自动跟随。
10. **多模态输入会让文本输出单价从 8.3 涨到 15.2**；如果只是纯文本闲聊，别顺手开视频帧，成本翻倍。

---

## 九、与其它 Realtime 实现的事件对照

三家的实时协议都朝 OpenAI Realtime 的语义靠拢（`session.update` / `input_audio_buffer.append` / `response.create` / `response.audio.delta`），迁移时主要改**端点、鉴权、字段名**：

| 语义 | Qwen-Omni（百炼） | GLM-Realtime（智谱） | OpenAI Realtime |
|------|-------------------|----------------------|-----------------|
| 会话配置 | `update_session()` | `session.update` | `session.update` |
| 推音频 | `append_audio` | `input_audio_buffer.append` | `input_audio_buffer.append` |
| **推视频帧** | `append_video` | `input_audio_buffer.append_video_frame` | （视频能力弱） |
| 提交轮次 | `commit()` | `input_audio_buffer.commit` | `input_audio_buffer.commit` |
| 触发响应 | `create_response()` | `response.create` | `response.create` |
| 打断 | `cancel_response()` | `response.cancel` | `response.cancel` |
| 工具结果回传 | `create_item(function_call_output)` | `conversation.item.create` | `conversation.item.create` |

→ **迁移成本主要在"能力矩阵"而非协议**：字段能对上，但 `tools`/`semantic_vad`/音频格式配置在哪个档位可用，三家各不相同（详见 [GLM 接入笔记](../glm/音视频通话接入与工程实践.md)）。

---

## 十、参考来源

1. [Python SDK 调用 Qwen-Omni 实时模型接口与参数（阿里云百炼）](https://help.aliyun.com/zh/model-studio/omni-realtime-python-sdk) —— 端点、方法、会话参数、VAD、限制、档位能力矩阵
2. [qwen3-omni-flash-realtime 模型信息（阿里云百炼）](https://help.aliyun.com/zh/model-studio/qwen3-omni-flash-realtime) —— 上下文、单价、限流、快照、不支持项
3. [Qwen-Omni 模型说明（阿里云百炼）](https://help.aliyun.com/zh/model-studio/qwen-omni) —— 音频/图片 token 换算规则
4. 官方 GitHub 示例（音频对话 / 音视频对话 / 本地素材 Manual 模式三份）

---

## 相关笔记

- [Qwen-Omni系列全景调研.md](./Qwen-Omni系列全景调研.md) —— 先搞清三条产品线再动手
- [Qwen3-Omni技术文档.md](./Qwen3-Omni技术文档.md) —— 开源权重的架构与自部署约束
- [GLM 音视频通话接入与工程实践](../glm/音视频通话接入与工程实践.md) —— 同一赛道另一家 API 的对照实现

---

*文档完 · 2026-09-11*
