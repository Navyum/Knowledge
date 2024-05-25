    * 红黑树和AVL树类似，都是在进行插入和删除操作时通过特定操作保持二叉查找树的平衡，从而获得较高的查找性能。
    * 在O(log n)时间内做查找，插入和删除，这里的n 是树中元素的数目。
    * 高度为2 lg(n)。
    * 性质：节点是红色或黑色。
    * 根节点是黑色。
    * 每个叶节点（NIL节点，空节点）是黑色的。
    * 每个红色节点的两个子节点都是黑色。(从每个叶子到根的所有路径上不能有两个连续的红色节点)。
    * 从任一节点到其每个叶子的所有路径都包含相同数目的黑色节点。
    * 用途：
时间敏感的应用，在最坏情况担保效率。
* * Node类定义：
    * classRBNode {
    * private:
    * intdata_;
    * SmartNodePtr left_;
    * SmartNodePtr right_;
    * SmartNodePtr parent_;
    * enumColor color_;
    * ...
    * };
* * 
    * 插入操作：如果是一个None的树，我们直接创建一个根节点，并且颜色为黑色
    * 所有插入的新的节点，颜色都是红色的
    * 如果插入节点后，插入节点的父节点是黑色，完成插入
        * 如果插入节点后，插入的节点的父节点红色 ，则分两种情况如果父亲节点的兄弟也是红色，都改为黑色，祖父节点改为红色，将祖父节点当做新节点并跳回第三步
        * 如果这个红色父节点没有同级的兄弟姐妹，或者兄弟是黑色，则需要重新考虑当前节点、父节点、祖父节点的排列位置（旋转）。
            * 旋转规则：（右旋——自己变为左孩子的右孩子；左旋——自己变为右孩子的左孩子。）LL-L
            * RL-RL
            * RR-R
            * LR-LR
            * (父节点)(插入节点)-([父节点]祖父节点旋转方向)
* 删除操作：
* [https://blog.csdn.net/lm2009200/article/details/70162811](https://blog.csdn.net/lm2009200/article/details/70162811)
* [https://zhuanlan.zhihu.com/p/25402654](https://zhuanlan.zhihu.com/p/25402654)
* * [http://www.503error.com/2017/%E7%BA%A2%E9%BB%91%E4%BA%8C%E5%8F%89%E6%A0%91%E7%9A%84%E6%8F%92%E5%85%A5%E4%B8%8E%E6%97%8B%E8%BD%AC/1338.html](http://www.503error.com/2017/%E7%BA%A2%E9%BB%91%E4%BA%8C%E5%8F%89%E6%A0%91%E7%9A%84%E6%8F%92%E5%85%A5%E4%B8%8E%E6%97%8B%E8%BD%AC/1338.html)
* [https://blog.csdn.net/sinat_30071459/article/details/50858310](https://blog.csdn.net/sinat_30071459/article/details/50858310)
* * 在线演示：
* [http://sandbox.runjs.cn/show/2nngvn8w](http://sandbox.runjs.cn/show/2nngvn8w)
