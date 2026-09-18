---
order: 7
---

# 动手:从零写一个最小循环

读懂了两种循环,现在亲手写一个。这是贯穿全课的实战项目 `tinyharness` 的第一块基石——一个能真的调模型、真的执行工具、真的转圈的 ReAct 循环,约 80 行 Python。后面每一章都会往它上面加东西。

> **这一节结束时,你会有**
>
> 一个文件 `tinyharness.py`,运行后能接受一句自然语言任务,让模型自主调用一个 `read_file` 工具、拿到结果、继续推理,直到给出答案。这就是一个最小但完整的 agent harness 内核。

前置:Python 3.10+,一个能用的模型 API(示例用 Anthropic Messages API 的伪封装 `call_model`,你可换成任意 provider——[CH3](../03-模型交互/ch3-io-streaming.md) 会讲真实的流式调用,本节先用非流式把骨架跑通)。

## 第 1 步:定义消息与模型调用

**消息数组 + 模型封装**

harness 的"记忆"就是一个 messages 列表([CH5](../05-上下文/ch5-ctx-principles.md) 会深挖它)。模型调用先做成一个函数,输入 messages 和 tools,返回模型响应。

```python
# tinyharness.py — 模型封装(可运行)
import json, anthropic
client = anthropic.Anthropic()   # 读环境变量 ANTHROPIC_API_KEY

def call_model(messages, tools):
    return client.messages.create(
        model="claude-sonnet-5",
        max_tokens=2048,
        messages=messages,
        tools=tools,          # 工具 schema 列表,下一步定义
    )
```

## 第 2 步:一个工具

**read_file:schema + 执行函数**

一个工具有两半:给模型看的 **schema**(它据此决定何时调、传什么参数),和真正执行的 **函数**。[CH4](../04-工具系统/ch4-tools-aci.md) 会讲工具设计的 ACI 原则,这里先做最简单的。

```python
# tinyharness.py — 工具定义(可运行)
# 给模型看的 schema
TOOLS = [{
    "name": "read_file",
    "description": "读取一个文本文件的内容",
    "input_schema": {
        "type": "object",
        "properties": {"path": {"type": "string"}},
        "required": ["path"],
    },
}]

# 真正执行的函数(名字与 schema 的 name 对应)
def run_read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        return f"错误:{e}"      # 错误也要可读地回给模型 → ACI 原则,CH4

TOOL_IMPL = {"read_file": run_read_file}
```

## 第 3 步:ReAct 循环

**看 → 想 → 做 → 记,转圈**

核心来了。这段 20 行就是你在 2.2 / 2.3 学的 ReAct 循环的最小实现——和 Claude Code 的 `queryLoop` 骨架一模一样,只是没有流式和压缩。

```python
# tinyharness.py — 循环(可运行)
def loop(user_task):
    messages = [{"role": "user", "content": user_task}]
    while True:                                     # ← 何时停:见下
        resp = call_model(messages, TOOLS)          # 看+想
        messages.append({"role": "assistant", "content": resp.content})

        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        if not tool_uses:                            # 无工具 → 自然终止
            return "".join(b.text for b in resp.content if b.type == "text")

        results = []
        for tu in tool_uses:                         # 做
            out = TOOL_IMPL[tu.name](**tu.input)
            results.append({"type": "tool_result",
                            "tool_use_id": tu.id, "content": out})
        messages.append({"role": "user", "content": results})  # 记
        # 回到 while 顶部,带着工具结果再问模型

if __name__ == "__main__":
    import sys
    print(loop(sys.argv[1]))
```

## 跑起来

```bash
$ export ANTHROPIC_API_KEY=...
$ python tinyharness.py "读一下 README.md,用一句话说它是干嘛的"
# 模型会自主调用 read_file(path="README.md"),拿到内容,再总结
```

如果它成功读了文件并总结——恭喜,你写出了一个能自主决策、调用工具、循环推进的 agent harness 内核。**这就是"loop + tokens"的全部魔法**,后面所有复杂度都是往这 80 行上加的。

## 对照真实 harness:你还差什么

诚实地讲,这个最小循环离生产级还有距离。把它和 Claude Code 的 `queryLoop` 对照,缺的每一样,正好是后面章节要补的:

| 你的最小循环 | 真实 harness(如 Claude Code) | 补在哪章 |
| --- | --- | --- |
| 非流式,等整条响应 | 流式收流,增量解析 tool_use | [CH3](../03-模型交互/ch3-io-streaming.md) |
| API 挂了就崩 | withRetry / 限流退避 / 缓存 | [CH3.2](../03-模型交互/ch3-io-reliability.md) |
| 只有 read_file | 42 个工具 + MCP + 安全护栏 | [CH4](../04-工具系统/ch4-tools-aci.md) |
| 无 system prompt 组装 | 系统提示 + 工具 schema + 记忆拼装 | [CH5.2](../05-上下文/ch5-ctx-systemprompt.md) |
| messages 无限增长会爆 | 近上限自动 compact | [CH5.3](../05-上下文/ch5-ctx-compact.md) |
| 工具直接执行,无审批 | 权限闸 + 沙箱 | [CH6](../06-权限安全/ch6-perm-principles.md) |
| `while True` 可能空转 | token 预算 + 停止钩子 + 循环卫生 | [CH9](../09-错误处理/ch9-errors.md) |

> **一个立刻能加的改进:防空转**
>
> 你的 `while True` 若模型反复调同一个失败工具,会无限烧钱。最小的护栏:加一个 `max_turns` 计数,超了就停。这正是 Claude Code `tokenBudget.ts` 做的事(2.2 讲过)。试着自己加上——这是你的循环走向生产级的第一步。

## 里程碑检查

> **里程碑 1 · 自测清单**
>
> - [ ] 能跑通"读文件并总结"的任务
> - [ ] 能说清代码里哪几行对应"看→想→做→记"
> - [ ] 能分清下面三个**不同**的概念(见下方澄清)
> - [ ] 加上了 `max_turns` 防空转
>
> 三项以上打勾,你就掌握了 harness 的心脏。带着这个 `tinyharness.py` 进入 CH3——我们要给它换上真实的流式引擎。

> **重要澄清:"无 tool_use" ≠ "任务完成"**
>
> 上面代码里 `无 tool_use → return`,准确的含义只是"**模型本轮不想再调工具了**",这是三件**不同**的事,别混:
>
> ① **模型本轮结束**:模型这次输出没有 tool_use。可能是干完了,*也可能*是它拒绝、提前收尾、或输出被 max_tokens 截断。
> ② **循环停止**:harness 决定不再转下一圈(无 tool_use、或达到 max_turns、或用户中断)。
> ③ **任务验收成功**:任务**真的**做对了——这需要**独立验收**(跑测试、检查产物),模型说"完成了"不算数。
>
> 本节的最小循环只做到 ②(靠"无 tool_use"停),**不等于** ③。真正的"完成"判定要靠独立验收——这正是 [CH10 自建评测](../10-可观测/ch10-observability.md)要补的:用预置测试客观判定,而非信模型自述。
