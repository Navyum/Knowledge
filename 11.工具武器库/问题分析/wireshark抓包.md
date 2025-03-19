## wireshark抓包


### 问题1: 网关层502
---

#### 背景：
估计是最近攻防等原因，运维将测试环境部分域名上了cloudflare（目前看主要是海外）

#### 业务方出现的问题：
原先使用这些域名做反向代理的upstream，在访问时出现 http 502

#### 最终定位：
跟cloudflare层的SSL握手失败

#### 如何解决：
在反向代理层添加  proxy_ssl_server_name on; 

#### 分析过程：
1. 复现问题：
    <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/948a66b5573e0091700f8bdc3696a561.png" width="80%"></p>
2. 查看域名解析情况：
    <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/46a1f13e9f01859b312094dfa5fbe24b.png" width="80%"></p>
3. 通过tcpdump进行抓包，在wireshark中打开
    <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/7c6e0c2d6131e36333e8c24a35cdefb8.png" width="80%"></p>
4. 查看详细失败：
    <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/4f15c3123bfaa068f9dc582112407e3b.png" width="80%"></p>
5. TLS握手失败错误码 40解读：
    TBD


### 问题2: nginx 负载均衡异常
---
