"""CH7 · 运行时与隔离。

把"执行动作的地方"抽象成可插拔后端。这里是最简的 LocalRuntime——
把所有文件/命令操作限制在一个工作区目录内（进程内沙箱）。
生产可换成容器/MicroVM 后端，上层接口不变（依赖倒置）。
"""
import os
import subprocess
from .permission import safe_resolve


class LocalRuntime:
    """本地运行时：所有操作限定在 workspace 目录内。"""

    def __init__(self, workspace: str):
        self.workspace = os.path.realpath(workspace)
        os.makedirs(self.workspace, exist_ok=True)

    def read_file(self, path: str, max_lines: int = 2000) -> str:
        target = safe_resolve(self.workspace, path)
        with open(target, encoding="utf-8") as f:
            lines = f.readlines()
        # ACI 原则2（紧凑）：读文件有行数上限，防撑爆上下文
        clipped = ""
        if len(lines) > max_lines:
            clipped = f"\n... [已截断，共 {len(lines)} 行，只显示前 {max_lines} 行]"
            lines = lines[:max_lines]
        return "".join(lines) + clipped

    def write_file(self, path: str, content: str) -> str:
        target = safe_resolve(self.workspace, path)
        os.makedirs(os.path.dirname(target) or self.workspace, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return f"已写入 {path}（{len(content)} 字符）"

    def list_dir(self, path: str = ".") -> str:
        target = safe_resolve(self.workspace, path)
        return "\n".join(sorted(os.listdir(target))) or "(空目录)"

    def bash(self, cmd: str, timeout: int = 30) -> str:
        """在工作区内跑命令。超时/非零退出都作为文本返回（错误即上下文）。"""
        proc = subprocess.run(
            cmd, shell=True, cwd=self.workspace, timeout=timeout,
            capture_output=True, text=True,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        return f"[exit={proc.returncode}]\n{out.strip()}"
