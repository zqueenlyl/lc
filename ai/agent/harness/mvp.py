"""最小编码 Harness：四件套 + 插件槽（无 LLM）

默认工具对齐 Pi：read / write / edit / bash。
另注册插件 run_tests，演示「一切皆插件」——测试不是焊死在内核里。

工作区里有一个算错税率的函数；循环：观察 → 选工具 → 执行 → 直到测试通过。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


# --- 假仓库 ---

BUGGY = """\
def tax(amount: int) -> int:
    # 错误：把 13% 写成了 3%
    return amount * 3 // 100
"""

TEST = """\
from shop import tax

def test_tax():
    assert tax(100) == 13, tax(100)
"""


@dataclass
class Workspace:
    files: dict[str, str]
    last_cmd: str = ""
    last_out: str = ""

    def read(self, path: str) -> str:
        if path not in self.files:
            raise FileNotFoundError(path)
        return self.files[path]

    def write(self, path: str, content: str) -> str:
        self.files[path] = content
        return f"wrote {path} ({len(content)} bytes)"

    def edit(self, path: str, old: str, new: str) -> str:
        src = self.read(path)
        if old not in src:
            return f"edit failed: pattern not found in {path}"
        self.files[path] = src.replace(old, new, 1)
        return f"edited {path}"

    def bash(self, cmd: str) -> str:
        self.last_cmd = cmd
        if cmd.strip() == "ls":
            self.last_out = "\n".join(sorted(self.files))
        elif cmd.startswith("cat "):
            path = cmd.split(maxsplit=1)[1]
            self.last_out = self.read(path)
        else:
            self.last_out = f"unsupported in sandbox: {cmd}"
        return self.last_out


# --- Harness ---

ToolFn = Callable[..., str]


@dataclass
class Harness:
    ws: Workspace
    tools: dict[str, ToolFn] = field(default_factory=dict)
    log: list[str] = field(default_factory=list)

    def register(self, name: str, fn: ToolFn) -> None:
        self.tools[name] = fn

    def call(self, name: str, **kwargs) -> str:
        if name not in self.tools:
            raise KeyError(f"unknown tool {name}; plugins={list(self.tools)}")
        out = self.tools[name](**kwargs)
        self.log.append(f"{name}({kwargs}) -> {out[:80]!r}")
        return out


def plugin_run_tests(ws: Workspace) -> str:
    """插件：执行内嵌断言，不开放任意代码。"""
    ns: dict = {}
    exec(ws.files["shop.py"], ns)  # noqa: S102 — 受控教学仓库
    try:
        assert ns["tax"](100) == 13
        return "PASS"
    except Exception as e:  # noqa: BLE001 — 要把失败喂回循环
        return f"FAIL: {e}"


# --- 「模型」：可解释规则，不是神经网络 ---

@dataclass
class PolicyAgent:
    harness: Harness
    max_steps: int = 8

    def run(self, goal: str) -> str:
        for step in range(1, self.max_steps + 1):
            src = self.harness.call("read", path="shop.py")
            if "amount * 3 // 100" in src:
                self.harness.call(
                    "edit",
                    path="shop.py",
                    old="amount * 3 // 100",
                    new="amount * 13 // 100",
                )
            result = self.harness.call("run_tests")
            print(f"step {step}: tests {result}")
            if result == "PASS":
                return f"done in {step} steps; goal={goal!r}"
        return "gave up"


def main() -> None:
    ws = Workspace(files={"shop.py": BUGGY, "test_shop.py": TEST})
    h = Harness(ws)
    # 最小核（Pi）
    h.register("read", lambda path: ws.read(path))
    h.register("write", lambda path, content: ws.write(path, content))
    h.register("edit", lambda path, old, new: ws.edit(path, old, new))
    h.register("bash", lambda cmd: ws.bash(cmd))
    # 插件（DeepSeek 取向：测试能力外挂）
    h.register("run_tests", lambda: plugin_run_tests(ws))

    print("tools:", sorted(h.tools))
    print("ls:\n", h.call("bash", cmd="ls"))
    print(PolicyAgent(h).run("fix VAT to 13%"))
    print("shop.py now:\n", ws.read("shop.py"))
    print("--- tool log ---")
    for line in h.log:
        print(line)


if __name__ == "__main__":
    main()
