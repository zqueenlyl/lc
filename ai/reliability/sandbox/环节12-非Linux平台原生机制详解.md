# 环节 12 · 非 Linux 平台的原生机制（macOS / Windows）

> [环节 01](./环节01-隔离原语详解.md) 讲的全是 Linux（namespace / cgroup / seccomp）。**macOS 和 Windows 上一个都没有**——它们各有自己的原语，而且**能力明显不对等**。做跨平台 Agent 沙箱（Claude Code 双平台、Codex 三平台）时，这张差异表是绕不开的。
> 所属总揽：[环节00-总揽与环节导航.md](./环节00-总揽与环节导航.md) 环节 12。
> 相邻环节：机制对照见 [环节 01](./环节01-隔离原语详解.md)；产品差异见 [环节 07](./环节07-Agent落地形态详解.md)；开销见 [环节 13](./环节13-开销实测与量级校准详解.md)。
> 适合人群：要做跨平台 Agent 沙箱、或要理解"为什么这些工具都优先 Linux"的工程师。
> 配套 Notebook：[环节12-非Linux机制演示.ipynb](./环节12-非Linux机制演示.ipynb)——纯 Python 手搓三平台能力对照矩阵、SBPL / AppContainer 风格的能力判定器、"能力缺口"打分。
> **版本口径（2026-09-12）**：`sandbox-exec` 自 macOS 10.15 起被 Apple 标记为 **deprecated**（仍随系统提供，Claude Code / Codex 都在用）；Windows 的隔离机制随版本演进较慢但策略（WDAC / AppContainer）会变。引用前回官方文档核。

---

## 0. 一句话定位

**Linux 的隔离是"内核给的积木"；macOS / Windows 是"系统给的一个进程沙箱 + 一套策略"——粒度更粗、能力不对等。**

```
Linux   ：namespace（视图）+ cgroup（资源）+ seccomp（syscall）+ capabilities + LSM
          → 五个维度都能自己拼，粒度最细

macOS   ：Seatbelt(SBPL) 一次性进程沙箱 + ulimit 资源 + TCC 用户授权
          → 一个"策略沙箱"，没有 namespace、没有 cgroup

Windows ：受限令牌 + ACL + Job Object（部分资源）+ AppContainer（能力模型）+ WDAC
          → 靠"身份降权 + 对象权限"，也没有 namespace
```

**直接后果**：同一套 Agent 沙箱代码，在三个平台上的**强度与可配项完全不同**——这是"为什么 Claude Code 只支持 macOS / Linux / WSL2，而 Codex 为 Windows 单独实现了一套"的根本原因。

---

## 1. macOS

### 1.1 Seatbelt（`sandbox-exec` + SBPL）：Agent 沙箱的实际底座

| 维度 | 说明 |
|---|---|
| 形态 | 用户态命令 `sandbox-exec -p '<profile>' <command>`，profile 用 **SBPL**（Sandbox Profile Language，类 Scheme 的 S 表达式）写 |
| 粒度 | **策略式**：`allow` / `deny` + 规则（`file-read*`、`file-write*`、`network*`、`process*`、`mach*`…） |
| 资源限制 | **不提供**。要配合 `ulimit`（`-u` 进程数 / `-v` 内存 / `-t` CPU 时间）等 POSIX 手段 |
| 进程视图 | **不隔离**（没有 PID namespace）——沙箱内进程能看到宿主进程 |
| 网络 | 支持按规则禁止（`(deny network*)`），本机实测**生效**（见 [环节 13](./环节13-开销实测与量级校准详解.md) §3） |
| 现状 | **Apple 已标记 deprecated**（10.15+），但仍随系统提供且被广泛使用 |

**Claude Code / Codex 的做法**：不是从零写 SBPL，而是**基于系统预置的 Seatbelt 基线 profile**（`/System/Library/Sandbox/Profiles/*.sb`）+ 动态追加规则。Codex 的实现就是从 `PermissionProfile` 动态生成 SBPL 参数再 spawn `/usr/bin/sandbox-exec`。

> **本机实测的一个重要发现（[环节 13](./环节13-开销实测与量级校准详解.md) §3）**：**SBPL 白名单极难手写**——把 `file-read*` 收紧到"只允许读几个目录"后，连 `/bin/ls` 都直接 `SIGABRT`（exit 134），不是优雅拒绝。这解释了为什么生产工具都用"系统基线 + 增量规则"而不是自造 profile。

### 1.2 另外三层（容易与 Seatbelt 混淆）

| 机制 | 是什么 | 与沙箱的关系 |
|---|---|---|
| **App Sandbox** | 通过 **entitlements** 声明的沙箱，面向 App Store 应用 | 与 Seatbelt 同源但用途不同；**命令行工具一般用不上** |
| **TCC** | 用户授权层（首次访问 `~/Documents`、摄像头、麦克风、屏幕录制时弹窗） | **独立于沙箱**：沙箱管"能不能调 API"，TCC 管"用户授不授权"。两层都要过 |
| **Endpoint Security** | 面向安全产品的系统扩展框架（需 entitlement） | 用于**观测/拦截**系统事件，不是隔离手段 |

