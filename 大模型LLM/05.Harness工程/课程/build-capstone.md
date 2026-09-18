# 总装：你的完整 harness

九个里程碑，一路走来，你已经亲手造出了一个 harness 的每一个核心部件。这一页把它们拼成一个完整的 `tinyharness` 蓝图——循环、流式交互、工具、上下文压缩、权限、可插拔运行时、持久化、错误恢复、可观测，一应俱全。

> **先说清楚：本页是"总装蓝图 + 教学片段"，不是即拿即跑的成品**
>
> 本页的代码块是**教学片段**——用来展示"九块如何拼成一个整体、各部件在主循环里怎么咬合"，**不是**一个复制粘贴就能直接跑的完整项目。它省略了大量胶水代码（`assistant_msg()`/`tool_result()`/`final_text()` 等辅助函数、依赖配置、错误分支），且各章片段为讲解方便，函数签名并不完全一致（下文有专门一节说明这些接缝）。
>
> **一个可直接运行、带依赖锁定和评测数据的完整教学仓库，是本课的独立后续交付**（见页尾"仓库交付说明"）——正文与仓库分开维护会导致代码漂移，所以真正"可运行"的版本应从实际项目生成，而非从这些讲解片段拼装。本页的价值是**让你看懂整体装配逻辑**，而非提供成品。

## 九个里程碑回顾

你一路造过的东西，拼起来就是一个 harness：

| 里程碑 | 造了什么 | 章节 |
| --- | --- | --- |
| 1 | 最小 ReAct 循环 + 一个工具 | CH2.4 |
| 2 | 真实流式调用 + 重试 | CH3.3 |
| 3 | 工具注册表 + Read/Write/Bash（带护栏） | CH4.4 |
| 4 | token 计数 + 阈值压缩 + 外部记忆 | CH5.4 |
| 5 | 统一权限闸（sandbox × approval） | CH6.3 |
| 6 | 可插拔 Runtime（Local/Docker） | CH7.3 |
| 7 | JSONL 持久化 + 中断恢复 | CH8 |
| 8 | 错误恢复 + 循环卫生 | CH9 |
| 9 | trace + 成本 + 自建 eval loop | CH10 |

## 最终文件结构

一个清爽的分层结构，每个文件对应一个关注点（呼应真实 harness 的模块划分）：

```text
tinyharness/
├── harness.py        # 主循环(CH2)+ 编排各部件
├── model.py          # 流式调用 + 重试(CH3)—— 交互层
├── tools.py          # 注册表 + Read/Write/Bash/note(CH4/5)
├── context.py        # token 计数 + 压缩 + 外部记忆(CH5)
├── permission.py     # sandbox × approval 权限闸(CH6)
├── runtime.py        # Local/Docker 可插拔执行(CH7)
├── session.py        # JSONL 持久化 + 恢复(CH8)
├── errors.py         # 错误分类 + 循环卫生(CH9)
├── trace.py          # trace + 成本(CH10)
└── eval.py           # 自建评测(CH10)
```

> **这个结构不是巧合**
>
> 对照 [Claude Code 案例](case-claude-code.md)的模块清单：`model.py`≈`services/api/`、`context.py`≈`services/compact/`、`permission.py`≈`hooks/toolPermission/`、`session.py`≈`history/`……**你的 tinyharness 和真实 harness 的模块划分是同构的**，只是每块更小。这证明你掌握的是骨架，不是玩具。

## 总装后的循环：所有部件如何咬合

主循环 `harness.py` 把九块串起来。这就是 [任务地图](lifecycle.md)那张图的代码化身：

