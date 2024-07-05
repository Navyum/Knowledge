1. 接口的作用：
    1. 隐藏细节：通过接口可以对对象进行必要的抽象
    2. 解耦：      通过接口，我们能够以模块化的方式构建起复杂、庞大的系统
    3. 权限控制：通过接口来控制接入方式和接入方的行为，降低安全风险

2. 使用接口的成本：
a. 内存逃逸：接口的动态数据类型对应的数据大小难以预料，所以接口中使用指针来存储数据。为了方便数据被寻址，平时分配在栈中的值一旦赋值给接口后，Go 运行时会在堆区为接口开辟内存（内存逃逸意味着堆内存分配时的时间消耗）

b. 查找接口中容纳的动态数据类型和它对应的方法的指针带来的开销

3. 值接收者和指针接收者：
    1. 实现了接收者是值类型的方法，会隐含实现接收者是指针类型的方法；
    2. 实现了接收者是指针类型的方法，不会自动生成对应接收者是值类型的方法；
    3. 对于实现了接收者是值类型的方法，无论调用者是对象还是对象指针，修改的都是对象的副本，不影响调用者；
    4. 对于实现了接收者是指针类型的方法，调用者修改的是指针指向的对象本身；
    5. 如何区分何时使用：
        1. 类型的成员都是由 Go 语言里内置的原始类型，如字符串，整型值等，那就定义值接收者类型的方法。（像内置的引用类型，如 slice，map，interface声明他们的时候，实际上是创建了一个 `header`， 对于他们也是直接定义值接收者类型的方法。这样，调用函数时，是直接 copy 了这些类型的 `header`，而 `header` 本身就是为复制设计的 ）
        2. 如果类型具备非原始的本质，不能被安全地复制，这种类型总是应该被共享，那就定义指针接收者的方法。比如 go 源码里的文件结构体（struct File）就不应该被复制，应该只有一份`实体` 

4. iface和eface二者区别：
iface描述的接口包含方法，而 eface则是不包含任何方法的空接口: interface{}

5. iface结构体说明:
```plain
type iface struct {
	tab  *itab    //接口的类型以及赋给这个接口的实体类型
	data unsafe.Pointer //指向接口具体的值，一般而言是一个指向堆内存的指针
}

type itab struct {
	inter  *interfacetype //描述了接口的类型
	_type  *_type //描述了实体的类型，包括内存对齐方式，大小等
	link   *itab
	hash   uint32 // copy of _type.hash. Used for type switches.
	bad    bool   // type does not implement interface
	inhash bool   // has this itab been added to hash?
	unused [2]byte
	fun    [1]uintptr // variable sized 放置和接口方法对应的具体数据类型的方法地址
}

type interfacetype struct {
	typ     _type //描述 Go 语言中各种数据类型的结构体
	pkgpath name //定义了接口的包名
	mhdr    []imethod  //接口所定义的函数列表
}
```

5.  iface内存模型：
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/ea9c54d9bf3b37ad38aa5543368ad439.png)



6. eface结构体：
```plain
type eface struct {
    _type *_type
    data  unsafe.Pointer
}
```

7. 接口的动态类型和动态值：
`tab` 是接口表指针指向类型信息，即动态类型。

`data` 是数据指针指向具体的数据，即动态值。

1. _type结构体:
```plain
type _type struct {
    // 类型大小
	size       uintptr
    ptrdata    uintptr
    // 类型的 hash 值
    hash       uint32
    // 类型的 flag，和反射相关
    tflag      tflag
    // 内存对齐相关
    align      uint8
    fieldalign uint8
    // 类型的编号，有bool, slice, struct 等等等等
	kind       uint8
	alg        *typeAlg
	// gc 相关
	gcdata    *byte
	str       nameOff
	ptrToThis typeOff
}
```

8. Go 语言各种数据类型都是在 `_type` 字段的基础上，增加一些额外的字段来进行管理的。
```plain
type arraytype struct {
	typ   _type
	elem  *_type
	slice *_type
	len   uintptr
}
type chantype struct {
	typ  _type
	elem *_type
	dir  uintptr
}
type slicetype struct {
	typ  _type
	elem *_type
}
type structtype struct {
	typ     _type
	pkgPath name
	fields  []structfield
}
```

9. 接口的构造过程：
10. 接口转换的原理：
    1. 当判定一种类型是否满足某个接口时，Go 使用类型的方法集和接口所需要的方法集进行匹配，如果类型的方法集完全包含接口的方法集，则可认为该类型实现了该接口(duck typing 🦆类型)
        1. 匹配的细节：某类型有 `m` 个方法，某接口有 `n` 个方法，则很容易知道这种判定的时间复杂度为 `O(mn)`，Go 会对方法集的函数按照函数名的字典序进行排序，所以实际的时间复杂度为 `O(m+n)` 
    2. 具体代码实现：
```plain
func convI2I(inter *interfacetype, i iface) (r iface) {
	tab := i.tab
	if tab == nil {
		return
	}
	if tab.inter == inter {
		r.tab = tab
		r.data = i.data
		return
	}
	r.tab = getitab(inter, tab._type, false)
	r.data = i.data
	return
}
```
函数参数 `inter` 表示接口类型，`i` 表示绑定了实体类型的接口，`r` 则表示接口转换了之后的新的 `iface`。 `iface` 是由 `tab` 和 `data` 两个字段组成。所以 `convI2I` 函数需要找到新 `interface` 的 `tab` 和 `data。`
我们还知道，`tab` 是由接口类型 `interfacetype` 和 实体类型 `_type`。所以最关键的语句是 `r.tab = getitab(inter, tab._type, false)` 

