---
title: FlameGraph-火焰图
date: 2025-06-17 11:26:14
author: Navyum
tags: 
 - 性能分析
 - 可视化
 - FlameGraph
categories: 
 - 工具
 - 性能分析
 - FlameGraph
article: true
index: true

headerDepth: 2
sticky: false
star: false
---

火焰图是一种分层数据**可视化工具**，用于直观展示程序中时间都花在了哪里。
栈采样：每秒多次，程序中的线程会被中断，同时记录下代码中的当前位置（基于线程的指令指针），以及到达该位置所调用的函数链。聚合结果。
说明：
    * y轴表示：堆栈深度，主函数更靠近底部
    * x轴表示：涵盖所有样本，其顺序无意义。<span style="color: rgb(255, 41, 65);">对于CPU火焰图来说，其宽度表示：该函数在 CPU 上运行或处于调用堆栈中的总时间。</span>

### 性能数据采集工具介绍
#### 1. 使用 Perf 采集数据
- 优点 ：
  - 学习成本低： Perf 是 Linux 自带的工具，命令简单易用。
  - 高效：直接采集 CPU 性能数据，生成火焰图的过程自动化。
  - 准确：能够精确采集函数调用栈和执行时间。
- 适用场景 ：Linux 系统下的应用程序性能分析。
- 示例 ：
  ```bash
    perf record -g -p <PID>      # 采集数据
    perf script > output.txt     # 转换数据
    stackcollapse-perf.pl output.txt > folded.txt # 聚合数据
    flamegraph.pl folded.txt > flamegraph.svg # 生成火焰图
   ```

#### 2. 使用 Async Profiler（针对 Java 应用）采集并分析
- 优点 ：
  - 学习成本低：专为 Java 设计，命令简单。
  - 高效：直接采集 JVM 的性能数据，支持多种分析模式（CPU、内存、锁等）。
  - 准确：能够精确采集 Java 方法的调用栈和执行时间。
- 适用场景 ：Java 应用的性能分析。
- 示例 ：
  ```bash
  ./profiler.sh -d 30 -f output.html <PID>
  ```
#### 3. 使用 Py-Spy（针对 Python 应用）采集并分析
- 优点 ：
  - 学习成本低：无需修改代码，命令简单。
  - 高效：直接采集 Python 程序的调用栈。
  - 准确：能够精确采集 Python 函数的调用栈和执行时间。
- 适用场景 ：Python 应用的性能分析。
- 示例 ：
  ```bash
  py-spy record -o output.svg --pid <PID>
   ```
#### 4. 使用 pprof（针对 Go 应用）
- 优点 ：
  - 学习成本低：Go 语言自带工具，集成度高。
  - 高效：直接采集 Go 程序的性能数据，支持多种分析模式（CPU、内存、阻塞等）。
  - 准确：能够精确采集 Go 函数的调用栈和执行时间。
- 适用场景 ：Go 应用的性能分析。
- 示例 ：
  ```bash
  go tool pprof -http=:8080 http://localhost:6060/debug/pprof/profile
   ```
#### 5. 使用 systemtap（所有应用）采集数据
- 优点 ：
  - 学习成本较高：需要学习对应的systemtap语法。
  - 高效：可以针对性的采集需要的数据，用户态、内核态都可以。
  - 准确：精准采集特定函数、变量的使用数据。
- 适用场景 ：更深层次的性能分析，适用于所有应用。
- 示例 ：
  ```bash
  stap script.stp -X PID > output.txt 
  stackcollapse-stap.pl output.txt | flamegraph.pl > flamegraph.svg
   ```

### 使用 FlameGraph 工具进行火焰图生成
- 优点 ：
  - 学习成本低：生成火焰图的过程自动化，命令简单。
  - 高效：将原始数据快速转换为直观的火焰图。
  - 准确：火焰图能够清晰展示性能瓶颈。
- 适用场景 ：所有支持火焰图生成的语言和工具。
- 示例 ：
  ```bash
  ./stackcollapse-xxx.pl output.txt > out.folded      # 转换数据
  ./flamegraph.pl        out.folded > flamegraph.svg  # 生成svg
   ```



### 参考：
[官方flamegraphs](https://www.brendangregg.com/flamegraphs.html)
[内存frame](https://www.brendangregg.com/FlameGraphs/memoryflamegraphs.html)