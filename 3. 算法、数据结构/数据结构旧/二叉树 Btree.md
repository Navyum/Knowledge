    * 定义：
二叉树是每个结点最多有两个子树的树结构。
    * 性质：二叉树第i层上的结点数目最多为2^i-1(i>=1)
    * 深度为k的二叉树至多有2^k-1个结点（k>=1）  (2^0+2^1...+2^(K-1) )
    * 包含n个结点的二叉树的高度至少为(log2^n)+1
    * 在任意一棵二叉树中，若叶子节点的个数为n0，度为2的结点数为n2，则n0=n2+1
        * 分类：完全二叉树: 若设二叉树的深度为h    1）除第 h 层外，其它各层的结点数都达到最大个数   2）第 h 层所有的结点都连续集中在最左边。
            * 特点：度为1的节点为0或1个，即n1=（0，1）
            * 叶子节点数计算： n为偶数 n/2   或   n为奇数（n+1）/2 
        * 满二叉树:
 高度为h，并且由2h-1个结点组成的二叉树，称为满二叉树
* ![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/9dd71d42ed87350d1096b52461aeb64c.png)

    * 顺序存储：同线性表顺序存储（一般用于完全二叉树）
        * 图解：
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/c9e425d48a7b4deebf255747bf6672f4.png)

            * 链式存储：
二叉链表:
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/b80b9c89f7fe0262c8715980b11b621e.png)

    * 二叉树遍历：从根节点出发，按照某次序访问二叉树的所有节点，使得节点被访问且仅被访问一次。遍历针对根节点的访问次序而言，依次从上到下，从左到右遍历。
        * 1.前序遍历：先访问根节点，然后前序遍历左子树，再前序遍历右子树。
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/2b01450b62704ea00b5d470dda29641b.png)

        * 2.中序遍历：中序遍历根节点左子树，在访问根节点，最后中序遍历右子树
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/11e3bc827767467302198aabb67de35d.png)

        * 3.后序遍历：从左到右先遍历叶子节点，最后访问根节点。
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/68b01a3f0559be5bfc76f8601c237b93.png)

    * 4.层序遍历：从根节点出发，从上而下逐层遍历，同一层从左到右遍历
    * 已知前序遍历顺序 + 后续遍历顺序 无法唯一确定二叉树
* 线索二叉树：
    * 含义：
孩子节点为空时，指向其前驱或者后驱节点的树
    * 背景：
由于二叉链表浪费很多空指针。
    * 优点：
线索二叉树方便查询某个节点的前驱和后继，而不用每次遍历。
* 用rtag，ltag记录孩子节点是否为空![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/df2288ac71ce4e99d77b809da8d92b05.png)

    * 树转化为二叉树：兄弟连接代替父子连接
将兄弟节点建立连接，将每个节点的第一个孩子节点保留，与其他孩子节点的连接都去除（兄弟连接当作二叉树的右节点）
    * 森林转化为二叉树:森林的每棵树都是兄弟
将每棵树转化为二叉树，将后一棵树作为兄弟连接起来（兄弟连接当作二叉树右节点）
    * 赫夫曼树：
![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/fb4b5ee0474ed176bf410eb437168a6f.png)

    * 赫夫曼编码：字母频率：A 27,B 8 ,C 15 ,D 15, E 30,F 5![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/8161ae957c1ad5034f21491f7dc94104.png)

    * ![图片](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/871e67cf878a31c9318a92b6018703fd.png)