```plain
func getitab(inter *interfacetype, typ *_type, canfail bool) *itab {
	// ……
    // 根据 inter, typ 计算出 hash 值
	h := itabhash(inter, typ)
	// look twice - once without lock, once with.
	// common case will be no lock contention.
	var m *itab
	var locked int
	for locked = 0; locked < 2; locked++ {
		if locked != 0 {
			lock(&ifaceLock)
        }
        
        // 遍历哈希表的一个 slot
		for m = (*itab)(atomic.Loadp(unsafe.Pointer(&hash[h]))); m != nil; m = m.link {
            // 如果在 hash 表中已经找到了 itab（inter 和 typ 指针都相同）
			if m.inter == inter && m._type == typ {
                // ……
                
				if locked != 0 {
					unlock(&ifaceLock)
				}
				return m
			}
		}
	}
    // 在 hash 表中没有找到 itab，那么新生成一个 itab
	m = (*itab)(persistentalloc(unsafe.Sizeof(itab{})+uintptr(len(inter.mhdr)-1)*sys.PtrSize, 0, &memstats.other_sys))
	m.inter = inter
    m._type = typ
    
    // 添加到全局的 hash 表中
	additab(m, true, canfail)
	unlock(&ifaceLock)
	if m.bad {
		return nil
	}
	return m
}
```

getitab 函数会根据 `interfacetype` 和 `_type` 去全局的 itab 哈希表中查找，如果能找到，则直接返回；否则，会根据给定的 `interfacetype` 和 `_type` 新生成一个 `itab`，并插入到 itab 哈希表，这样下一次就可以直接拿到 `itab`。

这里查找了两次，并且第二次上锁了，这是因为如果第一次没找到，在第二次仍然没有找到相应的 `itab` 的情况下，需要新生成一个，并且写入哈希表，因此需要加锁。这样，其他协程在查找相同的 `itab` 并且也没有找到时，第二次查找时，会被挂住，之后，就会查到第一个协程写入哈希表的 `itab` 。

```plain
// 检查 _type 是否符合 interface_type 并且创建对应的 itab 结构体 将其放到 hash 表中
func additab(m *itab, locked, canfail bool) {
	inter := m.inter
	typ := m._type
	x := typ.uncommon()

	// both inter and typ have method sorted by name,
	// and interface names are unique,
	// so can iterate over both in lock step;
    // the loop is O(ni+nt) not O(ni*nt).
    // 
    // inter 和 typ 的方法都按方法名称进行了排序
    // 并且方法名都是唯一的。所以循环的次数是固定的
    // 只用循环 O(ni+nt)，而非 O(ni*nt)
	ni := len(inter.mhdr)
	nt := int(x.mcount)
	xmhdr := (*[1 << 16]method)(add(unsafe.Pointer(x), uintptr(x.moff)))[:nt:nt]
	j := 0
	for k := 0; k < ni; k++ {
		i := &inter.mhdr[k]
		itype := inter.typ.typeOff(i.ityp)
		name := inter.typ.nameOff(i.name)
		iname := name.name()
		ipkg := name.pkgPath()
		if ipkg == "" {
			ipkg = inter.pkgpath.name()
		}
		for ; j < nt; j++ {
			t := &xmhdr[j]
            tname := typ.nameOff(t.name)
            // 检查方法名字是否一致
			if typ.typeOff(t.mtyp) == itype && tname.name() == iname {
				pkgPath := tname.pkgPath()
				if pkgPath == "" {
					pkgPath = typ.nameOff(x.pkgpath).name()
				}
				if tname.isExported() || pkgPath == ipkg {
					if m != nil {
                        // 获取函数地址，并加入到itab.fun数组中
						ifn := typ.textOff(t.ifn)
						*(*unsafe.Pointer)(add(unsafe.Pointer(&m.fun[0]), uintptr(k)*sys.PtrSize)) = ifn
					}
					goto nextimethod
				}
			}
		}
        // ……
        
		m.bad = true
		break
	nextimethod:
	}
	if !locked {
		throw("invalid itab locking")
    }

    // 计算 hash 值
    h := itabhash(inter, typ)
    // 加到Hash Slot链表中
	m.link = hash[h]
	m.inhash = true
	atomicstorep(unsafe.Pointer(&hash[h]), unsafe.Pointer(m))
}
```
 `additab` 会检查 `itab` 持有的 `interfacetype` 和 `_type` 是否符合，就是看 `_type` 是否完全实现了 `interfacetype` 的方法，也就是看两者的方法列表重叠的部分就是 `interfacetype` 所持有的方法列表。注意到其中有一个双层循环，乍一看，循环次数是 `ni * nt`，但由于两者的函数列表都按照函数名称进行了排序，因此最终只执行了 `ni + nt` 次，代码里通过一个小技巧来实现：第二层循环并没有从 0 开始计数，而是从上一次遍历到的位置开始。 
