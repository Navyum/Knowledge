---
title: golang学习笔记
author: navyum
date: 2025-06-21 22:24:10

article: true
index: true

headerDepth: 2
sticky: false
star: false

category:
  - 笔记
  - 踩坑笔记
tag:
  - 笔记
---

### omitempty踩坑
* 场景：json、struct转换
* 描述：在http response结构体中不要随意使用
* 陷阱：
    * 无法忽略掉嵌套结构体
    * 给它赋的值恰好等于默认空值,会被忽略
* 补充：因为go的变量有默认值，int为0，会导致业务定义的正常值0不返回
* 举例：
```go
    type PdfResponse struct {
        Ret  uint8    `json:"ret,omitempty"`
        Data *RetData `json:"data,omitempty"`
        Msg  string   `json:"msg"`
    }

    resp := &PdfResponse{
        Ret: 0️,
        Msg: "success",
        Data: &RetData{},
    }

    c.JSON(http.StatusOK, resp)

    //result:
    //{"data":null,"msg":"success"}
```


### replace的使用
* 场景： 多个项目包，本地引用
* 描述： 如果当前项目使用了其他gitlab的项目,可以将其下载到本地并使用replace进行替换
* replace替换支持相对路径
```
  go.mod： 
  replace gitlab.intsig.net/cs-server2/services/cs_proto => ../cs_proto
```

### protoc-go-inject-tag工具使用
* 场景：protoc-gen-go 生成proto.go
* 描述：解决使用protobuf时，因为没有自动生成form tag导致gin shouldbindquery等无法绑定
* 补充：使用inject-tag的弊端：生成proto.go文件后需要再执行一次，在原来的proto.go中新增form tag
* 命令行：`protoc-go-inject-tag -input= xx.pb.go`
* 案例说明：
* ```go
    //file: xx.proto
    message Html2PdfRequest {
        string url = 1;  //手动添加tag @gotags: form:"url" json:"url"
    }

    file: xx.pb.go 未使用inject-tag:
    type Html2PdfRequest struct {
	    state         protoimpl.MessageState
	    sizeCache     protoimpl.SizeCache
	    unknownFields protoimpl.UnknownFields

	    Url string `protobuf:"bytes,1,opt,name=url,proto3" json:"url" `
  }
    //file: xx.pb.go 使用inject-tag:
    type Html2PdfRequest struct {
	    state         protoimpl.MessageState
	    sizeCache     protoimpl.SizeCache
	    unknownFields protoimpl.UnknownFields

	    Url string `protobuf:"bytes,1,opt,name=url,proto3" json:"url" ` //@gotags: form:"url" json:"url"
  } 


### go init函数和main函数
* 场景：app 模块在包引入时即进行app变量初始化以及init调用
* 作用：在启动程序时初始化，并且实现sync.Once的作用，从而在其他地方使用app变量时，使用的是同一份已初始化的数据
* 初始化顺序：
    * 1. 变量初始化->init()->main()
    * 2. 初始化导入的包: runtime解析包依赖关系，没有依赖的包最先初始化
    * 3. 初始化包作用域变量: runtime解析变量依赖关系，没有依赖的变量最先初始化
* 举例：
    ```go    
    // app.go
    func init() {
	    AppCtx = newApp()
    }

    // 全局app
    type App struct {
        //配置AppCtx
        cfg config.Config

        ServiceRegister *service.Register
        DaoRegister     *dao.Register
        BisRegister     *bis.Register
    }

    func newApp() *App {
        return &App{}
    }

    // 初始化服务
    func (app *App) InitApp(cfg config.Config, sw *go2sky.Tracer) { ... }

    ...

    //main.go
    import (
    "gitlab.intsig.net/cs-server2/services/app_sync/app")
    ...

    app.AppCtx.InitApp(cfg, tracer)

    ...
    ```

### 包管理
* 背景：要想写好go代码，要不断理解包和基于包多实践
* 尽量把类型声明(struct)在被使用的文件中
* 按照业务逻辑层(通用分层)、按照功能职责（业务分层）进行包的设计
* ``` go
    paper-code/examples/groupevent
    ├── cmd/
    │   └── eventtimer/
    │       └── update/
    │       └── main.go
    │   └── eventserver/
    │       └── router/
    │           └── handler/
    │           └── router.go
    │       └── tests/
    │       └── main.go
    ├── internal/
    │   └── eventserver/
    │       └── biz/
    │           └── event/
    │           └── member/
    │       └── data/
    │           └── service/
    │   └── eventpopdserver/
    │       └── event/
    │       └── member/
    │   └── pkg/
    │       └── cfg/
    │       └── db/
    │       └── log/
    └── vendor/
    │   ├── github.com/
    │   │   ├── ardanlabs/
    │   │   ├── golang/
    │   │   ├── prometheus/
    │   └── golang.org/
    ├── go.mod
    ├── go.sum