> **一句话**：**Seatbelt 是内核强制的边界，TCC 是用户授权**。Computer Use 类场景（要录屏、控鼠标）必须同时处理这两层。

### 1.3 工程含义

1. **没有 cgroup** → 资源限制只能靠 `ulimit` / `setrlimit`（粒度粗：`-u` 限制的是"进程/线程数"，`-v` 限制地址空间而非 RSS）。
2. **没有 PID namespace** → 沙箱里能看到宿主进程，`/proc` 那套防泄露手段在 macOS 不存在（对应风险仍在，只是没法用同样的方式解决）。
3. **profile 脆弱** → 手写必漏；用系统基线 + 增量。
4. **`sandbox-exec` 已 deprecated** → 存在"未来某版本被移除"的风险，这是自建方案要评估的长期风险。

---

## 2. Windows

### 2.1 四件套：令牌 + ACL + Job Object + AppContainer

| 机制 | 作用 | 大致对应 Linux 的 |
|---|---|---|
| **受限令牌（Restricted Token）** | 把进程的权限令牌降权（去掉特权、把 SID 标记为 deny-only） | capabilities 裁剪 + `setuid` |
| **ACL** | 用文件/注册表/对象的访问控制表限制"能碰什么" | 文件权限 + LSM（粗粒度版） |
| **Job Object** | **资源限制**：内存上限、CPU 时间/速率、**活动进程数**、UI 限制（剪贴板/桌面） | **cgroup（部分）** |
| **AppContainer** | 低权限进程容器：能力（capabilities）显式声明 + 独立 SID + 强制 ACL | 容器（弱化版）+ Wasm 式能力模型 |
| **WDAC / AppLocker** | 应用控制（只允许签名/白名单程序运行） | 无直接对应（类似 LSM 的策略层） |
| **Windows Sandbox** | 基于 Hyper-V 的轻量 VM，面向交互式桌面 | 微 VM |

**Codex 的 Windows 实现**就是这套的组合：受限令牌 + ACL，并且管理**两个沙箱身份** `CodexSandboxOffline` / `CodexSandboxOnline`——**用"不同用户身份"表达"有没有网"**，这是 Windows 上没有 network namespace 时的一种替代设计。

### 2.2 与 Linux 的关键差异

| 维度 | Linux | Windows |
|---|---|---|
| 视图隔离 | namespace（部分/网络/挂载/PID） | **没有**；靠 ACL 决定"能访问哪些对象" |
| 资源限制 | cgroup v2（细粒度、可控比例） | **Job Object**（内存/CPU/进程数，粒度较粗） |
| syscall 过滤 | seccomp-bpf | **没有等价物**；靠 API 层（AppContainer 能力）+ 内核攻击面靠版本与缓解措施 |
| 网络隔离 | net namespace（默认无网） | 靠**防火墙规则 / AppContainer 能力 / 用户身份**，没有"空网络栈"这种默认值 |
| 文件系统 | mount ns + overlayfs | 靠 ACL + 虚拟化（对沙箱进程隐藏/重定向路径较难） |

> **一句话**：**Windows 的沙箱是"权限模型驱动"，Linux 的沙箱是"命名空间驱动"**。前者更难做到"默认全拒"，所以**WSL2 成了 Windows 上跑 Linux 风格沙箱的事实标准路径**。

### 2.3 WSL2：为什么它是岔路口

| | WSL1 | WSL2 |
|---|---|---|
| 内核 | 翻译层（无真实 Linux 内核特性） | **真实 Linux 内核（轻量 VM）** |
| bubblewrap 可用 | ❌（需要 user namespace 等内核特性） | ✅ |
| 沙箱能力 | 基本等于宿主 Windows | **等同 Linux**（namespace/cgroup/seccomp 都在） |

**这正是 Claude Code 文档里明确写"支持 macOS / Linux / WSL2，不支持原生 Windows 与 WSL1"的原因**。

---

## 3. 三平台能力对照表（选型的核心依据）

| 能力 | Linux | macOS | Windows（原生） | Windows（WSL2） |
|---|---|---|---|---|
| 文件系统隔离 | ✅ mount ns + overlayfs | ⚠️ SBPL 路径规则 | ⚠️ ACL | ✅ 同 Linux |
| 网络默认关 | ✅ net ns（默认无网） | ✅ `(deny network*)` | ⚠️ 需防火墙/能力配置 | ✅ net ns |
| 资源限制（CPU/内存） | ✅ cgroup v2 | ⚠️ `ulimit`（粗） | ✅ Job Object | ✅ cgroup v2 |
| 进程数限制 | ✅ `pids.max` | ⚠️ `ulimit -u` | ✅ Job Object | ✅ `pids.max` |
| syscall 过滤 | ✅ seccomp-bpf | ❌ | ❌（能力模型替代） | ✅ seccomp-bpf |
| 视图隔离（PID 等） | ✅ namespace | ❌ | ❌ | ✅ namespace |
| 独立内核档可用 | ✅ 微 VM / gVisor | ⚠️ 虚拟机（无容器运行时） | ✅（Hyper-V / Windows Sandbox） | ✅ |
| 容器生态 | ✅ 最好 | ❌（无原生容器） | ⚠️（容器跑在 Linux VM 里） | ✅ |

