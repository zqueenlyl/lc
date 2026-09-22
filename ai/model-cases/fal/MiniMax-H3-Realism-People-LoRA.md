# MiniMax-H3 Realism People LoRA

> 调研时间：2026-09-17 ｜ 范围：**fal** 组织发布的社区适配器 [`fal/MiniMax-H3-Realism-People-LoRA`](https://huggingface.co/fal/MiniMax-H3-Realism-People-LoRA)
> 组织身份见 [《fal 全景与生态》](./fal全景与生态.md)。基座是 MiniMax [`MiniMaxAI/MiniMax-H3`](https://huggingface.co/MiniMaxAI/MiniMax-H3)，规格见 [《MiniMax-H3 全景与架构》](../minimax/MiniMax-H3全景与架构.md)。
> 口径：本页「官方」= fal 模型卡 + fal 训练指南（Lovis Odin，2026-08-10）。凡两份材料打架，**以 fal 模型卡记载的已发布权重为准**，指南里的超参当训练过程记录。
> LoRA 公式对照：[PEFT / LoRA](../../foundation/peft-lora/README.md)（`W′ = W + γ · B A`）。本地怎么把 H3 **基座**拉起来见 [部署篇](../minimax/MiniMax-H3本地部署与API接入.md)。

---

## 一、摘要（TL;DR）

1. **这是一份人像写实 LoRA，不是新基座。** 底座仍是 33B H3 Omni Transformer；适配器只改共享注意力投影（融合 QKV：`diffusion_model.blocks.N.attn.qkv_proj`），文件约 **131 MB**。触发词 `r34l1sm`。
2. **一份权重覆盖 T2V / I2V / R2V。** 因为只碰各任务共用的注意力，不碰任务专用 conditioner。本地仍要按 FL2VA / Ref2VA 加载对应 H3 checkpoint，LoRA 是挂上去的皮肤，不是第三份基座。
3. **发布配方是后翻盘的。** 现网：`rank 32`、`1500` step、**高分辨率桶**。前一版（及 08-10 训练指南当时的胜出配方）是 `rank 16` / `5000` / medium。作者明确写：不是最高 rank、也不是最长 run 赢了，**训练分辨率更关键**——皮肤毛孔、发丝、胶片颗粒落在高频，低分桶的 latent 几乎带不上，适配器没东西可学。
4. **评测协议是同 prompt、同 seed、LoRA on vs off。** 触发词两边都写，所以效果不是触发词本身。模型卡放出 19 对、按保留顺序排列，自称不是从更大渲染批次里挑的。
5. **许可证跟基座走 MiniMax H3 Community License**（领土排除美 / 欧 / 英 / 韩、蒸馏禁令、营收门槛）。社区 LoRA 不另开协议。

**核心判断**：H3 已经是强泛化视频模型；这份适配器做的是「把分布推向真人特写」——皮肤别被抹平、表情别僵、光像片场、运镜略手持——并保住 H3 原生同步立体声。它是把 [PEFT 课](../../foundation/peft-lora/环节00-总揽与环节导航.md) 里「信任底座、只沿低维轨道搜」落到视频 DiT 上的现场样本：数据 176 条精修实拍、十六组配置人评、同一套 `W_eff = W + lora_B @ lora_A`。

---

## 二、它在 H3 系统里的位置

```
自由多模态输入
        │
        ▼
┌───────────────────┐     托管，未开源
│  H3-Context-IR    │
└─────────┬─────────┘
          ▼
┌───────────────────┐     开源 Base（33B）
│  H3-Base          │◄── 本 LoRA 挂在这里的共享 attn.qkv_proj
│  + People LoRA    │     默认仍 768p + 32 kHz 立体声
└─────────┬─────────┘
          ▼
┌───────────────────┐     托管，未开源
│ H3-Regenerate-2K  │     LoRA 不替代 Regen；2K 观感仍看你过不过这一段
└───────────────────┘
```

| 项 | 事实 |
|----|------|
| 发布方 | **fal**（作者 Lovis Odin），**不是 MiniMax** |
| 基座仓库 | MiniMax 官方 [`MiniMaxAI/MiniMax-H3`](https://huggingface.co/MiniMaxAI/MiniMax-H3) |
| 前代 | `MiniMax-H3-Realism-LoRA`；本版在更大、更偏人的数据集上重训 |
| 文件 | `h3-realism-people-t2v-i2v-r2v.safetensors`（约 131 MB） |
| 触发词 | `r34l1sm`（realism 的 leetspeak） |
| 强度 | `scale=1.0` 为设计点；`0.6–0.8` 轻涂 |

> **选型坑**：拿「开源 768p + 本 LoRA」去和海螺 App / 开放平台 2K 片比人像，比的仍是**系统**（有没有 IR、有没有 Regen），不是 LoRA 单独的能力。

---

## 三、它改什么、不改什么

模型卡口径：MiniMax H3 已经是强通用视频模型。本适配器把分布推向**以人为中心的镜头**——肖像、脸、干活的手、人群、日常角色。具体观感：

| 推 | 保 |
|----|----|
| 特写脸站得住；皮肤留纹理而不是磨皮 | H3 原生**音画同步立体声**（适配器不另接 vocoder） |
| 眼神与微表情连贯 | 时长 / 帧率 / 默认短边仍是 H3-Base 的 4–15 s、24 fps、768 |
| 光像片场；运镜带一点手持纪录片感 | 不宣称提升 2K、不宣称换 Context-IR |

**只改共享注意力**是工程关键：H3 的 Attention / FFN 没有模态专用分支（见 [架构篇](../minimax/MiniMax-H3全景与架构.md) §4.2），LoRA 键名是标准 H3 布局 `diffusion_model.blocks.N.attn.qkv_proj`（融合 QKV）。因此：

- ComfyUI 的 Load LoRA 可以直接吃 `.safetensors`，不必转换；
- 同一份文件能挂在文生、图生、参考生上；
- 推理栈只要会做 `W_eff = W + lora_B @ lora_A` 就能用——与 [环节 04](../../foundation/peft-lora/环节04-低秩适配公式详解.md) 同一行公式，这里的 `scale` 就是 γ。

FL2VA 与 Ref2VA 仍是**两份 Transformer checkpoint**（[部署篇](../minimax/MiniMax-H3本地部署与API接入.md) §一）。LoRA 不是把它们合并，只是键名布局兼容，加载哪份 variant 仍由任务决定。

---

## 四、怎么用

权重本身不绑托管。能跑 H3 的地方就能挂。

### 4.1 本地 ComfyUI

1. 把文件丢进 `models/loras/`：

```bash
wget https://huggingface.co/fal/MiniMax-H3-Realism-People-LoRA/resolve/main/h3-realism-people-t2v-i2v-r2v.safetensors
```

2. 在模型加载器与 sampler 之间插 **Load LoRA**。
3. prompt **开头**写触发词，再写场景。scale `1.0`；要轻一点用 `0.6–0.8`。

H3 工作流本身仍按 [部署篇 §三](../minimax/MiniMax-H3本地部署与API接入.md) 的官方模板（T2V / R2V），本 LoRA 只是多一个节点。

### 4.2 自建推理

任何能对 H3 应用 LoRA 的栈。有效权重：

```text
W_eff = W + scale · (lora_B @ lora_A)
```

`scale=0` 在数学上等于没挂适配器（fal 指南：他们核对过 zero-scale 与完全不加载 LoRA 只差编码噪声）。这是后面 A/B 评测能成立的前提。

### 4.3 托管（可选，不是绑定）

fal 提供带 `loras[]` 的 H3 端点，只是选项之一：

| 任务 | 端点 |
|------|------|
| 文生 | [minimax/h3/text-to-video/lora](https://fal.ai/models/minimax/h3/text-to-video/lora) |
| 图生 | [minimax/h3/image-to-video/lora](https://fal.ai/models/minimax/h3/image-to-video/lora) |
| 参考生 | [minimax/h3/reference-to-video/lora](https://fal.ai/models/minimax/h3/reference-to-video/lora) |

请求骨架（模型卡原文）：

```json
{
  "prompt": "r34l1sm, a young woman faces the camera in a quiet apartment at dusk, soft window light on her skin, shallow depth of field, subtle handheld sway, cinematic, photorealistic",
  "loras": [
    {
      "path": "https://huggingface.co/fal/MiniMax-H3-Realism-People-LoRA/resolve/main/h3-realism-people-t2v-i2v-r2v.safetensors",
      "scale": 1.0
    }
  ],
  "duration": 5,
  "resolution": "768P"
}
```

---

## 五、训练：176 条、十六组、人评翻盘

### 5.1 数据

| 项 | 模型卡 / 指南口径 |
|----|-------------------|
| 规模 | **176** 条人工精选实拍，围绕人：肖像、脸、工人、运动员、日常角色；从第一版 Realism 里最强的镜头扩来 |
| 筛选比 | 指南：253 候选里留下 176（手搓一键过片页）；扔掉的就是会污染风格的镜头 |
| 帧率 | 全部规范到严格 **24.000 fps**（H3 是 24 fps 模型；23.976 / 25 / 30 都要重采样） |
| 慢动作 | 审计时约 **2/3** 人像素材是 50–60 fps 拍、25–30 放的慢镜；用视觉 LLM 分类后 `setpts` + `atempo` 拉回自然速度。不处理就会把「飘」写进适配器 |
| 字幕 | 结构化场景 caption（主体 / 动作 / 场景 / 光 / 机位）；触发词只走一条路：要么 `trigger_phrase`，要么写进 txt，**禁止两边都写** |
| 音频 | **留音轨**。H3 音画联合训练，静音或噪声就是在教静音或噪声 |

分辨率桶（指南实践，非模型卡强制）：16:9 `1280×704`、scope `1280×544`、近方形 `960×704`，边长 32 倍数、面积接近、scale-to-fill + 中心裁。随机混分辨率会浪费训练信号。

### 5.2 现网权重 vs 指南当时的胜出配方

fal 用自家 H3 trainer。模型卡：十六组（步数、rank、学习率、训练分辨率）用**同 prompt、同 seed、adapter on vs off** 并排人评。

| | 发布权重（模型卡，以它为准） | 08-10 指南记载的当时胜出 |
|--|------------------------------|---------------------------|
| rank | **32** | 16（当时盲评里 16 打赢 32 / 64） |
| steps | **1500** | 5000，lr `1e-4` 慢炖 |
| 分辨率桶 | **high** | medium（当时认为 high 对 768P 推理不值） |
| 数据集 | 176 人像 | 先 53 条十一组，再 176 条五组 |

HF commit 写明替换关系：`rank 32 / 1500 / high` **was** `rank 16 / 5000 / medium`。模型卡后补的解释是机制性的：皮肤、毛孔、细发、颗粒活在**高频**；低训练桶的 latent 几乎不携带它们，适配器学不到。

这不否定指南其余结论，只说明**最后一次人评改了超参优先级**：

- 步数要跟数据量走：53 条时 1500 赢、5000 过拟合；数据扩到 176 后长 run 才值。现网又回到 1500，但是换了高分桶。
- rank 不是越大越好。风格适配器指南默认「很少需要超过 16」；人像高频细节最终选了 32。文件大约 131 MB，更高 rank 会到 2–4×。
- 评测只认 paired A/B。换 LoRA 或换 scale 之后，同 seed **不会**得到同一构图——每步去噪都会放大权重差。要比分布和细节，不要拿单帧对位。

### 5.3 若要自己训（指南操作层，非本仓库菜谱）

fal 四个 trainer 与推理任务对齐，按 step 计费：

| Trainer | 任务 |
|---------|------|
| `minimax/h3/t2v/trainer` | 文生 + 音频 |
| `minimax/h3/i2v/trainer` | 图生（首帧条件） |
| `minimax/h3/flf2v/trainer` | 首尾帧 |
| `minimax/h3/ref2va/trainer` | 参考视频 + 图 → 音视频 |

数据 zip：`01.mp4` 配 `01.txt`，10–200 条短片（最佳区间约 50–200），3–15 秒；先 `debug_dataset: true` 看预处理，再便宜的 1000-step，再并行扫几组。帧数须满足 `frames % 17 == 5`（22, 39, 56, 73, 90, 107, 124）——与 H3 VisualVAE 的时间对齐同一类约束（[部署篇](../minimax/MiniMax-H3本地部署与API接入.md) diffusers：`17*n+5`）。

默认超参（**trainer 默认，不是本 LoRA 发布值**）：steps 2000、lr `2e-4`、rank 32、resolution `medium`、73 帧。风格适配建议先从 rank 16、lr `2e-4` 起；慢炖用 `1e-4` + 更长 steps。

墙钟量级（指南，含排队）：2000-step t2v ~1.5 h；5000-step rank16 ~2.5 h。单价以 trainer 页为准。训完立刻把 `.safetensors` 拉回自己的桶——CDN 临时 URL 会过期。

---

## 六、工程坑清单

1. **LoRA ≠ 完整 H3 系统。** 本地仍是 768p Base；2K / IR 该走 API 还是走 API。
2. **触发词两边都写，A/B 才公平。** 模型卡 19 对就是这么做的；效果来自权重，不是咒语。
3. **`scale=0` 才是对照组。** 不要用「换一条不写触发词的 prompt」当对照。
4. **同 seed 不同 LoRA ≠ 同构图。** 去噪逐步分叉。人评要看一批 prompt，不要看一对。
5. **FL2VA / Ref2VA checkpoint 仍要配对任务。** 一份 LoRA 文件能挂两种，但不代替选对 variant。
6. **键名是融合 QKV 的 H3 布局。** 别拿 SD/Wan/Flux 的 LoRA 转换脚本硬转；作者说与其它能工作的 H3 LoRA 同一套键。
7. **慢镜头会写进运动先验。** 生成「发飘」先查训练集 fps，再查推理参数。
8. **静音素材会教静音。** 联合音画模型没有「画面 LoRA、声音原样」的免费午餐；本卡只说保住同步，没说音频风格不变。
9. **触发词不要双写。** `trigger_phrase` 与 caption 文件只留一条，否则伤遵循。
10. **许可证跟基座。** 美 / 欧 / 英 / 韩不在 Community License 领土内；禁止用 H3 或其输出（含本 LoRA 出片）蒸馏其它模型；对外托管仍要内容防护。见 [架构篇](../minimax/MiniMax-H3全景与架构.md) §七。
11. **训练素材版权。** 指南原文：只用你有权拿来训练的片子。人像写实 LoRA 的肖像权 / 深度伪造风险比风景 LoRA 高一档。

---

## 七、未披露边界

| 项 | 状态 |
|----|------|
| 十六组配置的完整超参表（每组 rank / lr / 分辨率 / 帧数） | 未公开，只有胜出配方与若干定性结论 |
| 高分辨率桶的具体像素 | 只写 high vs medium；指南的 1280×704 等是**数据预处理桶**，不等于 trainer 的 `resolution=high` 内部桶 |
| LoRA 是否覆盖全部 DiT block、α / dropout | 未写；只确认目标模块是共享 `attn.qkv_proj` |
| 同一文件在 FL2VA 与 Ref2VA 上是否数值对齐 | 宣称任务覆盖，未给两侧 A/B |
| 对 2K Regeneration 的增益 | 未测 / 未宣称 |
| 与前代 `MiniMax-H3-Realism-LoRA` 的逐项人评表 | 只说 successor + 更大偏人数据集 |
| 训练价（美元/step） | 指南写看 trainer 页，本快照不记 |

---

## 八、和本库其它页怎么接

| 页 | 这份案例补的那一块 |
|----|-------------------|
| [H3 全景与架构](../minimax/MiniMax-H3全景与架构.md) | 基座 33B、联合音画、开源只给 Base |
| [H3 本地部署与 API](../minimax/MiniMax-H3本地部署与API接入.md) | ComfyUI / SGLang / 768p vs 2K；本页只多一个 Load LoRA |
| [fal 全景与生态](./fal全景与生态.md) | 平台身份：托管推理 / trainer / 发 LoRA，不是模型实验室 |
| [PEFT / LoRA](../../foundation/peft-lora/README.md) | 现场样本：r 不是越大越好、训练分辨率决定高频能不能进 latent、同 seed A/B |
| [视频生成详解](../../foundation/video/视频生成详解.md) | 可控生成用适配器，不另训专家 |

---

## 九、参考来源

**发布物**

- [Hugging Face · fal/MiniMax-H3-Realism-People-LoRA](https://huggingface.co/fal/MiniMax-H3-Realism-People-LoRA)
- 权重：`https://huggingface.co/fal/MiniMax-H3-Realism-People-LoRA/resolve/main/h3-realism-people-t2v-i2v-r2v.safetensors`
- 前代：[fal/MiniMax-H3-Realism-LoRA](https://huggingface.co/fal/MiniMax-H3-Realism-LoRA)

**训练过程**

- [How to Train a LoRA for MiniMax H3](https://fal.ai/learn/devs/how-to-train-a-lora-for-minimax-h3)（Lovis Odin，2026-08-10）。指南里 rank 16 / 5000 / medium 是当时胜出；**现网权重以模型卡为准**。

**基座**

- [MiniMaxAI/MiniMax-H3](https://huggingface.co/MiniMaxAI/MiniMax-H3)
- [MiniMax H3 Community License](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE)
- 架构 / 部署：[全景](../minimax/MiniMax-H3全景与架构.md) · [部署](../minimax/MiniMax-H3本地部署与API接入.md)
- 平台：[fal全景与生态.md](./fal全景与生态.md)