* cmd/: 项目中的所有你将要编译成可执行程序的入口代码都放在cmd/ 文件夹里，这些代码和业务没有关系
* internal/: 在项目中不被复用，也不能被其他项目导入，仅被本项目内部使用的代码包即私有的代码包都应该放在internal文件夹下.
* internal包的导入规则是
* pkg/: 其他项目是可以直接导入
* vendor/: 包含了所有依赖的三方的源代码。早期版本使用，目前已被modules替代。
* kit/： 被不同应用项目导入的基础包
* 

### struct、map 如何选择
* struct，就是你知道key有哪些和对应的数据类型
* map，就是你不能确定key有哪些
* 结构体解析已知结构的json
* json解析到map[string]interface{}

### range 副本问题
* 使用range时，如何判断是否副本？
* range遍历时value是值的拷贝，所以通过value修改值不会生效
    * 解决方法：
    * 1. 遍历的对象中的value调整为指针类型，通过指针修改
    * 2. 通过遍历对象中的key进行修改value值


### io.ReadAll，io.Copy的区别
* io.ReadAll buffer size初始值512，基于slice动态扩容。小于512时，性能问题不大。只完成数据读出。只能用于数据全部读出来的场景。
* io.Copy buffer size固定为32kb，性能好。完成了读出 + 写入Writer。适用于边读边写的大数据场景。
* 如果读取出来的数据，是要用json再解码则可以直接使用 json.NewDecoder(reader).Decode(&v)，直接使用reader，无需buffer

