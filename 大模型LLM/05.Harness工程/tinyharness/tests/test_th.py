"""tinyharness 单元 + 集成测试。运行：python -m pytest tests/ 或 python tests/test_th.py"""
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from th import Harness, default_registry, LocalRuntime, PermissionPolicy, ScriptedModel
from th.errors import LoopHygiene
from th.context import compact, load_memory
from th.state import load_session, append_jsonl
from th.permission import safe_resolve


def _ws():
    tmp = tempfile.mkdtemp(prefix="th_test_")
    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "workspace")
    shutil.copytree(src, tmp, dirs_exist_ok=True)
    return tmp


def test_runtime_read_write():
    rt = LocalRuntime(_ws())
    assert "已写入" in rt.write_file("a.txt", "hi")
    assert rt.read_file("a.txt") == "hi"


def test_path_traversal_blocked():
    rt = LocalRuntime(_ws())
    try:
        safe_resolve(rt.workspace, "../../etc/passwd")
        assert False, "应拦截目录穿越"
    except PermissionError:
        pass


def test_readonly_policy_blocks_write():
    pol = PermissionPolicy(mode="readonly")
    ok, reason = pol.check("write_file", {"path": "x", "content": "y"})
    assert not ok and "只读" in reason


def test_dangerous_command_blocked():
    pol = PermissionPolicy(mode="auto")
    ok, _ = pol.check("bash", {"cmd": "rm -rf /"})
    assert not ok


def test_hygiene_only_counts_failures():
    h = LoopHygiene(threshold=3)
    for _ in range(5):
        h.record_success("read:x")          # 成功再多也不该 stuck
    assert not h.is_stuck("read:x")
    for _ in range(3):
        h.record_fail("bash:y")
    assert h.is_stuck("bash:y")
    h.record_success("bash:y")              # 一次成功即清零
    assert not h.is_stuck("bash:y")


def test_compact_keeps_head_and_tail():
    msgs = [{"role": "user", "content": f"m{i}"} for i in range(10)]
    out = compact(msgs, keep_recent=3)
    assert out[0] == msgs[0] and out[-3:] == msgs[-3:]
    assert any("已压缩" in str(m.get("content", "")) for m in out)


def test_memory_loaded():
    assert "pytest" in load_memory(_ws()) or "退出码" in load_memory(_ws())


def test_resume_marks_dangling_unknown():
    tmp = _ws()
    p = os.path.join(tmp, "s.jsonl")
    append_jsonl(p, {"role": "user", "content": "task"})
    append_jsonl(p, {"role": "assistant", "content":
                     [{"type": "tool_use", "id": "t1", "name": "bash", "input": {}}]})
    msgs = load_session(p)
    assert msgs[-1]["content"][0]["type"] == "tool_result"
    assert "结果未知" in msgs[-1]["content"][0]["content"]


def test_end_to_end_parsedate():
    tmp = _ws()
    rt = LocalRuntime(tmp)
    h = Harness(ScriptedModel(), default_registry(), rt,
                PermissionPolicy(mode="auto"))
    res = h.run("给 parse_date 补时区单测并跑通")
    assert res["status"] == "stopped"
    # 独立验收：测试文件已生成且能通过
    assert os.path.exists(os.path.join(tmp, "test_parse_date.py"))
    assert rt.bash("python test_parse_date.py").startswith("[exit=0]")


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            fn(); passed += 1; print(f"  ✓ {fn.__name__}")
        except Exception as e:
            print(f"  ✗ {fn.__name__}: {e}")
    print(f"\n{passed}/{len(fns)} 通过")
    sys.exit(0 if passed == len(fns) else 1)
