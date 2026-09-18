# 阅读清单 · 源码导航 · 合规 · 术语表

## A · 阅读清单（一手来源）

课程正式引用的一手资料。**优先读一手，别读二手转述。**

### A.1 设计原则（理论骨架）

| 文献 | 出处 | 用于章节 | 核心观点 |
|---|---|---|---|
| Building Effective Agents | anthropic.com/engineering | intro, CH2 | agent = 模型 + 软件脚手架；workflow vs agent |
| Effective Context Engineering | anthropic.com/engineering | CH5 | 最小高信号 token 集；context rot；三技法 |
| Writing Tools for Agents | anthropic.com/engineering | CH4 | 工具少而精；高信号结果；可纠错错误 |
| Multi-Agent Research System | anthropic.com/engineering | CH12 | orchestrator-worker；15× token；不适合紧耦合编码 |
| Context Engineering for AI Agents | Manus 官方博客 | CH5 | KV-cache 友好；Recitation；保留错误痕迹 |
| Don't Build Multi-Agents | Cognition 官方博客 | CH12 | 共享完整上下文；单线程线性 agent |

### A.2 术语定义与学术论文

| 来源 | 出处 | 用于 |
|---|---|---|
| Claude Code Glossary "Agentic harness" | code.claude.com/docs/en/glossary | intro 权威定义 |
| deepseek-harness architecture.md | github.com/deepseek-ai/deepseek-harness | intro / CH4.3 / CH11 |
| ReAct | arXiv 2210.03629 | CH2 循环范式源头 |
| CodeAct | arXiv 2402.01030 | CH2 用代码作为动作 |
| SWE-agent（ACI） | arXiv 2405.15793 | CH4 ACI 四原则+消融 |
| SWE-bench | arXiv 2310.06770 | CH7/CH10 分层镜像+判定 |

### A.3 入门读物

- Thorsten Ball《How to Build an Agent》—— agent = LLM + loop + tokens，~300 行。
- Geoffrey Huntley《how to build a coding agent》—— 上下文当稀缺内存。

## B · 源码导航

> **核实时间**
>
> 2026-09。仓库会演进，路径可能变化，以实际为准。

### Claude Code（泄露 TS，见 C）

| 关注点 | 路径 | 章 |
|---|---|---|
| 循环 | `src/query.ts`、`QueryEngine.ts`、`query/` | CH2 |
| 流式/重试/缓存 | `src/services/api/`（StreamingToolExecutor、withRetry、promptCacheBreakDetection） | CH3 |
| 工具 | `src/tools/`（42）、`BashTool/`（18 文件） | CH4 |
| 上下文 | `src/services/compact/`（11）、`utils/systemPrompt.ts`、`SessionMemory/` | CH5 |
| 权限 | `src/hooks/toolPermission/` | CH6 |
| 持久化/恢复 | `src/history.ts`、`utils/conversationRecovery.ts` | CH8 |
| 错误/卫生 | `utils/toolErrors.ts`、`constants/errorIds.ts`、`utils/QueryGuard.ts` | CH9 |
| 多 agent | `src/utils/swarm/` | CH12 |

### 开源四案例

| 案例 | 核心定位 | 许可 |
|---|---|---|
| OpenHands | EventStream + Runtime 抽象 + ActionExecutionServer | MIT |
| Codex | sandbox_mode × approval_policy + config 分层 + Seatbelt | Apache-2.0（Rust） |
| deepseek | core/agent-loop、core/tools、llm/llm+llm-deepseek、sandbox/guard、compaction/spill（Cordis） | MIT |
| multica | server/internal/daemon/（reconcile）、daemon/execenv/ | source-available · Multica License（Go） |

## C · 合规与来源说明

> **Claude Code 源码的性质与使用边界**
>
> **来源**：该 TS 源码来自 Claude Code 发行包中泄露的 source map（.map）还原，据镜像仓库自述泄露于 2026-03-31。**法律状态**：Anthropic 专有代码，无 LICENSE、未获授权。**风险**：随时可能被 DMCA 下架；商业复刻有明确侵权风险。

**本课使用边界**

