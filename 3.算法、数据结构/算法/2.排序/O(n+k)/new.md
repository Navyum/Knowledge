# new
* <span style="color: rgb(255, 41, 65);"> 非比较排序算法 </span>
* 算法流程：条件 一个长度为 $n$ 的数组，其元素是范围 $[0, 1)$ 内的浮点数
    1. 初始化 $k$ 个桶，将 $n$ 个元素分配到 $k$ 个桶中。
    2. 对每个桶分别执行排序（这里采用编程语言的内置排序函数）。
    3. 按照桶从小到大的顺序合并结果。
* 桶排序的优化：
    * 将元素均匀分配到各个桶中，时间复杂度趋近于$O(n)。可以借助值的概率分布。
    ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/9b5e1ed580a44cb933621d58303cc112.png)

* 图解：
![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/e071c5a7c5c6f087fb9dc231bda365b9.png)