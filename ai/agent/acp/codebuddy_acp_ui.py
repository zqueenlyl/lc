#!/usr/bin/env python3
"""用 ACP 驱动 CodeBuddy CLI 的最小终端 UI（仅标准库）。

它扮演 ACP 的 **Client** 一侧：把 `codebuddy --acp` 当子进程起，
用 JSON-RPC 2.0 over stdio（换行分帧）完成一次真实编码任务：

    initialize → session/new → session/prompt
      ← session/update: plan / tool_call / tool_call_update / message_chunk
      → fs/read_text_file · fs/write_text_file · terminal/* · request_permission
      → stopReason

运行：
    python3 codebuddy_acp_ui.py                    # 交互式，工作区 ./workspace
    python3 codebuddy_acp_ui.py --cwd /path/to/proj
    python3 codebuddy_acp_ui.py --yes              # 权限自动放行（无人值守）
    echo "写一个 hello.py" | python3 codebuddy_acp_ui.py --yes --once

首次运行会走 ACP 的 `authenticate`：`codebuddy` 的 authMethods 是
iOA / external(Google·GitHub) / internal(微信) / selfhosted(企业域)，
默认类型 `agent` 由 Agent 自己拉起登录页，等浏览器里点完才返回。

UI 内命令： /quit 退出 · /new 新开会话 · /load <id> 恢复会话 · /tools 列出本轮工具卡片
说明：本脚本会真实读写 --cwd 下的文件、真实执行 Agent 发起的命令。
"""

from __future__ import annotations

import argparse
import json
import os
import queue
import readline  # noqa: F401  （让 input() 支持行编辑与历史）
import subprocess
import sys
import threading
import time

