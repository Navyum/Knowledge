# 动手：给 tinyharness 一套真正的工具

CH2 只有一个 `read_file`。这一节按 ACI 原则,给 tinyharness 加一个小型注册表 + Read/Write/Bash 三个工具,每个都带护栏和高信号结果。里程碑 3。

> **这一节结束时,你会有**：一个 `tools.py`：装饰器式工具注册表（仿 deepseek 的 registry 思想）、Read（带行数上限）、Write、Bash（带只读模式护栏）,每个工具的结果都为模型优化过。循环层继续零改动。

## 第 1 步：一个极简注册表

**用装饰器注册工具。** 借 4.3 deepseek 的 registry 思想,做一个最小版：一个装饰器,把工具的 schema 和执行函数一起登记。

```python
# tools.py — 注册表
_REGISTRY = {}   # name -> {schema, fn}

def tool(name, description, schema):
    def deco(fn):
        _REGISTRY[name] = {
            "schema": {"name": name, "description": description,
                       "input_schema": schema},
            "fn": fn,
        }
        return fn
    return deco

def all_schemas():  return [t["schema"] for t in _REGISTRY.values()]
def run_tool(name, args):  return _REGISTRY[name]["fn"](**args)
```

## 第 2 步：Read / Write / Bash,各带护栏

**护栏是重点,不是执行。** 照 4.2 的教训：护栏才是工具的分量所在。

```python
# tools.py — 三个工具
MODE = "workspace-write"   # 或 "read-only",CH6 会用它做权限
MAX_LINES = 2000           # ACI 紧凑:仿 CC 的 MAX_LINES_TO_READ

@tool("read_file", "读取文本文件",
      {"type":"object","properties":{"path":{"type":"string"}},"required":["path"]})
def read_file(path):
    try:
        lines = open(path).read().splitlines()
        if len(lines) > MAX_LINES:                 # 护栏:防淹没上下文
            return f"[文件 {len(lines)} 行,只显示前 {MAX_LINES} 行]\n" + \
                   "\n".join(lines[:MAX_LINES])
        return "\n".join(lines) or "[空文件]"
    except Exception as e:
        return f"错误:{e}"                          # 高信号错误

@tool("write_file", "写入文本文件",
      {"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]})
def write_file(path, content):
    if MODE == "read-only":                        # 护栏:只读模式
        return "拒绝:当前只读模式"
    open(path, "w").write(content)
    return f"已写入 {path}({len(content)} 字符)"

@tool("bash", "执行 shell 命令",
      {"type":"object","properties":{"cmd":{"type":"string"}},"required":["cmd"]})
def bash(cmd):
    import subprocess
    if MODE == "read-only" and any(w in cmd for w in ["rm ",">","mv "]):
        return "拒绝:只读模式下疑似写操作"   # 极简护栏,CH6 会做真的
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    out = (r.stdout + r.stderr).strip()
    return out[:4000] or f"[退出码 {r.returncode},无输出]"  # 截断=紧凑
```

> **注意每个工具的护栏**
>
> Read 有**行数上限**（紧凑）、Write/Bash 有**只读模式检查**（护栏）、Bash 输出**截断到 4000 字符**（紧凑）、所有错误**可读返回**而非抛异常（高信号）。这些就是 ACI 四原则的最小落地。你的 `bash` 护栏还很粗糙——CH6 会把它换成真正的命令语义分析。

## 第 3 步：高信号结果

注意上面每个 return：空文件返回 `"[空文件]"` 而非空串,无输出命令返回 `"[退出码 X,无输出]"`。**永远给模型一个明确的信号**,别让它面对空白猜测——这是 Anthropic"返回高信号结果"原则的直接应用。

## 跑起来：现在能完成 parseDate 任务了

把循环里的 `TOOLS`/`TOOL_IMPL` 换成 `all_schemas()`/`run_tool()`。现在 tinyharness 有读、写、执行三样,理论上已能完成我们的主角任务：

```bash
$ python tinyharness.py "给 utils.py 里的 parseDate 补一个时区单测,放 test_parse.py,然后跑通"
# agent 会:read_file(utils.py) → write_file(test_parse.py) → bash("pytest test_parse.py")
# 看报错 → 再 write_file 修 → 再 bash 跑,直到绿
```

这正是[任务地图](lifecycle.md)走的那条链！你的 harness 已经能自主跑通一个真实编码任务了。

## 里程碑检查

> **里程碑 3 · 自测清单**
>
> - [ ] 三个工具都能用,装饰器注册生效
> - [ ] Read 对大文件会截断并提示
> - [ ] `MODE="read-only"` 时 Write/Bash 被拦
> - [ ] 每个工具的结果都对模型友好（无空白、错误可读）
> - [ ] 能跑通一个"读→写→执行→看报错→改"的完整小任务
>
> 你的 harness 已具备手脚。但它现在把整个历史无限堆进上下文——长任务会爆。CH5 解决这个。
