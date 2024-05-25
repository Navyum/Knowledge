* 含义：串是由零个或多个字符组成的有限序列。
* ADT String
    * Data:
元素仅由一个字符组成，相邻元素具有前驱和后继关系
    * Operation：StrAssign (T，*chars)         生成值为字符串常量chars的串T
    * Strcopy（T，S）
    * ClearString（S）
    * IsEmpty（S）
    * Strlen（S）
    * StrCompare（S,T）             S>T, return >0;S=T,return 0； S<T,return <0；
    * StrCat(T,S1,S2)
    * SubString(Sub ,S,pos,len)   pos =[1,Strlen(S)],len=[0,Strlen(S)+1-pos],Sub 返回pos开始的长度为len的子串。
    * Index（S,Sub,pos）             若S中存在pos位置之后的Sub子串，则返回第一次出现的位置
    * Replace（S,Sub,T）              用T代替S中的所有Sub子串
    * StrInsert（S，pos，T）        在S的pos位置插入T
    * StrDelete（S,pos，len）      在S的pos位置删除长度为len的子串
* edn ADT
*     * 查找子串：朴素模式匹配算法：
    * KMP模式匹配算法：
