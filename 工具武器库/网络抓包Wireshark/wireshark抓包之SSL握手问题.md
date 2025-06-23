---
title: wireshark抓包-SSL握手
date: 2025-03-28 15:11:25
author: Navyum
tags: 
 - 抓包
 - 网络分析
 - TSL握手失败
 - wireshark
categories: 
 - wireshark
 - 工具

article: true
index: true

headerDepth: 2
sticky: true
star: true
---
## wireshark抓包

### SNI问题导致的网关层返回502错误
---

### 背景：
最近攻防等原因，运维将测试环境部分域名上了cloudflare（主要是海外）

### 业务方出现的问题：
在nginx中，这些域名被用做反向代理的upstream，在添加cloudflare之后，访问出现 http 502，具体配置如下

### 出错的nginx配置
```nginx.conf
location /proxy/cn/
{
    proxy_pass https://user_cs_cn_backend/;
    proxy_http_version 1.1;
    proxy_set_header Host "api-cs-cn-sandbox.intsig.net";
    proxy_set_header Connection "keep-alive";
    proxy_connect_timeout 5;
    proxy_send_timeout 10;
    proxy_read_timeout 10;
}
```

```backend.conf
upstream user_cs_cn_backend {
    server api-cs-cn-sandbox.intsig.net:443;
    keepalive 100;
}
```

### 最终定位到原因：
直接原因：跟cloudflare层的SSL握手失败
根本原因：nginx的配置错误、nginx本身没有正确处理SNI

### 如何解决：
在反向代理层添加
```nginx.conf
location  /proxy/cn/ {
...
proxy_ssl_server_name on;
proxy_ssl_name "upstream-domain-name";
...
}
``` 

### 分析过程：
1. 复现问题：
    <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/948a66b5573e0091700f8bdc3696a561.png" width="80%"></p>
2. 查看域名解析情况：
    <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/46a1f13e9f01859b312094dfa5fbe24b.png" width="80%"></p>
3. 通过tcpdump进行抓包，在wireshark中打开
    <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/7c6e0c2d6131e36333e8c24a35cdefb8.png" width="80%"></p>
    <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/517590ec728251d6e3c2cc816e4a26e2.png" width="80%"></p>

4. 查看详细失败：
    <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/4f15c3123bfaa068f9dc582112407e3b.png" width="80%"></p>
5. TLS握手失败错误码 40解读：
    * 根本原因是 SNI 缺失，因为nginx在反向代理时，如果使用的是负载均衡的backend，默认会把host值、SNI传成backend的名称（user_cs_cn_backend），而不是真实的域名（巨坑）。
    * SNI解读：
        * SNI（Server Name Indication）允许客户端在TLS握手时指定要访问的域名，这样服务器可以返回正确的证书。
        * 在反向代理中，如果后端服务（网关）使用不同的域名（网关需要设置为多个域名对应一个公网ip），代理服务器必须正确传递SNI信息，否则后端可能无法识别请求，导致握手失败。
    * 基于这个原因，有两种处理方式：
        1. 不使用backend做负载均衡，而是直接写成对应域名。一般开发、测试环境可以这样操作。
           ```nginx.conf
                location /proxy/cn/
                {
                    proxy_pass https://api-cs-cn-sandbox.intsig.net/;
                    proxy_http_version 1.1;
                    proxy_set_header Connection "keep-alive";
                    proxy_connect_timeout 5;
                    proxy_send_timeout 10;
                    proxy_read_timeout 10;
                }
           ```
        2. 设置正确的SNI信息，proxy_ssl_server_name、proxy_ssl_name。如果涉及backend存在多个域名，则需要结合map、变量，来设置proxy_ssl_name。
            ```nginx.conf
            location  /proxy/cn/ {
            ...
            proxy_ssl_server_name on;
            proxy_ssl_name "upstream-domain-name";
            ...
            }
            ```