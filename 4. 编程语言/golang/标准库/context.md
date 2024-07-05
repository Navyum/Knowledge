1. 作用：context 用来解决 goroutine 之间`退出通知`、`元数据传递`的功能 
2. context 使用注意事项：
    1. 不要将 Context 塞到结构体里。直接将 Context 类型作为函数的第一参数，而且一般都命名为 ctx。
    2. 不要向函数传入一个 nil 的 context，如果你实在不知道传什么，标准库给你准备好了一个 context：todo。
    3. 不要把本应该作为函数参数的类型塞到 context 中，context 存储的应该是一些共同的数据。例如：登陆的 session、cookie 等。
    4. 同一个 context 可能会被传递到多个 goroutine，别担心，context 是并发安全的。
3. 相关函数：
这些函数都是幂等的，也就是说连续多次调用同一个方法，得到的结果都是相同的 

```plain
func WithCancel(parent Context) (ctx Context, cancel CancelFunc)
func WithDeadline(parent Context, deadline time.Time) (Context, CancelFunc)
func WithTimeout(parent Context, timeout time.Duration) (Context, CancelFunc)
func WithValue(parent Context, key, val interface{}) Context
```
4. WithValue查找过程：
    1. 内存结构：
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/1b05ecae8854b7b4bc2dd07bea5059d3.png)


和链表有点像，只是它的方向相反。Context 指向它的父节点，链表则指向下一个节点

    2. 查找过程：
它会顺着链路一直往上找，比较当前节点的 key 是否是要找的 key；如果是则直接返回 value（多个key满足，只返回接近的）；否则一直顺着 context 往前，最终找到根节点（一般是 emptyCtx），直接返回一个 nil。所以用 Value 方法的时候要判断结果是否为 nil。

因为查找方向是往上走的，所以父节点没法获取子节点存储的值，子节点却可以获取父节点的值。

    3. 创建过程：
创建 context 节点的过程实际上就是创建链表节点的过程。两个节点的 key 值是可以相等的，但它们是两个不同的 context 节点。

    4. 局限性：
        1. 查找效率低
        2. 多个节点设置相同的key，只会离当前节点接近的满足条件的一个结果
5. WithCancel过程：
```plain
type cancelCtx struct {
	Context

	// 保护之后的字段
	mu       sync.Mutex
	done     chan struct{}
	children map[canceler]struct{}
	err      error
}
```
 
`cancel()` 方法的功能就是关闭 channel：c.done；递归地取消它的所有子节点；从父节点从删除自己。达到的效果是通过关闭 channel，将取消信号传递给了它的所有子节点 。

当 WithCancel 函数返回的 CancelFunc 被调用或者是父节点的 done channel 被关闭（父节点的 CancelFunc 被调用），此 context（子节点） 的 done channel 也会被关闭。

![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/e5619f1e1058c0518fdbc7045f53670d.png)


6. 
