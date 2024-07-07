条件变量定义：

    当共享资源的状态不满足条件的时候，想操作它的线程再也不用循环往复地做检查了，只要等待通知就好了。

    条件变量的初始化离不开互斥锁，并且它的方法有的也是基于互斥锁的

    方法：等待通知（wait）、单发通知（signal）和广播通知（broadcast）

规则：

    利用条件变量可以实现单向的通知，而双向的通知则需要两个条件变量。这也是条件变量的基本使用规则。


Wait： wait方法总会把当前的 goroutine 添加到通知队列的队尾

Signal： signal方法总会从通知队列的队首开始，查找可被唤醒的 goroutine。所以，因Signal方法的通知，而被唤醒的 goroutine 一般都是最早等待的那一个。这两个方法的行为决定了它们的适用场景。如果你确定只有一个 goroutine 在等待通知，或者只需唤醒任意一个 goroutine 就可以满足要求，那么使用条件变量的Signal方法就好了。

Broadcast： 通知所有通知队列的goroutine，只要你设置好各个 goroutine 所期望的共享资源状态就可以了。

wait的流程：

1. 把调用它的 goroutine（也就是当前的 goroutine）加入到当前条件变量的通知队列中。
2. 解锁当前的条件变量基于的那个互斥锁。
3. 让当前的 goroutine 处于等待状态，等到通知到来时再决定是否唤醒它。此时，这个 goroutine 就会阻塞在调用这个Wait方法的那行代码上。
4. 如果通知到来并且决定唤醒这个 goroutine，那么就在唤醒它之后重新锁定当前条件变量基于的互斥锁。自此之后，当前的 goroutine 就会继续执行后面的代码了。
注意点：

    条件变量的通知具有即时性。也就是说，如果发送通知的时候没有 goroutine 为此等待，那么该通知就会被直接丢弃。在这之后才开始等待的 goroutine 只可能被后面的通知唤醒。


e.g.

goroutine 1：

lock.Lock()

for mailbox == 1 { 

    sendCond.Wait()

}

mailbox = 1

lock.Unlock()

recvCond.Signal()

gproutine 2：

lock.RLock()

for mailbox == 0 { 

    recvCond.Wait()

}

mailbox = 0

lock.RUnlock()

sendCond.Signal()

