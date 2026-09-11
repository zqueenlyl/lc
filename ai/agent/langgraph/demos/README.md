# LangGraph Demos

本目录包含 8 个覆盖不同应用类型的可运行示例，每个文件都是**独立脚本**，可直接 `python xxx.py` 运行。

## 运行环境

```bash
pip install -r requirements.txt
```

依赖 LLM 的示例需要设置 OpenAI API Key：

```bash
export OPENAI_API_KEY="sk-..."
```

## Demo 一览

| 文件 | 类型 | 是否依赖 LLM | 说明 |
|---|---|---|---|
| `01_basic_chain.py` | 线性流水线 | 否 | State / Node / Edge 最小示例 |
| `02_branching_router.py` | 条件分支/路由 | 否 | 按输入内容分流到不同处理 |
| `03_agent_loop.py` | ReAct Agent | 是 | 工具调用循环（本地计算器工具） |
| `04_parallel_fanout.py` | 并行 fan-out/fan-in | 否 | Send API 并发处理多任务 |
| `05_rag_agent.py` | RAG 检索增强 | 是 | 向量检索 + 生成（含重试） |
| `06_multi_agent.py` | 多智能体 Supervisor | 是 | 研究员 + 编码员 + 监督者路由 |
| `07_human_in_the_loop.py` | 人机协同 | 否 | interrupt 暂停等待人工审批 |
| `08_checkpointer_memory.py` | 持久化/记忆 | 否 | thread_id 会话隔离 + 断点回溯 |

## 快速验证

```bash
# 无 LLM 依赖，可直接跑
python 01_basic_chain.py
python 02_branching_router.py
python 04_parallel_fanout.py
python 07_human_in_the_loop.py
python 08_checkpointer_memory.py

# 需 LLM
python 03_agent_loop.py
python 05_rag_agent.py
python 06_multi_agent.py
```
