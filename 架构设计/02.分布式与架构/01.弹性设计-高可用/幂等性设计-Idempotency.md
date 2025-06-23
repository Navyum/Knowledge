# 幂等性设计-Idempotency

概念：

幂等性设计，就是说，一次和多次请求某一个资源应该具有同样的副作用。用数学的语言来表达就是：f(x) = f(f(x))。**注解：不强调获取的结果一致，而是对资源副作用是否一致。**

存在的原因：

系统解耦隔离后，服务间的调用可能会有三个状态，一个是成功（Success），一个是失败（Failed），一个是超时（Timeout）。前两者都是明确的状态，而超时则是完全不知道是什么状态。

解决方案：

a. 下游系统提供相应的查询接口。上游系统在 timeout 后去查询一下。如果查到了，就表明已经做了，成功了就不用做了，失败了就走失败流程。

b. 下游系统通过幂等性的方式。上游系统只管重试，下游系统保证一次和多次的请求结果是一样的。

幂等性方法：

    1. 全剧唯一ID
        1. uuid
        2. 雪花算法 snowflake
        3. 数据库自增id
幂等性存储实现：

新建： insert into … values … on DUPLICATE KEY UPDATE …

更新：update table set status = “paid” where id = xxx and status = “unpaid”

其他：mvvc  通过版本号控制

