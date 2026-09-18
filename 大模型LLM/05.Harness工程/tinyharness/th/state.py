"""CH8 · 状态持久化与恢复。

JSONL 事件日志：一行一条消息，只追加。恢复时反序列化 + 中断检测。
关键：中断的工具是"结果未知"，不是"未执行"——非幂等操作重做前必须先查。
"""
import os
import json


def append_jsonl(path: str, msg: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(msg, ensure_ascii=False) + "\n")


def _dangling_tool_use(msg: dict) -> str | None:
    """若 msg 是带 tool_use 但没配对 tool_result 的 assistant 消息，返回其 id。"""
    if msg.get("role") != "assistant":
        return None
    for b in msg.get("content", []):
        if isinstance(b, dict) and b.get("type") == "tool_use":
            return b["id"]
    return None


def load_session(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        msgs = [json.loads(l) for l in f if l.strip()]
    if msgs and (tid := _dangling_tool_use(msgs[-1])):
        # 崩溃点可能在工具执行前/中/后但结果没落盘——标"结果未知"而非"未执行"
        msgs.append({"role": "user", "content": [{"type": "tool_result",
            "tool_use_id": tid,
            "content": "[上次中断，此工具执行结果未知。若为写/命令类操作，"
                       "请先核查外部状态再决定是否重做，避免重复副作用。]"}]})
    return msgs