### vscode go跳转问题
[解决方案](https://juejin.cn/s/vscode%20golang%20%E8%B7%B3%E8%BD%AC%E9%85%8D%E7%BD%AE)

### map[string]struct{}的赋值问题
* struct{}应当作为整体，属于一个类型
* 其本质属于匿名结构体类型以及赋值操作
* 具体例子：
* ``` golang
    s=make(map[string]struct{})
    s["1"]=struct{}{}       //第一个{}跟随struct是一个整体，第二个是具体值，因为本身是空结构体，所以值为{}
* 一个带成员的匿名struct赋值：
* ``` golang
    b := make(map[string]*struct{ C int })
    b["s"] = &struct{C int}{
        C: 1,
    }
* ```
* 其他匿名类型：结构体匿名字段、匿名函数/闭包函数

### 检测类型是否实现了接口 var _ io.Writer = (*myWriter)(nil)
* 赋值语句可能会发生隐式类型转换，在转换的过程中，编译器会检测等号右边的类型是否实现了等号左边接口所规定的函数
* ```golang
    type myWriter struct {
    }

    /*func (w myWriter) Write(p []byte) (n int, err error) {
        return
    }*/

    func main() {
        // 检查 *myWriter 类型是否实现了 io.Writer 接口
        var _ io.Writer = (*myWriter)(nil)   //编译器会帮忙实现指针接收者的方法func (w *myWriter) Write

        // 检查 myWriter 类型是否实现了 io.Writer 接口
        var _ io.Writer = myWriter{}//解释下：把myWriter结构体对象绑定到io.Writer接口类型的动态值上
    }
  ```


### new和make
* new 函数：
    * func new(Type) *Type
    * new 返回类型Type的指针 *Type，是零值指针
    * new 仅仅分配空间
    * ``` golang
      //举例：
      type Student struct{}
      var i interface{} = new(Student) //等价于：
      var i interface{} = (*Student)(nil)
      ```
* make 函数：
    * func make(Type, size IntegerType) Type
    * make 返回类型Type
    * make 分配空间 + 初始化
    * make 只能 用于slice、map、chan 对象的初始化
    * make 因为限定只能对Type为 slice、map、chan初始化，所以返回的类型一定是引用类型

### 栈中分配的变量，出栈的时候不会被释放吗
    * ```golang
        func newInt *int {
            var i int
            return &i     //为何可以返回局部变量呢？
        }

        someInt := newInt()
      ```

### 逃逸分析
* 本质：编译器帮程序员决定变量的分配位置，把变量合理地分配到它该去的地方（堆/栈）
* > 1. 如果函数外部没有引用，则优先放到栈中；
  > 2. 如果函数外部存在引用，则必定放到堆中；
* 堆栈的对比：
    * 堆适合不可预知大小的内存分配
    * 堆分配速度较慢
    * 频繁堆分配会形成内存碎片
    * 堆需压迫通过垃圾回收（gc）才能释放，耗cpu；栈可以自动清理
* ```golang   
    package main
    type S struct {}

    func main() {
        var x S
        /*
          z是对x的拷贝，ref函数中对z取了引用，所以z不能放在栈上必须要逃逸到堆上，否则在ref函数之外，无法通过引用找到z。
          仅管在main函数中，直接丢弃了ref的结果，外部没有使用到引用，但是Go的编译器还没有那么智能，分析不出来这种情况。
        */
        _ = *ref(x)
    }

    func ref(z S) *S {
        return &z
    }
  ```

### go编译过程
从源文件到可执行目标文件的转化过程：
![compile](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/b290f1ee1f29670d608c425edfec2d96.png)

### go编译器优化函数
![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/85ada42f30bc8039720da3c7c03a1bbd.png)

### GC机制（对堆上的对象的清理）
* GC算法分类：
    1. 追踪式（从根开始，根据引用关系，完整扫描整个堆）
        1. 标记清扫：
            - 标记存活对象，清扫可回收对象
        2. 标记整理：
            - 在标记清扫基础上，优化内存使用，将对象尽可能放在连续内存上
        3. 增量式：
            - 在标记清扫基础上，将整个过程分批执行，已达到快速、实时目的
        4. 增量整理：
            - 在增量式基础上，添加对对象的内存整理
        5. 分代式：
            - 将对象根据存活时间的长短进行分类，根据分代假设对**年轻代**对象进行回收
            - 分代假设：
                - 如果一个对象存活时间不长则倾向于被回收
                - 如果一个对象已经存活很长时间则倾向于存活更长时间
            - 什么是分代：类似于70后、80后、90后
                - 新生代：存活时间小于某个值
                - 老年代：存活时间大于某个值
                - 永久代：永久不删除的对象
    2. 引用计数（每个对象自身包含一个被引用的计数器，计数器归零自动清理，存在缺陷，性能较低）
* 根对象、根集合的含义：
    - 它是垃圾回收器在标记过程时最先检查的对象，包括：
        1. 全局变量：程序在编译期就能确定的那些存在于程序整个生命周期的变量。
        2. goroutine 执行栈：每个 goroutine 都包含自己的执行栈，这些执行栈上包含栈上的变量及指向分配的goroutine
        3. 寄存器：寄存器的值可能表示一个指针，参与计算的这些指针可能指向某些赋值器分配的堆内存区块。
* Go的GC相关概念：
   - 三色标记清扫法（属于追踪式中的标记清扫，无分代，无整理）
        - 不整理的原因：
            - go使用tcmalloc，基本没有内存碎片问题，就算使用整理收益不高
            - 顺序内存分配器在go的多线程场景下并不适用
        - 不分代的原因：
            - go编译器有内存逃逸分析，可以将大部份年轻代对象存放在栈上，从而实现自动回收，并不需要通过gc；那些需要长期存在的对象才会被分配到需要进行垃圾回收的堆中。(即堆上的对象代际不明显，区分度不高)。
            - go的垃圾回收器与用户代码并发执行，使得STW的时间与对象的代际、对象的 size 没有关系
    - 三色抽象：
        - 一种描述追踪式回收器的方法，它的重要作用在于从逻辑上严密推导标记清理这种垃圾回收方法的正确性
        - 三色抽象规定的三种对象：
            - 白色对象（可能死亡）：
                - 未被回收器访问到的对象。
                - 在回收开始阶段，所有对象均为白色，当回收结束后，白色对象均不可达。
            - 灰色对象（波面）：
                - 正在被回收器访问到的对象。
                - 回收器需要对其中的一个或多个指针进行扫描，因为他们可能还指向白色对象。
            - 黑色对象（确定存活）：
                - 已被回收器访问到的对象，
                - 其中所有字段都已被扫描，黑色对象中任何一个指针都不可能直接指向白色对象。
    - 波面推进：
        - 对三色对象的回收过程其实是一个**波面**不断前进的过程。这个波面同时也是黑色对象和白色对象的边界，灰色对象就是这个波面。
        - 以灰色对象为波面，将黑色对象和白色对象分离，使波面不断向前推进，直到所有可达的灰色对象都变为黑色对象为止的过程。
          ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/53c95ad4fd4efeab51fee825eec022ba.png)
    - STW：
        - `Stop the World` or `Start the World`
        - STW在垃圾回收过程中：
            - 目的：为了保证实现的正确性、防止无止境的内存增长等问题
            - 手段：停止赋值器进一步操作对象图，即不允许赋值器修改对象的引用关系
            - 影响：在这个过程中整个用户代码被停止或者放缓执行，即goroutine会被暂停执行用户代码
        - 迭代优化：
            - 背景：Go1.14前，for循环内的goroutine不会中断，从而始终无法进入 STW 阶段。导致gc一直无法进行。
            - 优化：添加goroutine的异步抢占，使这类 goroutine能够被异步地抢占，使得STW 的时间不会超过抢占信号触发的周期
* Go并发标记清除：
    - 
    - 难点：**保证标记与清除过程的正确性**
        - 正确性的含义：
            - 不应出现对象的丢失
            - 不应错误的回收还不需要回收的对象
        - 不正确例子：![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/826ab9aff0dd5f0077ccdeef32bbd96f.png)
            当A成为波面时，又被C引用了，从而导致B没有被扫描到，最终B被错误回收
    - 如何破坏正确性：**同时满足以下条件**：
        * `条件1`: 赋值器修改对象图，导致**某一黑色对象引用白色对象**；
        * `条件2`: 从灰色对象出发，白色对象尚未被访问，而**访问路径被赋值器破坏**；
        - 结合上图进行解释：C引用了B并且，A到B的路径尚未被访问到。即白色对象再也无法从波面处访问，但是却被黑色对象又引用了。
    - 避免破坏正确性：**避免任一破环正确性的条件**
        * 避免`条件1`成立：白色对象只被灰色对象引用（阻断黑色对象引用白色）
        * 避免`条件2`成立：确保从灰色对象出发，总存在一条没有访问过的路径能到达白色对象（确保访问路径存在）
    - 强弱不变性：
        - 强三色不变性：同时避免的两个条件
        - 弱三色不变形：只满足避免条件2。即存在访问路径；允许黑色引用白色对象
    - 写屏障：
        - 指赋值器的写屏障，赋值器的写屏障是一种同步机制（通知的方式）
        - 目的：使赋值器在进行指针写操作时，能够“通知”回收器，达到不会破坏**弱三色不变性**的目的
        - 时机：所有写操作，即建立引用和解除引用时
        - 写屏障算法：
            - Dijkstra 插入屏障：
                - 避免`条件1`成立。
                - 具体做法：为了防止黑色对象指向白色对象，把对应的白色对象先变成灰色，然后在标记终止阶段STW时，重新扫描这些灰色对象。
                - 时机：所有写操作前
                - 对象：着色被引用者
                ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/7951eca316c22aebc3f3632a045a296d.png)

            - Yuasa 删除屏障：
                - 避免`条件2`成立
                - 具体做法：为了防止丢失从灰色对象到白色对象的路径，将变为黑色的对象再次变成灰色，即波面发生后退。
                - 时机：所有写操作后
                - 对象：着色引用者
                ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/ae454158ac349742cf7217c472eed8ba.png)
                - 优缺点：不需要标记结束阶段的重新扫描。但是因为会拦截写操作，从而导致波面的退后，产生“冗余”的扫描。

    - 混合写屏障：
        - go1.8，为了简化 GC 的流程，减少标记终止阶段的重扫成本。同时使用Dijkstra 插入屏障和Yuasa 删除屏障，称为混合写屏障。
        - 基本思想：**对正在被覆盖的对象进行着色（插入屏障），且如果当前线程的调用栈未扫描完成，则同样对指针进行着色（删除屏障）**
        - 缺点：无条件对引用双方进行着色。着色成本双倍，编译器插入的代码翻倍
    - 批量写屏障：引入缓存机制
        - go1.10 前后，实现了批量写屏障机制
        - 基本想法：**将需要着色的指针统一写入一个缓存，每当缓存满时统一对缓存中的所有指针进行着色**
* Go触发 GC 的时机：
    1. 主动：通过调用 runtime.GC
    2. 被动：
        1. 系统监控：当超过两分钟没有产生任何 GC 时，强制触发
        2. 步调算法（Pacing）：控制内存增长的比例
    - 内存分配过快：
        - GC触发后，会首先进入并发标记的阶段设置一个标志位enableMarkAssist。在goroutine分配内存时，走到mallocgc函数，暂停内存分配过快的goroutine去执行用户代码转而去做辅助标记的工作。
* GC的五个阶段：
    当前版本的 Go 以 STW 为界限，可以将 GC 划分为五个阶段：
    * STW期间，会停止用户代码的执行
    *   |阶段|说明|赋值器状态|
    | :-----: | :-----: | :-----: |
    | SweepTermination |清扫终止阶段，为下一个阶段的并发标记做准备工作，启动写屏障 |    STW     |
    |       Mark       | 并发标记阶段，与赋值器并发执行，写屏障开启            |    并发    |
    | MarkTermination  |标记结束阶段，保证一个周期内标记任务完成，停止写屏障    |    STW     |
    |      GCoff       |内存清扫阶段，将需要回收的内存归还到堆中，写屏障关闭    |    并发    |
    |      GCoff       |内存归还阶段，将过多的内存归还给操作系统，写屏障关闭    |    并发    |

- GC 关注的指标：
    - CPU利用率
    - 停顿时间
    - 停顿频率
    - 可扩展性
- GC调优：减少用户代码对 GC 产生的压力
    - 优化内存的申请速度，限制goroutine 的数量
    - 尽可能的少申请内存，按需申请
    - 复用已申请的内，sync.Pool复用需要的 buf
    - 调整GOGC参数（治标不治本）

### go协程、线程对比
* 内存开销： 2KB vs 2MB
* 创建、销毁开销：用户态 vs 内核态
* 切换开销： 保存3个寄存器 vs 保存16个寄存器

### go调度时机
|情形|说明|
|---|---|
|关键字 `go`|创建一个新的 goroutine，Go scheduler 会考虑调度|
|GC| 由于进行 GC 的 goroutine 也需要在 M 上运行，因此肯定会发生调度。当然，Go scheduler 还会做很多其他的调度，例如调度不涉及堆访问的 goroutine 来运行。|
|系统调用|当 g1 进行系统调用时，会阻塞对应的m1，g1会绑定到m1上，g1对应的p1会从m1解绑，重新找一个空闲的m2，或者新建一个m3，然后从LRQ获取g2运行；当g1的系统调用完成重新变成可运行态，会被放到全局运行队列或者原来的p1的本地运行队列，等待调度的发生|
|内存同步访问|同系统调用类似，atomic，mutex，channel 操作会阻塞goroutine|

### go runtime、program、os kernel的关系
![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/48bd79bfd4ffca1fc578a6698cf9acf0.png)
* runtime有点类似用户跟系统交互的中间代理
* runtime维护所有的 goroutines，通过scheduler来进行调度
* scheduler 相关结构体组成：
    * `g` 代表一个 goroutine，它包含：goroutine栈的一些字段，当前 goroutine 的状态，当前运行到的指令地址
    * `m` 表示内核线程，包含正在运行的 goroutine 等字段
    * `p` 代表一个虚拟的 Processor，它维护一个处于Runnable状态的 g 队列（本地可运行队列LRQ）和一个M，是连接Goroutine和线程的桥梁
    * `sched` 总览全局
### GPM
* GPM状态机：
    ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/ee5b938c62f75a47aae6c7400f0358f7.png)
    * G状态机：
        ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/7718933e3b9eef5324dcfec3ac53aa2b.png)
    * P状态机：
        ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/c1c6bafe989c43be7b23e474d0668f24.png)
    * M状态机：
        ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/a11695f322399e06a43b359adc2e4148.png)

* GPM完整流程图：
    ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/341ae661ef2b4867952a913a4681448f.png)
    1、 GPM 的调度流程从 go func()开始创建一个 goroutine,新建的G优先放入P的本地队列保存待执行的 goroutine（流程 2），当 M 绑定的 P 的的局部队列已经满了之后就会把 goroutine 放到全局队列（流 程 2-1）
    2、每个 P 和一个 M 绑定，M 是真正的执行 P 中 goroutine 的实体（流程 3）， M 从绑定的 P 中的局部队列获取 G 来执行
    3、当 M 绑定的 P 的局部队列为空时，M 会从全局队列获取到本地队列来执行 G （流程 3.1），当从全局队列中没有获取到可执行的 G 时候，M 会从其他 P 的局部队列中偷取 G 来执行（流程 3.2），这种从其他 P 偷的方式称为 work stealing
    4、一个M调度G执行的过程是一个循环机制
    5、 当 G 因系统调用（syscall）阻塞时会阻塞 M，此时 P 会和 M 解绑即 hand off，并寻找新的空闲的 M，若没有空闲的 M 就会新建一个 M（流程 5.1）
    6、当 G <span style="color: rgb(255, 76, 0);">因 channel 或者 network I/O 阻塞时，不会阻塞 M，M 会寻找其他的 G</span>；当阻塞的 G 恢复后会重新进入 runnable 进入 P 队列等待执 行（流程 5.3）
    7、 当M系统调用结束时候，这个G会尝试获取一个空闲的P执行，并放入到这个P的本地队列。如果获取不到P，则将G放入全局队列，等待被其他的P调度。然后M将进入缓存池睡眠。

* GMP调度过程中存在哪些阻塞：
    - I/O，select
    - syscall
    - channel
    - 等待锁
    - runtime.Gosched()
* GMP调度出现阻塞时：
    * 阻塞的原因是同步的（如系统调用或锁操作），对应的M会阻塞
    * 阻塞的原因是异步的（如网络I/O或通道操作），对应的M不会阻塞

* M:N模型：
    * N个go routine通过若干个P依附在M个线程（M）上

* 工作窃取：
    * 当前P的LRQ空了后，会从其他P偷取一半的G




### 函数栈、调用栈、运行栈
* 调用栈=运行栈
* 调用栈由若干个有调用关系的函数栈组成
* 函数栈用栈结构存储函数的局部变量、参数和返回地址等信息

### 栈内存和栈空间
* 栈 Stack用来描述一种"后进先出"（LIFO）的数据结构
* 栈内存是指计算机内存中的一块特殊区域，它由操作系统在程序启动时分配
* 栈空间是指为goroutine分配的用于存储函数调用栈的内存区域，函数返回内存会被释放
* 栈空间大多数都是位于栈内存中的
* 在Go语言中，goroutine的栈空间可能会被分配在堆内存中。物理位置上位于堆内存，但逻辑结构符合栈的特性，因此仍然称之为栈空间

### sysmon：
* sysmon运行在独立的线程上，不依赖P、M，进行无限循环
* sysmon的作用：
    * 长时间（2min）未发生gc，强制执行gc
    * 获取fd事件？？
    * 抢占，回收系统调用中的G对应的P，抢占长时间（10ms）运行的P
    * 释放自由列表中多余的项减少内存占用
