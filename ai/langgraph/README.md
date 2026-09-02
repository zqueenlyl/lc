# LangGraph 学习指南与示例合集

> LangGraph 是 LangChain 团队推出的**图状态机（Graph State Machine）编排框架**，用于把 LLM 应用中的多个步骤（节点）、条件跳转（边）、循环与状态用一张「图」清晰地组织起来，尤其擅长构建 **Agent**、**RAG**、**多智能体**、**人机协同** 等需要灵活控制流的应用。

本目录包含一份系统化学习文档，以及覆盖各类典型应用的**可运行 demo**。

---

## 目录结构

```
langgraph/
├── README.md                          # 本文件：总览 + 学习路线 + demo 导航
├── 01-核心概念与快速上手.md            # State / Node / Edge / 编译 / 执行
├── 02-条件分支与循环.md                # 路由、循环、ReAct Agent
├── 03-持久化-流式-人机协同.md          # Checkpointer / Streaming / interrupt
├── 04-多智能体与高级模式.md            # 子图 / 并行 / 多智能体 / 最佳实践
└── demos/
    ├── README.md                      # demo 运行说明
    ├── requirements.txt               # 依赖清单
    ├── 01_basic_chain.py              # 线性流水线
    ├── 02_branching_router.py         # 条件分支 / 路由
    ├── 03_agent_loop.py               # ReAct Agent 循环
    ├── 04_parallel_fanout.py          # 并行 fan-out / fan-in
    ├── 05_rag_agent.py                # RAG 检索增强生成
    ├── 06_multi_agent.py              # 多智能体（Supervisor）
    ├── 07_human_in_the_loop.py        # 人机协同（interrupt）
    └── 08_checkpointer_memory.py      # 持久化与记忆
```

---

## 学习路线

建议按顺序阅读：

| 顺序 | 文档 | 内容 | 对应 demo |
|---|---|---|---|
| 1 | [01-核心概念与快速上手.md](./01-核心概念与快速上手.md) | State、Node、Edge、编译执行、`add_messages` | `01_basic_chain.py` |
| 2 | [02-条件分支与循环.md](./02-条件分支与循环.md) | 条件边、路由、循环终止、`create_react_agent` | `02_branching_router.py`、`03_agent_loop.py` |
| 3 | [03-持久化-流式-人机协同.md](./03-持久化-流式-人机协同.md) | Checkpointer、thread 记忆、stream、interrupt/Command | `07_human_in_the_loop.py`、`08_checkpointer_memory.py` |
| 4 | [04-多智能体与高级模式.md](./04-多智能体与高级模式.md) | 子图、Send 并行、Supervisor 多智能体、最佳实践 | `04_parallel_fanout.py`、`06_multi_agent.py` |

> `05_rag_agent.py` 是综合实战：把「分支路由 + Agent 循环 + 检索」串成完整的 RAG Agent。

---

## 快速开始

```bash
# 1. 安装依赖
cd demos
pip install -r requirements.txt

# 2. 运行不依赖 LLM 的 demo（直接可跑）
python 01_basic_chain.py
python 02_branching_router.py
python 04_parallel_fanout.py
python 08_checkpointer_memory.py

# 3. 运行依赖 LLM 的 demo（需先设置 OPENAI_API_KEY）
export OPENAI_API_KEY="sk-..."
python 03_agent_loop.py
python 05_rag_agent.py
python 06_multi_agent.py
```

---

## 核心概念速览

- **State（状态）**：图中流转的共享数据，用 `TypedDict` 定义；字段可声明 reducer（如 `add_messages` 累加消息）。
- **Node（节点）**：一个处理函数，入参当前 State，返回「部分 State 更新」。
- **Edge（边）**：节点间的跳转；`add_edge` 固定跳转，`add_conditional_edges` 根据状态动态路由。
- **Compile / Invoke**：`compile()` 生成可执行图，`invoke()` 同步执行、`stream()` 流式执行。
- **Checkpointer**：给图加「记忆」，支持断点恢复、线程隔离（`thread_id`）。
- **interrupt / Command**：在节点中暂停，等待人类输入后继续。

---

## 相关文档

- 同仓库 RAG 全景：[../rag/rag-types.md](../rag/rag-types.md)、[../rag/rag-mvp.md](../rag/rag-mvp.md)
- LangGraph 官方文档：https://langchain-ai.github.io/langgraph/
