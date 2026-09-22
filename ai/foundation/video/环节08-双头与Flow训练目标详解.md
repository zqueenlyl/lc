# 视频生成 · 环节 08 · 双头与 Flow 训练目标

> 开源数字默认 MiniMax-H3 Base；机制对 2024 后潜空间 DiT / flow（类型 D/E）通用。总揽：[环节00](./环节00-总揽与环节导航.md)。类型见 [演化路线](./生视频模型演化路线与类型.md)。
> 全链路第八站：网络吐出的 5376 维向量，怎么变成两个可以求导的数。答案是**速度回归**——预测「从当前带噪 latent 指向干净 latent 的方向」，对真值速度做 MSE。
> 扩散数学底座：[图像扩散详解](../generative/diffusion/图像扩散模型详解.md)（DDPM）；本环节换成 Rectified Flow。官方未写论文级公式，以下与开源 scheduler / 社区 trainer 一致。
> 所属总揽：[环节00](./环节00-总揽与环节导航.md)。上一站 [环节07](./环节07-Omni-Block堆叠详解.md) → 下一站 [环节09](./环节09-训练管线详解.md)。
> 配套 Notebook：[环节08-双头与Flow训练目标演示.ipynb](./环节08-双头与Flow训练目标演示.ipynb)——1D 直线插值 + MSE；`flow_shift` 把 \(t\) 拧到哪。

---

## 1. 双头在干什么

`MiniMaxH3FinalLayer`：再一次 AdaLN（这次不分三模态，只随 \(t\)），然后：

- `video_out`: \(5376 \to 96\)（= 24×1×2×2 patch 维）fp32
- `audio_out`: \(5376 \to 32\) fp32

两头都打在 packed **每一行**上，再用 mask 取出视频行 / 音频行。文本行的速度预测会被丢掉——文本是条件，不是要去噪的对象。

两头不共享权重：96 维的视频 patch 和 32 维的音频 latent 几何性质不同，硬共享等于让一层线性同时拟合两种尺度。

## 2. Rectified Flow（工作模型）

数据 \(x_0\)（VAE latent），\(\varepsilon\sim\mathcal N(0,I)\)，\(t\in[0,1]\)：

\[
x_t=(1-t)\,x_0+t\,\varepsilon,\qquad v=\varepsilon-x_0
\]

\[
\mathcal L_{\text{video}}=\mathbb E\|u_\theta^{\text{vid}}(x_t,t,c)-v^{\text{vid}}\|^2
\quad+\quad
\mathcal L_{\text{audio}}=\mathbb E\|u_\theta^{\text{aud}}-v^{\text{aud}}\|^2
\]

同一 \(u_\theta\) 网络、两套 scheduler。社区最小 trainer 若没缓存真音频会把音频项置零——那是工程缺口。

直觉：DDPM 学「这一点加了多少噪声」；Rectified Flow 学「从数据指向噪声的那条直线的速度」。把这个速度场反向积分，就能从纯噪声走回数据（[环节 10](./环节10-Flow采样与推理详解.md)）。之所以敢用直线，是因为 [环节 03](./环节03-双VAE详解.md) 的 VAE 专门保证了潜空间「好学」。

## 3. 为什么视频 shift=12、音频 shift=3

`flow_shift=12.0` / `audio_flow_shift=3.0` 来自开源推理请求体。下面的时间扭曲与 SD3/FLUX **同类**，是社区工作模型，**官方未写**；且「拧向哪一侧」取决于调度器把 \(t=1\) 定义成噪声还是数据（本文 Rectified Flow 记号里 \(t=1\) 是噪声）：

\[
t'=\frac{s\,t}{1+(s-1)t}
\]

在这套记号下 \(s\) 越大，均匀随机的 \(t\) 越快被拧到靠近 1，也就是把更多训练/采样预算花在高噪声段。视频格子多、结构要先立住，用 12；音频序列短，用 3。**两套 unique timesteps 进 AdaLN**，不要共用一个标量。

## 4. CFG 蒸馏（输出头的产品形态）

标准 CFG 要两次前向：

\[
u_{\text{guided}}=u_\varnothing+w(u_c-u_\varnothing)
\]

发布权重把 \(w\) 烤进学生：推理没有 `guidance_scale` / `negative_prompt`。从蒸馏权重继续微调，模型已经「只会听条件」。教师权重 **未开源**。

省掉的是**整网第二遍前向**：6 万行 × 50 层 × 50 步，这一半算力在视频上是真金白银，代价是你失去了 guidance 这个旋钮。

## 5. 两个 loss 的形状账

10 秒片子：

```
L_video 在 60480 × 96 ≈ 5.8×10⁶ 个元素上平均
L_audio 在 ~400 × 32 ≈ 1.3×10⁴ 个元素上平均（每声道）
```

差约 450 倍。若不加权直接相加，音频梯度会被画面淹没，表现就是「画面越来越好、声音一直糊」。官方如何加权 **未披露**；自己微调时这是必须自己定的一件事。

另外记住哪些行进 loss：视频行进、音频行进、**文本行不进**；首尾帧/参考这些干净行也不进——它们是条件。

## 6. 工程要点

1. 训练一步随机 \(t\) 插值真 latent；不必每步 VAE decode。
2. 蒸馏权重不要在 loss 里再乘 guidance。
3. 首尾帧任务：对应位置的 \(x_0\) 已知，常把那些 token 当条件而不是当预测目标（具体 mask 以官方 pack 为准）。

## 7. 面试追问

- **H3 是怎么生成的？** 潜空间 flow matching + 双向 Transformer 去噪，整段音视频一起出，不是逐帧或逐段自回归续写。
- **为什么双头不共享？** 96 维视频格子 vs 32 维音频 latent，几何不同。

下一站：这个 loss 在时间上怎么排期。
