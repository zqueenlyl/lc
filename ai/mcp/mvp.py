"""MCP 最小协议形状（无外部依赖）

演示 Host / Client / Server：
  initialize → tools/list → tools/call

真实 MCP 走 JSON-RPC 2.0 + stdio/HTTP；这里用进程内对象模拟同一套消息。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Server：暴露 tools（真实实现里这是独立进程）
# ---------------------------------------------------------------------------
@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict
    handler: Callable[[dict], Any]


class McpServer:
    def __init__(self, name: str, tools: list[Tool]):
        self.name = name
        self._tools = {t.name: t for t in tools}

    def initialize(self) -> dict:
        return {
            "protocolVersion": "2025-03-26",
            "serverInfo": {"name": self.name, "version": "0.1.0"},
            "capabilities": {"tools": {}},
        }

    def list_tools(self) -> list[dict]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "inputSchema": t.input_schema,
            }
            for t in self._tools.values()
        ]

    def call_tool(self, name: str, arguments: dict) -> dict:
        tool = self._tools.get(name)
        if tool is None:
            return {"isError": True, "content": [{"type": "text", "text": f"unknown tool: {name}"}]}
        try:
            result = tool.handler(arguments)
            return {"isError": False, "content": [{"type": "text", "text": str(result)}]}
        except Exception as exc:  # noqa: BLE001 — MVP 把异常回传给 Host
            return {"isError": True, "content": [{"type": "text", "text": str(exc)}]}


# ---------------------------------------------------------------------------
# Client：对某一个 Server 的会话
# ---------------------------------------------------------------------------
class McpClient:
    def __init__(self, server: McpServer):
        self.server = server
        self.initialized = False

    def connect(self) -> dict:
        caps = self.server.initialize()
        self.initialized = True
        return caps

    def list_tools(self) -> list[dict]:
        assert self.initialized
        return self.server.list_tools()

    def call(self, name: str, arguments: dict) -> dict:
        assert self.initialized
        return self.server.call_tool(name, arguments)


# ---------------------------------------------------------------------------
# Host：管理 client，把「用户意图」路由到 tool（真实场景由 LLM 选工具）
# ---------------------------------------------------------------------------
@dataclass
class Host:
    clients: dict[str, McpClient] = field(default_factory=dict)

    def attach(self, alias: str, server: McpServer) -> dict:
        client = McpClient(server)
        caps = client.connect()
        self.clients[alias] = client
        return caps

    def all_tools(self) -> list[tuple[str, dict]]:
        out = []
        for alias, client in self.clients.items():
            for tool in client.list_tools():
                out.append((alias, tool))
        return out

    def invoke(self, alias: str, tool: str, arguments: dict) -> dict:
        return self.clients[alias].call(tool, arguments)


# ---------------------------------------------------------------------------
# 示例领域：迷你文档库
# ---------------------------------------------------------------------------
DOCS = {
    "mcp": "MCP 用 JSON-RPC 把 tools/resources/prompts 标准化，供 Host 发现并调用。",
    "a2a": "A2A 让两个独立 Agent 用 Agent Card 发现彼此并委托任务。",
    "rag": "RAG 在生成前检索外部知识，降低幻觉与知识过期。",
}


def search_docs(args: dict) -> str:
    q = str(args.get("query", "")).lower()
    hits = [k for k, v in DOCS.items() if q in k or q in v.lower()]
    return "hits: " + (", ".join(hits) if hits else "(none)")


def get_doc(args: dict) -> str:
    doc_id = args.get("id")
    if doc_id not in DOCS:
        raise KeyError(f"doc not found: {doc_id}")
    return DOCS[doc_id]


def build_docs_server() -> McpServer:
    return McpServer(
        "docs",
        [
            Tool(
                "search_docs",
                "按关键词搜索内部文档。当用户问「有哪些资料/某某是什么」时使用。",
                {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
                search_docs,
            ),
            Tool(
                "get_doc",
                "按文档 id 读取全文。id 必须来自 search_docs 的 hits。",
                {
                    "type": "object",
                    "properties": {"id": {"type": "string"}},
                    "required": ["id"],
                },
                get_doc,
            ),
        ],
    )


def fake_llm_pick_tools(question: str) -> list[tuple[str, str, dict]]:
    """真实 Host 把 tool schema 塞给模型；这里用规则模拟选工具。"""
    if "A2A" in question.upper():
        return [
            ("docs", "search_docs", {"query": "A2A"}),
            ("docs", "get_doc", {"id": "a2a"}),
        ]
    return [("docs", "search_docs", {"query": question})]


if __name__ == "__main__":
    host = Host()
    caps = host.attach("docs", build_docs_server())
    print("=== initialize ===")
    print(caps)

    print("\n=== tools/list ===")
    for alias, tool in host.all_tools():
        print(f"  [{alias}] {tool['name']}: {tool['description'][:40]}...")

    question = "A2A 是干什么的？"
    print(f"\n=== 用户问题: {question} ===")
    for alias, name, args in fake_llm_pick_tools(question):
        result = host.invoke(alias, name, args)
        text = result["content"][0]["text"]
        print(f"tools/call {name}{args} -> {text}  error={result['isError']}")
