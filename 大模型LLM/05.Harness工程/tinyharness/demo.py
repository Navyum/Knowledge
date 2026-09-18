"""端到端演示：跑通 parseDate 任务，打印每轮 trace。

用法：
    python demo.py                # 离线（ScriptedModel，无需 key）
    ANTHROPIC_API_KEY=... python demo.py   # 真实模型

演示会在一份临时工作区副本上操作，不污染 workspace/ 原始文件。
"""
import os
import shutil
import tempfile
from th import Harness, default_registry, LocalRuntime, PermissionPolicy, make_model


def main():
    src = os.path.join(os.path.dirname(__file__), "workspace")
    tmp = tempfile.mkdtemp(prefix="th_demo_")
    shutil.copytree(src, tmp, dirs_exist_ok=True)

    runtime = LocalRuntime(tmp)
    policy = PermissionPolicy(mode="auto")            # 演示用全自动
    session = os.path.join(tmp, "session.jsonl")
    h = Harness(make_model(), default_registry(), runtime, policy,
                session_path=session)

    task = "给 parse_date 补一个带时区的单元测试，并确保测试跑通。"
    print(f"任务：{task}\n工作区：{tmp}\n" + "-" * 60)
    result = h.run(task)

    print("每轮 trace：")
    for e in h.trace.entries:
        print(f"  轮{e['turn']}: {e['action']:<12} "
              f"{e['sec']}s  {e['tok']} tok")
    print("-" * 60)
    print(f"结束状态：{result['status']}  |  汇总：{result['trace']}")
    if result.get("final"):
        print(f"模型总结：{result['final']}")
    print(f"\n（会话日志：{session}）")


if __name__ == "__main__":
    main()
