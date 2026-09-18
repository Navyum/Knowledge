"""CH3 · 模型交互层。

统一 ModelClient 接口：complete(system, messages, tools) -> Completion。
- ScriptedModel：离线确定性脚本，无需 API key，用于演示与测试。
- AnthropicModel：可选，检测到 ANTHROPIC_API_KEY 时启用真实模型（含流式）。

消息格式统一为 Anthropic 风格 content blocks：
  assistant: {"role":"assistant","content":[{type:"text",...}|{type:"tool_use",...}]}
  user(工具结果): {"role":"user","content":[{type:"tool_result","tool_use_id":..,"content":..}]}
"""
import os
import json
from dataclasses import dataclass, field


@dataclass
class Completion:
    text: str = ""
    tool_uses: list = field(default_factory=list)   # [{"id","name","input"}]
    tokens: int = 0


class ScriptedModel:
    """按固定剧本推进 parseDate 任务，用于离线跑通全流程。

    每次 complete 时，依据"已经看到几条 tool_result"决定下一步动作，
    模拟 ReAct：读文件 → 写测试 → 跑测试 → 完成。
    """

    def __init__(self):
        self.step = 0

    def complete(self, system, messages, tools) -> Completion:
        # 数已完成的工具轮次（user 消息里带 tool_result 的条数）
        done = sum(1 for m in messages if _has_tool_result(m))
        self.step = done
        tok = len(json.dumps(messages, ensure_ascii=False)) // 4

        if done == 0:      # 第一步：读现有实现
            return Completion(tool_uses=[_tu("t1", "read_file",
                              {"path": "parse_date.py"})], tokens=tok)
        if done == 1:      # 第二步：写测试文件
            return Completion(tool_uses=[_tu("t2", "write_file",
                              {"path": "test_parse_date.py",
                               "content": _TEST_SRC})], tokens=tok)
        if done == 2:      # 第三步：跑测试
            return Completion(tool_uses=[_tu("t3", "bash",
                              {"cmd": "python test_parse_date.py"})], tokens=tok)
        # 第四步：看到测试通过，输出总结、不再调工具 → 循环自然停止
        return Completion(text="已为 parse_date 补充时区单测并跑通（exit=0）。"
                          "改动：新增 test_parse_date.py，覆盖 +08:00 与 Z 两种时区。",
                          tokens=tok)


def _tu(tid, name, inp):
    return {"id": tid, "name": name, "input": inp}


def _has_tool_result(m):
    c = m.get("content")
    return isinstance(c, list) and any(
        isinstance(b, dict) and b.get("type") == "tool_result" for b in c)


_TEST_SRC = '''from parse_date import parse_date
from datetime import timezone, timedelta

def main():
    d = parse_date("2024-01-01T12:00:00+08:00")
    assert d.utcoffset() == timedelta(hours=8), d.utcoffset()
    z = parse_date("2024-01-01T12:00:00Z")
    assert z.utcoffset() == timedelta(0), z.utcoffset()
    print("all tests passed")

if __name__ == "__main__":
    main()
'''


class AnthropicModel:
    """可选真实后端。需 pip install anthropic 且设 ANTHROPIC_API_KEY。"""

    def __init__(self, model="claude-sonnet-5"):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model = model

    def complete(self, system, messages, tools) -> Completion:
        api_tools = [{"name": t["name"], "description": t["description"],
                      "input_schema": {"type": "object",
                          "properties": {k: {"type": "string"} for k in t["required"]},
                          "required": t["required"]}} for t in tools]
        resp = self.client.messages.create(
            model=self.model, max_tokens=2048, system=system,
            messages=messages, tools=api_tools)
        text, tus = "", []
        for block in resp.content:
            if block.type == "text":
                text += block.text
            elif block.type == "tool_use":
                tus.append({"id": block.id, "name": block.name, "input": block.input})
        return Completion(text=text, tool_uses=tus,
                          tokens=resp.usage.input_tokens + resp.usage.output_tokens)


def make_model():
    """检测环境：有 key 且装了 anthropic 就用真实模型，否则用脚本模型。"""
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            return AnthropicModel()
        except Exception:
            pass
    return ScriptedModel()
