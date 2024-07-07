    * 队列 queue ： 一种FIFO 的List
定义：只允许在一端进行插入操作，另一端进行删除操作的线性表。
* ADT Queue
    * Data：
同线性表，元素具有相同类型，相邻元素具有前驱和后继关系。
    * Operation：InitQueue （*Q）
    * DestroyQueue （*Q）
    * ClearQueue （*Q）
    * QueueEmpty （Q）
    * GetHead （Q,*e）
    * EnQueue (*Q,e)
    * DeQueue (*Q,e)
    * QueueLength (Q)
* end ADT
        * 顺序存储：数据存储结构
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/4210c57ea0b9781efdb48755936a77ab.png)

        * 循环队列定义：队列的头尾相接的顺序存储结构
            * 顺序存储结构：
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/4210c57ea0b9781efdb48755936a77ab.png)

            * 图解：
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/91a544a9d7d5fe99e3db1c3ef9f13b54.png)

        * 链式存储数据存储结构：
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/e0ee709eeab6c7c9ba83921db9fa7202.png)

        * 图解：
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/71aba9b42642ccb779cfbc015afc6a14.png)