# --------------------------------------------------------------------------- #
# 终端渲染
# --------------------------------------------------------------------------- #
C_RESET = "\033[0m"
C_DIM = "\033[2m"
C_BOLD = "\033[1m"
C_CYAN = "\033[36m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_RED = "\033[31m"
C_MAGENTA = "\033[35m"

STATUS_ICON = {
    "pending": f"{C_DIM}○{C_RESET}",
    "in_progress": f"{C_YELLOW}◐{C_RESET}",
    "completed": f"{C_GREEN}✔{C_RESET}",
    "failed": f"{C_RED}✘{C_RESET}",
}
PLAN_ICON = {
    "pending": f"{C_DIM}□{C_RESET}",
    "in_progress": f"{C_YELLOW}◐{C_RESET}",
    "completed": f"{C_GREEN}■{C_RESET}",
}


def dim(s: str) -> str:
    return f"{C_DIM}{s}{C_RESET}"


# --------------------------------------------------------------------------- #
# ACP Client：JSON-RPC 2.0 over stdio（换行分帧）
# --------------------------------------------------------------------------- #
class AcpClient:
    def __init__(self, command: list[str], cwd: str, verbose: bool = False):
        self.cwd = os.path.abspath(cwd)
        self.verbose = verbose
        self.proc = subprocess.Popen(
            command,
            cwd=self.cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._id = 0
        self._lock = threading.Lock()
        self._responses: dict[int, dict] = {}
        self._cond = threading.Condition()
        self._requests: queue.Queue[dict] = queue.Queue()
        self._dead = False

        threading.Thread(target=self._reader, daemon=True).start()
        threading.Thread(target=self._stderr, daemon=True).start()

    # ---------- 发送 ----------
    def _write(self, payload: dict) -> None:
        line = json.dumps(payload, ensure_ascii=False)
        if self.verbose:
            print(dim(f"» {line[:400]}"))
        assert self.proc.stdin
        self.proc.stdin.write(line + "\n")
        self.proc.stdin.flush()

    def request(self, method: str, params: dict, timeout: float = 300.0) -> dict:
        with self._lock:
            self._id += 1
            rid = self._id
        self._write({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        deadline = time.time() + timeout
        with self._cond:
            while rid not in self._responses:
                if self._dead or time.time() > deadline:
                    raise RuntimeError(f"{method} 超时或 Agent 已退出")
                self._cond.wait(0.2)
            msg = self._responses.pop(rid)
        if "error" in msg:
            raise RuntimeError(f"{method} 出错: {msg['error']}")
        return msg.get("result", {})

    def notify(self, method: str, params: dict) -> None:
        self._write({"jsonrpc": "2.0", "method": method, "params": params})

    def respond(self, rid: int, result: dict) -> None:
        self._write({"jsonrpc": "2.0", "id": rid, "result": result})

    def respond_error(self, rid: int, code: int, message: str) -> None:
        self._write({"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": message}})

    # ---------- 接收 ----------
    def _reader(self) -> None:
        assert self.proc.stdout
        for line in self.proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                print(dim(f"[非 JSON 行] {line[:200]}"))
                continue
            if self.verbose:
                print(dim(f"« {line[:400]}"))
            if "id" in msg and "method" in msg:
                self._requests.put(msg)          # Agent → Client 的请求
            elif "id" in msg:
                with self._cond:
                    self._responses[msg["id"]] = msg
                    self._cond.notify_all()
            elif "method" in msg:
                self.on_notification(msg)         # 通知（无回包）
        self._dead = True

    def _stderr(self) -> None:
        assert self.proc.stderr
        for line in self.proc.stderr:
            print(dim(f"  │ {line.rstrip()}"))

    # 供 UI 覆写
    def on_notification(self, msg: dict) -> None:  # pragma: no cover - 由 UI 覆写
        pass


# --------------------------------------------------------------------------- #
# UI：渲染 + Agent 反向调用的实现
# --------------------------------------------------------------------------- #
class AcpUI:
    def __init__(self, client: AcpClient, auto_approve: bool, cwd: str):
        self.c = client
        self.cwd = os.path.realpath(cwd)   # macOS 上 /tmp 是 /private/tmp 的软链，统一真身再比路径
        self.auto = auto_approve
        self.session_id: str | None = None
        self.auth_methods: list[dict] = []
        self.tool_calls: dict[str, dict] = {}
        self.terminals: dict[str, dict] = {}
        self.text_open = False
        client.on_notification = self.on_notification  # type: ignore[assignment]
        threading.Thread(target=self._serve_requests, daemon=True).start()

    # ---------- 生命周期 ----------
    def initialize(self) -> dict:
        res = self.c.request(
            "initialize",
            {
                "protocolVersion": 1,
                "clientCapabilities": {
                    "fs": {"readTextFile": True, "writeTextFile": True},
                    "terminal": True,
                    "auth": {"terminal": True},
                },
                "clientInfo": {"name": "acp-tui", "title": "ACP TUI", "version": "0.1.0"},
            },
            timeout=60,
        )
        info = res.get("agentInfo") or {}
        caps = res.get("agentCapabilities") or {}
        self.auth_methods = res.get("authMethods") or []
        print(dim(f"已连接：{info.get('name') or 'codebuddy'} {info.get('version', '')} · "
                  f"protocol v{res.get('protocolVersion')} · "
                  f"loadSession={caps.get('loadSession', False)} · "
                  f"authMethods={[m.get('id') for m in self.auth_methods]}"))
        return res

    def authenticate(self, method_id: str | None, command: list[str]) -> None:
        """ACP 的 `authenticate`：协议驱动的由 Agent 自己弹登录，`terminal` 类型由 Client 起进程。"""
        if not self.auth_methods:
            return
        method = None
        for m in self.auth_methods:
            if method_id and m.get("id") == method_id:
                method = m
                break
        if method is None:
            method = self.auth_methods[0]
            if not method_id and not self.auto:
                print(f"{C_YELLOW}需要登录{C_RESET}")
                for i, m in enumerate(self.auth_methods, 1):
                    print(f"   {i}. {m.get('name')} ({m.get('id')})")
                raw = input("  选择登录方式 [1] > ").strip()
                idx = int(raw) - 1 if raw.isdigit() else 0
                method = self.auth_methods[min(max(idx, 0), len(self.auth_methods) - 1)]

        if (method.get("type") or "agent") == "terminal":
            args = method.get("args") or []
            env = {**os.environ, **(method.get("env") or {})}
            print(dim(f"  $ {command[0]} {' '.join(args)}   （终端登录）"))
            rc = subprocess.run([*command, *args], cwd=self.cwd, env=env).returncode
            if rc != 0:
                raise RuntimeError(f"终端登录失败，退出码 {rc}")
            self.initialize()
            return

        print(f"{C_YELLOW}等待登录完成{C_RESET}：{method.get('name')} —— 请在浏览器里确认，完成后自动继续")
        try:
            self.c.request("authenticate", {"methodId": method.get("id")}, timeout=300)
        except RuntimeError as exc:
            raise RuntimeError(f"登录未完成（{exc}）。可换 --auth-method 重试，或先在终端跑 {command[0]} 登录") from exc
        print(f"{C_GREEN}登录成功{C_RESET}")

    def new_session(self) -> None:
        try:
            res = self.c.request("session/new", {"cwd": self.cwd, "mcpServers": []}, timeout=120)
        except RuntimeError as exc:
            if "Authentication required" in str(exc):
                raise RuntimeError("尚未登录：Agent 拒绝了 session/new（auth_required）") from exc
            raise
        self.session_id = res.get("sessionId")
        print(dim(f"会话已建立：{self.session_id} · cwd={self.cwd}"))

    # ---------- 渲染 ----------
    def _end_text(self) -> None:
        if self.text_open:
            print()
            self.text_open = False

    def on_notification(self, msg: dict) -> None:
        if msg.get("method") != "session/update":
            return
        up = (msg.get("params") or {}).get("update") or {}
        kind = up.get("sessionUpdate")

        if kind == "agent_message_chunk":
            text = (up.get("content") or {}).get("text", "")
            self._end_text()
            print(f"{C_CYAN}◆ Agent{C_RESET} {text}", end="", flush=True)
            self.text_open = True

        elif kind == "agent_thought_chunk":
            text = (up.get("content") or {}).get("text", "")
            if text.strip():
                print(dim(f"  ↳ 思考：{text[:160]}"))

        elif kind == "tool_call":
            self._end_text()
            tid = up.get("toolCallId", "?")
            self.tool_calls[tid] = up
            title = up.get("title") or (up.get("rawInput") or {}).get("command") or "工具调用"
            locs = [f"{l.get('path')}:{l.get('line', '')}" for l in up.get("locations") or []]
            print(f"{C_MAGENTA}▸ {up.get('kind', 'other')}{C_RESET} {title}"
                  + (dim(f"  [{', '.join(locs)}]") if locs else ""))

        elif kind == "tool_call_update":
            self._end_text()
            tid = up.get("toolCallId", "?")
            prev = self.tool_calls.get(tid, {})
            prev.update(up)
            self.tool_calls[tid] = prev
            icon = STATUS_ICON.get(up.get("status", ""), "·")
            title = prev.get("title") or "工具调用"
            tail = ""
            if up.get("status") in ("completed", "failed"):
                out = self._flatten(up.get("content"))
                if out:
                    tail = dim(" → " + out[:200].replace("\n", " ⏎ "))
            print(f"  {icon} {title}{tail}")

        elif kind == "plan":
            self._end_text()
            print(f"{C_BOLD}计划{C_RESET}")
            for e in up.get("entries", []):
                print(f"  {PLAN_ICON.get(e.get('status', ''), '·')} {e.get('content')}")

        elif kind == "usage_update":
            u = up.get("usage") or {}
            print(dim(f"  [usage] {u}"))

        elif kind in ("available_commands_update", "current_mode_update", "config_option_update"):
            print(dim(f"  [{kind}] {up}"))

        else:
            self._end_text()
            print(dim(f"  [{kind}]"))

    @staticmethod
    def _flatten(content) -> str:
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return "\n".join(AcpUI._flatten(c) for c in content)
        if isinstance(content, dict):
            if content.get("type") == "text":
                return content.get("text", "")
            if "content" in content:
                return AcpUI._flatten(content["content"])
        return json.dumps(content, ensure_ascii=False)[:300]

    # ---------- 一轮 prompt ----------
    def prompt(self, text: str) -> str:
        assert self.session_id
        self._end_text()
        print(f"{C_BOLD}▷ 你{C_RESET} {text}")
        res = self.c.request(
            "session/prompt",
            {"sessionId": self.session_id, "prompt": [{"type": "text", "text": text}]},
            timeout=1800,
        )
        self._end_text()
        reason = res.get("stopReason", "?")
        color = C_GREEN if reason == "end_turn" else C_YELLOW
        print(f"{color}[stopReason={reason}]{C_RESET}\n")
        return reason

    def cancel(self) -> None:
        if self.session_id:
            self.c.notify("session/cancel", {"sessionId": self.session_id})

    # ---------- Agent → Client 的请求（fs / terminal / 权限）----------
    def _serve_requests(self) -> None:
        while True:
            msg = self.c._requests.get()
            rid, method = msg.get("id"), msg.get("method")
            params = msg.get("params") or {}
            try:
                self.c.respond(rid, self._handle(method, params))
            except Exception as exc:  # noqa: BLE001
                print(f"{C_RED}处理 {method} 失败：{exc}{C_RESET}")
                self.c.respond_error(rid, -32000, str(exc))

    def _handle(self, method: str, p: dict) -> dict:
        if method == "fs/read_text_file":
            path = self._safe(p["path"])
            with open(path, encoding="utf-8") as fh:
                return {"content": fh.read()}

        if method == "fs/write_text_file":
            path = self._safe(p["path"])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(p["content"])
            rel = os.path.relpath(path, self.cwd)
            print(f"{C_GREEN}✎ 写入{C_RESET} {rel} ({len(p['content'])} 字节)")
            return {}

        if method == "terminal/create":
            tid = f"t{len(self.terminals) + 1}"
            proc = subprocess.Popen(
                [p["command"], *(p.get("args") or [])],
                cwd=p.get("cwd") or self.cwd,
                env={**os.environ, **{e["name"]: e["value"] for e in p.get("env") or []}},
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
            )
            buf: list[str] = []
            self.terminals[tid] = {"proc": proc, "buf": buf, "cmd": p["command"]}
            threading.Thread(target=self._pump, args=(proc, buf), daemon=True).start()
            print(dim(f"  $ {p['command']} {' '.join(p.get('args') or [])}"))
            return {"terminalId": tid}

        if method == "terminal/output":
            t = self.terminals[p["terminalId"]]
            out = "".join(t["buf"])
            res = {"output": out, "truncated": False}
            if (t["proc"].poll()) is not None:
                res["exitStatus"] = {"exitCode": t["proc"].returncode}
            return res

        if method == "terminal/wait_for_exit":
            t = self.terminals[p["terminalId"]]
            return {"exitCode": t["proc"].wait()}

        if method == "terminal/kill":
            self.terminals[p["terminalId"]]["proc"].kill()
            return {}

        if method == "terminal/release":
            t = self.terminals.pop(p["terminalId"], None)
            if t and t["proc"].poll() is None:
                t["proc"].terminate()
            return {}

        if method == "session/request_permission":
            return self._permission(p)

        raise RuntimeError(f"未实现的方法：{method}")

    @staticmethod
    def _pump(proc: subprocess.Popen, buf: list[str]) -> None:
        assert proc.stdout
        for line in proc.stdout:
            buf.append(line)

    def _safe(self, path: str) -> str:
        path = os.path.realpath(os.path.abspath(path))
        if not path.startswith(self.cwd):
            print(f"{C_YELLOW}⚠ 越界路径{C_RESET} {path}（cwd={self.cwd}）")
        return path

    def _permission(self, p: dict) -> dict:
        call = p.get("toolCall") or {}
        options = p.get("options") or []
        title = call.get("title") or call.get("kind") or "工具调用"
        if self.auto:
            pick = self._pick(options, ("allow_once", "allow_always"))
            print(dim(f"  ⚡ 自动放行：{title} → {pick}"))
            return {"outcome": {"outcome": "selected", "optionId": pick}}
        self._end_text()
        print(f"\n{C_YELLOW}⚠ 权限请求{C_RESET} [{call.get('kind', 'other')}] {title}")
        for i, o in enumerate(options, 1):
            print(f"   {i}. {o.get('name')} ({o.get('kind')})")
        try:
            raw = input("  选择 [1] / n 拒绝 / a 始终允许 > ").strip().lower()
        except EOFError:
            raw = "1"
        if raw in ("n", "no"):
            pick = self._pick(options, ("reject_once", "reject_always"))
        elif raw in ("a", "always"):
            pick = self._pick(options, ("allow_always", "allow_once"))
        else:
            idx = int(raw) - 1 if raw.isdigit() else 0
            pick = options[min(max(idx, 0), len(options) - 1)].get("optionId", "allow_once")
        return {"outcome": {"outcome": "selected", "optionId": pick}}

    @staticmethod
    def _pick(options: list[dict], kinds: tuple[str, ...]) -> str:
        for k in kinds:
            for o in options:
                if o.get("kind") == k:
                    return o.get("optionId", k)
        return options[0].get("optionId", "allow_once") if options else "allow_once"


# --------------------------------------------------------------------------- #
# 主循环
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="ACP 终端 UI（驱动 CodeBuddy CLI）")
    ap.add_argument("--cmd", default="codebuddy", help="Agent 命令，默认 codebuddy")
    ap.add_argument("--cwd", default="./workspace", help="会话工作区（Agent 只读写这里）")
    ap.add_argument("--yes", action="store_true", help="权限自动放行")
    ap.add_argument("--auth-method", default=None,
                    help="登录方式 id（codebuddy: iOA / external / internal / selfhosted）")
    ap.add_argument("--once", action="store_true", help="从 stdin 读一行，跑完即退出")
    ap.add_argument("--verbose", action="store_true", help="打印原始 JSON-RPC 帧")
    args = ap.parse_args()

    cwd = os.path.realpath(os.path.abspath(args.cwd))
    os.makedirs(cwd, exist_ok=True)

    print(f"{C_BOLD}ACP 终端 UI{C_RESET} · agent={args.cmd} --acp · cwd={cwd}")
    print(dim("命令：/quit 退出 · /new 新会话 · /tools 本轮工具卡片 · Ctrl-C 取消当前轮\n"))

    # --cmd 可以是多段命令，例：--cmd "python3 mock_agent.py"
    client = AcpClient(args.cmd.split() + ["--acp"], cwd=cwd, verbose=args.verbose)
    try:
        ui = AcpUI(client, auto_approve=args.yes, cwd=cwd)
        ui.initialize()
        if ui.auth_methods:
            ui.authenticate(args.auth_method, [args.cmd])
        ui.new_session()

        if args.once:
            task = sys.stdin.readline().strip()
            if task:
                ui.prompt(task)
            return 0

        while True:
            try:
                raw = input(f"{C_GREEN}你 › {C_RESET}").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return 0
            if not raw:
                continue
            if raw in ("/quit", "/exit"):
                return 0
            if raw == "/new":
                ui.new_session()
                continue
            if raw == "/tools":
                for tid, tc in ui.tool_calls.items():
                    print(f"  {tc.get('kind')} · {tc.get('title')} · {tc.get('status')} · {tid}")
                continue
            try:
                ui.prompt(raw)
            except KeyboardInterrupt:
                ui.cancel()
                print(f"\n{dim('已发送 session/cancel')}")
    finally:
        try:
            client.proc.terminate()
        except Exception:  # noqa: BLE001
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
