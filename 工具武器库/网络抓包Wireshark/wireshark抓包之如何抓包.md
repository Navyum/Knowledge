---
title: wireshark抓包之如何抓包
author: Navyum
date: 2025-08-11 17:25:58

article: true
index: true

headerDepth: 2
sticky: true
star: true

tags: 
 - 抓包
 - wireshark抓包
categories: 
 - wireshark
 - 工具

---

## wireshark抓包之如何抓包

### Linux环境配置（需要进行https解析时）
- 添加sslkeylogfile（必须）
  ```bash
  touch /data/sslkeylogfile
  ```
- 设置SSLKEYLOGFILE：修改系统环境变量
  ```bash
  export SSLKEYLOGFILE="/data/sslkeylogfile"
  ```

### tcpdump基本使用
- 抓取指定域名/IP的包（二进制格式用于wireshark分析）
  ```bash
  ## -X 以十六进制和 ASCII 混合格式显示数据包内容（适合分析二进制协议）
  ## host 一般是从客户端抓包，设置为对应服务器IP或域名即可
  tcpdump -X host ip/domain -w file.pcap
  ```
- 指定抓取每个数据包的字节数（直接机器上查看ASCII）（默认是65536字节）
  ```bash
  ## -A 以 ASCII 格式显示数据包内容（适合查看 HTTP 等文本协议）
  tcpdump -A -s 100 host ip/domain
  ```


### wireshark基本使用
- 设置TLS的路径
 【编辑】->【首选项】->【Protocols】->【TLS】->【Pre-Master Secret log】-> "选中sslkeylogfile文件"
- 按协议筛选：直接输入协议名（如 http、tcp、tls、dns），只显示该协议的包
- 按内容筛选：
  ```bash
  # 显示 HTTP 请求中 URI 包含 login 的包
  http.request.uri contains "login"
  
  #显示数据包内容中包含 password 的包
  data contains "password"
  ```
- 追踪完整会话（流分析）
 【右键点击一个数据包】 → Follow → 选择协议（如 TCP Stream、UDP Stream、HTTP Stream）