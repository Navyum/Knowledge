---
title: eBPF技术
date: 2025-06-17 11:29:33
author: Navyum
tags: 
 - 性能分析
 - 可视化
 - eBPF
categories: 
 - 工具
 - 性能分析

article: true
index: true
headerDepth: 2
sticky: false
star: false
---

### eBPF的原理
使用验证器保证安全性，通过BPF映射实现内核-用户空间通信
所有与用户空间的交互都是通过 eBPF“映射”进行的，这些映射是键值存储。
每个 eBPF 程序都将在一定的有限执行时间内完成，即非图灵完备


### bcc
BCC适合使用了其他库的复杂脚本、守护进程

### bpftrace
* 优点：
  bpftrace基于内置Linux技术，不用追赶内核版本改动，稳定性更高
  脚本执行速度比systemtap快（使用llvm编译成BPF）

* 缺点：
  bpftrace语言特性上没有systemtap丰富，不太能进行复杂的探测操作
  探针附到函数一定偏移处不方便
  无法直接获取函数的局部变量
  无法直接获取结构体信息
  内核版本要求较高，在较旧的发行版上难以安装

### Cilium


参考：
https://github.com/bpftrace/bpftrace
https://catbro666.github.io/posts/46dd3f4b/
https://www.joyfulbikeshedding.com/blog/2019-01-31-full-system-dynamic-tracing-on-linux-using-ebpf-and-bpftrace.html
https://www.brendangregg.com/ebpf.html#bpftraceoneliners