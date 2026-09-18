"""CH4 · 工具系统（ACI）。

一个工具 = schema（给模型看）+ 执行函数（真干活）+ 结果格式化。
工具注册表统一管理，执行时绑定 runtime。
"""
from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    name: str
    description: str
    required: tuple           # 必填参数名
    run: Callable             # (runtime, args) -> str

    def schema(self) -> dict:
        return {"name": self.name, "description": self.description,
                "required": list(self.required)}


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def __contains__(self, name: str) -> bool:
        return name in self._tools

    def get(self, name: str) -> Tool:
        return self._tools[name]

    def names(self) -> list[str]:
        return list(self._tools)

    def schemas(self) -> list[dict]:
        return [t.schema() for t in self._tools.values()]


def default_registry() -> ToolRegistry:
    """课程用的四个内置工具：read_file / write_file / list_dir / bash。"""
    reg = ToolRegistry()
    reg.register(Tool("read_file", "读取工作区内一个文件的内容", ("path",),
                      lambda rt, a: rt.read_file(a["path"])))
    reg.register(Tool("write_file", "写入/覆盖工作区内一个文件", ("path", "content"),
                      lambda rt, a: rt.write_file(a["path"], a["content"])))
    reg.register(Tool("list_dir", "列出工作区内一个目录的条目", (),
                      lambda rt, a: rt.list_dir(a.get("path", "."))))
    reg.register(Tool("bash", "在工作区内执行一条 shell 命令", ("cmd",),
                      lambda rt, a: rt.bash(a["cmd"])))
    return reg
