# 对比与动手：可插拔 runtime

先看 Runtime 抽象的另外两种形态——multica 的"向外隔离"和 SWE-bench 的分层镜像，再把 tinyharness 的 bash 执行改造成可插拔的 runtime 接口。里程碑 6。

## multica：向外隔离一堆异构 harness

OpenHands 的 Runtime 是"隔离我**自己**的执行"。multica 的 `server/internal/daemon/execenv/` 是另一种形态——它自己不含 LLM 循环，而是编排 26 个异构 CLI（Claude Code、Codex 等），为**每一个被它调用的 harness** 提供隔离环境。

**向内 vs 向外**：

- **OpenHands**：我怎么隔离我自己的执行（向内）。
- **multica**：我怎么把一堆异构 harness 各自关进隔离盒子并统一编排（向外）——`codex_sandbox.go`、`isolation_unix/windows.go` 为不同 CLI 分别做隔离适配，home 目录/session 各自独立。

同一个"运行时隔离"概念，在不同抽象层复用。multica 的 Go 代码测试极密集（几乎每文件配 `_test.go`），是"生产级 agent 运行时工程"的规范范例。它的编排协调留到 [CH12](ch12-multi-agent.md)。

## SWE-bench：分层镜像做可复现

评测框架 SWE-bench（arXiv 2310.06770）的执行环境工程很值得借鉴：**Docker 三层镜像**——`base`（系统）→ `env`（依赖）→ `instance`（具体任务），层层缓存复用。判定用两组测试：`FAIL_TO_PASS`（issue 真修复）+ `PASS_TO_PASS`（没破坏既有），全过才算 resolved。这展示了"容器分层"如何同时实现**隔离 + 可复现 + 高效缓存**。

## 三后端取舍

| 后端 | 隔离 | 启动开销 | 可复现 | 可扩展 | 适合 |
| --- | --- | --- | --- | --- | --- |
| 进程内（你现在的） | 无 | 极低 | 差 | 差 | 玩具/完全可信 |
| 本地子进程 | 弱（同机） | 低 | 一般 | 差 | 本地 CLI 开发 |
| Docker 容器 | 强 | 中 | 强 | 中 | 不可信代码/CI/评测 |
| 远程 | 强 | 高 | 强 | 强 | 大规模/云端 |

**决策原则**：本地可信 → 子进程够；不可信代码/要可复现 → 容器（分层镜像做缓存）；大规模云端 → 远程。**但无论选哪个，先抽象统一 Runtime 接口**——这样今天用子进程，明天要上容器，改一个实现类即可。

## 动手：把执行改造成可插拔 runtime

### 第 1 步：定义 Runtime 接口 + 两个实现

照 OpenHands 范式：抽象一个 `Runtime`，给两个实现——本地子进程 + Docker。工具的执行统一走它。

```python
# runtime.py
import subprocess

class Runtime:                                # 抽象接口（仿 OpenHands）
    def run(self, cmd: str) -> str: raise NotImplementedError

class LocalRuntime(Runtime):                  # 本地子进程
    def run(self, cmd):
        r = subprocess.run(cmd, shell=True, capture_output=True,
                           text=True, timeout=30)
        return (r.stdout + r.stderr).strip()[:4000]

class DockerRuntime(Runtime):                 # 容器隔离
    def __init__(self, image="python:3.11", workdir="/work"):
        self.image, self.workdir = image, workdir
    def run(self, cmd):
        # 把命令扔进容器执行，工作区挂载进去（-v）
        full = ["docker", "run", "--rm", "--network", "none",   # 禁网！呼应CH6
                "-v", f"{os.getcwd()}:{self.workdir}", "-w", self.workdir,
                self.image, "bash", "-c", cmd]
        r = subprocess.run(full, capture_output=True, text=True, timeout=60)
        return (r.stdout + r.stderr).strip()[:4000]
```

### 第 2 步：bash 工具改为走 runtime

```python
# tools.py — bash 走 runtime
RUNTIME = LocalRuntime()          # 换成 DockerRuntime() 即容器隔离，其他不用改!

@tool("bash", "执行 shell 命令", {...})
def bash(cmd):
    return RUNTIME.run(cmd) or "[无输出]"   # 执行细节委托给 runtime
```

**体会依赖倒置**：改一行 `RUNTIME = DockerRuntime()`，你的 agent 就从"本机裸跑"变成"容器隔离 + 禁网"——工具代码、循环代码**一律不动**。这就是 7.1/7.2 讲的抽象的回报。注意 DockerRuntime 里 `--network none` 把 CH6 的"禁网"落到了物理层：就算 agent 被 injection 骗了想联网，容器根本没网络。**审批（CH6）+ 沙箱（CH7）两层叠加，防线才真正硬。**

## 里程碑 6 · 自测清单

- [ ] 定义了 Runtime 抽象接口 + Local/Docker 两实现
- [ ] bash 工具委托给 runtime，不再自己 subprocess
- [ ] 改一行 `RUNTIME=` 就能切换后端，其他代码不动
- [ ] （装了 Docker 的话）DockerRuntime 能跑通，且 `--network none` 生效
- [ ] 能说清"审批（CH6）+ 沙箱（CH7）如何两层叠加防住 injection"

核心 harness（循环/交互/工具/上下文/权限/运行时）六大件你都造过一遍了！接下来 CH8-10 补生产级的持久化、错误恢复、可观测。
