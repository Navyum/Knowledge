"""CH10 · 可观测与自建评测。

每轮记一条 trace；聚合成 turns/tokens/耗时。评测时每个任务前必须重置。
"""
import time


class Trace:
    def __init__(self):
        self.entries: list[dict] = []
        self._t0 = time.time()

    def record(self, turn: int, dt: float, tokens: int, action: str) -> None:
        self.entries.append({"turn": turn, "sec": round(dt, 3),
                             "tok": tokens, "action": action})

    def summary(self) -> dict:
        return {"turns": len(self.entries),
                "total_tok": sum(e["tok"] for e in self.entries),
                "total_sec": round(sum(e["sec"] for e in self.entries), 3)}

    def reset(self) -> None:
        self.entries.clear()
        self._t0 = time.time()
