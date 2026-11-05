#!/usr/bin/env python3
"""ACP 的浏览器版 UI（单文件，仅 Python 标准库）。

浏览器 ←(HTTP/JSON 轮询)→ 本进程 ←(JSON-RPC 2.0 over stdio / 换行分帧)→ Agent 子进程

两种 Agent：
  * demo      —— mock_agent.py，免登录，打开即用；会真实写文件、真实跑命令
  * codebuddy —— codebuddy --acp，真调 CodeBuddy CLI；首次需走 ACP 的 authenticate

运行：
    python3 web_ui.py                       # http://127.0.0.1:8765
    python3 web_ui.py --port 9000 --cwd /tmp/myproj
    python3 web_ui.py --agent codebuddy     # 默认就切到真 CLI
"""

from __future__ import annotations

import argparse
import json
import os
import queue
import subprocess
import sys
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------- #
# ACP Bridge：子进程 + JSON-RPC + 事件流
# --------------------------------------------------------------------------- #
class Bridge:
    def __init__(self, cwd: str):
        self.cwd = os.path.realpath(cwd)
        os.makedirs(self.cwd, exist_ok=True)
        self.lock = threading.RLock()
        self.events: list[dict] = []
        self.seq = 0
        self.proc: subprocess.Popen | None = None
        self.rid = 0
        self.responses: dict[int, dict] = {}
        self.perm_wait: dict[str, dict] = {}
        self.terminals: dict[str, dict] = {}
        self.session_id: str | None = None
        self.caps: dict = {}
        self.auth_methods: list[dict] = []
        self.agent = "demo"
        self.state = "idle"          # idle / ready / need_auth / working / error
        self.busy = False

    # ---------- 事件 ----------
    def emit(self, kind: str, **data) -> None:
        with self.lock:
            self.seq += 1
            self.events.append({"seq": self.seq, "kind": kind, "ts": round(time.time(), 3), **data})
            if len(self.events) > 3000:
                self.events = self.events[-1500:]
        text = data.get("text") or data.get("title") or ""
        print(f"[{kind}] {str(text)[:120]}", flush=True)

    def state_to(self, s: str) -> None:
        self.state = s
        self.emit("status", state=s, agent=self.agent, cwd=self.cwd,
                  sessionId=self.session_id, busy=self.busy)

    # ---------- 子进程 ----------
    def _command(self, agent: str) -> list[str]:
        if agent == "codebuddy":
            return ["codebuddy", "--acp"]
        return [sys.executable, os.path.join(HERE, "mock_agent.py")]

    def start(self, agent: str = "demo") -> None:
        self.stop()
        self.agent = agent
        cmd = self._command(agent)
        self.emit("log", text=f"启动 Agent：{' '.join(cmd)}")
        self.proc = subprocess.Popen(
            cmd, cwd=self.cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, bufsize=1,
        )
        threading.Thread(target=self._reader, daemon=True).start()
        threading.Thread(target=self._stderr, daemon=True).start()

        res = self.request("initialize", {
            "protocolVersion": 1,
            "clientCapabilities": {
                "fs": {"readTextFile": True, "writeTextFile": True},
                "terminal": True,
                "auth": {"terminal": True},
            },
            "clientInfo": {"name": "acp-web-ui", "title": "ACP Web UI", "version": "0.2.0"},
        }, timeout=60)
        self.caps = res.get("agentCapabilities") or {}
        self.auth_methods = res.get("authMethods") or []
        info = res.get("agentInfo") or {}
        self.emit("log", text=f"initialize 完成 · protocol v{res.get('protocolVersion')} · "
                              f"agent={info.get('name') or agent} {info.get('version', '')}")
        if self.auth_methods:
            self.emit("auth_required", methods=self.auth_methods)
            self.state_to("need_auth")
        else:
            self._new_session()

    def _new_session(self) -> None:
        res = self.request("session/new", {"cwd": self.cwd, "mcpServers": []}, timeout=120)
        self.session_id = res.get("sessionId")
        self.emit("log", text=f"会话已建立：{self.session_id}")
        self.state_to("ready")

    def authenticate(self, method_id: str) -> None:
        self.emit("log", text=f"authenticate({method_id})：请在浏览器完成登录…")
        self.request("authenticate", {"methodId": method_id}, timeout=300)
        self.emit("log", text="登录成功")
        self._new_session()

    def stop(self) -> None:
        p, self.proc = self.proc, None
        if p:
            try:
                p.terminate()
            except Exception:  # noqa: BLE001
                pass
        self.session_id = None
        self.responses.clear()
        self.terminals.clear()
        for w in self.perm_wait.values():
            w["done"].set()
        self.perm_wait.clear()

    # ---------- JSON-RPC ----------
    def _write(self, msg: dict) -> None:
        if not self.proc or not self.proc.stdin:
            raise RuntimeError("Agent 未启动")
        self.proc.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

    def request(self, method: str, params: dict, timeout: float = 300.0) -> dict:
        with self.lock:
            self.rid += 1
            rid = self.rid
        self._write({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        deadline = time.time() + timeout
        while time.time() < deadline:
            with self.lock:
                if rid in self.responses:
                    msg = self.responses.pop(rid)
                    if "error" in msg:
                        raise RuntimeError(f"{method}: {msg['error']}")
                    return msg.get("result", {})
            time.sleep(0.05)
        raise RuntimeError(f"{method} 超时（{timeout}s）")

    def notify(self, method: str, params: dict) -> None:
        self._write({"jsonrpc": "2.0", "method": method, "params": params})

    def _reader(self) -> None:
        assert self.proc and self.proc.stdout
        for line in self.proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                self.emit("log", text=f"[非 JSON] {line[:160]}")
                continue
            if "id" in msg and "method" in msg:
                threading.Thread(target=self._agent_request, args=(msg,), daemon=True).start()
            elif "id" in msg:
                with self.lock:
                    self.responses[msg["id"]] = msg
            elif msg.get("method") == "session/update":
                self.emit("update", update=(msg.get("params") or {}).get("update") or {})
        self.emit("log", text="Agent 进程已退出")

    def _stderr(self) -> None:
        assert self.proc and self.proc.stderr
        for line in self.proc.stderr:
            t = line.rstrip()
            if t:
                self.emit("log", text=f"│ {t[:200]}")

    # ---------- 一轮 prompt ----------
    def prompt(self, text: str) -> None:
        if not self.session_id or self.busy:
            return
        self.busy = True
        self.state_to("working")

        def run() -> None:
            try:
                res = self.request("session/prompt", {
                    "sessionId": self.session_id,
                    "prompt": [{"type": "text", "text": text}],
                }, timeout=1800)
                self.emit("stop", stopReason=res.get("stopReason", "?"))
            except Exception as exc:  # noqa: BLE001
                self.emit("error", text=str(exc))
            finally:
                self.busy = False
                self.state_to("ready" if self.session_id else "idle")

        threading.Thread(target=run, daemon=True).start()

    def cancel(self) -> None:
        if self.session_id:
            self.notify("session/cancel", {"sessionId": self.session_id})
            self.emit("log", text="已发送 session/cancel")

    # ---------- Agent → Client ----------
    def _agent_request(self, msg: dict) -> None:
        rid, method, p = msg["id"], msg["method"], msg.get("params") or {}
        try:
            result = self._handle(method, p)
            self._write({"jsonrpc": "2.0", "id": rid, "result": result})
        except Exception as exc:  # noqa: BLE001
            self.emit("error", text=f"{method}: {exc}")
            self._write({"jsonrpc": "2.0", "id": rid,
                         "error": {"code": -32000, "message": str(exc)}})

    def _handle(self, method: str, p: dict) -> dict:
        if method == "fs/read_text_file":
            with open(self._safe(p["path"]), encoding="utf-8") as f:
                return {"content": f.read()}

        if method == "fs/write_text_file":
            path = self._safe(p["path"])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(p["content"])
            rel = os.path.relpath(path, self.cwd)
            self.emit("file", path=rel, size=len(p["content"]))
            self.emit("log", text=f"✎ 写入 {rel}（{len(p['content'])} 字节）")
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
            self.terminals[tid] = {"proc": proc, "buf": buf}
            threading.Thread(target=self._pump, args=(proc, buf), daemon=True).start()
            self.emit("log", text=f"$ {p['command']} {' '.join(p.get('args') or [])}")
            return {"terminalId": tid}

        if method == "terminal/output":
            t = self.terminals[p["terminalId"]]
            res: dict = {"output": "".join(t["buf"]), "truncated": False}
            if t["proc"].poll() is not None:
                res["exitStatus"] = {"exitCode": t["proc"].returncode}
            return res

        if method == "terminal/wait_for_exit":
            return {"exitCode": self.terminals[p["terminalId"]]["proc"].wait()}

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

        raise RuntimeError(f"未实现方法 {method}")

    @staticmethod
    def _pump(proc: subprocess.Popen, buf: list[str]) -> None:
        assert proc.stdout
        for line in proc.stdout:
            buf.append(line)

    def _safe(self, path: str) -> str:
        return os.path.realpath(os.path.abspath(path))

    def _permission(self, p: dict) -> dict:
        call = p.get("toolCall") or {}
        options = p.get("options") or []
        key = f"p{int(time.time() * 1000)}"
        wait = {"done": threading.Event(), "optionId": None}
        self.perm_wait[key] = wait
        self.emit("permission", key=key, title=call.get("title") or "工具调用",
                  toolKind=call.get("kind") or "other", options=options)
        if not wait["done"].wait(300):
            self.perm_wait.pop(key, None)
            raise RuntimeError("权限请求超时（无人裁决）")
        self.perm_wait.pop(key, None)
        return {"outcome": {"outcome": "selected", "optionId": wait["optionId"]}}

    def decide(self, key: str, option_id: str) -> None:
        w = self.perm_wait.get(key)
        if w:
            w["optionId"] = option_id
            w["done"].set()
        self.emit("permission_done", key=key, optionId=option_id)

    # ---------- 工作区文件 ----------
    def files(self) -> list[dict]:
        out = []
        for root, dirs, names in os.walk(self.cwd):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules")]
            for n in names:
                full = os.path.join(root, n)
                out.append({"path": os.path.relpath(full, self.cwd),
                            "size": os.path.getsize(full)})
            if len(out) > 200:
                break
        return out

    def read_file(self, rel: str) -> str:
        path = self._safe(os.path.join(self.cwd, rel))
        if not path.startswith(self.cwd):
            raise RuntimeError("越界路径")
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read(20000)


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
BRIDGE: Bridge


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:  # 静音访问日志
        pass

    def _json(self, obj: dict, code: int = 200) -> None:
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self) -> None:
        u = urllib.parse.urlparse(self.path)
        if u.path == "/":
            body = HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        elif u.path == "/api/events":
            since = int(urllib.parse.parse_qs(u.query).get("since", ["0"])[0])
            with BRIDGE.lock:
                evs = [e for e in BRIDGE.events if e["seq"] > since]
            self._json({"events": evs, "seq": BRIDGE.seq, "state": BRIDGE.state,
                        "busy": BRIDGE.busy, "agent": BRIDGE.agent})
        elif u.path == "/api/files":
            self._json({"files": BRIDGE.files(), "cwd": BRIDGE.cwd})
        elif u.path == "/api/file":
            rel = urllib.parse.parse_qs(u.query).get("path", [""])[0]
            try:
                self._json({"path": rel, "content": BRIDGE.read_file(rel)})
            except Exception as exc:  # noqa: BLE001
                self._json({"error": str(exc)}, 400)
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        u = urllib.parse.urlparse(self.path)
        try:
            b = self._body()
            if u.path == "/api/start":
                BRIDGE.start(b.get("agent") or "demo")
            elif u.path == "/api/auth":
                threading.Thread(target=lambda: BRIDGE.authenticate(b["methodId"]),
                                 daemon=True).start()
            elif u.path == "/api/prompt":
                BRIDGE.prompt(b.get("text", ""))
            elif u.path == "/api/permission":
                BRIDGE.decide(b["key"], b["optionId"])
            elif u.path == "/api/cancel":
                BRIDGE.cancel()
            elif u.path == "/api/clear":
                with BRIDGE.lock:
                    BRIDGE.events = []
            else:
                return self._json({"error": "not found"}, 404)
            self._json({"ok": True})
        except Exception as exc:  # noqa: BLE001
            BRIDGE.emit("error", text=str(exc))
            self._json({"error": str(exc)}, 500)


# --------------------------------------------------------------------------- #
# 前端（单页，无外部依赖）
# --------------------------------------------------------------------------- #
HTML = r"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ACP UI · 编辑器 ↔ Agent</title>
<style>
:root{--bg:#0b0f14;--panel:#121821;--panel2:#171f2b;--line:#243040;--fg:#dce4ee;
--dim:#7d8da3;--accent:#4cc2ff;--green:#3ddc97;--yellow:#f5c451;--red:#ff6b6b;--violet:#b48cff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:14px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif}
header{height:56px;display:flex;align-items:center;gap:14px;padding:0 20px;
background:var(--panel);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10}
header h1{font-size:15px;margin:0;letter-spacing:.4px;font-weight:650}
header h1 span{color:var(--accent)}
.badge{font-size:11px;padding:3px 9px;border-radius:20px;background:var(--panel2);
border:1px solid var(--line);color:var(--dim);font-family:ui-monospace,monospace}
.dot{width:7px;height:7px;border-radius:50%;background:var(--dim);display:inline-block;margin-right:6px}
.dot.ready{background:var(--green);box-shadow:0 0 8px var(--green)}
.dot.working{background:var(--yellow);animation:pulse 1s infinite}
.dot.need_auth{background:var(--red)}
@keyframes pulse{50%{opacity:.35}}
.spacer{flex:1}
select,button,input{font:inherit;color:var(--fg);background:var(--panel2);
border:1px solid var(--line);border-radius:8px;padding:7px 11px;outline:none}
button{cursor:pointer;transition:.15s}button:hover{border-color:var(--accent);color:var(--accent)}
button.primary{background:var(--accent);color:#04121c;border-color:var(--accent);font-weight:650}
button.primary:hover{filter:brightness(1.12);color:#04121c}
button:disabled{opacity:.4;cursor:not-allowed}
main{display:grid;grid-template-columns:1fr 264px;height:calc(100vh - 56px)}
#stream{overflow-y:auto;padding:22px 26px 120px;scroll-behavior:smooth}
#composer{position:absolute;bottom:0;left:0;right:264px;padding:14px 26px 20px;
background:linear-gradient(transparent,var(--bg) 26%)}
.composer-in{display:flex;gap:10px;max-width:900px;margin:0 auto;background:var(--panel);
border:1px solid var(--line);border-radius:14px;padding:10px 12px;box-shadow:0 8px 30px #0006}
.composer-in input{flex:1;background:none;border:none;font-size:14px}
.composer-in input:focus{outline:none}
aside{border-left:1px solid var(--line);background:var(--panel);padding:18px 16px;overflow-y:auto}
aside h2{font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:var(--dim);margin:0 0 12px}
aside .path{font:11px ui-monospace,monospace;color:var(--dim);word-break:break-all;margin-bottom:14px}
.file{display:flex;justify-content:space-between;gap:8px;padding:7px 9px;border-radius:7px;cursor:pointer;
font:12px ui-monospace,monospace;color:var(--fg)}
.file:hover{background:var(--panel2);color:var(--accent)}
.file small{color:var(--dim)}
pre.code{background:#080c11;border:1px solid var(--line);border-radius:9px;padding:12px;
font:12px/1.6 ui-monospace,monospace;white-space:pre-wrap;word-break:break-all;color:#a8d8b9;max-height:40vh;overflow:auto}
.msg{margin:0 0 12px;max-width:900px}
.msg .who{font-size:11px;color:var(--dim);margin-bottom:4px;font-family:ui-monospace,monospace}
.bubble{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:11px 15px;
white-space:pre-wrap;word-break:break-word}
.bubble.user{background:#12283a;border-color:#1d4a68}
.bubble.agent{background:var(--panel)}
.card{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--violet);
border-radius:10px;padding:10px 14px;margin:8px 0;max-width:900px;font-size:13px}
.card .top{display:flex;gap:10px;align-items:center}
.kind{font:11px ui-monospace,monospace;padding:2px 7px;border-radius:5px;background:var(--panel2);
color:var(--violet);text-transform:uppercase}
.kind.execute{color:var(--yellow)}.kind.edit{color:var(--green)}.kind.read{color:var(--accent)}
.st{margin-left:auto;font-size:11px;color:var(--dim)}
.st.completed{color:var(--green)}.st.failed{color:var(--red)}.st.in_progress{color:var(--yellow)}
.card .out{font:12px ui-monospace,monospace;color:var(--dim);margin-top:6px;white-space:pre-wrap;
border-top:1px dashed var(--line);padding-top:6px}
.plan{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:10px 0;max-width:900px}
.plan h3{margin:0 0 8px;font-size:12px;color:var(--dim);text-transform:uppercase;letter-spacing:1px}
.plan div{padding:2px 0}.plan .i{display:inline-block;width:18px}
.log{font:11px/1.7 ui-monospace,monospace;color:var(--dim);padding:1px 0;white-space:pre-wrap}
.log.warn{color:var(--yellow)}.log.err{color:var(--red)}
.stop{display:inline-block;margin:10px 0;padding:4px 12px;border-radius:20px;
background:#12283a;color:var(--green);border:1px solid #1d4a68;font:12px ui-monospace,monospace}
.overlay{position:fixed;inset:0;background:#000a;display:flex;align-items:center;justify-content:center;z-index:50}
.modal{width:min(460px,90vw);background:var(--panel);border:1px solid var(--line);
border-radius:16px;padding:24px;box-shadow:0 20px 60px #000a}
.modal h3{margin:0 0 6px;font-size:16px}.modal p{color:var(--dim);margin:0 0 18px;font-size:13px}
.modal .opts{display:flex;flex-direction:column;gap:8px}
.modal button{text-align:left;padding:11px 14px}
.authbar{background:#2a1d10;border:1px solid #6a4a15;color:var(--yellow);
padding:10px 26px;font-size:13px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.authbar button{padding:4px 10px;font-size:12px}
.empty{color:var(--dim);text-align:center;margin-top:18vh;line-height:2}
.empty b{color:var(--fg);font-size:17px}
kbd{background:var(--panel2);border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:11px}
</style></head><body>
<header>
  <h1>ACP <span>UI</span></h1>
  <span class="badge">Client ↔ Agent</span>
  <span class="badge"><i class="dot" id="dot"></i><span id="state">idle</span></span>
  <span class="badge" id="cwd"></span>
  <span class="spacer"></span>
  <select id="agent" title="切换 Agent">
    <option value="demo">演示 Agent（免登录）</option>
    <option value="codebuddy">CodeBuddy CLI（真 ACP）</option>
  </select>
  <button id="restart">连接</button>
</header>
<div id="authbar" class="authbar" style="display:none"></div>
<main>
  <div style="position:relative">
    <div id="stream"></div>
    <div id="composer"><div class="composer-in">
      <input id="input" placeholder="让 Agent 写段代码… 例如：写个 hello.py 并跑通" autocomplete="off">
      <button id="send" class="primary">发送</button>
      <button id="cancel" title="session/cancel">停止</button>
    </div></div>
  </div>
  <aside>
    <h2>工作区文件</h2><div class="path" id="cwd2"></div>
    <div id="files"></div><div id="fileview"></div>
  </aside>
</main>
<div id="overlay" class="overlay" style="display:none"><div class="modal">
  <h3 id="ptitle">权限请求</h3><p id="pdesc"></p><div class="opts" id="popts"></div>
</div></div>
<script>
const $=(s)=>document.querySelector(s);
let since=0, stream=$('#stream'), permOpen=false;
const esc=(s)=>String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function scroll(){stream.scrollTop=stream.scrollHeight}
function add(html){stream.insertAdjacentHTML('beforeend',html);scroll()}
function log(t,cls=''){add(`<div class="log ${cls}">${esc(t)}</div>`)}
function files(){fetch('/api/files').then(r=>r.json()).then(d=>{
  $('#cwd2').textContent=d.cwd;
  $('#files').innerHTML=d.files.map(f=>`<div class="file" data-p="${esc(f.path)}"><span>${esc(f.path)}</span><small>${f.size}B</small></div>`).join('')||'<div class="log">（空）</div>';
  document.querySelectorAll('.file').forEach(el=>el.onclick=()=>fetch('/api/file?path='+encodeURIComponent(el.dataset.p)).then(r=>r.json()).then(x=>{
    $('#fileview').innerHTML=`<h2>${esc(x.path)}</h2><pre class="code">${esc(x.content??x.error)}</pre>`}));
})}function card(up){
  const id=up.toolCallId||'tc'+Math.random().toString(36).slice(2);
  let el=document.getElementById('card-'+id);
  if(!el){add(`<div class="card" id="card-${id}"><div class="top">
    <span class="kind ${esc(up.kind||'')}">${esc(up.kind||'other')}</span>
    <b class="title">${esc(up.title||(up.rawInput&&up.rawInput.command)||'工具调用')}</b>
    <span class="st"></span></div><div class="out"></div></div>`);el=document.getElementById('card-'+id)}
  if(up.title)el.querySelector('.title').textContent=up.title;
  if(up.status){const s=el.querySelector('.st');s.textContent=up.status;s.className='st '+up.status}
  const c=up.content;if(c!=null){
    let t=typeof c==='string'?c:Array.isArray(c)?c.map(x=>x.text??JSON.stringify(x)).join('\n'):JSON.stringify(c);
    el.querySelector('.out').textContent=t.slice(0,600)}
  else if(up.rawOutput!=null)el.querySelector('.out').textContent=String(up.rawOutput).slice(0,600);
}
function render(e){
  if(e.kind==='status'){
    $('#dot').className='dot '+e.state;$('#state').textContent=e.state;
    $('#cwd').textContent=e.cwd||'';$('#cwd2').textContent=e.cwd||'';
    $('#send').disabled=e.busy||e.state!=='ready';
  }else if(e.kind==='log'){log(e.text)}
  else if(e.kind==='error'){log('✘ '+e.text,'err')}
  else if(e.kind==='auth_required'){
    const bar=$('#authbar');bar.style.display='flex';
    bar.innerHTML='<span>⚠ 需要登录（ACP authenticate）</span>'+e.methods.map(m=>
      `<button onclick="auth('${esc(m.id)}')">${esc(m.name)}</button>`).join('');
  }else if(e.kind==='update'){
    const u=e.update,k=u.sessionUpdate;
    if(k==='agent_message_chunk'||k==='user_message_chunk'){
      let b=stream.querySelector('.bubble.typing');
      if(!b){const who=k.startsWith('user')?'你':'Agent';
        add(`<div class="msg"><div class="who">${who}</div><div class="bubble ${k.startsWith('user')?'user':'agent'} typing"></div></div>`);
        b=stream.querySelector('.bubble.typing')}
      b.textContent+=(u.content&&u.content.text)||'';
      if(k==='agent_message_chunk')b.dataset.live='1';scroll();
    }else if(k==='agent_thought_chunk'){
      const t=(u.content&&u.content.text)||'';if(t.trim())log('↳ 思考：'+t.slice(0,160));
    }else{
      stream.querySelectorAll('.bubble.typing').forEach(b=>b.classList.remove('typing'));
      if(k==='plan'){
        add(`<div class="plan"><h3>计划</h3>${(u.entries||[]).map(x=>
          `<div><span class="i">${x.status==='completed'?'■':x.status==='in_progress'?'◐':'□'}</span>${esc(x.content)}</div>`).join('')}</div>`);
      }else if(k==='tool_call'||k==='tool_call_update'){card(u)}
      else if(k==='usage_update'){log('[usage] '+JSON.stringify(u.usage))}
      else{log('['+k+']')}
    }
  }else if(e.kind==='stop'){
    stream.querySelectorAll('.bubble.typing').forEach(b=>b.classList.remove('typing'));
    add(`<div class="stop">stopReason = ${esc(e.stopReason)}</div>`);files();
  }else if(e.kind==='file'){log('✎ '+e.path+' 已写入');files()}
  else if(e.kind==='permission'){
    if(permOpen)return;permOpen=true;
    $('#ptitle').textContent='权限请求 · '+esc(e.toolKind||'other');
    $('#pdesc').textContent='['+esc(e.toolKind||'other')+'] '+esc(e.title);
    $('#popts').innerHTML=e.options.map(o=>
      `<button onclick="decide('${esc(e.key)}','${esc(o.optionId)}')">${esc(o.name)} <small>(${esc(o.kind)})</small></button>`).join('');
    $('#overlay').style.display='flex';
  }
}
function poll(){fetch('/api/events?since='+since).then(r=>r.json()).then(d=>{
  d.events.forEach(e=>{since=Math.max(since,e.seq);render(e)});
  $('#send').disabled=d.busy||d.state!=='ready';
}).catch(()=>{}).finally(()=>setTimeout(poll,220))}
function send(){const t=$('#input').value.trim();if(!t)return;
  add(`<div class="msg"><div class="who">你</div><div class="bubble user">${esc(t)}</div></div>`);
  $('#input').value='';fetch('/api/prompt',{method:'POST',body:JSON.stringify({text:t})})}
function auth(id){$('#authbar').style.display='none';log('authenticate('+id+')：等浏览器登录…','warn');
  fetch('/api/auth',{method:'POST',body:JSON.stringify({methodId:id})})}
function decide(k,id){$('#overlay').style.display='none';permOpen=false;
  fetch('/api/permission',{method:'POST',body:JSON.stringify({key:k,optionId:id})})}
$('#send').onclick=send;
$('#input').onkeydown=e=>{if(e.key==='Enter')send()};
$('#cancel').onclick=()=>fetch('/api/cancel',{method:'POST',body:'{}'});
$('#restart').onclick=()=>{stream.innerHTML='';$('#authbar').style.display='none';
  log('连接 '+ $('#agent').value +' …');fetch('/api/start',{method:'POST',body:JSON.stringify({agent:$('#agent').value})})};
files();poll();
log('ACP Web UI 就绪。点右上「连接」启动 Agent，或直接选好 Agent 后连接。');
</script></body></html>"""


def main() -> int:
    global BRIDGE
    ap = argparse.ArgumentParser(description="ACP 浏览器 UI")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--cwd", default=os.path.join(HERE, "web_workspace"))
    ap.add_argument("--agent", default="demo", choices=["demo", "codebuddy"])
    args = ap.parse_args()

    BRIDGE = Bridge(os.path.realpath(args.cwd))
    BRIDGE.state_to("idle")
    if args.agent:
        threading.Thread(target=lambda: BRIDGE.start(args.agent), daemon=True).start()

    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"ACP Web UI → http://127.0.0.1:{args.port}  (cwd={BRIDGE.cwd})", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        BRIDGE.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
