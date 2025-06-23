---
title: map
author: navyum
date: 2025-06-21 22:25:18

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

1. map的结构体：
```plain
// A header for a Go map.
type hmap struct {
    // Note: the format of the hmap is also encoded in cmd/compile/internal/reflectdata/reflect.go.
    // Make sure this stays in sync with the compiler's definition.
    count     int // # live cells == size of map.  Must be first (used by len() builtin)
    flags     uint8
    B         uint8  // log_2 of # of buckets (can hold up to loadFactor * 2^B items)
    noverflow uint16 // approximate number of overflow buckets; see incrnoverflow for details
    hash0     uint32 // hash seed,哈希函数

    buckets    unsafe.Pointer // array of 2^B Buckets. may be nil if count==0.
    oldbuckets unsafe.Pointer // previous bucket array of half the size, non-nil only when growing
    nevacuate  uintptr        // progress counter for evacuation (buckets less than this have been evacuated)

    extra *mapextra // optional fields
}
```

2. bucket桶结构体:
```plain
type bmap struct {
    topbits  [8]uint8
    keys     [8]keytype
    values   [8]valuetype
    pad      uintptr
    overflow uintptr
}
```

3.  hashmap结构图：
a. B = 5，buckets num = 2^5

b. bmap[0] 的bucket内，keys 已经装满8个，所以使用overflow 指向新的bucket，即拉链法

c. 插入: 使用hash函数计算出hash值，低8位用来查找对应的bucket，高8位用来在topbits内通过o(1)时间复杂度比较出对应key是否存在

![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/67692c2b23152dbafd5f313645c95610.png)




4.  桶内的key存放按照key...key...value...value各自存放。好处：key和value类型不一样时，可以减少padding损耗（内存对齐）。
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/b08d98123b8f7c7e68ae3b815db6a91d.png)


5. map处于扩容中间态时的遍历:
核心: 2 倍扩容时，老 bucket 会分裂到 2 个新 bucket 中去。而遍历操作会按照新 bucket 的序号顺序进行，碰到老 bucket 未搬迁的情况时，要在老 bucket 中找到将来要搬迁到新 bucket 来的 key。

B=1    扩容==>   B=2

![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/0fc666ec4de9a548b052331b31144a5f.png)


a. 假设经过初始化后，startBucket = 3，offset = 2。于是，遍历的起点将是 3 号 bucket 的 2 号 cell。

b. 因为 3 号 bucket 对应老的 1 号 bucket，因此先检查老 1 号 bucket 是否已经被搬迁过

c. 老 1 号 bucket 已经被搬迁过,所以它的 tophash[0] 值在 (0,4) 范围内，因此只用遍历新的 3 号 bucket。依次遍历 3 号 bucket 找到第一个非空的 key：元素 e

d. 继续从新 3 号 overflow bucket 中找到了元素 f 和 元素 g

e. 新3号 bucket 遍历完之后，回到了新 0 号 bucket。0 号 bucket 对应老的 0 号 bucket，经检查，老 0 号 bucket 并未搬迁，因此对新 0 号 bucket 的遍历就改为遍历老 0 号 bucket。

f. 老 0 号 bucket 在搬迁后将裂变成 2 个 bucket：新 0 号、新 2 号。而我们此时正在遍历的只是新 0 号 bucket。所以我们只会取出老 0 号 bucket 中那些在裂变之后，会被分配到新 0 号 bucket 中的那些 key。 （选择规则，基于hash值低位模4，得出bit = 00会被分配到新0号bucket），找到b、c

g. 遍历老的0号bucket会被分配到新bucket2（bit == 10）的key，找到a、d

h. 继续遍历到新 3 号 bucket 时，发现所有的 bucket 都已经遍历完毕

6. key 遍历的结果是无序的：
a. map 在扩容会发生 key 的搬迁，导致遍历结果无序。

b. go 使用随机一个bucket + 随机序号的 cell(offset) 开始遍历的方式杜绝硬编码map出现有序的结果。目的就是避免误解以为map遍历是有序的。


7. map 扩容重建：
    1. 扩容使用渐进式扩容方式，和redis的全局哈希表一样
    2. 扩容条件：如果溢出桶的数量过多，或者 Map 超过了负载因子大小，Map 就要进行重建。负载因子 = 哈希表中的元素数量(counts) / 桶的数量 (2^B)。Go 语言中的负载因子为 6.5。