- ✓ 仅用于**架构学习与原理印证**；正式引用以 Anthropic 官方博客/文档为准。
- ✓ 课程中所有 Claude Code 相关代码块均为**原创伪代码示意**，不复制真实源码；只讲架构、模块职责、文件定位。
- ✗ **不可分发**该源码、不可用于商业复刻、不可去除来源说明。

**合法可读的替代素材**

- `anthropics/claude-cookbooks`（MIT）：agent loop 显式写在 notebook 里，最适合合法读源码理解原理。
- `anthropics/anthropic-quickstarts`（MIT）：可运行入门应用。
- `anthropics/claude-agent-sdk-python`（MIT）：官方 Python SDK（注意：只是驱动闭源 CLI 的客户端壳，读不到核心 loop）。

> **数据核实说明**
>
> 本课调研于 2026-09 完成，以 GitHub 仓库内容、官方文档/博客、论文为一手来源。**star 数字未采信**（调研环境 GitHub star 数据异常），所有真伪/价值判断基于仓库文件内容本身。标注"推断"的内容（如 deepseek 的低缓存定价宣称）为合理推测，非确证事实。

## D · 术语表

| 术语 | 含义 |
|---|---|
| **harness** | 把无状态模型包裹成有状态、能行动、可循环 agent 的软件层。承担循环/工具/上下文/权限/运行时五职责。 |
| **ReAct** | Reason+Act 交替的推理范式，几乎所有 agent 循环的理论源头。 |
| **ACI** | Agent-Computer Interface，为 agent（而非人）设计工具接口的理念。四原则：简单/紧凑/高信号反馈/护栏。 |
| **context rot** | 上下文腐烂：上下文过长导致模型注意力被稀释、抓不住重点。 |
| **compaction** | 压缩：把冗长历史总结成摘要以腾出上下文空间。分 auto/micro 两级。 |
| **tool_use / tool_result** | 模型请求调用工具 / harness 返回的执行结果，配对出现。 |
| **MCP** | Model Context Protocol，工具扩展的事实标准，harness 的"USB 口"。 |
| **Runtime 抽象** | 把"执行动作的地方"变成可插拔后端（本地/容器/远程）的接口。 |
| **sandbox × approval** | 沙箱（能坏多大）× 审批（要不要做）的双层安全模型。 |
| **subagent** | 子 agent：在独立上下文窗口探索、只回传摘要，用于隔离读密集子任务。 |

---

## E · 工程溯源对照表：harness 借了哪些经典技术

harness 不是凭空发明的，它的每个职责为解决**性能（Token/延迟）、安全（隔离/权限）、确定性（状态/重放）**瓶颈，都借用了操作系统、分布式系统、编译器领域的成熟原语。这张表把"职责 → 关键技术 → 借自哪里 → 代表选型"串起来，作为全课的"工程视角索引"。

> **怎么读这张表（可信度分级）**
>
> - **✅ 一手核实**：课程已从源码/官方文档确认的机制。
> - **◐ 合理映射**：经典技术属实、项目选型据公开信息，但未逐一核到源码，措辞用"如/代表"。
> - **○ 设计视角**：是"可借鉴的思路/理想架构"，非该项目的字面实现，引用时注意区分。

**① 上下文管理**（Token 预算 vs 长任务膨胀）

| 关键技术 | 借自 | 代表选型 | 级别 | 课程位置 |
|---|---|---|---|---|
| 不可变状态 + COW 分支（Delta 状态树） | 函数式/文件系统 Copy-on-Write | LangGraph checkpoint | ◐ | [CH8](ch8-state.md) |
| 结构感知截断（保留头部签名 + 尾部异常） | 编译器 AST / 词法分析 | Claude Code、Aider | ◐ | [CH4](ch4-tools-claude-code.md) |
| KV-Cache 友好的增量摘要 | 注意力键值缓存复用 | Claude Code compact、AutoGPT | ✅ | [CH5.3](ch5-ctx-compact.md) |
| 上下文分页 / Off-loading（外部记忆） | OS 虚拟内存 / Paging | MemGPT / Letta | ◐ | [CH5.1](ch5-ctx-principles.md) |

**② 运行时与沙箱**（启动速度 vs 隔离强度）

