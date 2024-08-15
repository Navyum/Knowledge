# Go 语言经典知识总结

基于混合线程的并发编程模型自然不必多说

# 在数据类型方面有：

* 基于底层数组的切片；
* 用来传递数据的通道；
* 作为一等类型的函数；
* 可实现面向对象的结构体；
* 能无侵入实现的接口等。
# 在语法方面有：

* 异步编程神器go语句；
* 函数的最后关卡defer语句；
* 可做类型判断的switch语句；
* 多通道操作利器select语句；
* 非常有特色的异常处理函数panic和recover。
# 测试 Go 程序的程序测试套件：

* 独立的测试源码文件；
* 三种功用不同的测试函数；
* 专用的testing代码包；
* 功能强大的go test命令。
# Go语言提供的那些同步工具：

* 经典的互斥锁；
* 读写锁；
* 条件变量；
* 原子操作
# Go 语言特有的一些数据类型：

* 单次执行小助手sync.Once；
* 临时对象池sync.Pool；
* 帮助我们实现多 goroutine 协作流程的sync.WaitGroup、context.Context；
* 一种高效的并发安全字典sync.Map
# Go常用标准库：

sync

list

ring

strings

bytes

bufio

os

net

net/http

runtime

# GO内置函数（Built-in）

copy



逃逸分析

