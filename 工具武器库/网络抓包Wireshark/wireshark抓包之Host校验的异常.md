---
title: wireshark抓包-Host校验的异常
date: 2025-03-28 15:11:11
author: Navyum
icon: lucide-lab:shark

tags: 
 - wireshark
 - 抓包
 - tomcat
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

### nginx 负载均衡导致的400错误
---

### 背景：
因为转换服务比较耗CPU等资源，业务层针对pdf转offcie服务做负载均衡

### 出现问题：
未做负载均衡前，一切正常；添加负载均衡之后反而失败了

### 出错的nginx配置
```nginx.conf
location /aspose_sdk/
{
    client_body_buffer_size 30M;
    client_max_body_size 30M;
    proxy_pass http://aspose_sdk/;
    proxy_set_header Connection "";
    proxy_http_version 1.0;
    proxy_connect_timeout 10;
    proxy_send_timeout 30;
    proxy_read_timeout 300;
}
```

```backend.conf
upstream aspose_sdk {
    server 10.2.7.228:9081;
    server 10.2.7.229:9081;
    keepalive 10;
}
```

### 最终定位到原因：
直接原因：上游的aspose服务spring boot使用的是tomcat的网络框架，对host校验规则存在一些问题，不支持下划线。附[issue](https://github.com/spring-projects/spring-boot/issues/13236)
根本原因：nginx本身使用的backend别名作为Host name，没有正确处理host。（在不设置proxy_set_header的情况下，默认为 `proxy_set_header $proxy_host`）

### 分析过程：
1. 复现问题：
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/6a47790d218ab48980a42da6b727d9a7.png" width="80%"></p>
2. 通过tcpdump进行抓包，在wireshark中打开
   * 请求失败400
     <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/fe3f14217fb139fff3aa4318ae06a554.png" width="80%"></p>
   * 请求头信息
     <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/99522b1c9e8360f7f04775fe5583d6c9.png" width="80%"></p>
   * 正常的请求头信息
     <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/43cabc80eb46e25ee5f2639385e43285.png" width="80%"></p>

3. 解析抓包结果：
    1. 根据错误码4XX，初步可以断定是客户端（请求端）的问题
    2. 客户端问题，一般可以逐个分析请求头、请求体等信息是否正确，例如HTTP/1.1 强制要求必须要有Host头等等
    3. 对比分析正常、异常的抓包请求，分析差异点（关键步骤）
    4. 最终发现仅Host存在差异。此时可以进行实验操作，对Host进行修改再测试，最终发现是Host不正确，被nginx使用成了backend的名称aspose_sdk。
       相关资料：[nginx 官方文档](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_set_header)
       <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/accb47cd32248ea3c59922964d60872b.png" width="80%"></p>

4. 解决方案：
    1. 将upstream的名称去除下划线_，aspose_sdk改为asposeSdk
        * 主要是因为上游服务使用的是Springboot Tomcat历史版本问题
        * 说明：https://github.com/spring-projects/spring-boot/issues/13236
    2. 设置正确的Host，`proxy_set_header HOST $host`
       * 设置为正常的Host（虽然大多时候没啥问题，出问题可难排查）

### 延伸：
1. nginx 在使用upstream时，命名最好不要带符号和数字（避免出现问题）
2. 设置正确的Host（做好规范）
3. proxy_set_header的用法
    * `proxy_set_header HOST $host`：用户请求中的Host字段，不带端口
    * `proxy_set_header HOST $http_host`：用户请求中的Host字段，带端口
    * `proxy_set_header HOST $proxy_host`：反向代理中设置的上游的主机名
