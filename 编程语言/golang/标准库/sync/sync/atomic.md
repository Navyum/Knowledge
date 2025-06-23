---
title: atomic
author: navyum
date: 2025-06-21 22:28:38

article: true
index: true

headerDepth: 2
sticky: false
star: false

category:
  - 笔记
tag:
  - 笔记
---

互斥锁虽然可以保证临界区中代码的串行执行，但却不能保证这些代码执行的原子性（atomicity）

在众多的同步工具中，真正能够保证原子性执行的只有原子操作

原子操作在进行的过程中是不允许中断的，这个特性由底层CPU提供芯片级别的支持

原子操作支持的类型：

数据类型有：

int32、int64、uint32、uint64、uintptr

unsafe包中的Pointer以及 Value的类型（它可以被用来存储任意类型的值）

原子操作支持的方法：

加法（add）

比较并交换（compare and swap，简称 CAS）

加载（load）

存储（store）

交换（swap）


最佳实践：要想用atomic.AddUint32做减法：

1. delta ：= int32(-3)delta，uint32(delta)，就可以绕过编译器的检查并得到正确的结果了。但是uint32(int32(-3))不可行
2. 使用补码：^uint32(-N-1))
