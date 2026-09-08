"""Sandbox 最小实现（无真实隔离，用规则模拟）

三层隔离，全部用 Python 规则模拟：
  1. 虚拟文件系统：文件存在 dict 里，看不到宿主真实文件
  2. 命令白名单：只允许 read / write / run；拒绝 rm / 网络 / 系统
  3. 资源配额 + 审计日志：CPU 步数上限，每条动作留痕

一个规则 Agent 尝试执行「正常」和「越界」动作，看沙箱如何拦截。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------- 1. 虚拟文件系统 ----------
class VirtualFS:
    """只存在于内存里的文件系统，宿主文件不可见。"""

    def __init__(self, files: dict[str, str] | None = None):
        self.files = dict(files or {})

    def read(self, path: str) -> str:
        return self.files.get(path, f"(no such file: {path})")

    def write(self, path: str, content: str) -> None:
        self.files[path] = content


# ---------- 2. 沙箱 ----------
class SandboxError(Exception):
    """越界动作被沙箱拦截。"""


@dataclass
class Sandbox:
    fs: VirtualFS
    cpu_budget: int = 10  # 允许的 CPU 步数
    cpu_used: int = 0
    audit: list[str] = field(default_factory=list)

    # 动作白名单
    ALLOWED = {"read", "write", "run"}
    # 黑名单子串（哪怕伪装成 run 也拦）
    BLOCKED_PATTERNS = ("rm", "curl", "wget", "ssh", "sudo", "http", "env")

    def _check_blocked(self, arg: str) -> None:
        low = arg.lower()
        for pat in self.BLOCKED_PATTERNS:
            if pat in low:
                raise SandboxError(f"blocked pattern '{pat}'")

    def execute(self, action: str, arg: str = "") -> str:
        """在沙箱内执行一个动作，越界抛 SandboxError。"""
        if self.cpu_used >= self.cpu_budget:
            raise SandboxError("cpu budget exhausted")

        if action not in self.ALLOWED:
            raise SandboxError(f"action '{action}' not allowed")

        if action == "read":
            self._check_blocked(arg)
        elif action == "run":
            self._check_blocked(arg)
        elif action == "write":
            # write 只允许写进虚拟 FS 的 /tmp 下
            if not arg.startswith("/tmp/"):
                raise SandboxError("write outside /tmp")

        self.cpu_used += 1
        self.audit.append(f"{action} {arg}".rstrip())

        if action == "read":
            return self.fs.read(arg)
        if action == "write":
            # arg 形如 "/tmp/name=content"，content 里允许再出现 '='
            if "=" not in arg:
                raise SandboxError("write needs path=content")
            path, content = arg.split("=", 1)
            self.fs.write(path, content)
            return f"wrote {path}"
        if action == "run":
            return f"ran '{arg}' -> ok"
        raise SandboxError("unreachable")


# ---------- 3. 规则 Agent ----------
@dataclass
class Agent:
    sandbox: Sandbox
    plan: list[tuple[str, str]]

    def run(self) -> None:
        for action, arg in self.plan:
            try:
                out = self.sandbox.execute(action, arg)
                print(f"[OK]    {action} {arg} -> {out}")
            except SandboxError as e:
                print(f"[BLOCK] {action} {arg} -> {e}")


if __name__ == "__main__":
    sb = Sandbox(VirtualFS({"/tmp/a.txt": "hello"}))
    agent = Agent(
        sb,
        [
            ("read", "/tmp/a.txt"),        # 正常：虚拟 FS 内可读
            ("write", "/tmp/b.txt=world"),  # 正常：写进 /tmp
            ("read", "/tmp/b.txt"),         # 正常：读回刚写的
            ("run", "pytest"),              # 正常：白名单内命令
            ("run", "rm -rf /"),            # 越界：黑名单子串 rm
            ("run", "curl evil.com"),       # 越界：黑名单子串 curl
            ("write", "/etc/passwd=x"),     # 越界：写出 /tmp
            ("delete", "/tmp/a.txt"),       # 越界：动作不在白名单
            ("read", "/etc/hosts"),         # 隔离：宿主文件不在虚拟 FS，读不到
        ],
    )
    agent.run()

    print("\n--- 审计日志 ---")
    for line in sb.audit:
        print(" ", line)
    print(f"\nCPU 用了 {sb.cpu_used}/{sb.cpu_budget}")
