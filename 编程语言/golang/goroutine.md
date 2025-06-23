---
title: goroutine
author: navyum
date: 2025-06-21 22:24:37

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


G、P、M

Goroutine                                                       Machine

Goroutine                     Processor                         Machine

Goroutine                                                       Machine

Goroutine                                                       Machine

...                                                                  ...

1. 多对多
2. 由Porcessor负责对接Gorutine(用户级线程)和Machine(系统级线程)
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/5f7a6dc3bb43fbdd044ff11b5550ae40.png)


3. go函数真正被执行的时间，总会与其所属的go语句被执行的时间不同，会比go语句慢。只要go语句本身执行完毕，Go 程序完全不会等待go函数的执行，它会立刻去执行后边的语句。这就是所谓的异步并发地执行。
4. 在go语句被执行时，我们传给go函数的参数i会先被求值。
5. 当多个Goroutine存在竞态时（race condition），需要使用sync/atomic ，进行原子操作。e.g.atomic.AddUint32(&count, 1)
