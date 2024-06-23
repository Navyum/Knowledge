    * 含义：
由顶点的有穷非空集合和顶点之间的边的集合组成，表示为G（V,E）G为图，V是顶点集合，E是边的集合
    * 概念：顶点：图中数据元素
    * 无向边：顶点v1到顶点v2之间的边没有方向，则为无向边，用无序偶对（v1，v2）表示
    * 有向边：顶点v1到顶点v2之间的边有方向，则为有向边，用有序偶对<v1,v2> 表示
        * ADT GraphData：
顶点有穷非空集合和边的集合
        * Operation：CreateGraph(*G，V,VR)按照顶点集V和边弧集VR定义构造图G
        * DestroyGraph（*G)
        * LocateVex(G,u) 返回顶点u位置
        * GetVex（G，V）
        * PutVex(G,V,value）
        * FirstAdjVex（G，*v）返回顶点v的一个相邻顶点
        * NextAdjVex（G，v，*w）返回顶点v相对顶点w的下一个相邻顶点
        * InsertVex（*G，v）在图G中添加新顶点v
        * DeleteVex（*G，v）删除顶点v和相关弧
        * InsertArc（*G，v，w）在图G中添加弧(v,w)
        * DeleteArc(*G,v,w)删除弧（v，w）
        * DFSTraverse（G）深度优先遍历
        * HFSTaverse（G）广度优先遍历
* end ADT
*     * 数据存储结构：邻接矩阵（顺序存储）
    * ![图片](./IMG/图%20graph.md/fe1afde6.png)

        * 图解：
![图片](./IMG/图%20graph.md/8ecd781f.png)

        * 邻接表：（链式存储）![图片](./IMG/图%20graph.md/da3949f2.png)

            * 图解：（无向图）
![图片](./IMG/图%20graph.md/f43aae96.png)

    * 最小生成树：含义：构造连通网的最小代价生成树称为最小生成树
            * 构造算法：1.Prim算法
...
            * 2.Kruskal算法
...
    * 最短路径：含义：两个定点之间经过的边上权值之和最少的路径，第一个顶点叫做源点，最后一个顶点叫终点
            * 算法：1.Dijkstra算法：
...
            * 2.Floyd算法：
...
    * 拓扑排序：含义：对有向图构造拓扑序列的过程。
        * 概念：
拓扑序列：设G=(V,E)是一个具有n个顶点的有向图，V中的顶点序列v1，v2 ... vn 满足若从vi到vj有一条路径，则在顶点序列中顶点vi必须在顶点vj之前，则这样的顶点序列叫拓扑序列。
        * 算法：
拓扑排序算法
    * 最短路径：含义：从源点到汇点具有最大长度的路径叫做关键路径
        * 算法：
关键路径算法：
