

树 Tree

定义：

树是n个节点的有限集，n=0时为空树，

非空树：

1.有且仅有一个root根节点

2.n>1时，其余节点可分为m个互不相交的有限集，每个集合也是一个树，称为子树

相关概念：

层次：节点所在行号，根为1

树的深度：最大叶子节点的所属层次

节点的度：该节点的分支个数，二叉树（0～2）

ADT：


![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/0c1d6fca3be67763260ea6453ca58925.png)


数据结构：


![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/e8180d0918ea605aa71b089543ec47a6.png)
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/af0fab9904c983df786b7dbb22431929.png)


root的parent设为-1


孩子表示法（孩子数量不确定）：类似哈希表


![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/55d0ddf61eed395fdbf62cb35efcf304.png)


包括孩子节点，表头，树结构


![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/faf14ddbfe8d7d3fc505ec51afd841d9.png)
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/3a7dab9a6e223189092dba03adaa499e.png)


孩子兄弟表示法：（二叉树）


![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/4092e54e2115e76227d371528d76ae64.png)


节点：


![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/51642efd4b4ebcdbc86766dc363f8615.png)


