"""ACP 最小协议形状（无外部依赖）

演示 Client（编辑器）↔ Agent（编码 Agent）的一次会话：
    initialize → session/new → session/prompt
      → session/update: plan / tool_call / tool_call_update / agent_message_chunk
      → stopReason=end_turn
最后演示 session/cancel 返回 stopReason=cancelled。

真实 ACP 走 JSON-RPC 2.0 + stdio；这里用进程内对象模拟同一套消息，
不调用真实 LLM——Agent 侧用规则策略代替模型决策。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Client：编辑器侧。持有文件系统与终端，是权限的唯一裁决点。
# ---------------------------------------------------------------------------
@dataclass
class AcpClient:
    files: dict[str, str] = field(default_factory=dict)
    auto_approve: set[str] = field(default_factory=set)
    updates: list[dict] = field(default_factory=list)

    # --- 能力协商（真实协议里 clientCapabilities 随 initialize 回给 Agent）---
    def capabilities(self) -> dict:
        return {"fs": {"readTextFile": True, "writeTextFile": True}, "terminal": True}

    # --- Agent → Client：文件读写 ---
    def read_text_file(self, path: str) -> str:
        if path not in self.files:
            raise FileNotFoundError(f"no such file: {path}")
        return self.files[path]

    def write_text_file(self, path: str, content: str) -> None:
        self.files[path] = content

    # --- Agent → Client：终端（MVP 只认 pytest）---
    def terminal(self, command: str) -> str:
        if command.startswith("pytest"):
            return "1 passed"
        return f"unsupported command in mvp: {command}"

    # --- Agent → Client：请求式权限 ---
    def request_permission(self, tool_call: dict) -> str:
        key = tool_call["kind"]
        granted = key in self.auto_approve
        return "allow_once" if granted else "reject_once"

    # --- Agent → Client：流式通知 ---
    def session_update(self, session_id: str, update: dict) -> None:
        self.updates.append({"sessionId": session_id, **update})
        _print_update(update)


def _print_update(update: dict) -> None:
    kind = update["sessionUpdate"]
    if kind == "plan":
        entries = " | ".join(f"{e['status']}:{e['title']}" for e in update["entries"])
        print(f"  [plan] {entries}")
    elif kind == "tool_call":
        print(f"  [tool_call#{update['toolCallId']}] kind={update['kind']} title={update['title']}")
    elif kind == "tool_call_update":
        print(f"  [update#{update['toolCallId']}] status={update['status']}")
    elif kind == "agent_message_chunk":
        print(f"  [agent] {update['content']['text']}")
    elif kind == "agent_thought_chunk":
        print(f"  [thought] {update['content']['text']}")
    elif kind == "usage_update":
        print(f"  [usage] {update['usage']}")
    else:
        print(f"  [{kind}] {update}")


# ---------------------------------------------------------------------------
# Agent：ACP 的 agent 侧。真实实现里背后是 Harness 循环 + 模型。
# ---------------------------------------------------------------------------
class AcpAgent:
    def __init__(self, client: AcpClient):
        self.client = client
        self.sessions: dict[str, dict] = {}
        self._cancelled: set[str] = set()
        self._seq = 0

    def initialize(self, client_caps: dict) -> dict:
        self.client_caps = client_caps
        return {
            "protocolVersion": "0.x",
            "agentCapabilities": {
                "promptCapabilities": {"image": True, "audio": False, "embeddedContext": True},
                "loadSession": True,
                "mcpCapabilities": {"http": True, "sse": True},
            },
        }

    def session_new(self, cwd: str) -> str:
        session_id = f"sess-{len(self.sessions) + 1}"
        self.sessions[session_id] = {"cwd": cwd, "state": "idle"}
        return session_id

    def session_cancel(self, session_id: str) -> None:
        self._cancelled.add(session_id)

    def _emit(self, session_id: str, update: dict) -> None:
        self.client.session_update(session_id, update)

    def _next_tool_id(self) -> str:
        self._seq += 1
        return f"tc-{self._seq}"

    def _is_cancelled(self, session_id: str) -> bool:
        return session_id in self._cancelled

    # --- 一次 prompt：规则策略扮演「模型」 ---
    def session_prompt(self, session_id: str, blocks: list[dict]) -> dict:
        prompt = "".join(b.get("text", "") for b in blocks)
        target = "config.py"
        self.sessions[session_id]["state"] = "running"

        # 1) 计划
        self._emit(
            session_id,
            {
                "sessionUpdate": "plan",
                "entries": [
                    {"title": f"读 {target}", "status": "in_progress", "priority": "high"},
                    {"title": "把 MAX_RETRY 改成 5", "status": "pending", "priority": "high"},
                    {"title": "跑测试", "status": "pending", "priority": "medium"},
                ],
            },
        )

        # 2) 工具调用 #1：读文件（kind=read，走 Client 的 fs 能力）
        tc1 = self._next_tool_id()
        self._emit(
            session_id,
            {
                "sessionUpdate": "tool_call",
                "toolCallId": tc1,
                "title": f"读 {target}",
                "kind": "read",
                "status": "in_progress",
                "locations": [{"path": target, "line": 1}],
                "rawInput": {"path": target},
            },
        )
        if self._is_cancelled(session_id):
            return self._stop(session_id, "cancelled", [tc1])
        source = self.client.read_text_file(target)
        self._emit(
            session_id,
            {
                "sessionUpdate": "tool_call_update",
                "toolCallId": tc1,
                "status": "completed",
                "content": [{"type": "text", "text": source}],
                "rawOutput": source,
            },
        )
        self._emit(
            session_id,
            {
                "sessionUpdate": "plan",
                "entries": [
                    {"title": f"读 {target}", "status": "completed", "priority": "high"},
                    {"title": "把 MAX_RETRY 改成 5", "status": "in_progress", "priority": "high"},
                    {"title": "跑测试", "status": "pending", "priority": "medium"},
                ],
            },
        )

        # 3) 工具调用 #2：改文件（kind=edit → 必须先过 request_permission）
        tc2 = self._next_tool_id()
        call2 = {
            "toolCallId": tc2,
            "title": "编辑 config.py",
            "kind": "edit",
            "locations": [{"path": target}],
            "rawInput": {"path": target, "old": "MAX_RETRY = 3", "new": "MAX_RETRY = 5"},
        }
        self._emit(session_id, {"sessionUpdate": "tool_call", "status": "pending", **call2})
        self._emit(
            session_id,
            {
                "sessionUpdate": "agent_thought_chunk",
                "content": {"type": "text", "text": f"用户要求：{prompt.strip()}"},
            },
        )
        decision = self.client.request_permission(call2)
        print(f"  [permission] kind=edit -> {decision}")
        if decision.startswith("reject"):
            self._emit(
                session_id,
                {
                    "sessionUpdate": "tool_call_update",
                    "toolCallId": tc2,
                    "status": "failed",
                    "rawOutput": "用户拒绝了该编辑",
                },
            )
            self._emit(
                session_id,
                {
                    "sessionUpdate": "agent_message_chunk",
                    "content": {"type": "text", "text": "编辑被拒绝，未改动任何文件。"},
                },
            )
            return {"stopReason": "refusal"}

        if self._is_cancelled(session_id):
            return self._stop(session_id, "cancelled", [tc2])
        self._emit(
            session_id,
            {"sessionUpdate": "tool_call_update", "toolCallId": tc2, "status": "in_progress"},
        )
        patched = source.replace("MAX_RETRY = 3", "MAX_RETRY = 5")
        self.client.write_text_file(target, patched)
        self._emit(
            session_id,
            {
                "sessionUpdate": "tool_call_update",
                "toolCallId": tc2,
                "status": "completed",
                "content": [{"type": "text", "text": "MAX_RETRY: 3 -> 5"}],
            },
        )

        # 4) 工具调用 #3：跑测试（kind=execute）
        tc3 = self._next_tool_id()
        self._emit(
            session_id,
            {
                "sessionUpdate": "tool_call",
                "toolCallId": tc3,
                "title": "pytest",
                "kind": "execute",
                "status": "in_progress",
                "rawInput": {"command": "pytest -q"},
            },
        )
        output = self.client.terminal("pytest -q")
        self._emit(
            session_id,
            {
                "sessionUpdate": "tool_call_update",
                "toolCallId": tc3,
                "status": "completed",
                "content": [{"type": "text", "text": output}],
            },
        )
        self._emit(
            session_id,
            {
                "sessionUpdate": "plan",
                "entries": [
                    {"title": f"读 {target}", "status": "completed", "priority": "high"},
                    {"title": "把 MAX_RETRY 改成 5", "status": "completed", "priority": "high"},
                    {"title": "跑测试", "status": "completed", "priority": "medium"},
                ],
            },
        )
        self._emit(
            session_id,
            {
                "sessionUpdate": "usage_update",
                "usage": {"inputTokens": 1200, "outputTokens": 240},
            },
        )
        self._emit(
            session_id,
            {
                "sessionUpdate": "agent_message_chunk",
                "content": {
                    "type": "text",
                    "text": f"已把 {target} 的 MAX_RETRY 改成 5，pytest 结果：{output}。",
                },
            },
        )
        self.sessions[session_id]["state"] = "idle"
        return {"stopReason": "end_turn"}

    def _stop(self, session_id: str, reason: str, pending: list[str]) -> dict:
        for tc in pending:
            self._emit(
                session_id,
                {"sessionUpdate": "tool_call_update", "toolCallId": tc, "status": "failed"},
            )
        self.sessions[session_id]["state"] = "idle"
        return {"stopReason": reason}


# ---------------------------------------------------------------------------
# 跑一遍
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    client = AcpClient(
        files={"config.py": "MAX_RETRY = 3\nTIMEOUT = 10\n"},
        auto_approve={"edit"},  # 白名单里的 kind 自动放行
    )
    agent = AcpAgent(client)

    print("=== initialize（能力协商）===")
    caps = agent.initialize(client.capabilities())
    print("  client:", client.capabilities())
    print("  agent :", caps["agentCapabilities"])

    session_id = agent.session_new("/repo")
    print(f"\n=== session/new -> {session_id} ===")

    print("\n=== session/prompt：把 MAX_RETRY 从 3 改成 5 ===")
    result = agent.session_prompt(
        session_id,
        [{"type": "text", "text": "把 config.py 里的 MAX_RETRY 从 3 改成 5"}],
    )
    print(f"  stopReason = {result['stopReason']}")
    print(f"  文件当前内容 = {client.files['config.py']!r}")
    print(f"  update 条数 = {len(client.updates)}")

    # 权限被拒分支：清空白名单，编辑类工具全部拒绝
    print("\n=== 权限分支：auto_approve 清空后再改一次 ===")
    client.auto_approve = set()
    result2 = agent.session_prompt(
        session_id,
        [{"type": "text", "text": "把 MAX_RETRY 从 5 改成 8"}],
    )
    print(f"  stopReason = {result2['stopReason']}")

    # 取消分支：prompt 前先 cancel
    print("\n=== 取消分支：先 session/cancel 再 prompt ===")
    session2 = agent.session_new("/repo")
    agent.session_cancel(session2)
    result3 = agent.session_prompt(session2, [{"type": "text", "text": "重构整个仓库"}])
    print(f"  stopReason = {result3['stopReason']}")
