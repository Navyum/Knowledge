## README

### 动态追踪原理
动态追踪工具在逻辑上比较简单：大多是通过类C语言创建一个脚本，通过编译器翻译成探测代码。**通过一个内核地址模块加载探测代码到内核地址空间，然后patch到当前内核的二进制代码中**。探针将收集的数据写到中间缓冲（这些buffers往往是lock-free的，所以他们对内核性能有较少影响，且不需要切换上下文到追踪程序）。另一个独立的实体消费者读取这些buffers，然后输出数据。
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/8299a9ca33a70fb4ff37387be18a0b2c.png" width="80%"></p>


### linux系统动态追踪工具
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/ea0a557b76ea96275495ade94475e2b4.png" width="80%"></p>


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