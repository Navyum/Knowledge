# Claude Code 工具体系深剖

Claude Code 有 42 个内置工具。这一节挑三个最有代表性的,看它把 4.1 的 ACI 原则落成了什么样的真实代码——尤其是 BashTool,一个"跑命令"的工具背后藏着 18 个文件的安全设计。

> **关于本节源码**：基于 Claude Code 泄露 source map 还原（来源见[附录 C](appendix.md)）。只讲架构、文件职责与设计思路,代码为原创伪代码示意,不复制真实源码。

> **回到任务**：[任务地图](lifecycle.md)第 ⑩ 步"跑测试（危险操作）"。`parseDate` 任务要跑 `pytest`,靠的就是 BashTool。而"跑任意命令"是 agent 最危险的能力——本节你会看到 Claude Code 为这一个工具堆了多少安全设计。

## 先看一个工具怎么组织

Claude Code 每个工具是 `src/tools/` 下一个独立目录。以最简单的 `src/tools/FileReadTool/` 为例,它拆成几个文件：`prompt.ts`（给模型的 schema 与描述）、`UI.tsx`（结果怎么在终端渲染）、`utils.ts`（执行逻辑）。一个工具 = **schema + 执行 + 结果格式化**,和你 CH2 写的 `read_file` 同构,只是拆得更细。

注意一个 ACI 细节：FileReadTool 的 `prompt.ts` 里有 `MAX_LINES_TO_READ = 2000`——**读文件有行数上限**。这正是 ACI 原则 2（紧凑）的直接落地：防止 `cat` 一个巨型文件把上下文冲垮。

| 42 工具（部分） | 类别 | ACI 体现 |
| --- | --- | --- |
| Read / Write / Edit / Glob / Grep | 文件与检索 | 行数上限、唯一匹配、结果裁剪 |
| Bash / PowerShell | 命令执行 | AST（Abstract Syntax Tree，抽象语法树）安全分析、沙箱、破坏性警告 |
| Task / Agent / SendMessage | 子 agent 与协作 | 上下文隔离（→ CH12） |
| MCPTool / McpAuth | MCP 扩展 | 外部工具接入（→ 4.1） |
| EnterPlanMode / ExitPlanMode | 模式控制 | 约束 agent 行为阶段 |

## BashTool：一个命令工具,18 个文件的安全

这是最能说明"ACI 护栏"分量的例子。`src/tools/BashTool/` 目录里有 18 个文件,真正"执行命令"的逻辑只是一小部分,大半在做**执行前的安全判断**：

| 文件 | 职责 |
| --- | --- |
| `bashSecurity.ts` | 安全分析主逻辑 |
| `bashPermissions.ts` | 权限判断：这条命令要不要问用户（→ CH6） |
| `commandSemantics.ts` | 理解命令语义：它到底想干什么 |
| `destructiveCommandWarning.ts` | 识别破坏性命令（rm -rf 之类）并警告 |
| `pathValidation.ts` · `readOnlyValidation.ts` | 路径校验、只读模式校验 |
| `sedValidation.ts` · `sedEditParser.ts` | 专门解析/校验 sed 命令 |
| `shouldUseSandbox.ts` | 判断这条命令要不要进沙箱（→ CH6/CH7） |

> **为什么要 AST 解析命令**
>
> 关键设计：BashTool **不是拿到字符串直接扔进 shell**,而是先解析命令结构（语义分析）,搞清"这条命令是读还是写?会不会删东西?碰哪些路径?",据此决定：要不要问用户（权限）、要不要进沙箱（隔离）、要不要警告（破坏性）。
>
> 这就是 ACI 原则 4（护栏）的极致体现——**在执行前理解意图,而非执行后收拾残局**。你 CH2 的 `read_file` 只是 try/except,而生产级的命令工具要在动手前就把危险拦下。

**BashTool 执行前的安全管线（还原思路,伪代码）：**

```python
def bash_tool(command, mode):
    ast = parse_command(command)                 # commandSemantics
    if is_destructive(ast):                       # destructiveCommandWarning
        warn_user(ast)
    if mode == "read-only" and writes(ast):       # readOnlyValidation
        return "拒绝:只读模式下不能执行写操作"
    if needs_permission(ast):                     # bashPermissions → CH6
        if not ask_user(ast): return "用户拒绝"
    sandbox = should_use_sandbox(ast)             # shouldUseSandbox → CH7
    return execute(command, sandbox=sandbox)      # 真正执行只是最后一步
```

## FileEditTool：如何让模型可靠地改文件

`src/tools/FileEditTool/`。核心难题：模型说"把 A 改成 B",harness 怎么**精确、安全**地定位并替换?

Claude Code 的方案是 **old_string / new_string 唯一匹配**：模型要提供一段"旧文本"和"新文本",harness 要求旧文本在文件中**唯一出现**,匹配不到或匹配多处就报错,要求模型重新给更精确的上下文。

> **这是护栏,不是限制**
>
> 为什么不让模型直接给行号或整文件?因为行号会漂移、整文件重写易丢改动。"唯一匹配"强制模型提供足够的上下文来**无歧义定位**,匹配失败立刻反馈（高信号错误）让它重试。这就是 ACI 原则 4：**用护栏把"模糊编辑"这个错误挡在门外**,而不是等它改错了再修。

## Read / Grep：控制信噪比

这两个工具体现 ACI 原则 2、3（紧凑、高信号）。它们不是裸 `cat`/`grep`：

- **Read**：有 `MAX_LINES_TO_READ = 2000` 上限、支持 offset 分页、行号格式化。不会一次把巨型文件灌进上下文。
- **Grep**：结果数量有上限、格式化过、可按类型过滤。不会吐几百行淹没模型。

回到 `parseDate`：agent 用 Grep 找到 `parseDate` 定义在哪个文件,再用 Read（带 offset）只读相关那段——而不是把整个项目 cat 进去。**每个工具都在主动控制"喂给模型多少"**,这正是上下文工程（CH5）在工具层的前哨。

## 本节小结

1. 每个工具 = **schema + 执行 + 结果格式化**,独立成目录。
2. **BashTool 18 文件**：执行只是最后一步,大半在做"执行前的安全判断"——AST 解析命令语义 → 权限/沙箱/破坏性判断。
3. **FileEditTool 唯一匹配**：用护栏把"模糊编辑"挡在门外,匹配失败即高信号反馈。
4. **Read/Grep** 主动控信噪比（行数上限、结果上限）,是上下文工程在工具层的前哨。
5. 一句话：真实工具的复杂度,大半在护栏和信噪比,而非"执行"本身。