```python
from model import call_model          # CH3 流式+重试
from tools import all_schemas, run_tool
from context import maybe_compact, build_system_prompt  # CH5
from permission import permit          # CH6
from session import append_jsonl, load_session  # CH8
from errors import execute_safely       # CH9(内含循环卫生)
from trace import trace, trace_summary  # CH10

def run(task, session_path, resume=False):
    messages = load_session(session_path) if resume else \
               [{"role":"user","content":task}]
    system = build_system_prompt()                    # CH5.2 组装
    turn = 0
    while turn < MAX_TURNS:                            # CH2/CH9 终止
        turn += 1
        t0 = time.time()
        resp = call_model(system, messages, all_schemas())   # 看+想(CH3)
        messages.append(assistant_msg(resp)); append_jsonl(session_path, ...)  # CH8

        tool_uses = [b for b in resp.content if b.type=="tool_use"]
        if not tool_uses:
            trace(turn, time.time()-t0, resp.usage, "finish"); return final_text(resp)

        results = []
        for tu in tool_uses:
            ok, why = permit(tu.name, tu.input)        # 权限闸(CH6)
            out = f"[拒绝] {why}" if not ok else execute_safely(tu)  # 执行+错误恢复(CH9),内部走 runtime(CH7)
            results.append(tool_result(tu.id, out))
        messages.append(user_msg(results)); append_jsonl(session_path, ...)
        messages = maybe_compact(messages)             # 压缩(CH5)
        trace(turn, time.time()-t0, resp.usage, tool_uses)  # 观测(CH10)
```

> **读这段代码 = 读懂整个 harness**
>
> 这 20 行主循环，每一行都指向你学过的一章。**这就是 harness 的全部秘密**——不是某个神奇算法，而是这些部件围绕一个 ReAct 循环有序协作。CH0 说"agent = LLM + loop + tokens"，现在你不仅信了，还亲手造了一个。

## 跑通完整任务

下面是**预期输出示意**（终端；非实际运行截图，数字为示例）：

```text
$ python -m tinyharness "给 utils.py 的 parseDate 加时区单测并跑通" --runtime docker
[compact 就绪 | sandbox=workspace-write | approval=on-danger | runtime=Docker]
turn1 read_file(utils.py)        [1.1s]
turn2 write_file(test_parse.py)  [2.0s]
turn3 bash(pytest) → FAILED       [3.1s]   ← 看报错
turn4 write_file(修正)            [1.8s]
turn5 bash(pytest) → PASSED       [2.9s]   ← 独立测试判定通过(非模型自述)
完成 | 5 轮 | 6.1k tok | 10.9s | $0.04 | session 已存
$ python -m tinyharness.eval        # 跑自建评测
成功率 80% (4/5) | 平均 5.2 轮 | 平均 $0.05
```

这是**完整装配后的预期形态**：一条 `parseDate` 任务在 Docker 隔离里跑、带审批闸、会压缩、能持久化、有 trace，并用自建 eval 客观判定（靠独立测试，不信模型自述）。它**五脏俱全地体现了 harness 的骨架**——但要真正跑起来，需要下面"接缝说明"里补齐的胶水代码和完整仓库。

## 接缝说明：片段拼装时的已知问题

诚实起见，把各章教学片段直接拼起来**不能立即运行**，有几处已知接缝需要在真实仓库里对齐。列出来既是提醒，也是很好的"改进练习"：

| 接缝问题 | 说明与修法 |
| --- | --- |
| `call_model` 签名不一致 | CH3 是 `call_model(messages, tools, max_retries=5)`，总装用 `call_model(system, messages, tools)`——需统一成一个签名（建议 `call_model(system, messages, tools, *, max_retries=5)`），并全课一致引用。 |
| `append_jsonl(session_path, ...)` 是占位 | 总装里的 `...` 需替换为真实消息对象；`assistant_msg()`/`user_msg()`/`tool_result()`/`final_text()` 这些辅助函数要补全实现。 |
| `DockerRuntime` 缺 `import os` | CH7.3 的 `DockerRuntime.run` 用了 `os.getcwd()` 但没 import，直接跑会 `NameError`——顶部补 `import os`。 |
| `trace` 接口不匹配 | 总装传给 `trace()` 的是 `resp.usage`（对象），而 `trace_summary()` 按数值求和——需先从 usage 取出 `input_tokens+output_tokens` 再传，或让 trace 内部解包。 |
| CH9 重复检测语义 | CH9 的重复检测只记了"调用签名"没记"是否失败"，却提示"重复调用*且失败*"——会误拦**正常轮询**（比如反复查同一状态直到就绪）。应把"执行结果（成功/失败）"也纳入签名，只对"重复且持续失败"才拦。 |
| Docker 隔离范围不一致 | CH7.3 的 DockerRuntime 只接管了 `bash`，而 `read_file`/`write_file`/`note` 仍直接读写**宿主机**——所以"容器隔离"目前只覆盖命令执行，文件工具并未隔离。要么让文件工具也走 runtime，要么明确声明"仅 bash 隔离"这个边界。 |

