---
order: 9
---

# 重试 · 缓存 · token 计数

模型调用会超时、会限流、会 529 过载、会 prompt 太长。生产 harness 必须优雅应对每一种。这一节讲三件让调用"稳、省、可控"的事:重试退避、prompt 缓存、token 计数。

## 回到任务

还在[任务地图](../01-基础/lifecycle.md)第 ④ 步"调用模型"。CH2 的最小循环里,`call_model` 一旦网络抖动或限流就直接崩、任务前功尽弃。真实场景里 `parseDate` 任务可能要调模型十几次,任何一次失败都不该让整个任务挂掉——这一节就是给那一步加上"稳"。

## 调用会以各种方式失败

把失败分类,是应对的前提。Claude Code 在 `src/services/api/errors.ts` 里定义了一长串错误常量,归纳起来是几大类:

| 失败类型 | 典型信号 | 该怎么办 |
| --- | --- | --- |
| 限流 / 过载 | HTTP 429（Too Many Requests，请求过多）、`529 Overloaded` | 退避重试(可恢复) |
| 网络超时 / 抖动 | timeout、连接重置 | 退避重试 |
| prompt 太长 | `Prompt is too long` | 不能重试 → 先压缩再重发(CH5) |
| 鉴权 / 余额 | `Invalid API key`、`Credit balance too low` | 不可恢复 → 直接报给用户 |

**关键区分**

失败分两种:**可恢复**(限流/超时/过载 → 等一会重试就好)和**不可恢复**(鉴权错/余额不足 → 重试一万次也没用,直接告诉用户)。harness 的第一要务是**分对类**——对不可恢复的错误做重试,只是白白烧时间和钱。

## 重试:指数退避 + 错误分类

Claude Code 的重试逻辑在 `src/services/api/withRetry.ts`。从它的导出能看清设计:`BASE_DELAY_MS = 500`(基础延迟)、`getRetryDelay()`(算下次等多久)、`is529Error()`(识别过载)、`parseMaxTokensContextOverflowError()`(识别 prompt 超长)、`getDefaultMaxRetries()`(最大重试次数)。

```python
async def with_retry(call, max_retries=getDefaultMaxRetries()):
    for attempt in range(max_retries + 1):
        try:
            return await call()
        except Exception as e:
            if is_context_overflow(e):        # prompt 太长 → 不重试
                raise NeedCompaction(e)         # 交给上层压缩后重发 → CH5
            if not is_retryable(e) or attempt == max_retries:
                raise                          # 不可恢复 或 已到上限
            delay = BASE_DELAY_MS * (2 ** attempt) + jitter()  # 指数退避+抖动
            if is_529(e): delay = max(delay, longer_delay)  # 过载等更久
            await sleep(delay)
```

**三个必备细节**

① **指数退避**:延迟随重试次数翻倍(500ms→1s→2s…),别用固定间隔猛捶服务器。② **抖动(jitter)**:加个随机量,避免大量客户端同时重试造成"惊群"。③ **context overflow 特殊处理**:prompt 太长不是"等一会就好"的错,要抛给上层触发压缩([CH5.3](../05-上下文/ch5-ctx-compact.md))再重发——这是重试与上下文管理的接缝。

## prompt 缓存:省钱省延迟的大杀器

agent 循环每一圈都把"越来越长的历史"重新发给模型。如果每次都全量重新计算,成本和延迟随轮数线性上涨。**prompt 缓存**让模型服务端缓存住 prompt 的**稳定前缀**,后续请求命中缓存的部分大幅降价、提速。

但缓存很脆:**只要前缀变了一个字节,缓存就失效**。Claude Code 有一整个 `src/services/api/promptCacheBreakDetection.ts` 专门监测"缓存什么时候被打断",能看到 `CACHE_TTL_1HOUR_MS`(缓存有效期)、`recordPromptState()`(记录 prompt 状态快照)、`notifyCompaction()`(压缩会打断缓存,要通知)等。

> **缓存友好的黄金法则**
>
> **稳定的放前面,变动的放后面。** system prompt、工具 schema、项目记忆这些每轮不变的,放最前面吃满缓存;用户最新输入、变动的状态放后面。
>
> 两个杀手要警惕:① 在前缀里塞**会变的东西**(如当前时间戳)→ 每轮缓存全失效。② **压缩**会重写历史 → 必然打断缓存(所以 `notifyCompaction` 要记一笔)。这条法则在 [CH5](../05-上下文/ch5-ctx-principles.md) 讲 Manus"KV-cache（Key-Value cache，注意力键值缓存，prompt 缓存的底层机制）友好"时还会遇到。

## token 计数:一切预算的基础

harness 处处要知道"现在用了多少 token":判断要不要压缩(CH5)、判断预算够不够继续(CH2 的 `checkTokenBudget`)、算成本(CH10)。所以需要一个可靠的计数手段。

- **精确计数**:调用 API 的 count_tokens 端点,准但有网络开销。
- **估算**:本地用 tokenizer 或经验公式(如英文 ~4 字符/token)快速估,省调用。Claude Code 里有 `tokenCountWithEstimation` 一类的估算路径。
- **用响应里的用量**:模型响应的 `usage` 字段直接给了真实 input/output token 数,最准——但要到调用后才知道。

**实战策略**

组合用:循环中用**估算**快速判断"是不是快到压缩阈值了"(便宜、够用),用响应的 **`usage` 字段**做事后精确记账(成本追踪、预算扣减)。别为了精确在热路径上狂调 count_tokens 端点——那本身就是开销。

## 本节小结

> **要点**
>
> 1. 先**给失败分类**:可恢复(限流/超时/过载)→ 重试;不可恢复(鉴权/余额)→ 直接报。
> 2. 重试三要素:**指数退避 + 抖动 + context-overflow 特殊处理**(抛去压缩,不当普通重试)。
> 3. prompt 缓存黄金法则:**稳定前缀在前、变动在后**;时间戳和压缩是缓存杀手。
> 4. token 计数:估算用于热路径判断,`usage` 字段用于精确记账。
> 5. 这三件事是循环之外的"可靠性地基",CH8/CH9/CH10 会继续在其上建持久化、错误恢复、成本追踪。
