---
title: systemTap原理
date: 2025-04-03 10:32:56
author: Navyum
tags: 
 - SystemTap
 - 性能分析
categories: 
 - 工具
 - 性能分析
 - Systemtap
---

## systemTap原理
* 将stp文件编译为C文件，再将C文件编译为内核模块.ko文件，将.ko文件加载到内核中，最终利用内核提供的 `kprobes 机制`来设置探测点，采集数据存储到`probe.out`，从而进行系统性能分析。
### 一、systemTap运行流程
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/031aa72127709b2fa27f4e1fda97d28a.png"></p>

#### 1.Parse（词法语法分析）
#### 2.Elaborate（语义分析）
#### 3.Translate（生成 C 代码）
#### 4.Build（编译成内核模块.ko）
#### 5.Load/Run（加载运行）
* 说明：
    * 1~4步骤为编译.ko文件，可以在开发环境进行编译
    * 5步骤，将编译好的.ko文件，使用`staprun`程序在待检测环境运行（注意⚠️：需要确保开发环境、检测环境的内核版本一致）
* 原理：
    * **Kprobes，kernel probes，是 linux 内核的一个重要特性，也是一个轻量级的内核调试工具**
    * systemtap 调用的 kprobe 接口函数来注册 stp 脚本中定义的探测点。当内核运行到探测点时，就会调用对应的处理函数。
    * kprobe 执行过程，就是利用`中断处理`，将`原有指令`扩展成为执行 `pre_handler`-> 执行`原有指令` -> 执行 `post_handler`（类似于 AOP面向切面编程）
    * 其他的类似systemtap的工具：**eBPF（BCC、bpftrace）**、DTrace、**perf**、Strace

#### 6.Store Output（用户态 / 内核态交互，通讯）
生成probe.out文件，用于后续分析
#### 7.Stop/Unload（卸载）
通过stapio向内核发送退出信号


### 二、systemtap关系图
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/aac61ecde949c46d79919400cdf289b9.png" width="80%"></p>

### 三、systemtap存在的问题：
* 基于内核模块技术，在RHEL以外的系统上都不可靠
* 稳定性差。SystemTap不是内核的一部分，所以必须适配内核的改动。因为内核通常被stripped，DWARF格式调试信息被移除了，所以必须要安装对应的debuginfo包。
* 依赖dwarf，需要安装内核符号，<span style="color: rgb(255, 76, 65);">用户层程序则在编译时需要-g</span>
* 因为需要编译，所以systemtap相对DTrace慢很多

### 四、systemtap优点：
* 使用的脚本语言，所以支持的特性更全（如函数偏移、循环、函数局部变量、结构体引用）
* 具有成熟的用户态符号自动加载，可以写比较复杂的探针处理程序
* 内置了大量帮助程序(tapset)，可用于检测不同的目标