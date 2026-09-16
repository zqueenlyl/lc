# MiniMax-H3 本地部署与 API 接入

> 调研时间：2026-09-16 ｜ 配套：[《MiniMax-H3 全景与架构》](./MiniMax-H3全景与架构.md)
> 口径：`官方`=模型卡 / GitHub README / SGLang cookbook / Hugging Face diffusers 文档 / Community License；未在官方页核对的标「未核实」。
> 本页是**操作层**：checkpoint 怎么下、四套推理栈怎么选、本地 768p 与官方 2K 怎么拼、许可证雷区。

---

## 一、先锁三件事

1. **开源 ≠ 完整系统。** 本地 H3-Base 产出 768p + 立体声；`H3-Context-IR` 与 `H3-Regenerate-2K` 仍是托管 API。要对齐海螺 App / 开放平台 2K，必须走「IR API → 本地或云端 Base → Regen API」，或直接调一键创建接口。
2. **两个 variant 不要互相加载。** `fl2va` 服务 `t2va` + `fl2va`；`ref2va` 服务参考条件（含 V2V）。SGLang / vLLM 用 `--model-variant`，**不要把 `--model-path` 指到手动展开的子目录**。
3. **权重是 CFG 蒸馏的。** 没有 classifier-free guidance、没有 `negative_prompt` / `guidance_scale`。视频调度 `flow_shift=12.0`，音频 `audio_flow_shift=3.0`。每步一次前向。

---

## 二、仓库布局

Hugging Face / 原始 checkpoint（SGLang、vLLM）：

```text
MiniMaxAI/MiniMax-H3
├── model_index.json          # 仓库级入口
├── FL2VA/                    # t2va + fl2va
│   ├── model_index.json
│   ├── processor/ tokenizer/ text_encoder/
│   ├── transformer/
│   ├── visual_vae/ audio_vae/
└── Ref2VA/                   # ref2va（含 V2V）
    └── …同上结构，transformer 不同
```

diffusers 转换后把**除 Transformer 以外的组件共享一份**，布局变成：

| 子目录 | 工作流 |
|--------|--------|
| `transformer/` | `t2va`、`fl2va` |
| `transformer_ref/` | `ref2va` |
| 共享 | Visual VAE、Audio VAE、Qwen3-VL conditioner、tokenizer、processor、两套 scheduler |

官方数字（diffusers 文档）：**单个 Transformer 分区 bf16 ≈ 61.7 GB**；Qwen3-VL conditioner ≈ **62.1 GB**。`load_components()` 不带 `workflow=` 会把**两份** Transformer 都拉下来。

下载（按框架收窄，不要整仓盲拉）：

```bash
# SGLang / vLLM：原始双任务族
hf download MiniMaxAI/MiniMax-H3 \
  --include "model_index.json" "FL2VA/*" "Ref2VA/*" \
  --local-dir MiniMax-H3

# 只要文生 / 首尾帧
hf download MiniMaxAI/MiniMax-H3 \
  --include "model_index.json" "FL2VA/*" \
  --local-dir MiniMax-H3
```

diffusers **不必**预先 `hf download`：`ModularPipeline.from_pretrained("MiniMaxAI/MiniMax-H3", workflow="ref2va")` 只拉该工作流需要的子目录。

ModelScope 同源 ID：`MiniMax/MiniMax-H3`。SGLang 加 `SGLANG_USE_MODELSCOPE=true`，路径改 ModelScope ID，variant / 拓扑旗标不变。

精度：发布 checkpoint 为 **BF16**（AdaLN 相关投影在 FSDP 路径上保持 FP32，SGLang 明确说这条不牺牲数值正确性）。

---

## 三、四套推理栈怎么选

