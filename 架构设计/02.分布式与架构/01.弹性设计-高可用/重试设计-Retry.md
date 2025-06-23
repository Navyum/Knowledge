# 重试设计-Retry

定义：

     “重试”的语义是我们认为这个故障是暂时的，而不是永久的，所以，我们会去重试。

重试设计重点：

*  确定重试场景，即什么样的错误下需要重试。
       可重试：调用超时、返回已知的可以重试的错误（如繁忙中、流控中、维护中、资源不足等）

       不可重试：业务级错误，无权限等，技术级错误，bug，500

*  重试的时间和重试的次数。即重试策略。
       引入“指数级退避”策略，即每次重试，时间间隔成倍增加。类似：TCP拥塞控制

*  服务长期故障的处理。如果超过重试次数，或是重试时间，那么重试没有意义。触发熔断，对新请求直接返回错误直到服务恢复。
* 调用方需要做幂等设计，否则会不安全。
* 重试代码设计比较通用和简单。两种模式：  
          1. java annotation 2. service mesh

* 对于有事务相关的操作，我们可能会希望能重试成功，而不至于走业务补偿那样的复杂的回退流程。此时需要保存上下文。
拓展：

spring 重试策略：

* NeverRetryPolicy：只允许调用 RetryCallback 一次，不允许重试。
* AlwaysRetryPolicy：允许无限重试，直到成功，此方式逻辑不当会导致死循环。
* SimpleRetryPolicy：固定次数重试策略，默认重试最大次数为 3 次，RetryTemplate 默认使用的策略。
* TimeoutRetryPolicy：超时时间重试策略，默认超时时间为 1 秒，在指定的超时时间内允许重试。
* CircuitBreakerRetryPolicy：有熔断功能的重试策略，需设置 3 个参数 openTimeout、resetTimeout 和 delegate；关于熔断，会在后面描述。
* CompositeRetryPolicy：组合重试策略。有两种组合方式，乐观组合重试策略是指只要有一个策略允许重试即可以，悲观组合重试策略是指只要有一个策略不允许重试即不可以。但不管哪种组合方式，组合中的每一个策略都会执行。
backoff策略：

* NoBackOffPolicy：无退避算法策略，即立即重试；
* FixedBackOffPolicy：固定时间的退避策略，需设置参数 sleeper 和 backOffPeriod，sleeper 指定等待策略，默认是 Thread.sleep，即线程休眠，backOffPeriod 指定休眠时间，默认 1 秒。
* UniformRandomBackOffPolicy：随机时间退避策略，需设置 sleeper、minBackOffPeriod 和 maxBackOffPeriod。该策略在[minBackOffPeriod, maxBackOffPeriod]之间取一个随机休眠时间，minBackOffPeriod 默认为 500 毫秒，maxBackOffPeriod 默认为 1500 毫秒。
* ExponentialBackOffPolicy：指数退避策略，需设置参数 sleeper、initialInterval、maxInterval 和 multiplier。initialInterval 指定初始休眠时间，默认为 100 毫秒。maxInterval 指定最大休眠时间，默认为 30 秒。multiplier 指定乘数，即下一次休眠时间为当前休眠时间 *multiplier。
* ExponentialRandomBackOffPolicy：随机指数退避策略，引入随机乘数，之前说过固定乘数可能会引起很多服务同时重试导致 DDos，使用随机休眠时间来避免这种情况。
