---
title: wireshark抓包-SSL握手
date: 2025-03-28 15:11:25
author: Navyum
icon: lucide-lab:shark

tags: 
 - 抓包
 - 网络问题分析
 - TSL握手失败
 - wireshark抓包
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


### 证书过期问题导致的网关层返回502错误
---

### 背景：
新对接的新服务，在nginx上配置为反向代理upstream进行访问

### 业务方出现的问题：
访问时稳定复现502错误，但是使用curl则正常。nginx配置如下：

### 出错的nginx配置
```nginx.conf
location /test
{
    proxy_pass https://middleground_workonly_backend/xxx/xxx;
    proxy_http_version 1.1;
    proxy_set_header Host "xxx-sandbox-workonly.xxx.xxx";
    proxy_set_header Connection "keep-alive";
    proxy_connect_timeout 5;
    proxy_send_timeout 10;
    proxy_read_timeout 10;
}
```

```backend.conf
upstream middleground_workonly_backend {
    server xxx-sandbox-workonly.xxx.xxx:443;
    keepalive 100;
}
```

### 最终定位到原因：
直接原因：SSL握手校验不通过，导致握手失败
根本原因：服务端的证书过期

### 如何解决：
更新证书有效期

### 分析过程：
1. 复现问题：
   <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/567b0cd154d0ac2ed69d1d9b06dbb265.png" width="80%"></p>
2. 查看域名解析情况：
   <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/70a5358e761ebb8c11e611713d5eef22.png" width="80%"></p>
3. 通过tcpdump进行抓包，在wireshark中打开
   <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/a5d1a947bf4baba12c9be63539174ed9.png" width="80%"></p>
4. 查看详细失败：
   <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/3f57168739ae9cea17e33cebca34d773.png" width="80%"></p>

5. TLS握手失败错误码 80 解读：
    * Internal Error：服务端内部错误。一般是：
        * 证书问题
        * 握手协议不匹配
        * 无法协商密钥套件
    * 官方解释：[RFC](https://www.ietf.org/rfc/rfc5246.txt)
      >internal_error：
      > An internal error unrelated to the peer or the correctness of the
      > protocol (such as a memory allocation failure) makes it impossible
      > to continue.  This message is always fatal.
6. 进一步获取关键错误信息：
   使用SSL大杀器**openssl**查看握手详细信息：
   ```bash
    #查看SSL/TSL握手信息
    openssl s_client -connect domain:443 -debug
   ```
   <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/4d2a758cf46139dfa3d0dddd480b38bf.png" width="80%"></p>


   使用openssl解析证书查看有效期：
   ```bash
    #查看证书校验信息  -noout 不输出证书内容
    openssl s_client -connect domain:443  -servername domain | openssl x509 -noout -dates
   ```
   <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/bb156771d79dc6cc33054eb5ec11f759.png" width="80%"></p>

   最终确定证书已经过期！！
   