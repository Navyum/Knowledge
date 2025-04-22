---
title: Systemtap-Language-Reference中文版
date: 2025-04-14 18:57:08
author: Navyum
tags: 
 - systemtap手册、Systemtap手册、SystemTap中文版、systemTap中文版、SystemTap语法
categories: 
 - 英文翻译
---

# SystemTap 语言参考手册-中文版
----
本文为[《Systemtap-Language-Reference》](https://sourceware.org/systemtap/langref.pdf)中文版翻译，仅供学习参考使用，如有翻译错误，请及时联系作者[Navyum](https://github.com/Navyum/Navyum)更新修正。

原文最终修改时间：2024年11月8日

----

本文档源自Red Hat、IBM和Intel的员工为SystemTap项目贡献的其他文档。
版权所有© 2007 - 2013 Red Hat Inc.
版权所有© 2007 - 2009 IBM Corp.
版权所有© 2007 Intel Corporation。

在遵循GNU自由文档许可证1.2版或自由软件基金会发布的任何更高版本的条款下，允许复制、分发和/或修改本文档；但不包含不变章节、封面文字和封底文字。
GNU自由文档许可证可从[http://www.gnu.org/licenses/fdl.html](http://www.gnu.org/licenses/fdl.html)获取，或写信至美国马萨诸塞州波士顿市富兰克林街51号，五楼，自由软件基金会，邮编02110 - 1301。


## 目录
----
1. [SystemTap概述 8](#1.-SystemTap概述)
    * 1.1 [关于本指南 8](#1.1-关于本指南)
    * 1.2 [使用SystemTap的原因 8](#1.2-使用SystemTap的原因)
    * 1.3 [事件 - 动作语言 8](#1.3-事件---动作语言)
    * 1.4 [示例SystemTap脚本 8](#1.4-示例SystemTap脚本)
        * 1.4.1 [基本SystemTap语法和控制结构 8](#1.4.1-基本SystemTap语法和控制结构)
        * 1.4.2 [0到49之间的质数 9](#1.4.2-0到49之间的质数)
        * 1.4.3 [递归函数 10](#1.4.3-递归函数)
    * 1.5 [stap命令 11](#1.5-stap命令)
    * 1.6 [安全性 11](#1.6-安全性)
2. [SystemTap脚本的类型 12](#2.-SystemTap脚本的类型)
    * 2.1 [探测脚本 12](#2.1-探测脚本)
    * 2.2 [插件集脚本 12](#2.2-插件集脚本)
3. [SystemTap脚本的组件 12](#3.-SystemTap脚本的组件)
    * 3.1 [探测定义 13](#3.1-探测定义)
    * 3.2 [探测别名 13](#3.2-探测别名)
        * 3.2.1 [序言式别名(=) 14](#3.2.1-序言式别名%28=%29)
        * 3.2.2 [结语式别名(+=) 14](#3.2.2-结语式别名%28+=%29)
        * 3.2.3 [探测别名的用法 14](#3.2.3-探测别名的用法)
        * 3.2.4 [别名后缀 14](#3.2.4-别名后缀)
        * 3.2.5 [别名后缀和通配符 15](#3.2.5-别名后缀和通配符)
    * 3.3 [变量 15](#3.3-变量)
        * 3.3.1 [未使用的变量 16](#3.3.1-未使用的变量)
    * 3.4 [辅助函数 16](#3.4-辅助函数)
    * 3.5 [嵌入式C 18](#3.5-嵌入式C)
    * 3.6 [嵌入式C函数 18](#3.6-嵌入式C函数)
    * 3.7 [嵌入式C编译指示注释 19](#3.7-嵌入式C编译指示注释)
    * 3.8 [访问脚本级全局变量 20](#3.8-访问脚本级全局变量)
4. [探测点 21](#4.-探测点)
    * 4.1 [通用语法 21](#4.1-通用语法)
        * 4.1.1 [前缀 21](#4.1.1-前缀)
        * 4.1.2 [后缀 21](#4.1.2-后缀)
        * 4.1.3 [通配文件名、函数名 21](#4.1.3-通配文件名、函数名)
        * 4.1.4 [可选探测点 21](#4.1.4-可选探测点)
        * 4.1.5 [大括号展开 22](#4.1.5-大括号展开)
    * 4.2 [内置探测点类型（DWARF探测） 22](#4.2-内置探测点类型（DWARF探测）)
        * 4.2.1 [kernel.function, module().function 24](#4.2.1-kernel.function,-module%28%29.function)
    * 4.3 [函数返回探测 25](#4.3-函数返回探测)
    * 4.2.2 [kernel.statement, module().statement 25](#4.2.2-kernel.statement,-module%28%29.statement)
    * 4.4 [无DWARF探测 25](#4.4-无DWARF探测)
    * 4.5 [用户空间探测 25](#4.5-用户空间探测)
        * 4.5.1 [开始/结束变体 26](#4.5.1-开始/结束变体)
        * 4.5.2 [系统调用变体 27](#4.5.2-系统调用变体)
        * 4.5.5 [进程探测路径 28](#4.5.3-函数/语句变体)
        * 4.5.3 [函数/语句变体 27](#4.5.3-函数/语句变体)
        * 4.5.4 [绝对变体 27](#4.5.4-绝对变体)
        * 4.5.6 [目标进程模式 28](#4.5.6-目标进程模式)
        * 4.5.7 [静态用户空间探测 29](#4.5.7-静态用户空间探测)
    * 4.6 [Java探测 29](#4.6-Java探测)
    * 4.7 [PROCFS探测 30](#4.7-PROCFS探针)
    * 4.8 [标记探测 31](#4.8-标记探针)
    * 4.9 [跟踪点 31](#4.9-跟踪点)
    * 4.10 [系统调用探测 31](#4.10-系统调用探针)
    * 4.11 [定时器探测 32](#4.11-定时器探针)
    * 4.12 [特殊探测点 33](#4.12-特殊探针点)
        * 4.12.1 [begin 33](#4.12.1-begin)
        * 4.12.2 [end 33](#4.12.2-end)
        * 4.12.3 [error 33](#4.12.3-error)
        * 4.12.4 [begin、end和error探测序列 34](#4.12.4-begin、end和error探针序列)
        * 4.12.5 [never 34](#4.12.5-never)
5. [语言元素 34](#5-语言元素)
    * 5.1 [标识符 34](#5.1-标识符)
    * 5.2 [数据类型 34](#5.2-数据类型)
        * 5.2.1 [字面量 34](#5.2.1-字面量)
        * 5.2.2 [整数 35](#5.2.2-整数)
        * 5.2.3 [字符串 35](#5.2.3-字符串)
        * 5.2.4 [关联数组 35](#5.2.4-关联数组)
        * 5.2.5 [统计信息 35](#5.2.5-统计信息)
    * 5.3 [分号 35](#5.3-分号)
    * 5.4 [注释](#5.4-注释)
    * 5.5 [空白字符 36](#5.5-空白字符)
    * 5.6 [表达式 36](#5.6-表达式)
        * 5.6.1 [二元数值运算符 36](#5.6.1-二元数值运算符)
        * 5.6.2 [二元字符串运算符 36](#5.6.2-二元字符串运算符)
        * 5.6.3 [数值赋值运算符 36](#5.6.3-数值赋值运算符)
        * 5.6.4 [字符串赋值运算符 36](#5.6.4-字符串赋值运算符)
        * 5.6.5 [一元数值运算符 36](#5.6.5-一元数值运算符)
        * 5.6.6 [数值与字符串比较、正则表达式匹配运算符 36](#5.6.6-数值和字符串比较、正则表达式匹配运算符)
        * 5.6.7 [三元运算符 37](#5.6.7-三元运算符)
        * 5.6.8 [分组运算符 37](#5.6.8-分组运算符)
        * 5.6.9 [函数调用 37](#5.6.9-函数调用)
        * 5.6.10 [\$ptr->member 37](#5.6.10-`$ptr->member`)
        * 5.6.11 [指针类型转换 37](#5.6.11-指针类型转换)
        * 5.6.12 [\<value\> in \<array - name\> 38](#5.6.12-`<value>-in-<array-name>`)
        * 5.6.13 [\<value\>, ... in \<array - name\> 38](#5.6.13-`[-<value>,-...-]-in-<array-name>`)
    * 5.7 [从stap命令行传入的字面量 38](#5.7-从stap命令行传入的字面量)
        * 5.7.1 [\$1...\$\<NN\>用于字面量粘贴 38](#5.7.1-`$1...$<NN>`用于字面量粘贴)
        * 5.7.2 [\@1...\@\<NN\>用于字符串 38](#5.7.2-`@1...@<NN>`用于字符串)
        * 5.7.3 [示例 38](#5.7.3-示例)
    * 5.8 [条件编译 39](#5.8-条件编译)
        * 5.8.1 [条件 39](#5.8.1-条件)
        * 5.8.2 [基于可用目标变量的条件 39](#5.8.2-基于可用目标变量的条件)
        * 5.8.3 [基于内核版本的条件：kernel v, kernel vr 39](#5.8.3-基于内核版本的条件：`kernel-v`、`kernel-vr`)
        * 5.8.4 [基于架构的条件：arch 39](#5.8.4-基于架构的条件：`arch`)
        * 5.8.5 [基于权限级别的条件：systemtap privilege 40](#5.8.5-基于特权级别的条件：`systemtap-privilege`)
        * 5.8.6 [真和假标记 40](#5.8.6-真和假标记)
    * 5.9 [预处理器宏 40](#5.9-预处理器宏)
        * 5.9.1 [局部宏 40](#5.9.1-局部宏)
        * 5.9.2 [库宏 41](#5.9.2-库宏)
6. [语句类型 41](#6-语句类型)
    * 6.1 [break和continue 42](#6.1-break和continue)
    * 6.2 [try/catch 42](#6.2-try/catch)
    * 6.3 [delete 42](#6.3-delete)
    * 6.4 [EXP(expression) 42](#6.4-EXP-%28expression%29)
    * 6.5 [for 43](#6.5-for)
    * 6.6 [foreach 43](#6.6-foreach)
    * 6.7 [if 43](#6.7-if语句)
    * 6.8 [next 44](#6.8-next语句)
    * 6.9 [;(空语句) 44](#6.9-;（空语句）)
    * 6.10 [return 44](#6.10-return语句)
    * 6.11 [{}(语句块) 44](#6.11-{}（语句块）)
    * 6.12 [while 44](#6.12-while语句)
7. [关联数组 45](#7-关联数组)
    * 7.1 [示例 45](#7.1-示例)
    * 7.2 [值的类型 45](#7.2-值的类型)
    * 7.3 [数组容量 45](#7.3-数组容量)
    * 7.4 [数组环绕 45](#7.4-数组合并)
    * 7.5 [迭代，foreach 46](#7.5-迭代，foreach)
    * 7.6 [删除 46](#7.6-删除)
8. [统计信息（聚合） 46](#8-统计信息（聚合）)
    * 8.1 [聚合(<<<)运算符 47](#8.1-聚合（<<<）操作符)
    * 8.2 [提取函数 47](#8.2-提取函数)
    * 8.3 [整数提取器 47](#8.3-整数提取器)
        * 8.3.1 [@count(s) 47](#8.3.1-@count%28s%29)
        * 8.3.2 [@sum(s) 47](#8.3.2-@sum%28s%29)
        * 8.3.3 [@min(s) 47](#8.3.3-@min%28s%29)
        * 8.3.4 [@max(s) 47](#8.3.4-@max%28s%29)
        * 8.3.5 [@avg(s) 47](#8.3.5-@avg%28s%29)
    * 8.4 [直方图提取器 48](#8.4-直方图提取器)
        * 8.4.1 [@hist_linear 48](#8.4.1-@hist_linear)
        * 8.4.2 [@hist_log 49](#8.4.2-@hist_log)
    * 8.5 [删除 49](#8.5-删除)
9. [格式化输出 49](#9-格式化输出)
    * 9.1 [print 49](#9.1-print)
    * 9.2 [printf 50](#9.2-printf)
    * 9.3 [printd 52](#9.3-printd)
    * 9.4 [printdln 53](#9.4-printdln)
    * 9.5 [println 53](#9.5-println)
    * 9.6 [sprint 53](#9.6-sprint)
    * 9.7 [sprintf 53](#9.7-sprintf)
10. [插件集定义的函数 53](#10-Tapset定义的函数)
11. [进一步参考](#11-更多参考信息)


## 1. SystemTap概述
----

### 1.1 关于本指南
本指南全面介绍了SystemTap的语言结构和语法。其内容大量借鉴了手册页和教程中现有的SystemTap文档，为读者提供了一个查找语言语法和推荐用法的集中资源。为了更好地使用本指南，您应熟悉SystemTap的基本原理和操作。如果您是SystemTap的新手，教程是很好的入门资料。有关插件集的详细信息，请查看发行版提供的手册页。有关SystemTap参考资料的完整集合，请参见第11节。

### 1.2 使用SystemTap的原因
SystemTap提供了简化收集运行中Linux内核信息的基础架构，便于进一步分析。这种分析有助于找出性能或功能问题的根本原因。SystemTap旨在避免开发人员为收集这类数据而进行繁琐的插桩、重新编译、安装和重启操作。为此，它提供了一个简单的命令行界面和脚本语言，用于为内核和用户空间编写探测程序。借助SystemTap，开发人员、系统管理员和用户可以轻松编写脚本，收集和处理标准Linux工具无法获取的系统数据，相较于旧方法有显著改进。

### 1.3 事件 - 动作语言
SystemTap的语言是强类型、无声明的过程式语言，受dtrace和awk的启发。内核中的源代码点或事件与处理程序相关联，处理程序是同步执行的子例程。这些探测在概念上类似于GDB调试器中的“断点命令列表”。

SystemTap主要有两种最外层结构：探测（probes）和函数（functions）。在这些结构中，语句和表达式使用类似C语言的操作符语法和优先级。

### 1.4 示例SystemTap脚本
以下是一些示例脚本，展示了SystemTap的基本操作。更多示例可查看源目录中的examples/small demos/目录、SystemTap维基页面（http://sourceware.org/systemtap/wiki/HomePage）或SystemTap实战故事页面（http://sourceware.org/systemtap/wiki/WarStories）。

#### 1.4.1 基本SystemTap语法和控制结构
以下代码示例展示了SystemTap的语法和控制结构。
```bash
global odds, evens
probe begin { 
    # "no"和"ne"是局部整数
    for (i = 0; i < 10; i++) { 
        if (i % 2) odds[no++] = i;
        else evens[ne++] = i;
    }
    delete odds[2];
    delete evens[3];
}
exit()
probe end {
    foreach (x+ in odds) printf("odds[%d] = %d", x, odds[x]);
    foreach (x in evens-) printf("evens[%d] = %d", x, evens[x]);
}
```
这段代码的输出结果为：
```log
odds[0] = 1 
odds[1] = 3
odds[3] = 7
odds[4] = 9
evens[4] = 8
evens[2] = 4 
evens[1] = 2
evens[0] = 0
```
注意，所有变量类型都是自动推断的，并且所有局部变量和全局变量都会被初始化。整数初始化为0，字符串初始化为空字符串。

#### 1.4.2 0到49之间的质数
```bash
function isprime (x) { 
    if (x < 2) return 0;
    for (i = 2; i < x; i++) { 
        if (x % i == 0) return 0;
        if (i * i > x) break;
    }
    return 1;
}
probe begin { 
    for (i = 0; i < 50; i++)
        if (isprime (i)) printf("%d\n", i);
    exit()
}
```
这段代码的输出结果为：
```
2 
3 
5 
7
11
13
17
19
23
29
31
37
41
43
47
```

#### 1.4.3 递归函数
```bash
function fibonacci(i) { 
    if (i < 1) error("bad number");
    if (i == 1) return 1;
    if (i == 2) return 2;
    return fibonacci (i-1) + fibonacci (i-2);
}
probe begin { 
    printf("11th fibonacci number: %d", fibonacci (11));
    exit ()
}
```

这段代码的输出结果为：
```log
11th fibonacci number: 118
```
如果向该函数输入更大的数字，可能会超过MAXACTION或MAXNESTING限制，运行时会捕获这些错误。有关限制的更多信息，请参见1.6节。

### 1.5 stap命令
stap程序是SystemTap工具的前端。它接受用其脚本语言编写的探测指令，将这些指令转换为C代码，编译该C代码，并将生成的内核模块加载到运行的Linux内核中，以执行所需的系统跟踪或探测功能。您可以通过命名文件、标准输入或命令行提供脚本。SystemTap脚本会一直运行，直到出现以下情况之一：
- 用户使用CTRL - C中断脚本。
- 脚本执行exit()函数。
- 脚本遇到足够数量的软错误。
- 使用stap程序的 - c选项启动的被监控命令退出。

stap命令执行以下操作：
- 转换脚本
- 生成并编译内核模块
- 插入模块；输出到stap的标准输出
- CTRL - C卸载模块并终止stap

有关stap命令的完整选项列表，请查看stap(1)手册页。

### 1.6 安全性
SystemTap是一个管理工具，它会暴露内核内部数据结构和潜在的用户私有信息。运行它所构建的内核对象需要root权限，可通过对staprun程序使用sudo命令来实现。

staprun是SystemTap软件包的一部分，用于模块的加载和卸载以及内核与用户之间的数据传输。由于staprun不会对其接收的内核对象进行额外的安全检查，因此不要通过sudo为不可信用户授予提升的权限。

翻译器会强制执行某些安全约束，确保任何处理程序例程都不会运行过长时间、分配内存、执行不安全操作或无意干扰内核。脚本全局变量的使用受到锁定保护，以防止并发探测处理程序的操作。使用如嵌入式C（见3.5节）这样的guru模式结构可能会违反这些约束，导致内核崩溃或数据损坏。

资源使用限制由生成的C代码中的宏设置，可使用 - D标志覆盖这些限制。以下是部分宏的说明：
- MAXNESTING：递归函数调用的最大层数，默认值为10。
- MAXSTRINGLEN：字符串的最大长度。32位机器默认值为256字节，其他机器为512字节。
- MAXTRYLOCK：在声明可能发生死锁并跳过探测之前，等待全局变量锁的最大迭代次数，默认值为1000。
- MAXACTION：在单个探测命中期间执行的最大语句数，默认值为1000。
- MAXMAPENTRIES：如果在声明数组时未明确指定数组大小，数组的最大行数，默认值为2048。
- MAXERRORS：触发退出前的最大软错误数，默认值为0。
- MAXSKIPPED：触发退出前跳过的最大可重入探测数，默认值为100。
- MINSTACKSPACE：运行探测处理程序所需的最小空闲内核栈字节数。该数值应足够满足探测处理程序自身的需求，并加上一定的安全余量，默认值为1024。

如果在探测开始运行后stap或staprun出现问题，可以安全地终止这两个用户进程，并使用rmmod命令删除活动的探测内核模块，但可能会丢失一些待处理的跟踪消息。


## 2. SystemTap脚本的类型
----

### 2.1 探测脚本
探测脚本类似于程序，用于识别探测点和相关的处理程序。

### 2.2 插件集脚本
插件集脚本是探测别名和辅助函数的库。/usr/share/systemtap/tapset目录包含插件集脚本，虽然这些脚本看起来像常规的SystemTap脚本，但不能直接运行。


## 3. SystemTap脚本的组件
----

脚本语言中的主要结构是识别探测（probes）。探测将抽象事件与一个语句块（即探测处理程序）关联起来，当这些事件中的任何一个发生时，就会执行该语句块。

以下示例展示了如何使用两个探测来跟踪函数的进入和退出：
```bash
probe kernel.function("sys_mkdir").call { log("enter") } 
probe kernel.function("sys_mkdir").return { log("exit") }
```
要列出内核中可探测的函数，可以使用列表选项（`-l`）。例如：
```bash
$ stap -l ’kernel.function("*")’ | sort
```

### 3.1 探测定义
一般语法如下：
```bash
probe PROBEPOINT [, PROBEPOINT] { [STMT ...] }
```
事件通过一种称为探测点（probe points）的特殊语法来指定。翻译器定义了多种探测点，插件集脚本也可以使用别名定义其他探测点。提供的探测点在`stapprobes(3)`、`tapset::*(3stap)`和`probe::*(3stap)`手册页中列出。只要命名的`PROBEPOINT`事件中的任何一个发生，就会执行`STMT`语句块。

探测处理程序是根据每个事件的上下文进行解释的。对于与内核代码相关的事件，此上下文可能包括在该位置的源代码中定义的变量。这些目标变量（或“上下文变量”）在脚本中以变量形式呈现，其名称前缀为美元符号（`$`）。只有在编译内核时，编译器保留了这些变量（尽管进行了优化），才能访问它们。这与调试器处理优化代码时所施加的约束相同。其他事件可能几乎没有上下文。

### 3.2 探测别名
一般语法如下：
```bash
probe <alias> = <probepoint> { <prologue_stmts> } 
probe <alias> += <probepoint> { <epilogue_stmts> }
```

可以使用别名定义新的探测点。探测点别名看起来与探测定义类似，但它不是在给定点激活探测，而是将一个新的探测点名称定义为现有探测点的别名。新的探测别名可以引用一个或多个现有的探测别名。多个别名可以共享相同的底层探测点。例如：
```bash
probe socket.sendmsg = kernel.function("sock_sendmsg") { ... } 
probe socket.do_write = kernel.function("do_sock_write") { ... }
probe socket.send = socket.sendmsg, socket.do_write { ... }
```

有两种类型的别名，即序言式别名和结语式别名，分别由等号（`=`）和“`+=`”标识。

使用探测点别名的探测将创建一个实际的探测，并在前面加上别名的处理程序。这种前置行为有多种用途，它允许别名定义在将控制权传递给用户指定的处理程序之前，对探测的上下文进行预处理。以下是一些示例：
```bash
# 除非满足给定条件，否则跳过探测：
if ($flag1 != $flag2) next

# 提供描述探测的信息：
name = "foo"

# 将目标变量提取为普通局部变量：
var = $var
```

#### 3.2.1 序言式别名(=)
对于序言式别名，别名定义后面的语句块会隐式地添加到任何引用该别名的探测的开头作为序言。例如：
```bash
# 定义一个新的探测点syscall.read，它扩展为kernel.function("sys_read")，并将给定语句作为序言。
probe syscall.read = kernel.function("sys_read") {
    fildes = $fd
}
```

#### 3.2.2 结语式别名(+=)
别名定义后面的语句块会隐式地添加到任何引用该别名的探测的结尾作为结语。在结语中定义新变量没有用处（因为后续代码无法访问它们），但代码可以根据序言或用户代码设置的变量采取行动。例如：
```bash
# 定义一个新的探测点，并将给定语句作为结语。
probe syscall.read += kernel.function("sys_read") {
    if (traceme) println("tracing me")
}
```

#### 3.2.3 探测别名的用法
探测别名的使用方式与任何内置探测类型相同，只需命名即可：
```bash
probe syscall.read { printf("reading fd=%d\n", fildes) }
```

#### 3.2.4 别名后缀
在调用探测别名时可以包含一个后缀。如果探测点的初始部分仅与别名匹配，那么其余部分将被视为后缀，并在别名展开时附加到底层探测点上。例如：
```bash
/* 定义一个别名： */
probe sendrecv = tcp.sendmsg, tcp.recvmsg { ... }

/* 以基本形式使用别名： */
probe sendrecv { ... }

/* 使用带有附加后缀的别名： */
probe sendrecv.return { ... }
```

这里，第二次使用探测别名等同于编写`probe tcp.sendmsg.return, tcp.recvmsg.return`。另一个例子是，探测点`tcp.sendmsg.return`和`tcp.recvmsg.return`实际上在插件集`tcp.stp`中被定义为别名。它们扩展为`kernel.function("...").return`形式的探测点，因此也可以添加后缀：

```bash
probe tcp.sendmsg.return.maxactive(10) { 
    printf("returning from sending %d bytes\n", size)
}
```
这里，探测点扩展为`kernel.function("tcp_sendmsg").return.maxactive(10)`。

#### 3.2.5 别名后缀和通配符
在展开通配符时，SystemTap通常不会考虑别名后缀的扩展。但当遇到没有普通扩展的通配符元素时除外。例如：
```bash
probe some_unrelated_probe = ... { ... }
probe myprobe = syscall.read { ... }
probe myprobe.test = some_unrelated_probe { ... }
probe myprobe.* { ... }
probe myprobe.ret* { ... }
```
这里，`return`将是`myprobe`的有效后缀。通配符`myprobe.*`匹配普通别名`myprobe.test`，因此不包括后缀扩展`myprobe.return`。相反，`myprobe.ret*`不匹配任何普通别名，所以后缀`myprobe.return`会作为扩展包含在内。

### 3.3 变量
变量和函数的标识符是字母数字序列，可以包含下划线（`_`）和美元符号（`$`）字符，但不能以普通数字开头。默认情况下，每个变量在其所在的探测或函数语句块中是局部的，因此其作用域和生命周期仅限于特定的探测或函数调用。标量变量会隐式地被类型化为字符串或整数。关联数组的值也可以是字符串或整数，并且由字符串或整数组成的元组用作键。数组必须声明为全局变量，不允许使用局部数组。

翻译器会对所有标识符（包括数组索引和函数参数）进行类型推断。如果标识符在类型相关的使用上不一致，将导致错误。

变量可以声明为全局变量。全局变量在所有探测之间共享，并且只要SystemTap会话处于活动状态，它们就会一直存在。所有全局变量都在同一个命名空间中，无论它们在哪个脚本文件中被定义。由于可能存在并发限制（例如多个探测处理程序），在处理程序运行时，每个被探测使用的全局变量都会自动进行读锁或写锁。全局声明可以在脚本文件的最外层任何位置编写，而不仅仅是在代码块内。在会话关闭时，会自动显示已写入但从未读取的全局变量。以下声明将`var1`和`var2`标记为全局变量。翻译器将为每个变量推断值类型，如果变量被用作数组，还会推断其键类型。
```bash
global var1[=<value>], var2[=<value>]
```

使用`private`关键字可以将全局变量的作用域限制在插件集或用户脚本文件中。定义私有全局变量时，`global`关键字是可选的。以下声明将`var1`和`var2`标记为私有全局变量。
```bash
private global var1[=<value>]
private var2[=<value>]
```

#### 3.3.1 未使用的变量
SystemTap翻译器会删除未使用的变量。从未写入或读取的全局变量将被丢弃，仅写入但从未读取的局部变量也会被丢弃。这种优化会删除在探测别名中定义但在探测处理程序中未使用的变量。如果需要，可以使用`-u`选项禁用此优化。

### 3.4 辅助函数
一般语法：
```bash
function <name>[:<type>] ( <arg1>[:<type>], ... )[:<priority>] { <stmts> }
```

SystemTap脚本可以定义子例程来分解常见的工作。函数可以接受任意数量的标量参数，并且必须返回单个标量值。这里的标量指整数或字符串。有关标量的更多信息，请参见3.3节和5.2节。以下是一个函数声明的示例：

```bash
function thisfn (arg1, arg2) {
    return arg1 + arg2
}
```

注意，这里通常没有类型声明，类型由翻译器推断。如果需要，函数定义可以为其返回值、参数或两者包含显式类型声明，这对于嵌入式C函数很有帮助。在以下示例中，类型推断引擎只需要推断`arg2`（一个字符串）的类型：

```bash
function thatfn:string(arg1:long, arg2) {
    return sprintf("%d%s", arg1, arg2)
}
```

函数可以调用其他函数或进行递归调用，但有固定的嵌套限制。请参见1.6节。

可以使用`private`关键字将函数标记为私有，以将其作用域限制在定义它的插件集或用户脚本文件中。以下是一个私有函数定义的示例：

```bash
private function three:long () { return 3 }
```

如果函数在没有到达显式`return`语句的情况下结束，将根据类型推断返回隐式的`0`或`""`。

函数在运行时和编译时都可以被重载。

运行时重载允许在模块运行时根据运行时条件选择要执行的函数，这可以通过脚本函数中的`next`语句和嵌入式C函数中的`STAP_NEXT`宏来实现。例如：

```bash
function f() { 
    if (condition) next; 
    print("first function") 
} 
function f() %{ STAP_NEXT; print("second function") %} 
function f() { print("third function") }
```

在调用函数`f()`时，如果`condition`求值为`true`，执行将转移到第三个函数并打印“third function”。注意，第二个函数无条件地被跳过。

参数重载允许在编译时根据提供给函数调用的参数数量选择要执行的函数。例如：

```bash
function g() { print("first function") } 
function g(x) { print("second function") }
g() -> "first function" 
g(1) -> "second function"
```

注意，在上述示例中不会发生运行时重载，因为对于函数调用，只会解析出一个函数。如果在函数中没有更多重载时使用`next`语句，将触发运行时异常。只有当函数具有相同的参数数量时才会发生运行时重载，具有相同名称但不同参数数量的函数是完全不相关的。

执行顺序由可以指定的优先级值决定。如果未指定显式优先级，用户脚本函数的优先级高于库函数。用户脚本函数和库函数的默认优先级值分别为0和1。具有相同优先级的函数按声明顺序执行。例如：
```bash
function f():3 { 
    if (condition) next; 
    print("first function") 
} 
function f():1 { 
    if (condition) next; 
    print("second function") 
} 
function f():2 { print("third function") }
```

### 3.5 嵌入式C
SystemTap支持一种guru模式，在这种模式下，诸如代码和数据内存引用保护等脚本安全功能会被移除。通过向`stap`命令传递`-g`选项来设置guru模式。在guru模式下，翻译器会接受脚本文件顶层中由“`%{`”和“`%}`”标记包围的C代码。嵌入式C代码会被逐字转录，不进行分析，直接插入到生成的C代码的顶层。因此，guru模式对于在生成的模块顶层添加`#include`指令或为其他嵌入式代码提供辅助定义很有用。

在guru模式下，嵌入式C代码块也可以作为SystemTap函数的主体（如3.6节所述），并且可以替代任何SystemTap表达式。在后一种情况下，代码块必须包含符合C语法的有效表达式。

以下是各种允许的嵌入式C代码包含方法的示例：
```bash
%{ 
#include <linux/in.h>
#include <linux/ip.h> 
%} /* <-- 顶层 */

/* 读取存储在给定地址的char值： */
function __read_char:long(addr:long) %{ 
    /* pure */ 
    STAP_RETURN(kderef(sizeof(char), STAP_ARG_addr));
%} /* <-- 函数体 */
CATCH_DEREF_FAULT();

/* 根据iphdr确定IP数据包是否为TCP： */
function is_tcp_packet:long(iphdr) { 
    protocol = @cast(iphdr, "iphdr")->protocol;
    return (protocol == %{ IPPROTO_TCP %}); /* <-- 表达式 */
}
```

### 3.6 嵌入式C函数
一般语法：
```bash
function <name>:<type> ( <arg1>:<type>, ... )[:<priority>] %{ <C_stmts> %}
```

函数体中允许使用嵌入式C代码。在这种情况下，脚本语言体将完全被“`%{`”和“`%}`”标记包围的一段C代码所取代。包含的代码可以执行C解析器允许的任何合理且安全的操作。

对于用SystemTap语言编写的代码，存在一些未记录但复杂的并发、资源消耗和运行时限制的安全约束。这些约束不适用于嵌入式C代码，因此使用嵌入式C代码时要格外小心。在解引用指针时要特别注意，使用`kread()`宏来解引用任何可能无效或危险的指针。如果不确定，应谨慎行事并使用`kread()`。`kread()`宏是嵌入式C生成的代码中使用的安全机制之一，可防止可能导致系统崩溃的指针访问。

例如，要在嵌入式C中访问指针链`name = skb->dev->name`，可以使用以下代码：

```bash
struct net_device *dev; 
char *name; 
dev = kread(&(skb->dev)); 
name = kread(&(dev->name));
```

用于输入和输出值的内存位置通过名为`STAP_ARG_foo`（用于名为`foo`的参数）和`STAP_RETVALUE`的宏提供给函数。可以使用`STAP_ERROR`发出错误信号，使用`STAP_PRINTF`进行输出，使用`STAP_RETURN`提前返回函数。以下是一些示例：

```bash
function integer_ops:long (val) %{ 
    STAP_PRINTF("%d\n", STAP_ARG_val);
    STAP_RETVALUE = STAP_ARG_val + 1;
    if (STAP_RETVALUE == 4) 
        if (STAP_RETVALUE == 3) 
            STAP_ERROR("wrong guess: %d", (int) STAP_RETVALUE);
    STAP_RETVALUE ++; 
    STAP_RETURN(0);
%}

function string_ops:string (val) %{ 
    strlcpy(STAP_RETVALUE, STAP_ARG_val, MAXSTRINGLEN);
    strlcat(STAP_RETVALUE, "one", MAXSTRINGLEN);
    if (strcmp(STAP_RETVALUE, "three-two-one")) 
        STAP_RETURN("parameter should be three-two-");
%}

function no_ops () %{ 
    STAP_RETURN(); /* 推断该函数没有返回值 */
%}
```

如果翻译器无法从使用中推断函数参数和返回值的类型，则应声明这些类型。翻译器不会分析函数内部的嵌入式C代码。

您应该检查为普通脚本语言函数生成的C代码，以编写兼容的嵌入式C代码。通常，所有SystemTap函数和探测在禁用中断的情况下运行，因此在嵌入式C中不能调用可能会睡眠的函数。

### 3.7 嵌入式C编译指示注释
嵌入式C块可以包含各种标记来声明优化和安全属性：
- `/* pure */` 表示C代码没有副作用，如果脚本代码不使用其值，则可以完全省略。
- `/* stable */` 表示C代码在任何给定的探测处理程序调用中总是具有相同的值，因此重复调用可以自动替换为记忆化的值。此类函数不得接受任何参数，并且也必须是`/* pure */`的。
- `/* unprivileged */` 表示C代码非常安全，即使是无特权用户也可以使用。（这对于在插件集中定义可被无特权代码使用的嵌入式C函数特别有用。）
- `/* myproc-unprivileged */` 表示C代码非常安全，只要当前探测的目标在用户自己的进程内，即使是无特权用户也可以使用。
- `/* guru */` 表示C代码非常不安全，SystemTap用户必须指定`-g`（guru模式）才能使用，即使该C代码是从插件集中导出的。
- `/* unmangled */` 在嵌入式C函数中使用，表示应在函数内部提供旧版（1.8之前）的参数访问语法。因此，除了`STAP_ARG_foo`和`STAP_RETVALUE`之外，还可以在函数内部使用`THIS->foo`和`THIS->__retvalue`。这对于快速迁移为SystemTap 1.7及更早版本编写的代码很有用。
- `/* unmodified-fnargs */` 在嵌入式C函数中使用，表示函数参数在函数体内不会被修改。
- `/* string */`仅在嵌入式C表达式中使用，意味着该表达式具有`const char *`类型，应被视为字符串值，而非默认的长整型数值。

### 3.8 访问脚本级全局变量
在嵌入式C函数和代码块中可以访问脚本级全局变量。若要读取或写入全局变量`var`，必须先在嵌入式C函数或代码块中添加`/* pragma:read:var */`或`/* pragma:write:var */`标记，这将提供`STAP_GLOBAL_GET_*`和`STAP_GLOBAL_SET_*`宏，分别用于读取和写入操作。例如：
```bash
global var
global var2[100]
function increment() %{
    /* pragma:read:var */
    /* pragma:write:var */
    /* pragma:read:var2 */
    /* pragma:write:var2 */
    STAP_GLOBAL_SET_var(STAP_GLOBAL_GET_var() + 1); //var++
    STAP_GLOBAL_SET_var2(1, 1, STAP_GLOBAL_GET_var2(1, 1) + 1); //var2[1,1]++
%}
```

变量在嵌入式C函数和表达式中均可读取和设置。从嵌入式C代码返回的字符串会被转换为指针。变量还必须在脚本级别进行赋值，以便进行类型推断。映射赋值不会返回写入的值，因此链式操作不起作用。


## 4. 探测点
----

### 4.1 通用语法
探测点的通用语法是由点分隔的符号序列。这将事件命名空间划分为多个部分，类似于域名系统的风格。每个组件标识符都由字符串或数字字面量进行参数化，其语法类似于函数调用。

以下都是语法有效的探测点：
```bash
module{"ext3"}.function("ext3_*")
kernel.function("foo")
kernel.function("foo").return
kernel.function("no_such_function")?
syscall.*
end
timer.ms(5000)
```
探测点大致可分为同步或异步两类。同步事件在任何处理器执行与规范匹配的指令时发生，这为这些探测点提供了一个参考点（指令地址），从而可能获取更多上下文数据。其他类型的探测点则涉及异步事件，如定时器，它们没有固定的参考点。每个探测点规范可以通过使用通配符或别名匹配多个位置，并且所有匹配位置都会被探测。一个探测声明可以包含多个用逗号分隔的规范，这些规范都会被探测。

#### 4.1.1 前缀
前缀用于指定探测目标，如`kernel`（内核）、`module`（模块）、`timer`（定时器）等。

#### 4.1.2 后缀
后缀用于进一步限定要探测的点，例如`.return`用于表示被探测函数的退出点。没有后缀则表示函数的入口点。

#### 4.1.3 通配文件名、函数名
组件中可以包含星号（`*`）字符，它会扩展为其他匹配的探测点。例如：
```bash
kernel.syscall.*
kernel.function("sys_*")
```

#### 4.1.4 可选探测点
探测点后面可以跟一个问号（`?`）字符，表示该探测点是可选的，如果它无法扩展，也不会导致错误。这种效果会在别名或通配符扩展的所有层级中传递。

#### 4.1.5 大括号展开
大括号展开是一种允许生成一系列探测点的机制，与 shell 展开非常相似。一个组件可以用一对花括号括起来，表示由逗号分隔的一个或多个子组件将各自构成一个新的探测点。花括号可以任意嵌套。展开结果的顺序基于乘积顺序。

问号（`?`）、感叹号（`!`）指示符和探测点条件不能放在最后一个组件之前的任何展开中。

以下是大括号展开的示例：
```bash
syscall.{write,read}
# 展开为 syscall.write, syscall.read

{kernel,module("nfs")}.function("nfs*")!
# 展开为
kernel.function("nfs*")!, module("nfs").function("nfs*")!
```

### 4.2 内置探测点类型（DWARF探测）
这类探测点使用目标内核或模块的符号调试信息，这些信息可以在未剥离的可执行文件或单独的调试信息包中找到。它们通过在源文件或目标代码中指定一组点，允许在目标执行路径中合理地放置探测点。当任何处理器上执行匹配的语句时，将在该上下文中运行探测处理程序。

内核中的点通过模块、源文件、行号、函数名或这些的某种组合来标识。

以下是当前支持的探测点规范列表：
```bash
kernel.function(PATTERN)
kernel.function(PATTERN).call
kernel.function(PATTERN).return
kernel.function(PATTERN).return.maxactive(VALUE)
kernel.function(PATTERN).inline
kernel.function(PATTERN).label(LPATTERN)
module(MPATTERN).function(PATTERN)
module(MPATTERN).function(PATTERN).call
module(MPATTERN).function(PATTERN).return.maxactive(VALUE)
module(MPATTERN).function(PATTERN).inline
kernel.statement(PATTERN)
kernel.statement(ADDRESS).absolute
module(MPATTERN).statement(PATTERN)
```

- `.function`变体：在命名函数的开头附近放置一个探测点，这样函数参数可以作为上下文变量使用。
- `.return`变体：在命名函数返回的时刻放置一个探测点，这样返回值可以作为`$return`上下文变量使用。入口参数在返回探测的上下文中也可访问，不过函数可能已经修改了它们的值。返回探测可以进一步用`.maxactive`修饰，它指定了可以同时被探测的指定函数的实例数量。在大多数情况下，你可以省略`.maxactive`，因为默认值（`KRETACTIVE`）应该就足够了。但是，如果你注意到跳过的探测数量过多，可以尝试将`.maxactive`设置为逐渐增大的值，看看跳过的探测数量是否减少。
- `.inline`修饰符：用于`.function`，它会过滤结果，只包含内联函数的实例。`.call`修饰符则选择相反的子集。`.exported`修饰符过滤结果，只包含导出函数。内联函数没有可识别的返回点，所以`.return`在`.inline`探测中不被支持。
- `.statement`变体：在精确的位置放置一个探测点，暴露在该位置可见的局部变量。

在上述探测描述中，`MPATTERN`代表一个字符串字面量，用于标识感兴趣的已加载内核模块；`LPATTERN`代表源程序标签。`MPATTERN`和`LPATTERN`都可以包含星号（`*`）、方括号（`[]`）和问号（`?`）通配符。

`PATTERN`代表一个字符串字面量，用于标识程序中的一个点。它由三部分组成：
1. 第一部分是函数名，就像在`nm`程序的输出中出现的那样。这部分可以使用星号和问号通配符来匹配多个名称。
2. 第二部分是可选的，以`@`字符开头。后面跟着包含该函数的源文件路径，路径中可以包含通配符模式，如`mm/slab*`。在大多数情况下，路径应该是相对于Linux源目录的顶层，不过对于某些内核，可能需要使用绝对路径。如果相对路径名不起作用，可以尝试使用绝对路径。
3. 第三部分在给出文件名部分时是可选的。它用于标识源文件中的行号，前面加上`:`或`+`。如果前面是`:`，则行号被视为绝对行号；如果前面是`+`，则行号是相对于函数入口的相对行号。使用`:*`可以匹配函数中的所有行，使用`:x-y`可以匹配从`x`到`y`的行范围。

或者，将`PATTERN`指定为一个数字常量，以表示相对模块地址或绝对内核地址。

一些在编译单元中可见的源级变量，如函数参数、局部变量或全局变量，对探测处理程序是可见的。在脚本中，通过在变量名前加上美元符号来引用这些变量。此外，一种特殊的语法允许对结构、指针、数组进行有限的遍历，获取变量的地址或对整个结构进行漂亮打印。
- `$var`：引用作用域内的变量`var`。如果它是类似于整数的类型，在脚本使用时会被转换为64位整数。类似于字符串（`char *`）的指针会通过`kernel_string()`或`user_string()`函数复制为SystemTap字符串值。
- `@var("varname")`：是`$varname`的另一种语法。它还可以用于访问特定编译单元（CU）中的全局变量。`@var("varname@src/file.c")`引用在编译`src/file.c`文件时定义的全局（可以是文件局部或外部）变量`varname`。解析变量的CU是探测点所在模块中第一个与给定文件名匹配且文件名路径最短的CU（例如，给定`@var("foo@bar/baz.c")`，如果有`src/sub/module/bar/baz.c`和`src/bar/baz.c`两个CU，则选择第二个CU来解析`foo`）。
 - `@var("varname", "/path/to/exe-or-so")`：这种表示法也支持显式指定全局或顶层静态变量所在的可执行文件或库文件路径。
 - `$var->field`或`@var("var@file.c")->field`：用于遍历结构的字段。间接运算符可以重复使用，以访问更深层次的指针。
 - `$var[N]`或`@var("var@file.c")[N]`：用于对数组进行索引。索引使用字面数字给出。
 - `&$var`或`&@var("var@file.c")`：提供变量的地址，类型为`long`。它还可以与字段访问或数组索引结合使用，如`&var->field`、`&@var("var@file.c")[N]`或这些访问器的组合，以提供特定字段或数组元素的地址。
 - 使用单个`$`或双`$$`后缀：可以提供变量数据类型的浅或深字符串表示形式。使用单个`$`，如`$var$`，将提供一个字符串，其中仅包含变量结构类型的所有基本类型字段的值，但不包含任何嵌套复杂类型的值（这些值将用`{...}`表示）。使用双`$$`，如`@var("var")$$`，将提供一个字符串，其中还包括嵌套数据类型的所有值。
 - `$$vars`：展开为一个字符字符串，等效于`sprintf("parm1=%x ... parmN=%x var1= %x ... varN=%x", $parm1, ..., $parmN, $var1, ..., $varN)`。
 - `$$locals`：展开为一个字符字符串，等效于`sprintf("var1=%x ... varN=%x", $var1, ..., $varN)`。
 - `$$parms`：展开为一个字符字符串，等效于`sprintf("parm1=%x ... parmN=%x", $parm1, ..., $parmN)` 。

#### 4.2.1 kernel.function, module().function
 - `.function`变体：在命名函数的开头附近放置一个探测点，这样函数参数可以作为上下文变量使用。
 - 通用语法：
```bash
kernel.function("func[@file]")
module("modname").function("func[@file]")
```

 - 示例：
```bash
# 引用所有名称中包含 "init" 或 "exit" 的内核函数：
kernel.function("*init*"), kernel.function("*exit*")

# 引用 "kernel/time.c" 文件中跨越第240行的任何函数：
kernel.function("*@kernel/time.c:240")

# 引用ext3模块中的所有函数：
module("ext3").function("*")
```

#### 4.2.2 kernel.statement, module().statement
 - `.statement`变体：在精确的位置放置一个探测点，暴露在该位置可见的局部变量。
 - 通用语法：
```bash
module("modname").statement("func@file:linenumber")
kernel.statement("func@file:linenumber")
```

 - 示例：
```bash
# 引用kernel/time.c文件中第296行的语句：
kernel.statement("*@kernel/time.c:296")

# 引用fs/bio.c文件中bio_init函数内偏移3处的语句：
kernel.statement("bio_init@fs/bio.c+3")
```

### 4.3 函数返回探测
 - `.return`变体：在命名函数返回的时刻放置一个探测点，这样返回值可以作为`$return`上下文变量使用。在返回探测的上下文中，入口参数也可访问，不过其值可能已被函数修改。内联函数没有可识别的返回点，所以`.return`在`.inline`探测中不被支持。

### 4.4 无DWARF探测
在没有调试信息的情况下，你仍然可以使用`kprobe`系列的探测来检查内核和模块函数的入口和出口点。使用这些探测时，你无法查找函数的参数或局部变量。不过，你可以通过以下步骤来访问参数：

当在函数入口处停止时，你可以按编号引用函数的参数。例如，当探测声明如下的函数时：
```c
asmlinkage ssize_t sys_read(unsigned int fd, char __user *buf, size_t count)
```

你可以分别将`fd`、`buf`和`count`的值获取为`uint arg(1)`、`pointer arg(2)`和`ulong arg(3)` 。在这种情况下，你的探测代码必须首先调用`asmlinkage()`，因为在某些架构上，`asmlinkage`属性会影响函数参数的传递方式。

当处于返回探测中时，如果没有DWARF信息，`$return`是不被支持的，但你可以调用`returnval()`来获取函数返回值通常存储的寄存器的值，或者调用`returnstr()`来获取该值的字符串版本。

并且在任何代码探测点，你都可以调用`register("regname")`来获取探测点命中时指定CPU寄存器的值。`uregister("regname")`与`register("regname")`类似，但将值解释为无符号整数。

SystemTap支持以下结构：
```bash
kprobe.function(FUNCTION)
kprobe.function(FUNCTION).return
kprobe.module(NAME).function(FUNCTION)
kprobe.module(NAME).function(FUNCTION).return
kprobe.statement(ADDRESS).absolute
```

对于内核函数，使用`.function`探测；对于指定模块的函数，使用`.module`探测。如果你不知道内核或模块函数的绝对地址，可以使用`.statement`探测。在`FUNCTION`和`MODULE`名称中不要使用通配符，通配符会导致探测无法注册。此外，`statement`探测仅在guru模式下可用。

### 4.5 用户空间探测
在配置了包含`utrace`或`uprobes`扩展的内核上，SystemTap支持用户空间探测。

#### 4.5.1 开始/结束变体
结构：
```bash
process.begin
process("PATH").begin
process(PID).begin
process.thread.begin
process("PATH").thread.begin
process(PID).thread.begin
process.end
process("PATH").end
process(PID).end
process.thread.end
process("PATH").thread.end
process(PID).thread.end
```

 - `.begin`变体：当由`PID`或`PATH`描述的新进程创建时被调用。如果未指定`PID`或`PATH`参数（例如`process.begin`），该探测会标记任何新生成的进程。
 - `.thread.begin`变体：当由`PID`或`PATH`描述的新线程创建时被调用。
 - `.end`变体：当由`PID`或`PATH`描述的进程终止时被调用。
 - `.thread.end`变体：当由`PID`或`PATH`描述的线程终止时被调用。

#### 4.5.2 系统调用变体
结构：
```bash
process.syscall
process("PATH").syscall
process(PID).syscall
process.syscall.return
process("PATH").syscall.return
process(PID).syscall.return
```

 - `.syscall`变体：当由`PID`或`PATH`描述的线程进行系统调用时被调用。系统调用号可在`$syscall`上下文变量中获取。系统调用的前六个参数可在`$argN`参数中获取，例如`$arg1`、`$arg2`等。
 - `.syscall.return`变体：当由`PID`或`PATH`描述的线程从系统调用返回时被调用。系统调用号可在`$syscall`上下文变量中获取。系统调用的返回值可在`$return`上下文变量中获取。

#### 4.5.3 函数/语句变体
结构：
```bash
process("PATH").function("NAME")
process("PATH").statement("*@FILE.c:123")
process("PATH").function("*").return
process("PATH").function("myfun").label("foo")
```

SystemTap支持在用户空间程序和共享库中进行完整的符号源级探测。这些探测与前面描述的基于符号DWARF的内核或模块探测完全类似，并暴露类似的上下文`$`变量。更多信息请参见4.2节。

以下是一个示例，展示了对用户空间符号探测的原型支持：
```bash
# stap -e ’probe process("ls").function("*").call { log(probefunc()." ".$$parms) }’ \
-c ’ls -l’
```

要运行此脚本，需要为指定的程序提供调试信息，并且内核要支持`utrace`。如果看到“pass 4a-time”构建失败，请检查你的内核是否支持`utrace`。

#### 4.5.4 绝对变体
像`process(PID).statement(ADDRESS).absolute`这样的非符号探测点类似于`kernel.statement(ADDRESS).absolute`，它们都使用未经验证的原始虚拟地址，并且不提供`$`变量。目标`PID`参数必须指定一个正在运行的进程，而`ADDRESS`必须指定一个有效的指令地址。列出的进程的所有线程都将被探测。这是一种guru模式探测。

#### 4.5.5 进程探测路径
对于所有进程探测，`PATH`名称引用的可执行文件的搜索方式与shell相同：如果路径名以斜杠（`/`）字符序列开头，则使用指定的显式路径；否则在`$PATH`中搜索。例如，以下探测语法：
```bash
probe process("ls").syscall {}
probe process("./a.out").syscall {}
```

与以下语法的效果相同：
```bash
probe process("/bin/ls").syscall {}
probe process("/my/directory/a.out").syscall {}
```

如果指定的进程探测没有`PID`或`PATH`参数，则会探测所有用户线程。但是，如果在目标进程模式下调用SystemTap，则进程探测将仅限于与目标进程相关的进程层次结构。如果`stap`在`--unprivileged`模式下运行，则仅选择当前用户拥有的进程。

#### 4.5.6 目标进程模式
目标进程模式（通过`stap -c CMD`或`-x PID`调用）会隐式地将所有`process.*`探测限制在给定的子进程中。它不会影响`kernel.*`或其他类型的探测。`CMD`字符串通常直接运行，而不是通过“`/bin/sh -c`”子shell运行，因为`utrace`和`uprobe`探测会收到相当“干净”的事件流。如果`CMD`中存在元字符（如重定向操作符），则仍会使用“`/bin/sh -c CMD`”，并且`utrace`和`uprobe`探测将从shell接收事件。例如：
```bash
% stap -e ’probe process.syscall, process.end { printf("%s %d %s\n", execname(), pid(), pp())}’ \
-c ls
```

此命令的输出如下：
```log
ls 2323 process.syscall
ls 2323 process.syscall
ls 2323 process.end
```
如果`PATH`指定一个共享库，则可以探测所有映射该共享库的进程。如果安装了dwarf调试信息，可以尝试使用以下语法的命令：
```bash
probe process("/lib64/libc-2.8.so").function("....") { ... }
```

此命令会探测所有调用该库的线程。输入“`stap -c CMD`”或“`stap -x PID`”会将其限制为仅目标命令及其子进程。你可以使用`$$vars`等。你可以使用`-d DIRECTORY`选项为`stap`命令提供调试信息的位置。要将探测点限定到特定进程所需的库中的某个位置，可以尝试使用以下语法的命令：
```bash
probe process("...").library("...").function("....") { ... }
```

库名可以使用通配符。

第一种语法将探测特定进程的程序链接表中的函数。第二种语法还将添加该进程所需的库的程序链接表。可以指定`.plt("...")`来匹配特定的`plt`条目。
```bash
probe process("...").plt { ... }
probe process("...").plt process("...").library("...").plt { ... }
```

#### 4.5.7 静态用户空间探测
你可以使用以下语法探测编译到程序和共享库中的符号静态检测点：
```bash
process("PATH").mark("LABEL")
```

`.mark`变体由应用程序中使用`STAP_PROBE1(handle,LABEL,arg1)`定义的静态探测调用。`STAP_PROBE1`在`sdt.h`文件中定义。参数如下：
|参数|定义|
|--|--|
|handle|应用程序句柄|
|LABEL|与`.mark`参数相对应|
|arg1|参数|

对于有一个参数的探测，使用`STAP_PROBE1`；对于有2个参数的探测，使用`STAP_PROBE2`，依此类推。探测的参数可在上下文变量`$arg1`、`$arg2`等中获取。

作为`STAP_PROBE`宏的替代方法，你可以使用dtrace脚本创建自定义宏。`sdt.h`文件还通过`DTRACE_PROBE`和相关的python dtrace脚本提供了与dtrace兼容的标记。在基于dtrace的构建中，如果需要`dtrace -h`或`-G`功能，可以使用这些标记。

### 4.6 Java探测
SystemTap通过使用Byteman作为后端支持对Java方法的探测。Byteman是JBoss项目中的一个检测工具，SystemTap可以利用它来监控Java程序中特定方法或行的调用。

SystemTap通过生成一个Byteman脚本列出要检测的探测点，然后调用Byteman的`bminstall`实用程序来实现这一功能。可以通过使用SystemTap的`-J OPTION`选项将自定义选项`-D OPTION`（更多详细信息请参阅Byteman文档）传递给`bminstall`。SystemTap还提供了`-j`选项，作为`-J org.jboss.byteman.compile.to.bytecode`的简写形式。

目前，这种Java检测支持还是一个原型功能，存在一些主要限制：Java探测一次只能附加到一个Java进程；除了第一个被观察的Java进程之外，其他Java进程将被忽略。此外，Java探测目前不能跨用户使用；stap脚本必须在与被探测的Java进程相同的用户下运行（因此，当前以root身份运行的stap脚本不能探测非root用户的Java进程中的方法）。

翻译器支持四种探测点变体：
```bash
java("PNAME").class("CLASSNAME").method("PATTERN")
java("PNAME").class("CLASSNAME").method("PATTERN").return
java(PID).class("CLASSNAME").method("PATTERN")
java(PID).class("CLASSNAME").method("PATTERN").return
```

前两个探测点通过Java进程的名称来引用Java进程。`PATTERN`参数指定要探测的Java方法的签名。签名必须由方法的准确名称后跟一个包含参数类型的括号列表组成，例如`myMethod(int,double,Foo)`。不支持通配符。

可以通过在方法签名后附加行号（以冒号分隔）来设置探测在方法内的特定行触发，就像在其他类型的探测中一样：`myMethod(int,double,Foo):245`。

`CLASSNAME`参数用于标识方法所属的Java类，可以包含或不包含包限定符。默认情况下，探测仅在不覆盖原始类方法定义的类的后代上触发。但是，`CLASSNAME`可以使用可选的插入符号前缀，如`class("^org.my.MyClass")`，这指定探测也应在覆盖原始方法的`MyClass`的所有后代上触发。例如，使用以下探测点可以一次性探测`org.my.MyApp`程序中所有签名为`foo(int)`的方法：
```bash
java("org.my.MyApp").class("^java.lang.Object").method("foo(int)")
```

最后两个探测点的工作方式类似，但通过PID来引用Java进程。（已经运行的进程的PID可以使用`jps`实用程序获取。）

Java探测中定义的上下文变量包括`$provider`（用于标识提供触发方法定义的类）和`$name`（用于给出方法的签名）。方法的参数可以使用上下文变量`$arg1`到`$arg10`来访问，最多可访问方法的前10个参数。

### 4.7 PROCFS探针
这些探针点允许在`/proc/systemtap/MODNAME`中创建、读取和写入procfs伪文件。指定SystemTap模块的名称为`MODNAME`。翻译器支持四种探针点变体：
- `procfs("PATH").read`
- `procfs("PATH").write`
- `procfs.read`
- `procfs.write`

`PATH`是要创建的文件名，相对于`/proc/systemtap/MODNAME`。如果未指定`PATH`（如前面列表中的最后两个变体），`PATH`默认为`"command"`。

当用户读取`/proc/systemtap/MODNAME/PATH`时，会触发相应的procfs读探针。将要读取的字符串数据赋值给一个名为`$value`的变量，如下所示：
```bash
procfs("PATH").read {
    $value = "100\n"
}
```

当用户写入`/proc/systemtap/MODNAME/PATH`时，会触发相应的procfs写探针。用户写入的数据可在名为`$value`的字符串变量中获取，如下所示：
```
procfs("PATH").write {
    printf("User wrote: %s", $value)
}
```

### 4.8 标记探针
这类探针点连接到插入内核或模块中的静态探针标记。这些标记是内核中的特殊宏调用，与基于DWARF的探针相比，它们使探测更快、更可靠。使用探针标记不需要DWARF调试信息。

标记探针点以`kernel`前缀开头，该前缀标识用于查找标记的符号表来源。后缀是标记本身的名称：`mark.("MARK")`。标记名称字符串可以包含通配符，它会与内核或模块编译时给标记宏指定的名称进行匹配。可选地，你可以指定`format("FORMAT")`。指定标记格式字符串可以区分名称相同但格式字符串不同的两个标记。

与标记探针关联的处理程序会读取在宏调用站点指定的任何可选参数，这些参数名为`$arg1`到`$argNN`，其中`NN`是宏提供的参数数量。数字和字符串参数以类型安全的方式传递。

与标记关联的标记格式字符串可在`$format`中获取。标记名称字符串可在`$name`中获取。

以下是标记探针的构造：
- `kernel.mark("MARK")`
- `kernel.mark("MARK").format("FORMAT")`

有关标记探针的更多信息，请参阅http://sourceware.org/systemtap/wiki/UsingMarkers。

### 4.9 跟踪点
这类探针点连接到插入内核或内核模块中的静态探测跟踪点。与标记探针一样，这些跟踪点是内核开发人员插入的特殊宏调用，目的是使探测比基于DWARF的探针更快、更可靠。探测跟踪点不需要DWARF调试信息。跟踪点的参数类型比标记探针更严格。

跟踪点探针以`kernel`开头。下一部分是跟踪点本身的名称：`trace("name")`。跟踪点名称字符串可以包含通配符，它会与内核开发人员在跟踪点头文件中定义的名称进行匹配。

与基于跟踪点的探针关联的处理程序可以读取在宏调用站点指定的可选参数。这些参数根据跟踪点作者的声明进行命名。例如，跟踪点探针`kernel.trace("sched_switch")`提供参数`$rq`、`$prev`和`$next`。如果参数是复杂类型（如结构体指针），则脚本可以使用与DWARF `$target`变量相同的语法来访问字段。跟踪点参数不能被修改；但是，在guru模式下，脚本可以修改参数的字段。

跟踪点的名称可在`$$name`中获取，跟踪点所有参数的名称-值对字符串可在`$$vars`或`$$parms`中获取。

### 4.10 系统调用探针
`syscall.*`别名定义了数百个探针。它们使用以下语法：
- `syscall.NAME`
- `syscall.NAME.return`

通常，对于`syscalls(2)`手册页中列出的每个普通系统调用，都会定义两个探针：一个用于进入系统调用，一个用于从系统调用返回。从不返回的系统调用没有相应的`.return`探针。

每个探针别名定义了各种变量。查看tapset源代码是查找变量定义的最可靠来源。一般来说，标准手册页中列出的每个变量都可作为脚本级变量使用。例如，`syscall.open`会暴露文件名、标志和模式。此外，大多数别名都有一组标准变量，如下所示：
- `argstr`：整个参数列表的美观打印形式，不带括号。
- `name`：系统调用的名称。
- `retstr`：对于返回探针，是系统调用结果的美观打印形式。

并非所有探针别名都遵循这些通用准则。如果你遇到不符合的情况，请将其作为错误报告。

### 4.11 定时器探针
你可以使用标准内核节拍（jiffies）定时器定义的时间间隔来异步触发探针处理程序。一个节拍是内核定义的时间单位，通常在1到60毫秒之间。翻译器支持两种探针点变体：
- `timer.jiffies(N)`
- `timer.jiffies(N).randomize(M)`

探针处理程序每`N`个节拍运行一次。如果指定了`randomize`组件，则每次处理程序执行时，会在范围`[-M ... +M]`内的一个线性分布随机值添加到`N`上。`N`被限制在合理范围内（1到大约1,000,000），`M`被限制为小于`N`。在这两种情况下都没有提供目标变量。探针可以在多个处理器上并发运行。

时间间隔可以用时间单位指定。有两种与节拍定时器类似的探针点变体：
- `timer.ms(N)`
- `timer.ms(N).randomize(M)`

这里，`N`和`M`以毫秒为单位指定，但完整的时间单位选项包括秒（`s`或`sec`）、毫秒（`ms`或`msec`）、微秒（`us`或`usec`）、纳秒（`ns`或`nsec`）和赫兹（`hz`）。赫兹定时器不支持随机化。

定时器的分辨率取决于目标内核。对于2.6.17之前的内核，定时器仅限于节拍分辨率，因此时间间隔会向上舍入到最接近的节拍间隔。在2.6.17之后，实现使用高精度定时器（hrtimers）以获得更高的精度，不过最终的分辨率将取决于架构。在任何一种情况下，如果指定了`randomize`组件，则在进行任何舍入之前，随机值将被添加到时间间隔上。

分析定时器可用于提供在每个系统时钟周期在所有CPU上执行的探针。这个探针不带参数，如下所示：
```
timer.profile.tick
```

被中断进程的完整上下文信息是可用的，这使得这个探针适合用于实现基于时间的采样分析器。

建议使用tapset探针`timer.profile`，而不是`timer.profile.tick`。当底层功能可用时，这个探针点的行为与`timer.profile.tick`相同，并且在一些缺少相应分析定时器功能的近期内核上，会回退使用`perf.sw.cpu_clock`。

以下是定时器使用的示例：
- 表示每1000个节拍的周期性中断：`timer.jiffies(1000)`
- 每5秒触发一次：`timer.sec(5)`
- 表示每1000 ± 200个节拍的周期性中断：`timer.jiffies(1000).randomize(200)`

### 4.12 特殊探针点
探针点`begin`和`end`由翻译器定义，分别指会话启动和关闭的时间。在这两种情况下都没有目标变量可用。

#### 4.12.1 begin
`begin`探针是SystemTap会话的开始。所有`begin`探针处理程序都会在会话启动期间运行。

#### 4.12.2 end
`end`探针是SystemTap会话的结束。所有`end`探针会在会话正常关闭期间运行，例如在SystemTap退出函数调用之后，或者用户中断之后。如果会话因错误而关闭，则不会运行`end`探针。

#### 4.12.3 error
`error`探针点与`end`探针类似，不同之处在于，当会话因错误结束时，探针处理程序会运行。在这种情况下，`end`探针会被跳过，但每个`error`探针仍会尝试运行。你可以使用`error`探针在脚本终止时进行清理或执行最终操作。

以下是一个简单的示例：
```bash
probe error {
    println ("Oops, errors occurred. Here’s a report anyway.")
    foreach (coin in mint) {
        println (coin)
    }
}
```

#### 4.12.4 begin、end和error探针序列
`begin`、`end`和`error`探针可以指定一个可选的序列号，该序列号控制它们的运行顺序。如果未提供序列号，则序列号默认为零，探针将按照它们在脚本文件中出现的顺序运行。序列号可以是正数或负数，对于希望在`begin`探针中进行初始化的tapset编写者来说特别有用。以下是一些示例：
- 在tapset文件中：
```bash
probe begin(-1000) {
    ...
}
```
- 在用户脚本中：
```bash
probe begin {
    ...
}
```
用户脚本的`begin`探针默认为序列号零，因此tapset的`begin`探针将首先运行。

#### 4.12.5 never
`never`探针点由翻译器定义，表示永远不会触发。它的语句会进行符号和类型正确性分析，但它的探针处理程序永远不会运行。这个探针点与可选探针结合使用可能会很有用。请参阅4.1.4节。 


## 5 语言元素
----

### 5.1 标识符
标识符用于给变量和函数命名。它们是由字母和数字组成的序列，还可以包含下划线（_）和美元符号`（$）`。其语法与C语言标识符相同，只不过美元符号在SystemTap中也是合法字符。以美元符号开头的标识符会被解释为对目标软件中变量的引用，而不是SystemTap脚本变量。标识符不能以纯数字开头。

### 5.2 数据类型
SystemTap语言包含少量数据类型，但无需进行类型声明。变量的类型根据其使用方式推断得出。为了支持这种类型推断，翻译器会强制要求函数参数、返回值、数组索引和数组值的类型保持一致。字符串和数字之间不存在隐式类型转换。如果标识符在类型使用上不一致，将会报错。

#### 5.2.1 字面量
字面量分为字符串或整数。整数字面量可以用C语言的表示法，以十进制、八进制或十六进制的形式表达，不使用类型后缀（如L或U）。

#### 5.2.2 整数
整数可以是十进制、十六进制或八进制，其表示法与C语言相同。整数是64位有符号数，不过解析器也接受（并进行环绕处理）大于正 \(2^{63}\) 但小于 \(2^{64}\) 的值。

#### 5.2.3 字符串
字符串用引号（“string”）括起来，支持标准C语言的反斜杠转义字符。字符串字面量可以拆分成多个部分，这些部分会被拼接在一起，示例如下：
```
str1 = "foo" "bar"  // 结果为 "foobar"
str2 = "a good way to do a multi-line\n"
         "string literal"  // 结果为 "a good way to do a multi-line\nstring literal"
str3 = "also a good way to " @1 " splice command line args"  // 假设命令行中@1的值为foo，结果为 "also a good way to foo splice command line args"
```
可以看到，脚本参数也能拼接到字符串字面量中。

字符串的长度受限于`MAXSTRINGLEN`。有关这个限制及其他限制的更多信息，请参阅1.6节。

#### 5.2.4 关联数组
详见第7节。

#### 5.2.5 统计信息
详见第8节。

### 5.3 分号
分号代表空语句，即什么也不做的语句。它是可选的，用作语句之间的分隔符，有助于检测语法错误并减少语法歧义。

### 5.4 注释
支持以下三种注释形式：
- `# ...`：Shell风格，注释到行尾。
- `// ...`：C++风格，注释到行尾。
- `/* ... */`：C风格注释。

### 5.5 空白字符
与C语言一样，空格、制表符、回车符、换行符和注释都被视为空白字符。解析器会忽略空白字符。

### 5.6 表达式
SystemTap支持许多运算符，其通用语法、语义和优先级与C语言和awk类似。算术运算遵循C语言中对有符号整数的运算规则。如果解析器检测到除零或溢出情况，会生成错误。以下小节列出了这些运算符。

#### 5.6.1 二元数值运算符
`* / % + - > >> >>> < << & ^ | && ||`

#### 5.6.2 二元字符串运算符
` . `（字符串连接）

#### 5.6.3 数值赋值运算符
`= *= /= %= += -= >>= <<= &= ^= |=`

#### 5.6.4 字符串赋值运算符
`= .=`

#### 5.6.5 一元数值运算符
`+ - ! ~ ++ --`

#### 5.6.6 数值和字符串比较、正则表达式匹配运算符
`< > <= >= == != =~ !~`

`=~`和`!~`运算符用于进行正则表达式匹配。第二个操作数必须是包含有效正则表达式的字符串字面量。`=~`运算符在匹配成功时返回1，匹配失败时返回0；`!~`运算符在匹配失败时返回1。正则表达式语法支持POSIX扩展正则表达式的大部分特性，但不支持子表达式重用（\1）功能。匹配成功后，可以使用`matched` tapset函数提取匹配的子字符串和子表达式。`ngroups` tapset函数用于返回最后一次成功匹配的正则表达式中的子表达式数量。

#### 5.6.7 三元运算符
`cond ? exp1 : exp2`

#### 5.6.8 分组运算符
`( exp )`

#### 5.6.9 函数调用
通用语法：
`fn ([ arg1, arg2, ... ])`

#### 5.6.10 `$ptr->member`
`ptr`是在探测上下文中可用的内核指针。

#### 5.6.11 指针类型转换
使用`@cast()`运算符支持类型转换。脚本可以为长整型值定义指针类型，然后使用与`$target`变量相同的语法访问类型成员。当指针保存到脚本整型变量中后，翻译器会丢失从该指针访问成员所需的类型信息。`@cast()`运算符用于告知翻译器如何读取指针。

以下语句将`p`解释为指向名为`type_name`的结构体或联合体的指针，并解引用其成员`value`：
`@cast(p, "type_name"[, "module"])->member`

可选的`module`参数用于告知翻译器从何处查找该类型的信息。可以用冒号（:）分隔的列表形式指定多个模块。如果未指定`module`参数，对于DWARF探针，翻译器默认使用探测模块；对于函数和其他所有探针类型，则默认使用`kernel`。

以下语句从内核任务结构体中获取父进程的PID：
`@cast(pointer, "task_struct", "kernel")->parent->tgid`

如果没有正常的调试信息，翻译器可以从尖括号（<>）包围的头文件中创建包含类型信息的模块。对于内核头文件，需在前面加上`kernel`以使用合适的构建系统。其他所有头文件则使用默认的GCC参数构建为用户模块。以下是示例语句：
`@cast(tv, "timeval", "<sys/time.h>")->tv_sec`
`@cast(task, "task_struct", "kernel<linux/sched.h>")->tgid`

在guru模式下，翻译器允许脚本为类型转换后的指针成员分配新值。在`void*`成员的类型可能在运行时确定的情况下，类型转换也很有用。
```bash
probe foo { 
    if ($var->type == 1) { 
        value = @cast($var->data, "type1")->bar 
    } else { 
        value = @cast($var->data, "type2")->baz 
    } 
    print(value) 
} 
```

#### 5.6.12 `<value> in <array name>`
如果数组包含具有指定索引的元素，则此表达式求值为真。

#### 5.6.13 `[ <value>, ... ] in <array name>`
索引值的数量必须与之前指定的索引数量匹配。

### 5.7 从stap命令行传入的字面量
字面量可以是用双引号（” ”）括起来的字符串或整数。有关整数的信息，请参阅5.2.2节；有关字符串的信息，请参阅5.2.3节。
命令行末尾的脚本参数会作为字面量展开。在所有接受字面量的上下文中都可以使用这些参数。引用不存在的参数编号会报错。

#### 5.7.1 `$1...$<NN>`用于字面量粘贴
使用`$1...$<NN>`将整个参数字符串粘贴到输入流中，这些字符串会进一步进行词法标记化处理。

#### 5.7.2 `@1...@<NN>`用于字符串
使用`@1...@<NN>`将整个参数转换为字符串字面量。

#### 5.7.3 示例
例如，有一个名为`example.stp`的脚本如下：
```bash
probe begin {
    printf("%d, %s\n", $1, $2)
}
```
如果这样调用：
`# stap example.stp ’5+5’ mystring`
那么`5+5`会替换`$1`，”mystring”会替换`@2`，输出结果为：
`10, mystring`

### 5.8 条件编译

#### 5.8.1 条件
解析过程中的一个步骤是简单的预处理阶段。预处理器支持条件编译，其一般形式与三元运算符（5.6.7节）类似。
`%( CONDITION %? TRUE-TOKENS %)`
`%( CONDITION %? TRUE-TOKENS %: FALSE-TOKENS %)`

`CONDITION`是一个有限制的表达式，其格式由第一个关键字决定。通用语法如下：
`%( <condition> %? <code> [ %: <code> ] %)`

#### 5.8.2 基于可用目标变量的条件
谓词`@defined()`用于测试某个`$variable/expression`在翻译时是否可解析。以下是使用示例：
```bash
probe foo {
    if (@defined($bar))
        log ("$bar is available here")
}
```

#### 5.8.3 基于内核版本的条件：`kernel v`、`kernel vr`
如果条件表达式的第一部分是标识符`kernel v`或`kernel vr`，则第二部分必须是六个标准数值比较运算符之一：“<”、“<=”、“==”、“!=”、“>”或“>=”，第三部分必须是包含RPM风格版本 - 发布值的字符串字面量。如果目标内核的版本（可通过`-r`选项进行覆盖）与给定的版本字符串匹配，则条件返回真。比较操作由glibc函数`strverscmp`执行。

`kernel v`仅指内核版本号，如“2.6.13”；`kernel vr`指包括发布代码后缀的内核版本号，如“2.6.13 - 1.322FC3smp”。

#### 5.8.4 基于架构的条件：`arch`
如果条件表达式的第一部分是标识符`arch`（表示处理器架构），则第二部分是字符串比较运算符“==”或“!=”，第三部分是用于匹配的字符串字面量。这种比较是简单的字符串相等或不相等比较。目前支持的架构字符串有`i386`、`i686`、`x86_64`、`ia64`、`s390`和`powerpc`。

#### 5.8.5 基于特权级别的条件：`systemtap privilege`
如果条件表达式的第一部分是标识符`systemtap privilege`（表示systemtap脚本的编译特权级别），则第二部分是字符串比较运算符“==”或“!=”，第三部分是用于匹配的字符串字面量。这种比较是简单的字符串相等或不相等比较。可能的特权字符串有“stapusr”（表示无特权脚本）和“stapsys”或“stapdev”（表示有特权脚本）。一般来说，要测试脚本是否有特权，最好使用`!= "stapusr"`。

这个条件可用于编写既能在无特权模式下运行，又能在有特权模式下提供额外功能的脚本。

#### 5.8.6 真和假标记
`TRUE-TOKENS`和`FALSE-TOKENS`是零个或多个通用解析器标记，可能包含嵌套的预处理器条件。如果条件为真，则将`TRUE-TOKENS`粘贴到输入流中；如果条件为假，则粘贴`FALSE-TOKENS`。例如，以下代码在目标内核版本早于2.6.5时会导致解析错误：
`%( kernel_v <= "2.6.5" %? **ERROR** %)`  // 无效的标记序列

以下代码可适应假设的内核版本变化：
```bash
probe kernel.function ( %( kernel_v <= "2.6.12" %? "__mm_do_fault" %: %)) { 
    /* ... */ 
} 
%( kernel_vr == "2.6.13-1.8273FC3smp" %? "do_page_fault" %: UNSUPPORTED %)
%( arch == "ia64" %? %)
probe syscall.vliw = kernel.function("vliw_widget") {}
```

以下代码根据内核配置选项的存在进行适应：
`%( CONFIG_UPROBE == "y" %? %)
probe process.syscall {}`

### 5.9 预处理器宏
这个特性可帮助脚本消除某些类型的重复代码。

#### 5.9.1 局部宏
预处理器还支持简单的宏设施。

使用以下结构定义带零个或多个参数的宏：
`@define NAME %( BODY %)`
`@define NAME(PARAM_1, PARAM_2, ...) %( BODY %)`

在宏体中，通过在参数名前加上`@`符号来引用宏参数。定义好宏之后，通过在宏名前加上`@`符号来调用宏：
```
@define foo %( x %)
@define add(a,b) %( ((@a)+(@b)) %)
@foo = @add(2,2)
```
目前，宏展开在条件编译之前的单独阶段进行。因此，无论条件求值结果如何，条件表达式中的`TRUE`和`FALSE`标记都会进行宏展开。这有时可能会导致错误，例如：

```
// 以下代码会导致冲突：
%( CONFIG_UPROBE == "y" %? @define foo %( process.syscall %)
%:
@define foo %( **ERROR** %)
%)
```

```
// 以下代码按预期正常工作：
@define foo %( 
%( CONFIG_UPROBE == "y" %? process.syscall %: **ERROR** %)
%)
```

第一个示例不正确，因为在条件求值之前的阶段，两个`@define`都会被求值。

#### 5.9.2 库宏
通常，宏定义只在其所在的文件内有效。因此，在tapset中定义的宏对使用该tapset的用户不可用。

可以通过在tapset搜索路径中包含`.stpm`文件来定义公共可用的库宏。这些文件只能包含`@define`结构，这些宏定义在所有tapset和用户脚本中都可见。

## 6 语句类型
----
语句用于在函数和探针处理程序中实现过程控制流。单个探针事件响应中执行的语句总数限制为`MAXACTION`，默认值为1000。请参阅1.6节。

### 6.1 break和continue
使用`break`或`continue`退出或迭代最内层的循环语句，例如在`while`、`for`或`foreach`语句中。其语法和语义与C语言相同。

### 6.2 try/catch
使用`try/catch`在脚本中处理大多数运行时错误，而不是终止正在执行的探针处理程序。其语义与C++类似，`try/catch`块可以嵌套。可以通过可选地命名一个变量来捕获错误字符串。
```bash
try {
    // 执行某些操作
    // 触发错误，如kread(0)、除零操作或error("foo")
} catch (msg) { 
    // 如果不关心错误字符串，可以省略(msg)
    // 处理错误
    // println("caught error ", msg)
}
// 执行继续
```

### 6.3 delete
`delete`用于删除元素。

以下语句从数组`ARRAY`中删除由索引元组指定的元素。该元素的值将不再可用，后续迭代也不会报告该元素。删除不存在的元素不会报错。
`delete ARRAY[INDEX1, INDEX2, ...]`

以下语法用于删除数组`ARRAY`中的所有元素：
`delete ARRAY`

以下语句用于删除标量`SCALAR`的值。整数和字符串会分别清零和置为空字符串（""），而统计信息会重置为初始的空状态。
`delete SCALAR`

### 6.4 EXP (expression)
表达式会执行一个返回字符串或整数值的表达式，并丢弃该值。

### 6.5 for
通用语法：
`for (EXP1; EXP2; EXP3) STMT`

`for`语句与C语言中的`for`语句类似。`for`表达式首先执行`EXP1`进行初始化。只要`EXP2`不为零，就会执行`STMT`，然后执行迭代表达式`EXP3`。

### 6.6 foreach
通用语法：
`foreach (VAR in ARRAY) STMT`

`foreach`语句用于遍历命名全局数组的每个元素，并将当前键赋值给`VAR`。在该语句执行期间，数组不能被修改。如果在`VAR`或`ARRAY`标识符后添加单个加号（+）或减号（-）运算符，迭代顺序将按索引或值的升序或降序排序。

以下语句与第一个示例类似，但用于数组使用键元组进行索引的情况。最多只能在一个`VAR`或`ARRAY`标识符上使用排序后缀。
`foreach ([VAR1, VAR2, ...] in ARRAY) STMT`

可以结合前两种语法，同时捕获完整的元组和键，如下所示：
`foreach (VAR = [VAR1, VAR2, ...] in ARRAY) STMT`

以下语句与第一个示例相同，只是`limit`关键字将循环迭代次数限制为`EXP`次。`EXP`在循环开始时求值一次。
`foreach (VAR in ARRAY limit EXP) STMT`

### 6.7 if语句
通用语法：
```
if (EXP) STMT1 [ else STMT2 ]
```
`if`语句将一个整数值的`EXP`与零进行比较。如果`EXP`不为零，就执行`STMT1`；如果为零，则执行`STMT2`（`else STMT2`部分是可选的） 。

`if`命令的语法和语义与C语言中的`if`语句相同。

### 6.8 next语句
`next`语句会立即从包含它的探针处理程序中返回。在函数中使用时，执行会立即转移到下一个重载函数。

### 6.9 ;（空语句）
通用语法：
```
statement1;
statement2
```
分号代表空语句，即什么也不做。它作为语句之间的可选分隔符很有用，可以提高语法错误的检测能力，并处理某些语法歧义。

### 6.10 return语句
通用语法：
```
return EXP
```
`return`语句从包含它的函数中返回`EXP`的值。如果函数不需要返回值，那么就不需要`return`语句，此时函数会有一种特殊的未知类型，没有返回值。

### 6.11 {}（语句块）
这是一个语句块，由花括号括起来，里面可以包含零个或多个语句。通用语法如下：
```
{
    STMT1
    STMT2
    ...
}
```
语句块会按顺序依次执行块内的每个语句。语句之间通常不需要分隔符或终止符。语句块的语法和语义与C语言中的相同。

### 6.12 while语句
通用语法：
```
while (EXP) STMT
```
`while`语句的语法和语义与C语言中的`while`语句相同。在上述语句中，只要整数值的`EXP`求值结果不为零，解析器就会执行`STMT`。 



## 7 关联数组
----
关联数组通过哈希表实现，其最大大小在启动时设定。关联数组规模较大，无法在单个探针处理程序运行时动态创建，因此必须声明为全局变量。数组的基本操作包括设置和查找元素，这些操作采用awk语法：数组名后接左括号（[）、最多九个由逗号分隔的索引表达式，以及右括号（]）。每个索引表达式可以是字符串或数字，只要在整个脚本中类型保持一致即可。

### 7.1 示例
- 增加指定数组槽的值：
```
foo [4,"hello"]++
```
- 更新统计信息：
```
processusage [uid(),execname()]++
```
- 设置时间戳参考点：
```
times [tid()]=get_cycles()
```
- 计算时间戳差值：
```
delta = get_cycles() - times [tid()]
```

### 7.2 值的类型
数组元素可以设置为数字、字符串或聚合类型。在数组的使用过程中，元素类型必须保持一致。数组的首次赋值会定义其元素的类型。未设置的数组元素在获取时会返回空值（零或空字符串），但在成员测试中不会被视为存在。

### 7.3 数组容量
数组大小可以显式指定，也可以采用默认的最大大小，该最大大小由`MAXMAPENTRIES`定义。有关更改`MAXMAPENTRIES`的详细信息，请参见1.6节。

可以按如下方式显式指定数组大小：
```
global ARRAY[<size>]
```
如果未指定大小参数，则创建的数组将容纳`MAXMAPENTRIES`个元素。

### 7.4 数组合并
数组可以使用百分号（%）进行合并。这意味着，当插入的元素数量超过数组的容量时，先前输入的元素将被覆盖。此功能适用于常规数组和统计类型的数组。

可以按如下方式标记数组合并：
```
global ARRAY1%[<size>], ARRAY2%
```

### 7.5 迭代，foreach
与awk类似，SystemTap的`foreach`循环遍历数组的键元组，而不仅仅是值。通过在代码中添加额外的加号（+）或减号（-），可以按任何单个键或值对迭代进行排序，也可以使用`limit`关键字将迭代限制为少数元素。以下是一些示例：
- 按任意顺序进行简单循环：
```
foreach ([a,b] in foo) fuss_with(foo[a,b])
```
- 按值的升序进行循环：
```
foreach ([a,b] in foo+) { ... }
```
- 按第一个键的降序进行循环：
```
foreach ([a-,b] in foo) { ... }
```
- 按降序打印数组中的前10个元组和值：
```
foreach (v = [i,j] in foo- limit 10) printf("foo[%d,%s] = %d\n", i, j, v)
```
`break`和`continue`语句在`foreach`循环中同样有效。由于数组可能很大，但探针处理程序必须快速执行，因此应尽可能编写能提前退出迭代的脚本。为了简化操作，SystemTap禁止在`foreach`迭代过程中对数组进行任何修改。

有关`foreach`的完整说明，请参见6.6小节。

### 7.6 删除
`delete`语句可以从数组中按索引删除单个元素，也可以一次性清空整个数组。详细信息和示例请参见6.3小节。


## 8 统计信息（聚合）
----
聚合实例用于收集数值统计信息，在需要快速大量积累新数据时非常有用。这些实例在无排他锁的情况下运行，仅存储聚合的流统计信息。聚合仅对全局变量有意义，它们可以单独存储，也可以作为关联数组的元素存储。有关使用统计元素合并关联数组的信息，请参见7.4节。

### 8.1 聚合（<<<）操作符
聚合操作符是“<<<”，其作用类似于赋值或C++输出流操作。左操作数指定一个标量或数组索引左值，必须声明为全局变量。右操作数是一个数值表达式。其含义直观：将给定数字作为样本添加到用于计算统计信息的数字集合中。具体要收集的统计信息列表由提取函数单独指定。以下是一个示例：
```
a <<< delta_timestamp
writes[execname()] <<< count
```

### 8.2 提取函数
对于作用于给定标识符的每个不同提取函数实例，翻译器会计算一组统计信息。每次执行提取函数时，都会在所有处理器上计算该时刻的聚合。每个函数的第一个参数与聚合操作左侧使用的左值类型相同。

### 8.3 整数提取器
以下函数提供了提取聚合信息的方法。

#### 8.3.1 @count(s)
此语句返回聚合`s`中积累的样本数量。

#### 8.3.2 @sum(s)
此语句返回聚合`s`中所有样本的总和。

#### 8.3.3 @min(s)
此语句返回聚合`s`中所有样本的最小值。

#### 8.3.4 @max(s)
此语句返回聚合`s`中所有样本的最大值。

#### 8.3.5 @avg(s)
此语句返回聚合`s`中所有样本的平均值。

### 8.4 直方图提取器
以下函数提供了提取直方图信息的方法。使用`print`系列函数打印直方图时，会将直方图对象呈现为表格形式的“ASCII艺术”条形图。

#### 8.4.1 @hist_linear
语句`@hist_linear(v,L,H,W)`表示聚合`v`的线性直方图，其中`L`和`H`分别表示值范围的下限和上限，`W`表示范围内每个桶的宽度（或大小）。下限和上限值可以为负，但总体差值（上限减去下限）必须为正。宽度参数也必须为正。

在输出中，连续的空桶范围可能会用波浪号（~）字符替换。这可以在命令行中通过`-DHIST_ELISION=<num>`进行控制，其中`<num>`指定要打印的范围顶部和底部的空桶数量，默认值为2。`<num>`为0时将删除所有空桶，`<num>`为负时将禁用删除功能。

例如，如果指定`-DHIST_ELISION=3`，并且直方图中有10个连续的空桶，则会打印前3个和后3个空桶，中间4个空桶将用波浪号（~）表示。

以下是一个示例：
```bash
global reads
probe netdev.receive {
    reads <<< length
}
probe end {
    print(@hist_linear(reads, 0, 10240, 200))
}
```
这将生成以下输出：
```log
value       count
0           1650
200 |       8
400 |       0
600 |       0
800 |       0
1000 |      0
1200 |      0
1400 |      1
1600 |      0
1800 |      0
```
这表明有1650次网络读取的大小在0到199字节之间，8次读取在200到399字节之间，1次读取在1200到1399字节之间。波浪号（~）字符表示800到999字节的桶因空而被删除，2000字节及更大的空桶也被删除。

#### 8.4.2 @hist_log
语句`@hist_log(v)`表示以2为底的对数直方图。空桶的替换方式与`@hist_linear()`相同（见上文）。

以下是一个示例：
```bash
global reads
probe netdev.receive {
    reads <<< length
}
probe end {
    print(@hist_log(reads))
}
```
这将生成以下输出：
```log
 value |-------------------------------------------------- count
     8 |                                                      0
    16 |                                                      0
    32 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  4285
    64 |                                                     81
   128 |@@@@@@@@@@@@@@@                                    1320
   256 |@@@@@@@@@@@@@@@@@@@@                               1742
   512 |@@@@                                                344
  1024 |@@@@@                                               430
  2048 |@@@@@@@                                             621
  4096 |@@@@@@@@@@@                                         959
  8192 |@                                                   146
 16384 |                                                     34
 32768 |                                                     20
 65536 |                                                      0
131072 |                                                      0
```

### 8.5 删除
对聚合变量应用`delete`语句（6.3小节）将使其重置为初始的空状态。


## 9 格式化输出
----

### 9.1 print
- **通用语法**：
  ```
  print()
  ```
- 此函数打印任何类型的单个值。

### 9.2 printf
- **通用语法**：
  ```
  printf(fmt:string, ...)
  ```
- `printf`函数接受一个格式化字符串作为参数，以及多个相应类型的值，并将它们全部打印出来。格式必须是一个字符串字面常量。`printf`的格式化指令与C语言中的类似，但翻译器会对其类型进行全面检查。
- 格式化字符串可以包含如下定义的标签：
  ```
  %[flags][width][.precision][length]specifier
  ```
其中，`specifier`是必需的，用于定义相应参数值的类型和解释方式。下表详细列出了`specifier`参数的取值：
| 说明符 | 输出 | 示例 |
| --- | --- | --- |
| d或i | 有符号十进制数 | 392 |
| o | 无符号八进制数 | 610 |
| s | 字符串 | sample |
| u | 无符号十进制数 | 7235 |
| x | 无符号十六进制数（小写字母） | 7fa |
| X | 无符号十六进制数（大写字母） | 7FA |
| p | 指针地址 | 0x0000000000bc614e |
| b | 使用计算机的本机字节顺序将二进制值写为文本。字段宽度指定要写入的字节数。有效规范为%b、%1b、%2b、%4b和%8b。默认宽度为8（64位）。 | 见下文 |
| % | 后跟另一个%字符将向标准输出写入%。 | % |
- 标签还可以包含标志、宽度、精度和修饰符子说明符，这些都是可选的，具体规范如下：
| 标志 | 描述 |
| --- | --- |
| -（减号） | 在给定的字段宽度内左对齐。默认是右对齐（见宽度子说明符）。 |
| +（加号） | 即使是正数，也在结果前加上加号或减号。默认情况下，只有负数前会加上减号。 |
| （空格） | 如果不写入符号，则在值前插入一个空格。 |
| # | 与o、x或X说明符一起使用时，非零值前分别加上0、0x或0X。 |
| 0 | 在指定填充时（见宽度子说明符），用零而不是空格填充数字。 |
| 宽度 | 描述 |
| --- | --- |
| (数字) | 要打印的最小字符数。如果要打印的值短于此数字，结果将用空格填充。即使结果更长，值也不会被截断。 |
| 精度 | 描述 |
| --- | --- |
| .数字 | 对于整数说明符（d、i、o、u、x、X）：精度指定要写入的最小数字位数。如果要写入的值短于此数字，结果将用前导零填充。即使结果更长，值也不会被截断。精度为0意味着对于值0不写入任何字符。对于s：这是要打印的最大字符数。默认情况下，会打印所有字符，直到遇到结束空字符。未指定精度时，默认值为1。如果指定了句点但未明确指定精度值，则假定为0。 |
- **二进制写入示例**：
  ```bash
  probe begin {
      for (i = 97; i < 110; i++)
          printf("%3d: %1b%1b%1b\n", i, i, i-32, i-64)
      exit()
  }
  ```
这段代码的输出为：
```log
97: aA!
100: dD$
98: bB"
99: cC#
101: eE%
102: fF&
103: gG’
104: hH(
105: iI)
106: jJ*
107: kK+
108: lL,
109: mM-
```

### 9.3 printd
- **通用语法**：
  ```bash
  printd(delimiter:string, ...)
  ```
- 此函数接受一个字符串分隔符和两个或更多任意类型的值，然后用分隔符分隔并打印这些值。分隔符必须是一个字符串字面常量。
- 例如：
  ```bash
  printd("/", "one", "two", "three", 4, 5, 6)
  ```
输出结果为：
```log
one/two/three/4/5/6
```

### 9.4 printdln
- **通用语法**：
  ```
  printdln(delimiter:string, ...)
  ```
- 此函数的操作与`printd`类似，但会在末尾追加一个换行符。

### 9.5 println
- **通用语法**：
  ```
  println()
  ```
- 此函数的操作与`print`类似，用于打印单个值，但会在末尾追加一个换行符。

### 9.6 sprint
- **通用语法**：
  ```
  sprint:string()
  ```
- 此函数的操作与`print`类似，但返回字符串而不是打印它。

### 9.7 sprintf
- **通用语法**：
  ```
  sprintf:string(fmt:string, ...)
  ```
- 此函数的操作与`printf`类似，但返回格式化后的字符串而不是打印它。


## 10 Tapset定义的函数
----
与内置函数不同，Tapset定义的函数在Tapset脚本中实现。这些函数在`tapset::*(3stap)`、`function::*(3stap)`和`probe::*(3stap)`手册页中有单独的文档说明，并在`/usr/share/systemtap/tapset`目录下实现。

## 11 更多参考信息

如需更多信息，请参见：
- SystemTap教程：http://sourceware.org/systemtap/tutorial/
- SystemTap维基页面：http://sourceware.org/systemtap/wiki
- SystemTap文档页面：http://sourceware.org/systemtap/documentation.html
- 从解压的源tar包或GIT目录中，可查看`src/examples`目录中的示例、`src/tapset`目录中的Tapset脚本以及`src/testsuite`目录中的测试脚本。
- Tapset的手册页。要列出相关手册页，请运行命令“man -k tapset::”。
- 单个探针点的手册页。要列出相关手册页，请运行命令“man -k probe::”。
- 单个SystemTap函数的手册页。要列出相关手册页，请运行命令“man -k function::”。 