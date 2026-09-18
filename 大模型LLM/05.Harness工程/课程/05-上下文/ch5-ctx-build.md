---
order: 18
---

# 动手：给 tinyharness 加压缩与外部记忆

这一节堵上 tinyharness 最大的漏洞——历史无限增长。加三样：token 计数、阈值触发的压缩、一个 `notes.md` 外部记忆。里程碑 4。做完，你的 harness 能跑真正的长任务了。

> **这一节结束时，你会有**
> tinyharness 的循环里多了：每轮估算 token → 超阈值时把旧历史总结成摘要（仿 autoCompact）→ agent 可用 `note` 工具写外部记忆。长任务不再撑爆。

## 第 1 步：token 计数（估算版）

**先能估，才能判断何时压。** 照 CH3.2：热路径用估算，别狂调 count 端点。最粗但够用的估算：字符数 / 4。

`tinyharness.py`（可运行，估算）：

```python
def estimate_tokens(messages):
    total = 0
    for m in messages:
        c = m["content"]
        text = c if isinstance(c, str) else json.dumps(c, ensure_ascii=False)
        total += len(text) // 4          # 极粗估算，英文 ~4 字符/token
    return total
```

## 第 2 步：阈值压缩（仿 autoCompact）

**留缓冲，别等满。** 照 5.3 的教训：提前留缓冲触发，保留最近几轮 + 系统信息，把中间旧历史交给模型总结成一条摘要。

`tinyharness.py`（可运行，压缩）：

```python
CONTEXT_LIMIT = 30000       # 假设窗口（演示用小值）
COMPACT_BUFFER = 6000       # 留缓冲：剩这么多就压（仿 AUTOCOMPACT_BUFFER）
KEEP_RECENT = 4             # 保留最近 N 条不压

def maybe_compact(messages):
    if estimate_tokens(messages) < CONTEXT_LIMIT - COMPACT_BUFFER:
        return messages                          # 还没到，不压
    head = messages[:1]                          # 保留首条（通常是任务）
    old, recent = messages[1:-KEEP_RECENT], messages[-KEEP_RECENT:]
    if not old:
        return messages
    # 让模型把旧历史总结成摘要（保留结论，丢弃过程）
    summary = client.messages.create(
        model="claude-sonnet-5", max_tokens=1024,
        messages=old + [{"role": "user", "content":
            "用要点总结以上对话：已完成什么、关键结论、还没解决的问题。只输出摘要。"}],
    ).content[0].text
    print("[compact] 已压缩历史")
    return head + [{"role": "user", "content": f"[历史摘要]\n{summary}"}] + recent
```

> **对照真实 harness**
> 你这个是最小版。真实的 autoCompact（5.3）还会：按 API 轮次分组压（不切碎一轮）、压缩后把正在编辑的文件重新拉回来（POST_COMPACT 恢复）、保留 thinking block。你现在缺"恢复"——如果任务里 agent 压缩后还要改某文件，得让它重新 read 一次。这正是升级方向。

## 第 3 步：外部记忆（note 工具）

**让 agent 把要点写到上下文之外。** 照 5.1 技法②：给 agent 一个写笔记的工具。压缩会丢细节，但写进 `notes.md` 的东西不会丢——需要时 read 回来。这就是"上下文只留指针"。

`tools.py`（可运行，追加 note 工具）：

```python
@tool("note", "把重要信息追加到 notes.md 外部记忆，压缩后也不会丢",
      {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]})
def note(text):
    with open("notes.md", "a") as f:
        f.write(text + "\n")
    return "已记入 notes.md"
```

在 system prompt 里加一句引导："遇到关键结论或长期要记的信息，用 note 工具写下来。"agent 就会主动用它对抗遗忘。这正是 Manus 的 Recitation/文件记忆思想的最小实现。

## 第 4 步：接进循环并跑起来

在循环里每次追加消息后，调一次 `maybe_compact`：

`tinyharness.py`（可运行，循环里插入压缩）：

```python
        messages.append({"role": "user", "content": results})
        messages = maybe_compact(messages)     # ← 就加这一行
        # 回到 while 顶部
```

终端：

```bash
$ python tinyharness.py "逐个读 src/ 下所有 .py 文件，总结每个的职责，写进 notes.md"
[调用 read_file: src/a.py]
[调用 note: a.py 负责…]
[compact] 已压缩历史          # ← 文件多时自动触发，任务继续不崩
[调用 read_file: src/b.py]
...
```

## 里程碑检查

> **里程碑 4 · 自测清单**
> - [ ] 长任务（读很多文件）不再撑爆，会看到 [compact] 触发
> - [ ] 压缩保留了首条任务 + 最近几轮，中间压成摘要
> - [ ] 阈值留了缓冲（不是满了才压）
> - [ ] agent 会用 note 工具把要点写进 notes.md
> - [ ] 能说清你的实现相比真实 autoCompact 缺了什么（恢复/分组/thinking 保留）
>
> 你的 harness 现在能跑长任务了。但它还在无脑执行危险命令——CH6 加权限。