> **读法**：这张表解释了**为什么几乎所有 Agent 沙箱工具都是"Linux 优先、macOS 次之、Windows 靠 WSL2"**。macOS 的短板是"没有资源与 syscall 维度"，Windows 的短板是"没有 namespace"。

---

## 4. 工程含义（做跨平台沙箱的四条）

1. **抽象层要按"能力"而不是"机制"设计**：上层只说"禁网 / 只读工作目录 / 限 512MB"，下层各平台自己映射（Linux→net ns、macOS→SBPL、Windows→Job Object + 防火墙）。
2. **能力不对等必须暴露成"降级"而不是静默忽略**：在 macOS 上做不到 `pids.max` 那种精度，就要显式告知（性能档 vs 加固档），而不是假装配了。
3. **优先 WSL2（Windows）与"容器后端"（macOS）**：与其在宿主原生层面勉强做，不如把隔离放在 Linux 侧（Docker Desktop / 远端 Linux 沙箱）——这是大多数产品的实际选择。
4. **deprecated 风险要记账**：`sandbox-exec` 被标记 deprecated 多年仍在用，但一旦移除，所有基于它的方案都要重做——**自建方案要评估这个长期风险**，托管云沙箱则把这个风险转移给了厂商。

---

## 5. 面试高频追问

| 追问 | 回答要点 |
|---|---|
| macOS 有 namespace / cgroup 吗？ | **都没有**；Seatbelt 是策略式进程沙箱，资源要靠 `ulimit` |
| TCC 和沙箱是什么关系？ | 两层：沙箱（内核强制）管"能不能调 API"，TCC（用户授权）管"用户授不授权"，都要过 |
| Windows 靠什么限制资源？ | **Job Object**（内存 / CPU / 进程数 / UI）；隔离靠受限令牌 + ACL + AppContainer |
| Windows 为什么没有网络 namespace？ | 权限模型驱动，无"空网络栈"默认值；靠防火墙/能力/身份；所以身份成了表达"有没有网"的手段（Codex 的 Offline/Online） |
| 为什么 Claude Code 不支持原生 Windows？ | 它的 Linux 侧依赖 bubblewrap（需 user ns 等内核特性），WSL1 与原生 Windows 都没有 → 只能 WSL2 |
| `sandbox-exec` 被 deprecated 了还用？ | 是：已被标记多年但仍随系统提供；生产工具（Claude Code / Codex）都在用，属已知长期风险 |
| 跨平台沙箱最难的是什么？ | **能力不对等**——不是"接口不同"，而是"某些维度在某个平台根本做不到"，必须设计降级路径 |

---

## 6. 坑清单

1. **以为"沙箱"在三平台是同一件事**：粒度与可配项完全不同，一套参数照搬必然失真。
2. **手写 SBPL 白名单**：本机实测证明极易把进程搞到直接 `SIGABRT`；用系统基线 + 增量。
3. **在 macOS 上指望 cgroup 级资源控制**：`ulimit -v` 限制的是地址空间（不等于 RSS），且不控 CPU 份额。
4. **忽略 TCC**：要录屏/控鼠的 Computer Use 场景，权限弹窗没处理会直接卡住。
5. **在原生 Windows 上找 network namespace**：不存在；要么用能力/防火墙，要么走 WSL2。
6. **只测 WSL1**：bubblewrap 需要 WSL2 的内核特性，WSL1 上直接不可用。
7. **忘记 deprecated 风险**：基于 `sandbox-exec` 的方案要评估长期维护成本。
8. **把 Windows Sandbox 当容器用**：它是交互式桌面 VM，不适合"每任务一个实例"的高频调度。

---

## 7. 相关笔记

- Linux 原语（对照基座）→ [环节01-隔离原语详解.md](./环节01-隔离原语详解.md)
- 平台差异在产品上的体现（Claude Code / Codex / Pi）→ [环节07-Agent落地形态详解.md](./环节07-Agent落地形态详解.md) §1
- 各平台的实际开销（含本机 Seatbelt 实测）→ [环节13-开销实测与量级校准详解.md](./环节13-开销实测与量级校准详解.md)
- 平台化加固配置（Linux 侧的 Docker / K8s）→ [环节11-平台化落地详解.md](./环节11-平台化落地详解.md)
- 白名单为什么要"观察期 + 数据驱动"→ [环节09-可观测性与验收详解.md](./环节09-可观测性与验收详解.md) §2
