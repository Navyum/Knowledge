---
title: 静态动态追踪原理
date: 2025-06-17 11:26:41
author: Navyum
tags: 
 - 性能分析
 - 可视化
 - trace
categories: 
 - 工具
 - 性能分析

article: true
index: true

headerDepth: 2
sticky: false
star: false
---

### 动态追踪原理
动态追踪工具在逻辑上比较简单：大多是通过类C语言创建一个脚本，通过编译器翻译成探测代码。**通过一个内核地址模块加载探测代码到内核地址空间，然后patch到当前内核的二进制代码中**。探针将收集的数据写到中间缓冲（这些buffers往往是lock-free的，所以他们对内核性能有较少影响，且不需要切换上下文到追踪程序）。另一个独立的实体消费者读取这些buffers，然后输出数据。
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/8299a9ca33a70fb4ff37387be18a0b2c.png" width="60%"></p>


### linux系统动态追踪工具
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/ea0a557b76ea96275495ade94475e2b4.png" width="40%"></p>


#### 查看可以进行跟踪的内核符号-kprobe

```
sudo bpftrace -l
```

#### 查看可以进行跟踪的用户态符号-uprobe

```
nm /path-to-binary
```


### 如何选择？
* 内核版本比较早，选择systemtap
* 追求体验，选择systemtap
* 追求性能，选择bpftrace
* 追求安全性，选择bpftrace

### 关于静态检测和动态追踪
静态检测：对静态快照的检测，一般是出现问题后，对coredump进行"尸检"
动态追踪：实时动态聚合，一般是出现问题后，在程序尚未出现异常前，通过实时观察程序变化，进行"体检"

## 资料
[awesome-systemtap](https://github.com/lichuang/awesome-systemtap-cn?tab=readme-ov-file)