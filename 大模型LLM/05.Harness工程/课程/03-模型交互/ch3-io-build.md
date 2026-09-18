---
order: 10
---

# 动手:给 tinyharness 换上真实流式引擎

CH2 里 `tinyharness` 用的是"等整条响应"的玩具调用。这一节把它换成生产级的流式 + 重试,让它能实时吐字、能扛住限流。里程碑 2。

> **这一节结束时,你会有**
>
> `tinyharness` 的 `call_model` 升级为:实时流式打印模型输出、自动累积并解析 tool_use、遇限流/超时自动指数退避重试。循环主体(CH2 写的)几乎不用动——这正是好抽象的价值。

## 第 1 步:流式调用 + 增量渲染

**用 SDK 的流式接口**

好消息(3.1 说过):官方 SDK 已内置碎片累积。用 `stream()` 接口,你能一边拿文本增量实时打印,一边在结束时拿到组装好的完整 message。

```python
# tinyharness.py — 流式 call_model(可运行)
def call_model_streaming(messages, tools):
    with client.messages.stream(
        model="claude-sonnet-5", max_tokens=2048,
        messages=messages, tools=tools,
    ) as stream:
        for text in stream.text_stream:      # 文本增量,实时打印
            print(text, end="", flush=True)
        print()
        return stream.get_final_message()  # SDK 已帮你把碎片拼成完整 message
```

SDK 内部就是 3.1 讲的"按 index 累积、到 stop 才 parse"——你现在理解它在做什么,所以能放心用。

## 第 2 步:用重试包裹

**指数退避 + 错误分类**

把 3.2 的重试逻辑做成一个装饰器,套在调用外面。区分可恢复/不可恢复。

```python
# tinyharness.py — 重试(可运行)
import time, random
import anthropic

RETRYABLE = (anthropic.RateLimitError, anthropic.APITimeoutError,
             anthropic.InternalServerError)   # 529 也属这类

def call_model(messages, tools, max_retries=5):
    for attempt in range(max_retries + 1):
        try:
            return call_model_streaming(messages, tools)
        except anthropic.BadRequestError as e:
            if "too long" in str(e).lower():
                raise NeedCompaction()      # 交给 CH5 压缩后重发
            raise                          # 其他 400 不可恢复
        except RETRYABLE as e:
            if attempt == max_retries: raise
            delay = 0.5 * (2 ** attempt) + random.random()  # 退避+抖动
            print(f"\n[重试 {attempt+1}] {delay:.1f}s 后…")
            time.sleep(delay)

class NeedCompaction(Exception): pass   # 占位,CH5 实现压缩
```

## 第 3 步:接回循环(几乎不用改)

**循环主体保持不变**

关键收获:CH2 写的 `loop()` 主体**一行都不用改**。它调的还是 `call_model(messages, TOOLS)`,只是这个函数内部从"非流式"变成了"流式+重试"。这就是把"模型交互"抽象成一个函数的价值——上层循环不关心底下是否流式、是否重试。

**这就是分层的力量**

你刚经历了一次真实的"关注点分离":**循环层**只管"看→想→做→记"的编排,**交互层**管"怎么可靠地跟模型说话"。换 provider、加缓存、改重试策略,都只动交互层,循环层岿然不动。真实 harness(Claude Code 的 `query.ts` vs `services/api/`)也是这么分的。

## 跑起来

```bash
$ python tinyharness.py "读 README.md 并总结"
我来读一下文件…               # ← 现在是实时逐字冒出来的
[调用 read_file: README.md]
这个项目是…                    # ← 拿到内容后继续流式输出
```

对比 CH2:输出从"卡住几秒后整段蹦出"变成"实时逐字流出",且网络抖动时会自动重试而非崩溃。你的 harness 向生产级迈了关键一步。

## 里程碑检查

> **里程碑 2 · 自测清单**
>
> - [ ] 模型输出能实时逐字打印
> - [ ] 能自动累积并解析出 tool_use(靠 SDK 的 get_final_message)
> - [ ] 手动断网/触发限流时,能看到退避重试而非直接崩
> - [ ] 能说清"为什么循环主体不用改"(交互层被抽象了)
> - [ ] 理解 `NeedCompaction` 为什么单独拎出来(prompt 超长不是普通重试)
>
> 下一站 CH4:给它一套真正好用的工具。
