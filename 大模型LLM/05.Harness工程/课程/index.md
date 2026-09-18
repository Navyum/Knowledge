---
order: 1
---

# 亲手造一个,把模型变成 Agent 的引擎

面向有 Agent 基础的工程师,目标是达到 harness 开发水平。

不只讲原理,更带你从零构建一个能跑真实编码任务的 harness。四主线并行:概念 · 一条真实任务串联 · 五个开源实现源码精读 · 完整实战建造。

[开始学习 →](01-基础/intro.md)

本课概况:4 条并行主线、13 个章节、5 个案例深剖、9 个动手里程碑。

## 四条主线并行

不是四套割裂的内容,而是贯穿每一章的四个视角。你会同时从原理、真实任务、真实源码、亲手实现四个角度理解每个部件。

- **主线 1 · 概念**:每个部件的原理与设计问题——它解决什么、有哪些绕不开的难题。
- **主线 2 · 任务串联**:用一条真实任务(给 parseDate 加时区单测)端到端串起整个 harness 处理流程。
- **主线 3 · 源码精读**:逐个拆解五个真实 harness 的核心实现——架构、模块职责、数据流。
- **主线 4 · 动手建造**:9 个里程碑,从零造出功能完整、可运行的 tinyharness。

## 六部,十三章

课程结构,共 34 页。

### 01 · 基础

- [什么是 harness](01-基础/intro.md)
- [一条任务的完整生命周期](01-基础/lifecycle.md)

### 02–07 · 核心机制(六章)

- [CH2 · Agent 循环](02-agent循环/ch2-loop-paradigms.md)
- [CH3 · 模型交互层](03-模型交互/ch3-io-streaming.md)
- [CH4 · 工具系统](04-工具系统/ch4-tools-aci.md)
- [CH5 · 上下文与 Prompt](05-上下文/ch5-ctx-principles.md)
- [CH6 · 权限与安全](06-权限安全/ch6-perm-principles.md)
- [CH7 · 运行时与隔离](07-运行时/ch7-rt-principles.md)

### 08–10 · 生产级实现

- [CH8 · 状态持久化与恢复](08-状态持久化/ch8-state.md)
- [CH9 · 错误处理与恢复](09-错误处理/ch9-errors.md)
- [CH10 · 可观测与自建评测](10-可观测/ch10-observability.md)

### 11–13 · 高级

- [CH11 · 模型绑定 vs 中立](11-模型绑定/ch11-model-binding.md)
- [CH12 · 多 Agent 编排](12-多agent/ch12-multi-agent.md)
- [CH13 · 生产化与稳定性](13-生产化/ch13-production.md)

### 收尾 · 总装与提炼

- [总装 · 完整 harness](15-收尾/build-capstone.md)
- [融会贯通](15-收尾/synthesis.md)
- [附录](15-收尾/appendix.md)

## 五个真实开源 harness

案例深剖,属于主线 4 专区。核心章按主题横切,案例专区按 harness 纵切——每个 harness 端到端讲清架构、请求流程、核心模块。全部 2026-09 一手核实。

| 案例 | 定位 | 核心看点 | 许可 |
| --- | --- | --- | --- |
| [Claude Code](14-案例深剖/case-claude-code.md) | CLI 标杆 · 生成器循环 | query 循环、42 工具、compact 子系统、hook 权限、swarm 多 agent | 泄露源码,仅作架构学习 |
| [OpenHands](14-案例深剖/case-openhands.md) | 自主平台 · 事件驱动 | EventStream + Runtime 抽象,可回放/接管/分布 | MIT |
| [Codex CLI](14-案例深剖/case-codex.md) | 双层安全标杆 | sandbox × approval 二维正交,Seatbelt 沙箱 | Apache-2.0 · Rust |
| [deepseek-harness](14-案例深剖/case-deepseek.md) | 一切皆插件 · 中文生态 | 无特权核心,连循环都是可换插件;中立核心 + DeepSeek 适配 | MIT · preview |
| [multica](14-案例深剖/case-multica.md) | 编排层 · harness 之上 | 编排 26 个异构 CLI,execenv 隔离 + issue/review 协调 | source-available（Multica License）· Go |

**对照点**(相关章节带过):Aider(git 兜底)· Gemini CLI(Policy Engine)· SWE-agent/mini(复杂度辩论)。

---

调研与核实时间:2026-09 · 各案例状态、源码路径以核实日为准 · 一手来源见附录 A

合规声明:Claude Code 源码来自 source map 泄露、无授权许可,仅作架构学习,不可分发或商业复刻。OpenHands/Codex/deepseek-harness 为标准开源(MIT/Apache-2.0);multica 为 source-available(Multica License,含商用/托管附加限制)。详见附录 C。
