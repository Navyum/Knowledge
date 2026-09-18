"""tinyharness —— 课程配套的最小可运行 harness。

按五职责组织，对应课程章节：
  loop/harness    → CH2 Agent 循环
  model           → CH3 模型交互层（流式在真实后端里）
  tools           → CH4 工具系统（ACI）
  context         → CH5 上下文管理（组装 + 压缩）
  permission      → CH6 权限与安全
  runtime         → CH7 运行时（本地沙箱）
  state           → CH8 状态持久化与恢复
  errors          → CH9 错误处理与循环卫生
  trace           → CH10 可观测与自建评测

离线默认用 ScriptedModel（无需 API key）；设了 ANTHROPIC_API_KEY 可切真实模型。
"""
from .harness import Harness
from .tools import Tool, ToolRegistry, default_registry
from .runtime import LocalRuntime
from .permission import PermissionPolicy
from .model import ScriptedModel, make_model
from .trace import Trace

__all__ = ["Harness", "Tool", "ToolRegistry", "default_registry",
           "LocalRuntime", "PermissionPolicy", "ScriptedModel",
           "make_model", "Trace"]
