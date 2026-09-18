"""CH5 · 上下文管理：组装 system prompt + 压缩。

顺序即缓存：稳定的放前面（身份、工具 schema、项目记忆），变动的放后面。
压缩：历史超阈值时，把早期轮次总结掉，保留任务与近几轮。
"""
import os
import json


def load_memory(workspace: str) -> str:
    """加载项目记忆（AGENTS.md / CLAUDE.md），就近覆盖：项目级优先。"""
    for name in ("AGENTS.md", "CLAUDE.md"):
        p = os.path.join(workspace, name)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return f.read().strip()
    return ""


def build_system_prompt(tools_schemas: list, memory: str) -> str:
    """按'稳定→变动'排列，利于 KV-cache 命中。"""
    parts = [
        "你是 tinyharness 里的编码 agent。通过调用工具完成任务，"
        "完成后用纯文本给出简短总结（不再调工具即视为本轮结束）。",
        "可用工具：\n" + json.dumps(tools_schemas, ensure_ascii=False, indent=2),
    ]
    if memory:
        parts.append("项目约定（务必遵守）：\n" + memory)
    return "\n\n".join(parts)


def estimate_tokens(messages: list) -> int:
    """粗估 token 数（教学版：按字符 / 4）。"""
    return sum(len(json.dumps(m, ensure_ascii=False)) for m in messages) // 4


def compact(messages: list, keep_recent: int = 4) -> list:
    """两级压缩的最简版：保留首条（任务）+ 最近 keep_recent 条，
    中间用一条摘要占位。真实实现会调模型生成结构化摘要。"""
    if len(messages) <= keep_recent + 1:
        return messages
    head = messages[:1]
    tail = messages[-keep_recent:]
    dropped = len(messages) - len(head) - len(tail)
    summary = {"role": "user", "content":
               f"[已压缩中间 {dropped} 条历史。任务与最近进展见上下文首尾。]"}
    return head + [summary] + tail
