"""CH2 · Agent 循环 —— 把五职责串成一个闭环。

流程：组装上下文 → 调模型 → 有无 tool_use？
  有 → 权限检查 → 运行时执行 → 结果回写 → 回到顶部
  无 → 循环停止（注意：停止≠任务成功，成功要靠独立验收，见 eval.py）
兜底：达到 max_turns / 被取消。
"""
import json
from . import context as ctx
from .errors import format_tool_error, LoopHygiene
from .state import append_jsonl, load_session
from .trace import Trace


class Harness:
    def __init__(self, model, registry, runtime, policy, *,
                 max_turns=12, compact_threshold=6000,
                 session_path=None, trace=None):
        self.model = model
        self.registry = registry
        self.runtime = runtime
        self.policy = policy
        self.max_turns = max_turns
        self.compact_threshold = compact_threshold
        self.session_path = session_path
        self.trace = trace or Trace()
        self.hygiene = LoopHygiene()

    def _persist(self, msg):
        if self.session_path:
            append_jsonl(self.session_path, msg)

    def run(self, task: str, cancel=None) -> dict:
        memory = ctx.load_memory(self.runtime.workspace)
        system = ctx.build_system_prompt(self.registry.schemas(), memory)

        # 恢复优先：有 session 就续跑，否则以任务起头
        messages = load_session(self.session_path) if self.session_path else []
        if not messages:
            messages = [{"role": "user", "content": task}]
            self._persist(messages[0])

        import time
        for turn in range(1, self.max_turns + 1):
            if cancel and cancel():
                return {"status": "cancelled", "turns": turn - 1,
                        "trace": self.trace.summary()}

            if ctx.estimate_tokens(messages) > self.compact_threshold:
                messages = ctx.compact(messages)

            t0 = time.time()
            comp = self.model.complete(system, messages, self.registry.schemas())
            dt = time.time() - t0
            action = "finish" if not comp.tool_uses else \
                ",".join(t["name"] for t in comp.tool_uses)
            self.trace.record(turn, dt, comp.tokens, action)

            # 组装 assistant 消息
            content = []
            if comp.text:
                content.append({"type": "text", "text": comp.text})
            for tu in comp.tool_uses:
                content.append({"type": "tool_use", **tu})
            asst = {"role": "assistant", "content": content}
            messages.append(asst)
            self._persist(asst)

            if not comp.tool_uses:      # 无 tool_use → 循环自然停止
                return {"status": "stopped", "final": comp.text,
                        "turns": turn, "trace": self.trace.summary()}

            # 执行每个 tool_use，收集 tool_result
            results = []
            for tu in comp.tool_uses:
                out = self._exec_tool(tu)
                results.append({"type": "tool_result",
                                "tool_use_id": tu["id"], "content": out})
            user_msg = {"role": "user", "content": results}
            messages.append(user_msg)
            self._persist(user_msg)

        return {"status": "max_turns", "turns": self.max_turns,
                "trace": self.trace.summary()}

    def _exec_tool(self, tu: dict) -> str:
        name, args = tu["name"], tu.get("input", {})
        sig = name + ":" + json.dumps(args, sort_keys=True, ensure_ascii=False)

        # 1. 循环卫生：只拦"连续失败"
        if self.hygiene.is_stuck(sig):
            return "[卫生] 此调用已连续失败 3 次，请换一种方法或说明卡在哪。"
        # 2. 未知工具
        if name not in self.registry:
            self.hygiene.record_fail(sig)
            return f"[错误] 未知工具 {name}，可用：{self.registry.names()}"
        # 3. 必填参数校验
        tool = self.registry.get(name)
        missing = [k for k in tool.required if k not in args]
        if missing:
            self.hygiene.record_fail(sig)
            return f"[参数错误] 缺少必填参数 {missing}"
        # 4. 权限闸
        ok, reason = self.policy.check(name, args)
        if not ok:
            self.hygiene.record_fail(sig)
            return reason
        # 5. 运行时执行（错误即上下文）
        try:
            out = tool.run(self.runtime, args)
            self.hygiene.record_success(sig)
            return out
        except Exception as e:
            self.hygiene.record_fail(sig)
            return format_tool_error(e)
