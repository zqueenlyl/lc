#!/usr/bin/env python3
"""给 codebuddy_acp_ui.py 做自检用的**假 Agent**（不联网、不调模型）。

它实现 ACP 的 agent 侧：stdio + 换行分帧的 JSON-RPC 2.0。
一次 prompt 里把该演的都演一遍：

    plan → tool_call#1(edit) → request_permission → fs/write_text_file
         → tool_call#2(execute) → terminal/create → terminal/wait_for_exit → terminal/output
         → agent_message_chunk → stopReason=end_turn

它还会反向调用 Client（fs / terminal / 权限），所以能用来验证 Client 那半边写对没有。

运行（通常由 UI 拉起，也可手动）：
    python3 codebuddy_acp_ui.py --cmd "python3 mock_agent.py" --cwd /tmp/acp_ws
"""

from __future__ import annotations

import json
import os
import sys
import threading
import time

CWD = os.getcwd()


class MockAgent:
    def __init__(self) -> None:
        self._id = 0
        self._cond = threading.Condition()
        self._responses: dict[int, dict] = {}
        self.caps: dict = {}

    # ---------- 发送 ----------
    def _write(self, msg: dict) -> None:
        sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    def notify(self, method: str, params: dict) -> None:
        self._write({"jsonrpc": "2.0", "method": method, "params": params})

    def request(self, method: str, params: dict, timeout: float = 60.0) -> dict:
        self._id += 1
        rid = self._id
        self._write({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        deadline = time.time() + timeout
        with self._cond:
            while rid not in self._responses:
                if time.time() > deadline:
                    raise RuntimeError(f"{method} 无响应")
                self._cond.wait(0.1)
            msg = self._responses.pop(rid)
        if "error" in msg:
            raise RuntimeError(f"{method} 被拒：{msg['error']}")
        return msg.get("result", {})

    def update(self, session_id: str, update: dict) -> None:
        self.notify("session/update", {"sessionId": session_id, "update": update})

    # ---------- 主循环 ----------
    def run(self) -> None:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            msg = json.loads(line)
            if "id" in msg and "method" in msg:
                self._handle_request(msg)
            elif "id" in msg:
                with self._cond:
                    self._responses[msg["id"]] = msg
                    self._cond.notify_all()

    def _handle_request(self, msg: dict) -> None:
        rid, method, params = msg["id"], msg["method"], msg.get("params") or {}
        # session/prompt 一边等响应一边还要反向调用 Client，必须放到别的线程，
        # 否则读循环被自己堵死（响应永远读不到）。
        if method == "session/prompt":
            threading.Thread(target=self._prompt_worker, args=(rid, params), daemon=True).start()
            return
        try:
            result = self._dispatch(method, params)
            self._write({"jsonrpc": "2.0", "id": rid, "result": result})
        except Exception as exc:  # noqa: BLE001
            self._write({"jsonrpc": "2.0", "id": rid,
                         "error": {"code": -32000, "message": str(exc)}})

    def _prompt_worker(self, rid: int, params: dict) -> None:
        try:
            self._turn(params["sessionId"], params["prompt"])
            self._write({"jsonrpc": "2.0", "id": rid, "result": {"stopReason": "end_turn"}})
        except Exception as exc:  # noqa: BLE001
            self._write({"jsonrpc": "2.0", "id": rid,
                         "error": {"code": -32000, "message": str(exc)}})

    def _dispatch(self, method: str, p: dict) -> dict:
        if method == "initialize":
            self.caps = p.get("clientCapabilities") or {}
            return {
                "protocolVersion": 1,
                "agentCapabilities": {"loadSession": True,
                                      "promptCapabilities": {"image": False}},
                "agentInfo": {"name": "mock-agent", "title": "Mock Agent", "version": "0.1.0"},
                "authMethods": [],
            }

        if method == "session/new":
            return {"sessionId": "mock_sess_1"}

        if method == "session/prompt":
            self._turn(p["sessionId"], p["prompt"])
            return {"stopReason": "end_turn"}

        raise RuntimeError(f"mock agent 未实现：{method}")

    # ---------- 一轮假的编码任务 ----------
    def _turn(self, sid: str, prompt: list[dict]) -> None:
        text = "".join(b.get("text", "") for b in prompt if b.get("type") == "text")

        self.update(sid, {"sessionUpdate": "plan", "entries": [
            {"content": "写 hello.py", "status": "in_progress", "priority": "high"},
            {"content": "跑一遍验证", "status": "pending", "priority": "medium"},
        ]})

        # ① 写文件（先要权限，再反向调 Client 的 fs）
        self.update(sid, {"sessionUpdate": "tool_call", "toolCallId": "tc1",
                          "title": "写 hello.py", "kind": "edit", "status": "in_progress",
                          "locations": [], "rawInput": {"path": "hello.py"}})
        if self.caps.get("fs", {}).get("writeTextFile"):
            perm = {"sessionId": sid,
                    "toolCall": {"toolCallId": "tc1", "title": "写 hello.py", "kind": "edit"},
                    "options": [{"optionId": "allow_once", "name": "Allow once", "kind": "allow_once"},
                                {"optionId": "reject_once", "name": "Reject", "kind": "reject_once"}]}
            outcome = self.request("session/request_permission", perm)
            if outcome.get("outcome", {}).get("outcome") != "selected" or \
                    outcome.get("outcome", {}).get("optionId") != "allow_once":
                self.update(sid, {"sessionUpdate": "tool_call_update", "toolCallId": "tc1",
                                  "status": "failed", "content": [{"type": "text", "text": "被拒绝"}]})
                return
            code = "print('hello acp')\n"
            self.request("fs/write_text_file", {"sessionId": sid,
                                                "path": os.path.join(CWD, "hello.py"),
                                                "content": code})
        self.update(sid, {"sessionUpdate": "tool_call_update", "toolCallId": "tc1",
                          "status": "completed",
                          "content": [{"type": "text", "text": "hello.py 已写入"}]})

        # ② 跑命令（反向调 Client 的 terminal）
        if self.caps.get("terminal"):
            self.update(sid, {"sessionUpdate": "tool_call", "toolCallId": "tc2",
                              "title": "python3 hello.py", "kind": "execute", "status": "in_progress",
                              "rawInput": {"command": "python3 hello.py"}})
            t = self.request("terminal/create", {"sessionId": sid, "command": "python3",
                                                 "args": ["hello.py"], "cwd": CWD})
            tid = t["terminalId"]
            self.request("terminal/wait_for_exit", {"sessionId": sid, "terminalId": tid})
            out = self.request("terminal/output", {"sessionId": sid, "terminalId": tid})
            self.request("terminal/release", {"sessionId": sid, "terminalId": tid})
            self.update(sid, {"sessionUpdate": "tool_call_update", "toolCallId": "tc2",
                              "status": "completed",
                              "content": [{"type": "text", "text": out.get("output", "")}]})

        # ③ 收尾
        self.update(sid, {"sessionUpdate": "agent_thought_chunk",
                          "content": {"type": "text", "text": f"（mock）收到：{text[:40]}"}})
        for chunk in ("搞定", "：", " hello.py", " 已写入并跑通。"):
            self.update(sid, {"sessionUpdate": "agent_message_chunk",
                              "content": {"type": "text", "text": chunk}})
        self.update(sid, {"sessionUpdate": "usage_update",
                          "usage": {"inputTokens": 123, "outputTokens": 45}})


if __name__ == "__main__":
    MockAgent().run()
