1. TTL
    1. TTL初始值为 8 位，所以取值范围是 0~255：Windows 是 128，Linux 是 64
    2. TTL 是从出发后就开始递减的
2. TCP keep-alive 和HTTP Keep-alive
作用：心跳保活、健康检查

定义：定时发送心跳探测包；对于心跳回复包有超时限制。

Time 列的类型选择很重要

setsockopt() 系统调用时设置

间隔时间：net.ipv4.tcp_keepalive_time，其值默认为 7200（秒），也就是 2 个小时。最大探测次数：net.ipv4.tcp_keepalive_probes，在探测无响应的情况下，可以发送的最多连续探测次数，其默认值为 9（次）。最长间隔：net.ipv4.tcp_keepalive_intvl，在探测无响应的情况下，连续探测之间的最长间隔，其值默认为 75（秒）。

http：Connection: Keep-alive Connection: Close（应用场景：api网关通过应用层协议关闭TCP长连接）

