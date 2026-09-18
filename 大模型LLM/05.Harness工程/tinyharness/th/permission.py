"""CH6 · 权限与安全。

两种互补机制：审批（要不要做）× 沙箱（能坏多大）。这里实现审批闸 +
路径规范化防目录穿越。真正的执行隔离在 runtime.py。
"""
import os
from dataclasses import dataclass, field


# 危险命令的朴素识别（教学版；生产应走 AST 解析，见 CH4）
_DANGEROUS = ("rm -rf", "mkfs", ":(){", "dd if=", "> /dev/")


@dataclass
class PermissionPolicy:
    mode: str = "auto"                       # auto | approve | readonly
    allow_write: bool = True
    allow_bash: bool = True
    approver: object = None                  # 可调用：(action:str)->bool，用于 approve 模式
    audit: list = field(default_factory=list)

    def check(self, tool_name: str, args: dict) -> tuple[bool, str]:
        """返回 (是否放行, 拒绝原因)。放行前记审计。"""
        self.audit.append({"tool": tool_name, "args": args})

        if self.mode == "readonly" and tool_name in ("write_file", "edit_file", "bash"):
            return False, f"[权限拒绝] 只读模式，禁止 {tool_name}"

        if tool_name in ("write_file", "edit_file") and not self.allow_write:
            return False, "[权限拒绝] 写操作被策略禁用"

        if tool_name == "bash":
            if not self.allow_bash:
                return False, "[权限拒绝] bash 被策略禁用"
            cmd = str(args.get("cmd", ""))
            if any(d in cmd for d in _DANGEROUS):
                return False, f"[权限拒绝] 检测到危险命令：{cmd!r}"

        # approve 模式：写/执行类需人工点头
        if self.mode == "approve" and tool_name in ("write_file", "edit_file", "bash"):
            if self.approver and not self.approver(f"{tool_name} {args}"):
                return False, "[权限拒绝] 用户未批准此操作"

        return True, ""


def safe_resolve(root: str, path: str) -> str:
    """路径规范化 + 越界检查：防 ../../etc/passwd 目录穿越。"""
    root_abs = os.path.realpath(root)
    target = os.path.realpath(os.path.join(root_abs, path))
    if target != root_abs and not target.startswith(root_abs + os.sep):
        raise PermissionError(f"路径越界：{path} 逃出了工作区 {root}")
    return target
