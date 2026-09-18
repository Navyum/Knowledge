"""CH10 · 最小 eval loop：任务集 → 跑 harness → 独立验收 → 聚合指标。

关键：'循环停止'不等于'任务成功'。成功由独立验收（跑预置检查命令）判定。
每个任务前 TRACE 必须重置，否则指标会跨任务累加。
"""
import os
import shutil
import tempfile
from th import Harness, default_registry, LocalRuntime, PermissionPolicy, make_model
from th.trace import Trace

EVAL_SET = [
    {"task": "给 parse_date 补一个带时区的单元测试，并确保测试跑通。",
     "check": "python test_parse_date.py"},
]


def run_eval():
    src = os.path.join(os.path.dirname(__file__), "workspace")
    results = []
    trace = Trace()
    for case in EVAL_SET:
        trace.reset()                                  # 关键：跨任务不累加
        tmp = tempfile.mkdtemp(prefix="th_eval_")
        shutil.copytree(src, tmp, dirs_exist_ok=True)
        rt = LocalRuntime(tmp)
        h = Harness(make_model(), default_registry(), rt,
                    PermissionPolicy(mode="auto"), trace=trace)
        h.run(case["task"])
        # 独立验收：跑检查命令，退出码 0 才算成功
        verdict = rt.bash(case["check"])
        ok = verdict.startswith("[exit=0]")
        results.append({"task": case["task"], "pass": ok, **trace.summary()})

    rate = sum(r["pass"] for r in results) / len(results)
    print(f"成功率 {rate:.0%}（{sum(r['pass'] for r in results)}/{len(results)}）")
    for r in results:
        mark = "✓" if r["pass"] else "✗"
        print(f"  {mark} {r['task'][:24]}… turns={r['turns']} tok={r['total_tok']}")
    return results


if __name__ == "__main__":
    run_eval()
