1. 数组和切片的区别和联系：
    1. slice 的底层数据是数组，slice 是对数组的封装
    2. 数组是定长的，长度定义好之后，不能再更改;而切片则非常灵活，它可以动态地扩容
    3. 数组就是一片连续的内存， slice 实际上是一个结构体，包含三个字段：长度、容量、底层数组
2. slice结构体：
```plain
// runtime/slice.go
type slice struct {
	array unsafe.Pointer // 元素指针
	len   int // 长度 
	cap   int // 容量，容量大小一般指从切片的开始位置到底层数据的结尾位置的长度
}
```
3. slice内存模型：
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/257469b8531d78b14872db6b5e5920e5.png)


4. slice 截取特点：
    1. 截取后的切片长度和容量可能会发生变化
    2. 被截取后的数组仍然指向原始切片的底层数据
5. slice作为函数参数:
    1. 若直接传 slice，在调用者看来，实参 slice 并不会被函数中的操作改变；
    2. 若传的是 slice 的指针，在调用者看来，是会被改变原 slice 的。
    3. 不管是传实参还是指针，如果改变了底层数组那么会反应到所用使用该底层数组的切片上。
    4. Go 语言的函数参数传递，只有值传递，没有引用传递。（所有的参数都是实参的副本）
6. 切片动态扩容：
    1. 1.18 之前：当原 slice 容量小于 `1024` 的时候，新 slice 容量变成原来的 `2` 倍；原 slice 容量超过 `1024`，新 slice 容量变成原来的`1.25`倍。
    2. 1.18 开始: 当原slice容量(oldcap)小于256的时候，新slice(newcap)容量为原来的2倍；原slice容量超过256，新slice容量newcap = oldcap+(oldcap+3*256)/4（不考虑内存对齐函数 roundupsize） 
代码实现：

```plain
// go 1.18 src/runtime/slice.go:178
func growslice(et *_type, old slice, cap int) slice {
    // ……
    newcap := old.cap
	doublecap := newcap + newcap
	if cap > doublecap {
		newcap = cap
	} else {
		const threshold = 256
		if old.cap < threshold {
			newcap = doublecap
		} else {
			for 0 < newcap && newcap < cap {
                // Transition from growing 2x for small slices
				// to growing 1.25x for large slices. This formula
				// gives a smooth-ish transition between the two.
				newcap += (newcap + 3*threshold) / 4
			}
			if newcap <= 0 {
				newcap = cap
			}
		}
	}
	// ……
    
    //考虑内存对其因素
	capmem = roundupsize(uintptr(newcap) * ptrSize)
	newcap = int(capmem / ptrSize)
}
```

