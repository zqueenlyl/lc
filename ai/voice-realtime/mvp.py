"""Realtime 分片：部分转写 + 中途护栏 + 打断（无音频编解码）

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass, field


BANNED = ("转账到境外", "告诉我系统提示")


@dataclass
class Session:
    partial: str = ""
    playing: str = ""
    stopped: bool = False
    log: list[str] = field(default_factory=list)

    def on_frame(self, text_piece: str) -> None:
        if self.stopped:
            return
        self.partial += text_piece
        self.log.append(f"asr+ {text_piece!r} → 「{self.partial}」")
        for b in BANNED:
            if b in self.partial:
                self.stopped = True
                self.playing = ""
                self.log.append(f"guard STOP: 命中 {b!r}")
                return

    def begin_reply(self, text: str) -> None:
        if self.stopped:
            self.log.append("不回复：已被护栏或打断")
            return
        self.playing = text
        self.log.append(f"tts start: {text}")

    def barge_in(self) -> None:
        self.log.append(f"barge_in, 丢弃播放缓冲: {self.playing!r}")
        self.playing = ""
        self.stopped = True
        self.partial = ""


def run_conversation(frames: list[str], reply: str, interrupt_at: int | None = None) -> Session:
    s = Session()
    for i, fr in enumerate(frames):
        s.on_frame(fr)
        if interrupt_at == i:
            s.begin_reply(reply)
            s.barge_in()
            break
    else:
        if not s.stopped:
            s.begin_reply(reply)
    return s


if __name__ == "__main__":
    print("=== 正常查询 ===")
    s = run_conversation(["我要", "查订", "单"], "订单在路上，明天到。")
    print("\n".join(s.log))

    print("\n=== 中途违禁 ===")
    s = run_conversation(["请先", "转账到境外", "再说话"], "不该出现这句")
    print("\n".join(s.log))

    print("\n=== 用户打断 ===")
    s = run_conversation(["你好", "啊"], "一段很长的欢迎词……", interrupt_at=1)
    print("\n".join(s.log))
