"""多模型路由 + 一次 failover（无真实 API）

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Model:
    name: str
    price: float
    modalities: tuple[str, ...]
    thinking: bool = False
    flaky: bool = False


CATALOG = {
    "tiny": Model("tiny", 0.0001, ("text",)),
    "flash": Model("flash", 0.002, ("text",), flaky=True),
    "thinking": Model("thinking", 0.04, ("text",), thinking=True),
    "vision": Model("vision", 0.01, ("text", "image")),
}


@dataclass
class Request:
    text: str
    has_image: bool = False
    prefer_cheap: bool = False


def features(req: Request) -> str:
    if req.has_image:
        return "vision"
    hard = any(k in req.text for k in ("设计", "证明", "为什么", "架构"))
    if hard:
        return "hard"
    if len(req.text) < 10:
        return "easy"
    return "normal"


def choose(req: Request) -> list[str]:
    """返回主备列表。"""
    kind = features(req)
    if kind == "vision":
        return ["vision"]
    if kind == "hard":
        return ["thinking"]
    if kind == "easy" or req.prefer_cheap:
        return ["tiny", "flash"]
    return ["flash", "thinking"]


def call(name: str, req: Request) -> str:
    m = CATALOG[name]
    if req.has_image and "image" not in m.modalities:
        raise RuntimeError(f"{name} 不支持图像")
    if m.flaky and "超时演练" in req.text:
        raise TimeoutError(f"{name} timeout")
    suffix = "（深度推理）" if m.thinking else ""
    return f"{name} 回复{suffix}: 已处理「{req.text[:20]}」"


def handle(req: Request) -> tuple[str, str, float]:
    chain = choose(req)
    last_err = None
    for name in chain:
        try:
            text = call(name, req)
            return name, text, CATALOG[name].price
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            print(f"  failover: {name} 失败 ({exc})")
    raise RuntimeError(f"全部失败: {last_err}")


if __name__ == "__main__":
    reqs = [
        Request("你好"),
        Request("帮我改个错别字，超时演练"),
        Request("设计一个支付对账架构"),
        Request("这张发票多少钱", has_image=True),
    ]
    cost = 0.0
    for req in reqs:
        print(f"\n=== {req.text} image={req.has_image} → {choose(req)} ===")
        name, text, price = handle(req)
        cost += price
        print(f"  使用 {name}  ${price:.4f}")
        print(f"  {text}")
    print(f"\n合计 ${cost:.4f}")