| 栈 | 适合 | 入口 |
|----|------|------|
| **ComfyUI ≥ 0.30** | 工作站试跑、节点工作流 | [官方教程](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)；模板 [T2V](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_t2v.json) / [R2V](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_r2v.json) |
| **SGLang Diffusion** | 生产 HTTP、多卡、NVIDIA / AMD 有实测菜谱 | [cookbook](https://docs.sglang.io/cookbook/diffusion/MiniMax/MiniMax-H3) |
| **vLLM** | 要 OpenAI 风格视频端点、跟现有 vLLM 集群 | [recipes.vllm.ai/MiniMaxAI/MiniMax-H3](https://recipes.vllm.ai/MiniMaxAI/MiniMax-H3) |
| **diffusers Modular** | Python 管线、单卡 offload / int8、细抠 scheduler | [HF diffusers · MiniMax-H3](https://huggingface.co/docs/diffusers/main/api/pipelines/minimax_h3) |

原则：**不要混框架的量化文件、目录布局和启动参数**，除非该指南明确写了互通。

---

## 四、SGLang：官方验证过的拓扑

安装：`uv pip install "sglang[diffusion]" --prerelease=allow`。

最小启动（README 示例，4 卡 + Ulysses4；H200 类「整模驻留」机）：

```bash
sglang serve \
  --model-path MiniMaxAI/MiniMax-H3 \
  --num-gpus 4 \
  --ulysses-degree 4 \
  --performance-mode speed \
  --host 0.0.0.0 \
  --port 30010 \
  --model-variant fl2va
```

`ref2va` 换端口、换 `--model-variant ref2va`。`speed` 把组件尽量驻留 GPU；`memory` 才走省显存放置。**不要**为了对齐官方数值打开 `torch.compile`：SGLang 写明当前 compile 路径会改数值输出，推荐 lossless 预设全部 eager。

### 4.1 官方默认菜谱（SGLang cookbook §8）

| 硬件 | 默认驻留 | 其它 |
|------|----------|------|
| B300 | 8× Ulysses8 | 8× FSDP + Ulysses8 |
| B200 | 8× Ulysses8 | 4× FSDP + Ulysses4 |
| **H200** | **4× Ulysses4** | 4× FSDP + Ulysses4 |
| **H100 80GB** | **4× TP2 + Ulysses2** | 4× TP4 + Ulysses1；4× FSDP + Ulysses4 |
| MI300X / MI355X | 8× Ulysses8 | 1/2/4 卡 scaling |
| **2× RTX 5090 32GB** | **TP2 + layerwise offload**（20 个 DiT block 驻留） | 需约 **384 GiB 级主机内存**（实测机 377 GiB） |

H100 注意：纯 Ulysses4 **装不下**完整流水线驻留；速度默认是 TP2+Ulysses2。Qwen encoder 在 `encoder-parallel=auto` 时会叠到空闲的 Ulysses 卡上，这和 DiT 的 TP **不是一回事**。

2×5090 要点：layerwise 只改放置与传输，不改 BF16/FP32 数学。Video VAE encoder 与约 577 MiB 的 Audio VAE **保持驻留**；text encoder 与 video VAE decoder 一层 prefetch、零驻留层。

Ring attention **与 H3 的 packed 多段注意力不兼容**，只用 Ulysses。

### 4.2 异步视频端点

协议是 **OpenAI 兼容的异步 `/v1/videos`**：提交 → 轮询 `status` → 下 MP4。成片契约：H.264 **24 fps** + AAC 立体声 **32 kHz**。

`target.duration_seconds` ∈ **[4, 15]**。官方验证负载常用 5 秒、短边 768、16:9 → 1344×768。

文生（T2VA）骨架：

```bash
curl -sS -X POST http://127.0.0.1:30010/v1/videos \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiniMaxAI/MiniMax-H3",
    "prompt": "…",
    "seconds": 5,
    "task": "t2va",
    "conditions": [],
    "target": {
      "short_edge": 768,
      "aspect_ratio": "16:9",
      "duration_seconds": 5.0
    },
    "num_outputs_per_prompt": 1,
    "num_inference_steps": 50,
    "flow_shift": 12.0,
    "audio_flow_shift": 3.0,
    "seed": 1101
  }'
```

FL2VA：`task=fl2va`，`conditions` 里 `type=image`、`role=keyframe`、`frame_index` ∈ `{0, -1}` 或两者。图像要当**真正的首/尾帧**用 FL2VA；只要身份 / 风格、允许重构图则改走 Ref2VA。

V2V：**没有**独立 `v2v` 任务值。启动 `ref2va`，请求仍 `task=ref2va`，条件里给视频。`type=video` 允许无声；`type=video_audio` 要求双流都在。Ref2VA **不是**像素对齐的视频编辑，没有 denoise strength，不要指望逐帧保原片。`start_time_seconds` 从长片里切一段，音画同一偏移。

### 4.3 官方测过的时延（同一套 5s / 1344×768 / 50 step / 单请求）

来源：SGLang cookbook §8，单次测量，**不是**跨机横向 SLO。

| 拓扑 | 权重 | 精度 | 流水线时延 | 峰值 / GPU |
|------|------|------|------------|------------|
| 8×B300 Ulysses8 | FL2VA | BF16 | **19.04 s** | 83.6 GB |
| 8×B300 Ulysses8 | FL2VA | FP8 | 18.03 s | 51.9 GB |
| 8×B300 Ulysses8 | Ref2VA | BF16 | 29.12 s | 84.0 GB |
| 4×H100 TP2+Ulysses2 | — | lossless | **13.25 s** | 66.0 GB |
| 2×RTX 5090 TP2 offload | FL2VA | BF16 | **559.67 s**（去噪 525 + 解码 34） | 26.3 GiB |

同一 5090 菜谱若只跑 5-step，inference ≈ 78 s——那是预览档，不是 50-step 成品质感。

`num_outputs_per_prompt>1` 会拉长墙钟（官方一例：5-step 双输出 155 s vs 单输出 78 s）。要吞吐用副本，不要指望单进程靠这个参数变快。

---

## 五、diffusers Modular

H3 **没有**经典 `DiffusionPipeline`，只有 Modular blocks。`pipe.doc` 会打印当前 workflow 的入参。

```python
from diffusers import ModularPipeline
import torch

pipe = ModularPipeline.from_pretrained("MiniMaxAI/MiniMax-H3", workflow="ref2va")
pipe.load_components(dtype=torch.bfloat16)
```

不传 `workflow=` 则一次加载两份 Transformer，按调用入参选工作流。

约束（diffusers 文档，与模型卡略有出入处已标明）：

- 24 fps；`num_frames` 向上对齐到视频 VAE 可解的 `17*n+5`，时长需落在文档写的窗口（diffusers 写 **5–15 s**，模型卡 / SGLang 写 **4–15 s**——以你用的栈报错为准）。
- 短边 768；`height`/`width` 须为 **32 的倍数**。无关键帧时默认 16:9 画布。
- 一个 `generator` 三次采样：先条件噪声，再视频噪声，再音频噪声。同一 generator 状态应得到同一音画。
- `num_inference_steps` 计的是含终端 0 的 sigma 格点，实际前向少一次。
- 小画布是最大速度杠杆：960×544 每步大约是训练画布 1344×768 的 **2.3×**（官方文档口径）。

显存：

- **单张 80GB**：`ComponentsManager.enable_auto_cpu_offload`；Hopper 上 `pipe.transformer.set_attention_backend("_flash_3_hub")` 自称约 3×。
- **24–32GB 消费卡**：对 Transformer 与 Qwen encoder 做 **int8 weight-only**（跳过若干 proj / embed），再 group offload 流式跑 DiT。这是 diffusers 文档里的官方 loader 路径，不是第三方剪枝权重。

社区流传的「12GB / 剪枝 int8 / MLX 16GB」数字**不是**这份官方 BF16 仓库的菜谱，本页不采用。

---

## 六、开放平台 API：本地 Base + 官方 IR / 2K

域名（**按量 Key 与 Token Plan、国内/国际不要混用**——providers 篇旧坑仍然成立）：

| | 国内 | 全球 |
|--|------|------|
| 控制台 | `platform.minimaxi.com` | `platform.minimax.io` |
| API `base` | `https://api.minimaxi.com` | `https://api.minimax.io` |

文档页（SPA，字段以控制台 OpenAPI 为准）：

| 能力 | 路径 slug |
|------|-----------|
| 一键创建（官方 2K 工作流） | `video-generation-v2-create` |
| 只要 IR | `video-generation-v2-h3-context-ir` |
| 768p → 2K | `video-generation-v2-regeneration` |

混合验证（官方 README「完整 2K 工作流」）：

```bash
SGLANG_DEPLOYMENT_URL="<sglang-url>"
MINIMAX_API_BASE="https://api.minimaxi.com"   # 或 https://api.minimax.io
TOKEN="<token>"
```

推荐顺序：

1. `h3-context-ir` → 得到结构化 `content.prompt`（含 `integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music` 等段）以及 `duration`、`ratio`。IR 响应里 `model` 为 `"MiniMax-H3"`，`task_type` 为 `"h3_context_ir"`。
2. 把 IR 文本交给本地 H3-Base，产出 768p MP4。
3. `regeneration`：`base_video` 用**可公开访问的 URL**（示例里的 Base64 Data URL 仅演示；生产不要这么传）。
4. 用官方仓库 `scripts/readme/` 下的 T2VA / I2VA / Ref2VA 案例做回归——每案都带「纯 API 2K / 纯 API 768p」对照片。

IR 本身也按 token 计（官方案例用量级：文生约 8.5k total、首帧图生约 23k、参考音视频约 39k）。**未在本页核实单价。**

Context-IR 的 prompt 很长，这是特性：它就是把多模态关系写成 Base 能读的「镜头剧本 + 声景 + 配乐」。本地短 prompt 跳过 IR，质量落差主要来自这里，不是引擎没装对。

提示词技能（不调外部 API，可进 Cursor / Claude Code）：

```bash
npx skills add https://github.com/MiniMax-AI/MiniMax-H3 --skill h3-prompt-writing
```

`base-en.txt` 服务文本/关键帧，`ref-en.txt` 服务 Ref2VA。其余 8 个 skill 绑 MiniMax Hub 画布，**不能**当通用 Agent skill 用。

---

## 七、工程坑清单

1. **开源 768p ≠ API 2K。** 比画质前先锁「是否过 IR / 是否过 Regen」。
2. **FL2VA / Ref2VA 权重不互通。** 首尾帧请求打到 ref2va 服务，或参考视频打到 fl2va，属于配错 variant。
3. **V2V 没有独立 task。** 只有 `ref2va` + 视频条件。
4. **音频不能当唯一输入。** 必须配图或视频。
5. **CFG 蒸馏。** 传 `guidance_scale` / 负向 prompt 会被忽略或报错，不要按 SD/Wan 习惯调。
6. **两套 scheduler。** 视频 `shift=12`、音频 `shift=3`；改一个不改另一个会音画节奏拆开。
7. **时长窗口。** 模型卡 / SGLang：4–15 s；diffusers：帧数对齐后 5–15 s。越界先查你用的栈。
8. **画布对齐。** 边长 32 倍数；默认短边 768。私自拉到 2K 不是 Regenerator，只是把 Base 硬放大。
9. **`torch.compile` 改数值。** 要对齐官方 case，保持 eager。
10. **国内/国际 base_url 与 Key 类型。** 混用表现为鉴权失败或静默打到空环境（历史坑，见 [providers MiniMax](../providers/各大厂商代表模型总览.md#36-minimax)）。
11. **错误模型。** MiniMax 原生对话接口是「HTTP 200 + `base_resp.status_code`」派；H3 视频任务走另一套异步 `status`。客户端不要用聊天解析器去拆 `/v1/videos`。
12. **许可证领土。** 美 / 欧 / 英 / 韩不在 Community License 适用领土内；对外托管要有内容防护；禁止用输出蒸馏其它模型。见架构篇 §七。
13. **必须用仓库里的 tokenizer。** Encoder 是 Qwen3-VL-32B，但 H3 加了特殊 token；不要换成上游 Qwen 原版 tokenizer。
14. **审核。** IR / 开放平台会对输入和增强 prompt 过机审。本地 Base **不会**自动带同一套护栏——对外提供服务时许可证要求你自己做。

---

## 八、验证清单（跑通了再谈优化）

本地 768p：

1. 只下一份 variant，SGLang `--model-variant` 与请求 `task` 一致。
2. T2VA 5s / 16:9 / 50 step 能下到带音轨的 MP4。
3. FL2VA 用 `frame_index=0` 的图，首帧可辨认为输入图（允许轻微运动，不应换成另一个人）。
4. Ref2VA 至少跑通「图+视频」或官方 `scripts/readme/reproducible-768p-ref2va-request.sh`。

要对齐官方 2K：

5. 同一 prompt 走 IR → Base → Regen，并与 `video-generation-v2-create` 直出片并排看（官方 README 每个 case 都给了对照）。
6. Regen 的 `base_video` 用公网 URL，不要生产传 Data URL。

---

## 九、参考来源

- [HF MiniMaxAI/MiniMax-H3](https://huggingface.co/MiniMaxAI/MiniMax-H3)
- [GitHub MiniMax-AI/MiniMax-H3](https://github.com/MiniMax-AI/MiniMax-H3)（含 `README.zh-CN.md`、复现脚本）
- [SGLang cookbook · MiniMax-H3](https://docs.sglang.io/cookbook/diffusion/MiniMax/MiniMax-H3)
- [diffusers · MiniMax-H3](https://huggingface.co/docs/diffusers/main/api/pipelines/minimax_h3)
- [vLLM recipes](https://recipes.vllm.ai/MiniMaxAI/MiniMax-H3)
- [ComfyUI 教程](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)
- 创建 / IR / Regen API：[全球文档](https://platform.minimax.io/docs/api-reference/video-generation-v2-create) ｜ [国内文档](https://platform.minimaxi.com/docs/api-reference/video-generation-v2-create)