| 关键技术 | 借自 | 代表选型 | 级别 | 课程位置 |
|---|---|---|---|---|
| OverlayFS 增量快照（毫秒级回滚） | Linux 联合文件系统 | SWE-agent、Devin 类 | ◐ | [CH7 沙箱光谱](ch7-rt-principles.md) |
| MicroVM（Firecracker/KVM） | 轻量级硬件虚拟化 | E2B、Modal | ◐ | [CH7 沙箱光谱](ch7-rt-principles.md) |
| Namespaces + Cgroups + Seccomp | Linux 容器三件套 | OpenHands、Docker 沙箱 | ✅ | [CH7](ch7-rt-principles.md) |
| eBPF 运行时监控（无侵入挂钩） | Linux 内核可观测 | 企业审计层 | ○ | [CH7 沙箱光谱](ch7-rt-principles.md) · [CH10](ch10-observability.md) |

**③ 权限与安全**（LLM 不确定性 vs 执行确定性）

| 关键技术 | 借自 | 代表选型 | 级别 | 课程位置 |
|---|---|---|---|---|
| 命令 AST 静态解析（非正则黑名单） | 编译器 Lexer/Parser | Claude Code BashTool | ✅ | [CH4](ch4-tools-claude-code.md) · [CH6](ch6-perm-principles.md) |
| 出站代理 + SNI 域名白名单 | 网络透明代理 / TLS 检查 | E2B、K8s NetworkPolicy | ◐ | [CH6 注入防御](ch6-perm-principles.md) |
| 路径规范化 + chroot/Landlock（防目录穿越） | OS 文件系统安全 | SWE-agent | ◐ | [CH6](ch6-perm-principles.md) |
| 能力基安全 / Macaroons（带时效范围的强类型 token） | 能力安全模型 | MCP 权限设计**受此启发** | ○ | [CH4 MCP](ch4-tools-aci.md) |

**④ 工具系统**（简单 Schema vs 复杂真实交互）

| 关键技术 | 借自 | 代表选型 | 级别 | 课程位置 |
|---|---|---|---|---|
| PTY 伪终端仿真（Stateful Shell） | Unix 伪终端 | Claude Code、OpenHands | ✅ | [CH4](ch4-tools-claude-code.md) · [CH7](ch7-rt-openhands.md) |
| JSON Schema JIT 校验（Pydantic/Zod） | 强类型运行时校验 | LangChain、LlamaIndex | ◐ | [CH9 畸形 tool call](ch9-errors.md) |
| DAG 并行拓扑调度 | 分布式任务编排 | Semantic Kernel、CrewAI | ◐ | [CH12](ch12-multi-agent.md) |
| 增量流式解析 + 背压 | 流式 SSE / 部分 JSON 解析 | Vercel AI SDK、Claude CLI | ✅ | [CH3](ch3-io-streaming.md) |

**⑤ 循环与调度**（死循环风险 vs 可重放性）

| 关键技术 | 借自 | 代表选型 | 级别 | 课程位置 |
|---|---|---|---|---|
| Event Sourcing（事件溯源，100% 重放） | 分布式系统事件溯源 | OpenHands EventStream、LangGraph | ✅ | [CH2](ch2-loop-openhands.md) · [CH8](ch8-state.md) |
| 熔断器 + 环路检测（Hash/语义查重） | 微服务 Circuit Breaker | Claude Code QueryGuard | ✅ | [CH9](ch9-errors.md) |
| FSM / 状态图约束（Conditional Edges） | 有限状态自动机 | LangGraph、MetaGPT | ◐ | [CH2](ch2-loop-paradigms.md) |
| Checkpoint/Resume（WAL 预写日志思想） | 数据库 Write-Ahead Logging | LangGraph Checkpointers | ✅ | [CH8](ch8-state.md) |

> **一句话总结**
>
> harness 工程的"新"，主要在**把 LLM 的不确定性接进确定性系统**这件事上；而它用来接的"管道"，几乎全是 OS / 分布式 / 编译器早已验证过的老技术。看懂一个 harness，很大程度是看懂它在每个职责上选了哪个经典原语、以及为什么。
