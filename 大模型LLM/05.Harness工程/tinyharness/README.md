# tinyharness

课程配套的**最小可运行 harness**，与《Harness 工程系统化课程》九个动手里程碑一一对应。
纯标准库实现，离线即可跑通（无需 API key）；也支持切真实 Anthropic 模型。

## 快速开始

```bash
cd tinyharness

python3 tests/test_th.py     # 9 个单元+集成测试
python3 demo.py              # 端到端跑通 parseDate 任务，打印每轮 trace
python3 eval.py              # 最小 eval loop：独立验收 + 聚合指标

# 切真实模型（可选）
pip install anthropic
ANTHROPIC_API_KEY=sk-... python3 demo.py
```

离线默认用 `ScriptedModel`——按固定剧本模拟 ReAct（读文件→写测试→跑测试→完成），
让你在没有 key 的情况下也能看到完整循环真实地读写文件、执行命令、验收结果。

## 五职责 → 代码映射

| 模块 | 职责 | 课程章 |
|---|---|---|
| `th/harness.py` | Agent 循环（组装→调模型→权限→执行→回写→判停） | CH2 |
| `th/model.py` | 模型交互层（ScriptedModel / AnthropicModel） | CH3 |
| `th/tools.py` | 工具系统（ACI：schema+执行+格式化，4 个内置工具） | CH4 |
| `th/context.py` | 上下文管理（system prompt 组装 + 压缩 + AGENTS.md 记忆） | CH5 |
| `th/permission.py` | 权限与安全（审批闸 + 路径穿越防护） | CH6 |
| `th/runtime.py` | 运行时（LocalRuntime 本地沙箱，可换后端） | CH7 |
| `th/state.py` | 状态持久化与恢复（JSONL + 中断检测） | CH8 |
| `th/errors.py` | 错误处理与循环卫生（错误即上下文 + 只拦失败重复） | CH9 |
| `th/trace.py` | 可观测与自建评测（trace + 汇总，每任务重置） | CH10 |

## 三个关键设计（对应课程要点）

1. **停止 ≠ 成功**：循环靠"无 tool_use"停止（`harness.py`），但任务是否成功由
   `eval.py` 的**独立验收**（跑预置检查命令、看退出码）判定——两者严格分开。
2. **循环卫生只拦失败**：`LoopHygiene` 只记失败的调用、成功即清零，
   连续成功读同一文件不会误判死循环。
3. **中断是"结果未知"不是"未执行"**：`state.py` 恢复时把悬空 tool_use 标为
   "结果未知"，提示非幂等操作重做前先核查外部状态，避免二次副作用。

## 目录

```
tinyharness/
├── th/              核心包（九个职责模块）
├── workspace/       示例任务：待补时区支持的 parse_date.py + AGENTS.md
├── demo.py          端到端演示
├── eval.py          自建评测
└── tests/test_th.py 测试（9 个）
```

## 边界（诚实说明）

- ScriptedModel 是**确定性剧本**，不含真实推理——它的价值是让循环、工具、权限、
  持久化、评测这些 **harness 机制** 可离线验证。要看真实模型决策，设 `ANTHROPIC_API_KEY`。
- LocalRuntime 是**进程内沙箱**（路径限制 + 危险命令拦截），非强隔离。
  生产级隔离（容器/MicroVM）见课程 CH7 沙箱光谱，此处只做接口示范。