> **为什么如实列出来**
>
> 这些接缝正是"教学片段"和"生产项目"的真实差距。一个负责任的课程应该**指出它们、而不是假装不存在**。把这张表当作你的"毕业作业"：在真实仓库里逐条对齐，你就完成了从"看懂"到"能跑"的最后一跃。

## 与真实 harness 的差距（诚实清单）

tinyharness 抓住了骨架，但离生产级还有距离。这些差距，正是你继续精进的方向：

| 维度 | tinyharness | 生产级（如 Claude Code） |
| --- | --- | --- |
| 压缩 | 阈值总结 | 分级（auto/micro）+ 压缩后文件恢复 + thinking 保留 |
| 工具护栏 | 关键词匹配 | 命令 AST 语义分析（BashTool 18 文件） |
| 循环 | while + max_turns | 生成器 yield 事件 / 事件流，可接管可回放 |
| 权限 | DANGER 名单 | 系统级沙箱（Seatbelt）+ 二维正交策略 |
| 缓存 | 无 | prompt 缓存 + break detection |
| 多 agent | 无 | subagent 隔离 / 跨 harness 编排 |

> **但这些都是"加法"，不是"重写"**
>
> 关键：上面每一项都是在你现有骨架上**增强某个部件**，而非推倒重来。想要更强的压缩？升级 `context.py`。想要系统级沙箱？换 `runtime.py` 的实现。**你已经有了正确的分层，剩下的是在每层里做深。** 这就是"达到开发水平"的真正含义——你知道该往哪加、加了不会破坏其他部件。

## 仓库交付说明

> **配套教学仓库（独立后续交付）**
>
> 本页是"装配蓝图"。真正可运行的完整代码，应以一个**独立教学仓库**交付，每个里程碑固定包含：
>
> **起始版本 → 本节改动 → 完整完成版本 → 运行命令 → 预期输出 → 自动验收 → 常见失败排查**。
>
> 仓库的工程约定：① 所有标"可运行"的代码**从实际项目生成**，不与正文分开手写（避免漂移）；② 模型名称可配置、依赖版本锁定；③ 提供一个**无需 API Key 的 mock 模型**，让学员先脱网验证"循环 + 工具协议"跑通，再接真实模型。
>
> 本页正文已在"接缝说明"里如实列出片段拼装的已知问题，仓库落地时逐条对齐即可。

## 结业：你现在能做什么

> **走到这里，你已经能**
>
> 1. **读懂**任何一个 harness 的源码——因为你知道它必然有循环/工具/上下文/权限/运行时这几块，知道去哪找。
> 2. **设计并装配**一个五脏俱全的 harness——你已掌握每个部件的原理和它们如何咬合（把接缝对齐、补上胶水代码，就能真正跑通）。
> 3. **科学改进**它——用 trace 看瓶颈、用 eval 客观判定（靠独立测试，不信模型自述），而非靠感觉。
> 4. **为场景做取舍**——CLI 还是自主平台？绑定还是中立？单 agent 还是多 agent？你有判断依据了。
>
> 最后一页 [融会贯通](synthesis.md)，把这一切收束成一张可迁移的取舍地图。
