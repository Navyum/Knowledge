---
title: Systemtap-Beginners-Guide中文版
date: 2025-04-15 00:12:34
author: Navyum
tags: 
 - Systemtap新手指南
 - Systemtap
categories: 
 - 英文翻译
 - 工具
 - 性能分析
 - Systemtap

---

# SystemTap v5.2 新手指南-中文版
----
本文为[《Systemtap-Beginners-Guide》](https://sourceware.org/systemtap/SystemTap_Beginners_Guide.pdf)中文版翻译，仅供学习参考使用，如有翻译错误，请及时联系作者[Navyum](https://github.com/Navyum/Navyum)更新修正。


## SystemTap简介
----
作者：
- Don Domingo
- William Cohen

SystemTap新手指南
SystemTap 5.2 SystemTap新手指南 SystemTap简介


Author Don Domingo ddomingo@redhat.com
Author William Cohen wcohen@redhat.com
Red Hat, Inc.
Copyright © 2013 Red Hat, Inc

----

本文档为自由软件；您可以依据由自由软件基金会发布的GNU通用公共许可证第二版的条款对其进行再分发及修改。

本程序是基于希望它有用的目的而发布，但不提供任何形式的担保，甚至不包含适销性或特定用途适用性的默示担保。如需了解更多详情，请查阅GNU通用公共许可证。

您应该已经随本程序收到了一份GNU通用公共许可证副本；如果没有，请写信至自由软件基金会，地址为美国马萨诸塞州波士顿市富兰克林街51号5楼，邮编02110 - 1301。

如需更多详细信息，请查看Linux源代码发行版中的COPYING文件。

本指南提供了关于如何使用SystemTap来更细致地监控Linux系统不同子系统的基本说明。

## 目录：
----
* [前言](#前言)
    * 1. [文档约定](#1.-文档约定)
        * 1.1. [排版约定](#1.1-排版约定：)
        * 1.2. [引用块约定](#1.2-引用约定：)
        * 1.3. [注释和警告](#1.3-注意事项和警告：)
    * 2. [我们需要您的反馈！](#2.-我们需要反馈！)
* [第1章 引言](#第1章-引言)
    * 1.1. [文档目标](#1.1-文档目标)
    * 1.2. [SystemTap功能](#1.2-SystemTap功能)
    * 1.3. [SystemTap的局限性](#1.3-SystemTap的局限性)
* [第2章 使用SystemTap](#第2章-使用SystemTap)
    * 2.1. [安装和设置](#2.1-安装和设置)
        * 2.1.1. [安装SystemTap](#2.1.1-安装SystemTap：)
        * 2.1.2. [手动安装所需的内核信息包](#2.1.2-手动安装所需的内核信息软件包：)
        * 2.1.3. [初始测试](#2.1.3-初始测试：)
    * 2.2. [为其他计算机生成检测工具](#2.2-为其他计算机生成检测代码)
    * 2.3. [运行SystemTap脚本](#2.3-运行SystemTap脚本)
        * 2.3.1. [SystemTap飞行记录器模式](#2.3.1-SystemTap飞行记录器模式)
            * 2.3.1.1. [内存飞行记录器](#2.3.1.1-内存飞行记录器：)
            * 2.3.1.2. [文件飞行记录器](#2.3.1.2-文件飞行记录器：)
* [第3章 理解SystemTap的工作原理](#第3章-理解SystemTap的工作原理)    
    * 3.1. [架构](#3.1-架构)
    * 3.2. [SystemTap脚本](#3.2-SystemTap脚本)
        * 3.2.1. [事件](#3.2.1-事件)
        * 3.2.2. [SystemTap处理程序/主体](#3.2.2-SystemTap处理程序/主体)
        * 3.2.2.2 [类型转换](#3.3.2.2-类型转换)
    * 3.3. [基本的SystemTap基本处理程序结构](#3.3-基本的SystemTap处理程序构造)
        * 3.3.1. [变量](#3.3.1-变量)
        * 3.3.2. [目标变量](#3.3.2-目标变量)
            * 3.3.2.1 [美化打印目标变量](#3.3.2.1-美化打印目标变量)
            * 3.3.2.2 [类型转换](#3.3.2.2-类型转换)
            * 3.3.2.3 [检查目标变量的可用性](#3.3.2.3-检查目标变量的可用性)
        * 3.3.3. [条件语句](#3.3.3-条件语句)
            * [If/Else语句](#If/Else语句)
            * [While循环](#While循环)
            * [For循环](#For循环)
            * [条件运算符](#条件运算符)
        * 3.3.4. [命令行参数](#3.3.4-命令行参数)
    * 3.4. [关联数组](#3.4-关联数组)
    * 3.5. [SystemTap中的数组操作](#3.5-SystemTap中的数组操作)
        * 3.5.1. [分配关联值](#3.5.1-分配关联值)
        * 3.5.2. [从数组读取值](#3.5.2-从数组读取值)
        * 3.5.3. [增加关联值](#3.5.3-增加关联值)
        * 3.5.4. [处理数组中的多个元素](#3.5.4-处理数组中的多个元素)
        * 3.5.5. [清除/删除数组和数组元素](#3.5.5-清除/删除数组和数组元素)
        * 3.5.6. [在条件语句中使用数组](#3.5.6-在条件语句中使用数组)
        * 3.5.7. [计算统计聚合](#3.5.7-计算统计聚合)
    * 3.6. [Tapsets](#3.6-Tapsets)
* [第4章 用户空间探测](#第4章-用户空间探测)
    * 4.1. [用户空间事件](#4.1-用户空间事件)
    * 4.2. [访问用户空间目标变量](#4.2-访问用户空间目标变量)
    * 4.3. [用户空间堆栈回溯](#4.3-用户空间栈回溯)
* [第5章 有用的SystemTap脚本](#第5章-有用的SystemTap脚本)
    * 5.1. [网络](#5.1-网络)
        * 5.1.1. [网络分析](#5.1.1-网络分析)
        * 5.1.2. [跟踪网络套接字代码中调用的函数](#5.1.2-跟踪网络套接字代码中调用的函数)
        * 5.1.3. [监控传入的TCP连接](#5.1.3-监控传入的TCP连接)
        * 5.1.4. [监控TCP数据包](#5.1.4-监控TCP数据包)
        * 5.1.5. [监控内核中的网络数据包丢弃](#5.1.5-监控内核中的网络数据包丢弃)
    * 5.2. [磁盘](#5.2-磁盘)
        * 5.2.1. [汇总磁盘读写流量](#5.2.1-汇总磁盘读写流量)
        * 5.2.2. [跟踪每个文件读写的I/O时间](#5.2.2-跟踪每个文件读写的I/O时间)
        * 5.2.3. [跟踪累积I/O](#5.2.3-跟踪累积I/O)
        * 5.2.4. [I/O监控（按设备）](#5.2.4-I/O监控（按设备）)
        * 5.2.5. [监控文件的读写操作](#5.2.5-监控文件的读写操作)
        * 5.2.6. [监控文件属性变化](#5.2.6-监控文件属性变化)
        * 5.2.7. [定期打印I/O块时间](#5.2.7-定期打印I/O块时间)
    * 5.3. [性能分析](#5.3-性能分析)
        * 5.3.1. [统计函数调用次数](#5.3.1-统计函数调用次数)
        * 5.3.2. [调用图跟踪](#5.3.2-调用图跟踪)
        * 5.3.3. [确定内核态和用户态的耗时](#5.3.3-确定内核态和用户态的耗时)
        * 5.3.4. [监控轮询应用程序](#5.3.4-监控轮询应用程序)
        * 5.3.5. [跟踪最常用的系统调用](#5.3.5-跟踪最常使用的系统调用)
        * 5.3.6. [跟踪每个进程的系统调用量](#5.3.6-跟踪每个进程的系统调用量)
    * 5.4. [识别有竞争的用户空间锁](#5.4-识别用户空间中的竞争锁)
* [第6章 理解SystemTap错误](#第6章-理解SystemTap错误)
    * 6.1. [解析和语义错误](#6.1-解析和语义错误)
    * 6.2. [运行时错误和警告](#6.2-运行时错误和警告)
* [第7章 参考文献](#第7章-参考文献)
* [第8章 Appendix A. Revision History（修改历史）](#第8章-Appendix-A.-Revision-History（修改历史）)
* [第9章 Index（索引）](#第9章-Index（索引）)

## 前言
----

### 1. 文档约定
本手册使用了多种约定来突出特定的单词和短语，并引起对特定信息的关注。

在PDF和纸质版中，本手册使用了来自Liberation Fonts字体集的字体。如果您的系统安装了该字体集，HTML版也会使用；否则，将显示其他等效字体。注意：Red Hat Enterprise Linux 5及更高版本默认包含Liberation Fonts字体集。

#### 1.1 排版约定：
使用四种排版约定来突出特定的单词和短语，这些约定及其适用情况如下：
- **等宽加粗**：
  用于突出系统输入，包括shell命令、文件名和路径，也用于突出按键和按键组合。
  例如：要查看当前工作目录中文件my_next_bestselling_novel的内容，请在shell提示符下输入`cat my_next_bestselling_novel`命令，然后按回车键执行该命令。
  
  上述内容包括文件名、shell命令和按键，均以等宽加粗显示，且通过上下文可区分。按键组合可通过连接各部分的加号与单个按键区分开来。
  例如：按回车键执行命令；按`Ctrl+Alt+F2`组合键切换到虚拟终端。
  
  第一个示例突出显示要按下的特定按键，第二个示例突出显示一个按键组合，即同时按下的一组三个按键。如果讨论源代码，段落中提及的类名、方法、函数、变量名和返回值将以上述等宽加粗格式呈现。
  例如：与文件相关的类包括表示文件系统的`filesystem`、表示文件的`file`和表示目录的`dir`。每个类都有其相关的权限集。

- **比例加粗**：
  用于表示在系统中遇到的单词或短语，包括应用程序名称、对话框文本、带标签的按钮、复选框和单选按钮标签、菜单标题和子菜单标题。
  例如：从主菜单栏中选择**系统**→**首选项**→**鼠标**，以启动**鼠标首选项**。在“按钮”选项卡中，选中**左手习惯鼠标**复选框，然后点击**关闭**，即可将鼠标主按钮从左侧切换到右侧（使鼠标适合左手使用）。
  
  要在gedit文件中插入特殊字符，请从主菜单栏中选择**应用程序**→**附件**→**字符映射表**。接下来，从**字符映射表**菜单栏中选择**搜索**→**查找…**，在**搜索**字段中输入字符名称，然后点击**下一步**。您查找的字符将在**字符表**中突出显示。双击该突出显示的字符，将其放入**要复制的文本**字段中，然后点击**复制**按钮。现在切换回您的文档，从gedit菜单栏中选择**编辑**→**粘贴**。
  
  上述文本包括应用程序名称、系统范围的菜单名称和菜单项、特定应用程序的菜单名称以及GUI界面中的按钮和文本，均以比例加粗显示，且通过上下文可区分。
- **等宽加粗斜体或比例加粗斜体**：
  无论是等宽加粗还是比例加粗，添加斜体表示可替换或可变文本。斜体表示您不应按字面输入的文本，或根据情况显示的变化文本。

  例如：要使用ssh连接到远程机器，请在shell提示符下输入`ssh username@domain.name`。如果远程机器是example.com，且您在该机器上的用户名是john，则输入`ssh john@example.com`。
  `mount -o remount file-system`命令用于重新挂载指定的文件系统。例如，要重新挂载/home文件系统，命令为`mount -o remount /home`。
  要查看当前安装软件包的版本，使用`rpm -q package`命令。它将返回如下结果：*package-version-release*。
  
  注意上述加粗斜体的单词：username、domain.name、file-system、package、version和release。每个单词都是一个占位符，要么是您在发出命令时输入的文本，要么是系统显示的文本。除了用于表示作品标题的标准用法外，斜体还表示首次使用的新的重要术语。
  例如：Publican是一个*DocBook*出版系统。

#### 1.2 引用约定：
终端输出和源代码列表在视觉上与周围文本区分开来。发送到终端的输出采用等宽罗马字体显示，如下所示：
```
books books_tests Desktop1 Desktop documentation downloads drafts mss images notes photos scripts svgs stuff svn
```

源代码列表也采用等宽罗马字体，但添加了语法高亮，如下所示：
```java
package org.jboss.book.jca.ex1;
import javax.naming.InitialContext;
public class ExClient{
    public static void main(String args[]) 
    throws Exception{
        InitialContext iniCtx = new InitialContext();
        Object ref = iniCtx.lookup("EchoBean");
        Object ref;
        EchoHome home;
        EchoHome home = (EchoHome) ref;
        Echo echo = home.create();
        Echo echo;
        System.out.println("Created Echo");
        System.out.println("Echo.echo('Hello') = " + echo.echo("Hello"));
    }
}
```

#### 1.3 注意事项和警告：
最后，我们使用三种视觉样式来引起对可能被忽略的信息的关注。
- **注意**：注意事项是针对手头任务的提示、快捷方式或替代方法。忽略注意事项通常不会产生负面后果，但您可能会错过一些能让您的工作更轻松的技巧。
- **重要**：重要事项详细说明了容易被忽略的内容，例如仅适用于当前会话的配置更改，或者在更新生效前需要重启的服务。忽略标有“重要”的框不会导致数据丢失，但可能会引起困扰和挫折。
- **警告**：警告不应被忽视。忽略警告很可能会导致数据丢失。

### 2. 我们需要反馈！
如果您在本手册中发现排版错误，或者您想到了改进本手册的方法，我们很乐意听取您的意见！请在Bugzilla中提交报告：http://sourceware.org/bugzilla/，产品选择systemtap。

提交报告时，请务必包括报告所涉及的具体文件或URL，以及手册的标识符：SystemTap_Beginners_Guide。

如果您对改进文档有建议，请在描述时尽量具体。如果您发现了错误，请包括章节编号和一些周围的文本，以便我们轻松找到它 。


## 第1章 引言
----
SystemTap是一个跟踪和探测工具，它允许用户详细研究和监控计算机系统（特别是内核）的活动。它提供的信息类似于netstat、ps、top和iostat等工具的输出，但旨在为收集到的信息提供更多的过滤和分析选项。

### 1.1 文档目标
SystemTap提供了用于监控运行中的Linux内核以进行详细分析的基础架构。这可以帮助管理员和开发人员确定错误或性能问题的根本原因。

如果没有SystemTap，监控运行内核的活动将需要繁琐的仪器化、重新编译、安装和重启过程。SystemTap旨在消除这些步骤，允许用户通过运行用户编写的SystemTap脚本收集相同的信息。

SystemTap最初是为具有中级到高级内核知识的用户设计的。因此，对于对Linux内核知识和经验有限的管理员或开发人员来说，它的用处较小。此外，现有的许多SystemTap文档都是针对知识丰富且经验丰富的用户，这使得学习该工具同样困难。

为了降低这些障碍，编写《SystemTap新手指南》的目标如下：
- 向用户介绍SystemTap，使其熟悉其架构，并提供设置说明；
- 提供预先编写的SystemTap脚本，用于监控系统不同组件中的详细活动，以及如何运行这些脚本和分析其输出的说明。

### 1.2 SystemTap功能
- **灵活性**：SystemTap的框架允许用户开发简单的脚本，用于调查和监控内核空间中发生的各种内核函数、系统调用和其他事件。因此，SystemTap与其说是一个工具，不如说是一个允许您开发自己的特定于内核的取证和监控工具的系统。
- **易用性**：如前所述，SystemTap允许用户探测内核空间事件，而无需对内核进行仪器化、重新编译、安装和重启。

第5章“有用的SystemTap脚本”中列举的大多数SystemTap脚本展示了其他类似工具（如top、oprofile或ps）原生不具备的系统取证和监控功能。提供这些脚本是为了给读者提供广泛的SystemTap应用示例，并进一步向他们传授在编写自己的SystemTap脚本时可以使用的功能。

### 1.3 SystemTap的局限性
当前版本的SystemTap在探测各种内核的内核空间事件时提供了多种选项。然而，SystemTap探测用户空间事件的能力取决于内核支持（Utrace机制），而许多内核中没有这种支持。因此，只有部分内核版本支持用户空间探测。

目前，SystemTap社区的开发工作致力于提高SystemTap的用户空间探测能力。


## 第2章 使用SystemTap
----
本章记录了如何在系统中安装SystemTap，并解释了如何使用stap实用程序运行SystemTap脚本。

### 2.1 安装和设置
要部署SystemTap，需要安装SystemTap软件包以及相应的内核的-devel、-debuginfo和-debuginfo-common软件包。如果您的系统安装了多个内核，并且您打算在多个内核上使用SystemTap，还需要为每个内核版本安装-devel和-debuginfo软件包。

以下各节将更详细地讨论安装过程。
#### 2.1.1 安装SystemTap：
要部署SystemTap，需安装以下RPM软件包：
- systemtap
- systemtap-runtime

要安装这些软件包，请以root用户身份运行以下命令：
```bash
yum install systemtap systemtap-runtime
```
注意，在使用SystemTap之前，您仍然需要安装所需的内核信息软件包。在现代系统上，以root用户身份运行以下命令来安装这些软件包：
```bash
stap-prep
```
如果此命令不起作用，请尝试如下所述的手动安装。

#### 2.1.2 手动安装所需的内核信息软件包：
SystemTap需要有关内核的信息，以便在其中放置检测代码（换句话说，进行探测）。这些信息还允许SystemTap生成检测代码。
所需信息包含在与您的内核匹配的-devel、-debuginfo和-debuginfo-common软件包中。普通“香草”内核所需的-devel和-debuginfo软件包如下：
  - kernel-debuginfo
  - kernel-debuginfo-common
  - kernel-devel

同样，PAE内核所需的软件包是kernel-PAE-debuginfo、kernel-PAE-debuginfo-common和kernel-PAE-devel。
要确定您的系统当前使用的内核，请使用：
```bash
uname -r
```

例如，如果您打算在i686机器上的2.6.18 - 53.el5内核版本上使用SystemTap，请下载并安装以下RPM软件包：
  - kernel-debuginfo-2.6.18-53.1.13.el5.i686.rpm
  - kernel-debuginfo-common-2.6.18-53.1.13.el5.i686.rpm
  - kernel-devel-2.6.18-53.1.13.el5.i686.rpm
**重要提示**：-devel、-debuginfo和-debuginfo-common软件包的版本、变体和架构必须与您希望使用SystemTap探测的内核完全匹配。
安装所需内核信息软件包的最简单方法是通过yum install和debuginfo-install命令。debuginfo-install命令包含在yum-utils软件包的较新版本中（例如，版本1.1.10），并且还需要一个合适的yum存储库，以便从中下载和安装-debuginfo和-debuginfo-common软件包。您可以安装所需的内核的-devel、-debuginfo和-debuginfo-common软件包。

当启用了适当的软件存储库后，使用以下命令为特定内核安装相应的软件包：
```bash
yum install kernelname-devel-version
debuginfo-install kernelname-version
```

将kernelname替换为适当的内核变体名称（例如，kernel-PAE），将version替换为目标内核的版本。例如，要为kernel-PAE-2.6.18-53.1.13.el5内核安装所需的内核信息软件包，请运行：
```bash
yum install kernel-PAE-devel-2.6.18-53.1.13.el5
debuginfo-install kernel-PAE-2.6.18-53.1.13.el5
```

一旦您手动将所需软件包下载到机器上，请以root用户身份运行以下命令来安装它们：
```bash
rpm --force -ivh package_names
```
#### 2.1.3 初始测试：
如果您当前正在使用打算用SystemTap探测的内核，则可以立即测试部署是否成功。如果不是，请重启系统并加载适当的内核。
要开始测试，请运行以下命令：
  ```bash
  stap -v -e 'probe vfs.read {printf("read performed\n"); exit()}'
  ```

此命令指示SystemTap打印“read performed”，然后在检测到虚拟文件系统读取后正确退出。如果SystemTap部署成功，它将打印类似于以下的输出：

```log
Pass 1: parsed user script and 45 library script(s) in 340usr/0sys/358real ms.
Pass 2: analyzed script: 1 probe(s), 1 function(s), 0 embed(s), 0 global(s) in 290usr/260sys/568real ms.
Pass 3: translated to C into "/tmp/stapiArgLX/stap_e5886fa50499994e6a87aacdc43cd392_399.c" in 490usr/430sys/938real ms.
Pass 4: compiled C into "stap_e5886fa50499994e6a87aacdc43cd392_399.ko" in 3310usr/430sys/3714real ms.
Pass 5: starting run.
read performed Pass 5: run completed in 10usr/40sys/73real ms.
```
  
输出的最后三行（以Pass 5开头）表明SystemTap能够成功创建用于探测内核的检测代码，运行检测代码，检测到正在探测的事件（在这种情况下，是虚拟文件系统读取），并执行有效的处理程序（打印文本，然后无错误地关闭）。

### 2.2 为其他计算机生成检测代码
当用户运行SystemTap脚本时，SystemTap会基于该脚本构建一个内核模块。随后，SystemTap将这个模块加载到内核中，这样就能直接从内核提取指定数据（更多信息可参考3.1节“架构”中的3.1节“SystemTap会话”流程 ）。
然而通常情况下，SystemTap脚本仅能在部署了SystemTap的系统上运行（如2.1节“安装与设置”所述）。这意味着，如果想在十台系统上运行SystemTap，就需要在所有这些系统上进行部署。在某些情形下，这既不可行也并非最佳选择。例如，公司策略可能禁止管理员在特定机器上安装提供编译器或调试信息的RPM软件包，从而阻碍了SystemTap的部署。为解决这个问题，SystemTap支持交叉检测功能。

交叉检测是指在一台计算机上根据SystemTap脚本生成SystemTap检测模块，以供另一台计算机使用的过程。该过程具有以下优势：
- 可在单个主机上安装适用于多种机器的内核信息软件包。
- 每个目标机器仅需安装一个RPM软件包（即systemtap-runtime软件包），便可使用生成的SystemTap检测模块。

为简化表述，本节将使用以下术语：
- **检测模块**：由SystemTap脚本构建的内核模块。该SystemTap模块在主机系统上构建，并将被加载到目标系统的目标内核上。
- **主机系统**：用于从SystemTap脚本编译检测模块，以便将其加载到目标系统上的系统。
- **目标系统**：为其构建SystemTap脚本检测模块的系统。
- **目标内核**：目标系统的内核，即打算加载或运行检测模块的内核。

若要配置主机系统和目标系统，请完成以下步骤：
1. 在每个目标系统上安装systemtap-runtime软件包。
2. 在每个目标系统上运行`uname -r`命令，确定正在运行的内核。
3. 在主机系统上安装SystemTap。您将在主机系统上为目标系统构建检测模块。有关安装SystemTap的说明，请参考2.1.1节“安装SystemTap”。
4. 根据之前确定的目标内核版本，按照2.1.2节“手动安装所需内核信息软件包”中的描述，在主机系统上安装目标内核及相关RPM软件包。如果多个目标系统使用不同的目标内核，则针对目标系统使用的每个不同内核重复此步骤 。

完成这些步骤后，您现在可以在主机系统上为任何目标系统构建检测模块。

要构建检测模块，请在主机系统上运行以下命令（务必指定合适的值）：
```bash
stap -p4 -r kernel_version script -m module_name
```

此处，`kernel_version`指目标内核的版本（即目标机器上`uname -r`命令的输出结果），`script`指要转换为检测模块的脚本，`module_name`是所需的检测模块名称。

**注意**：若要确定正在运行的内核的架构表示法，可以运行以下命令：
```bash
uname -m
```

一旦编译好检测模块，将其复制到目标系统，然后使用以下命令加载：
```bash
staprun module_name.ko
```

例如，要为目标内核2.6.18 - 92.1.10.el5（x86_64架构）从名为simple.stp的SystemTap脚本创建检测模块simple.ko，可使用以下命令：
```bash
stap -r 2.6.18-92.1.10.el5 -e 'probe vfs.read {exit()}' -m simple
```

这将创建一个名为simple.ko的模块。要使用这个检测模块，将其复制到目标系统，并在目标系统上运行以下命令：
```bash
staprun simple.ko
```

**重要提示**：主机系统的架构和所运行的Linux发行版必须与目标系统相同，这样构建的检测模块才能正常工作。

### 2.3 运行SystemTap脚本
SystemTap附带了多个命令行工具，可用于监控系统活动。stap命令从SystemTap脚本读取探测指令，将这些指令转换为C代码，构建内核模块，并将其加载到正在运行的Linux内核中。staprun命令用于运行SystemTap检测，即运行在交叉检测过程中由SystemTap脚本构建的内核模块。

运行stap和staprun需要提升系统权限。由于并非所有用户都能获得root访问权限来运行SystemTap，因此可以通过将非特权用户添加到以下用户组之一，使其能够在自己的机器上运行SystemTap检测：
- **stapdev**：该组成员可以使用stap命令运行SystemTap脚本，或使用staprun运行SystemTap检测模块。运行stap命令需要将SystemTap脚本编译为内核模块并加载到内核中，此操作需要提升系统权限，而stapdev组成员被授予了这些权限。但需要注意的是，这些权限实际上也赋予了stapdev组成员root访问权限。因此，仅应将stapdev组成员身份授予那些您信任的、可拥有root访问权限的用户。
- **stapusr**：该组成员只能使用staprun命令运行SystemTap检测模块。此外，他们只能运行位于/lib/modules/kernel_version/systemtap/目录下的模块。请注意，此目录必须仅由root用户拥有，且仅可由root用户写入。

stap命令可从文件或标准输入读取SystemTap脚本。若要让stap从文件读取SystemTap脚本，需在命令行中指定文件名：
```bash
stap file_name
```
若要指示stap从标准输入读取SystemTap脚本，可使用`-`替换文件名。请注意，任何想要使用的命令行选项都必须在`-`之前插入。例如，为使stap命令的输出更详细，可输入：
```bash
echo "probe timer.s(1) {exit()}" | stap -v -
```
以下是一些常用的stap选项：
- **-v**：使SystemTap会话的输出更详细。可以多次重复此选项，以提供有关脚本执行的更多详细信息。例如：
```bash
stap -vvv script.stp
```
  当脚本运行遇到错误时，此选项特别有用。有关常见SystemTap脚本错误的更多信息，请参考第6章“理解SystemTap错误”。
- **-o file_name**：将标准输出发送到名为file_name的文件中。
- **-S size,count**：将输出文件的最大大小限制为size兆字节，最多存储count个文件。此选项为SystemTap实现了日志轮转操作，生成的文件名带有序列号后缀。
- **-x process_id**：将SystemTap处理函数`target()`设置为指定的进程ID。有关`target()`的更多信息，请参考SystemTap函数。
- **-c command**：将SystemTap处理函数`target()`设置为指定的命令，并在该命令执行期间运行SystemTap检测。有关`target()`的更多信息，请参考SystemTap函数。
- **-e script**：使用script而非文件作为SystemTap翻译器的输入。
- **-F**：使用SystemTap的飞行记录器模式，并使脚本在后台运行。有关飞行记录器模式的更多信息，请参考2.3.1节“SystemTap飞行记录器模式” 。

有关stap命令的更多信息，请参考stap(1)手册页。有关staprun命令和交叉检测的更多信息，请参考2.2节“为其他计算机生成检测代码”或staprun(8)手册页。

#### 2.3.1 SystemTap飞行记录器模式
SystemTap的飞行记录器模式允许长时间运行SystemTap脚本，并且只关注最近的输出。该模式会限制生成的输出量。

飞行记录器模式有两种变体：内存模式和文件模式。在这两种情况下，SystemTap脚本均作为后台进程运行。

##### 2.3.1.1 内存飞行记录器：
当飞行记录器模式未指定文件名时，SystemTap会使用内核内存中的缓冲区来存储脚本的输出。一旦加载了SystemTap检测模块且探针开始运行，检测操作就会分离并在后台运行。当感兴趣的事件发生时，可以重新连接到检测操作，查看内存缓冲区中的近期输出以及后续的持续输出。

要使用内存飞行记录器模式运行SystemTap脚本，可使用带`-F`命令行选项的stap命令：
```bash
stap -F iotime.stp
```

脚本启动后，stap会打印一条类似以下的消息，为您提供重新连接到正在运行的脚本的命令：
```
Disconnecting from systemtap module. To reconnect, type "staprun -A stap_5dd0073edcb1f13f7565d8c343063e68_19556"
```

当感兴趣的事件发生时，运行以下命令连接到当前正在运行的脚本，输出内存缓冲区中的近期数据，并获取持续输出：
```bash
staprun -A stap_5dd0073edcb1f13f7565d8c343063e68_19556
```

默认情况下，内核缓冲区大小为1MB。可以使用`-s`选项指定缓冲区大小（以兆字节为单位，向上取整到2的幂次方）来增大该值。例如，在SystemTap命令行中使用`-s2`将指定缓冲区大小为2MB。

##### 2.3.1.2 文件飞行记录器：
飞行记录器模式也可以将数据存储到文件中。可以使用`-S`选项，后跟两个用逗号分隔的数字参数来控制保留的文件数量和大小：第一个参数是每个输出文件的最大大小（以兆字节为单位），第二个参数是保留的最新文件数量。若要指定文件名，可使用`-o`选项，后跟文件名。SystemTap会自动为文件名添加数字后缀，以指示文件的顺序。

以下命令以文件飞行记录器模式启动SystemTap，输出到名为/tmp/pfaults.log.[0 - 9]+的文件中，每个文件大小为1MB或更小，并保留最新的两个文件：
```bash
stap -F -o /tmp/pfaults.log -S 1,2 pfaults.stp
```

该命令会将进程ID打印到标准输出。向该进程发送SIGTERM信号可终止SystemTap脚本并停止数据收集。例如，如果前面的命令列出的进程ID为7590，则以下命令将停止SystemTap脚本：
```bash
kill -s SIGTERM 7590
```

在这个例子中，脚本仅保留最近生成的两个文件，SystemTap会自动删除较旧的文件。因此，`ls -sh /tmp/pfaults.log.*`命令会列出两个文件：
```
1020K /tmp/pfaults.log.5 44K /tmp/pfaults.log.6
```

若要查看最新数据，可读取编号最高的文件，在本例中为/tmp/pfaults.log.6。 


## 第3章 理解SystemTap的工作原理
----
SystemTap允许用户编写并复用简单脚本，深入探究运行中的Linux系统的活动。这些脚本旨在快速（且安全地）提取、过滤和汇总数据，以诊断复杂的性能（甚至功能）问题。

SystemTap脚本的核心思想是定义事件并为其提供处理程序。当SystemTap运行脚本时，它会监测这些事件；一旦事件发生，Linux内核就会作为一个快速子例程运行相应的处理程序，然后继续执行。

事件有多种类型，如函数的进入/退出、定时器到期、会话终止等。处理程序是一系列脚本语言语句，用于指定事件发生时要执行的操作。这些操作通常包括从事件上下文中提取数据、将其存储到内部变量中，以及打印结果。

### 3.1 架构
当你运行一个SystemTap脚本时，一个SystemTap会话便开始了。这个会话按以下方式进行：
1. 首先，SystemTap会根据现有的tapset库（通常位于/usr/share/systemtap/tapset/）检查脚本中使用的任何tapset。SystemTap会用tapset库中的相应定义替换找到的tapset。
2. 然后，SystemTap将脚本翻译成C语言，并运行系统C编译器，根据脚本创建一个内核模块。执行此步骤的工具包含在systemtap软件包中（更多信息请参考2.1.1节 “安装SystemTap”）。
3. SystemTap加载该模块，然后启用脚本中的所有探针（事件和处理程序）。systemtap - runtime软件包中的staprun（更多信息请参考2.1.1节 “安装SystemTap”）提供了此功能。
4. 当事件发生时，其相应的处理程序会被执行。
5. 一旦SystemTap会话终止，探针会被禁用，内核模块也会被卸载。

这个过程由一个命令行程序stap驱动。这个程序是SystemTap的主要前端工具。关于stap的更多信息，请在SystemTap正确安装到你的机器上后，参考man stap命令。

### 3.2 SystemTap脚本
在大多数情况下，SystemTap脚本是每个SystemTap会话的基础。SystemTap脚本指示SystemTap收集何种类型的信息，以及在收集到这些信息后要执行的操作。

如第3章 “理解SystemTap的工作原理” 所述，SystemTap脚本由两个部分组成：事件和处理程序。一旦SystemTap会话开始，SystemTap就会监测操作系统中指定的事件，并在事件发生时执行处理程序。
- **注意**：一个事件及其相应的处理程序统称为一个探针。一个SystemTap脚本可以有多个探针。一个探针的处理程序通常被称为探针主体。

在应用程序开发方面，使用事件和处理程序类似于在程序的命令序列中插入诊断打印语句来对代码进行检测。这些诊断打印语句使你能够在程序运行后查看执行的命令历史。

SystemTap脚本允许在不重新编译代码的情况下插入检测代码，并且在处理程序方面提供了更大的灵活性。事件作为处理程序运行的触发器；可以指定处理程序记录特定数据并以特定方式打印它。
- **格式**：SystemTap脚本使用.stp文件扩展名，其中包含以下格式编写的探针：
  ```
  probe event {statements}
  ```
  SystemTap支持每个探针有多个事件；多个事件用逗号（,）分隔。如果在单个探针中指定了多个事件，那么当任何一个指定事件发生时，SystemTap都会执行处理程序。

  每个探针都有一个相应的语句块。这个语句块用花括号（{}）括起来，包含每次事件发生时要执行的语句。SystemTap按顺序执行这些语句；在多个语句之间通常不需要特殊的分隔符或终止符。

- **注意**：SystemTap脚本中的语句块遵循与C编程语言相同的语法和语义。一个语句块可以嵌套在另一个语句块中。

  SystemTap允许你编写函数，将多个探针使用的代码提取出来。这样，你无需在多个探针中重复编写相同的语句序列，而是可以将指令放在一个函数中，如下所示：
  ```
  probe event {function_name(arguments)} 
  function function_name(arguments) {statements}
  ```
  当事件的探针执行时，function_name中的语句也会被执行。参数是传递给函数的可选值。

- **重要提示**：3.2节 “SystemTap脚本” 旨在向读者介绍SystemTap脚本的基础知识。为了更好地理解SystemTap脚本，建议你参考第5章 “有用的SystemTap脚本”；其中的每一节都对脚本、其事件、处理程序和预期输出进行了详细解释。

#### 3.2.1 事件
SystemTap事件大致可分为两类：同步事件和异步事件。

- **同步事件**：当任何进程在内核代码的特定位置执行一条指令时，就会发生同步事件。这为其他事件提供了一个参考点，从这个点可以获取更多的上下文数据。

  同步事件的示例包括：
    - **syscall.system_call**：系统调用system_call的入口。如果你想要监测系统调用的退出，可以在事件后附加.return。例如，要指定close系统调用的入口和退出，分别使用syscall.close和syscall.close.return。
    - **vfs.file_operation**：虚拟文件系统（VFS）的file_operation事件的入口。与syscall事件类似，在事件后附加.return可以监测file_operation操作的退出。
    - **kernel.function("function")**：内核函数function的入口。例如，kernel.function("sys_open")指的是系统中任何线程调用内核函数sys_open时发生的 “事件”。要指定内核函数sys_open的返回，在事件语句后附加return字符串，即kernel.function("sys_open").return。

  定义探针事件时，可以使用星号（*）作为通配符。你还可以跟踪内核源文件中函数的入口或退出。考虑以下示例：
  ```
  probe kernel.function("*@net/socket.c") { }
  probe kernel.function("*@net/socket.c").return { }
  ```

  在前面的示例中，第一个探针的事件指定了内核源文件net/socket.c中所有函数的入口。第二个探针指定了所有这些函数的退出。请注意，在这个示例中，处理程序中没有语句，因此不会收集或显示任何信息。
    - **kernel.trace("tracepoint")**：tracepoint的静态探针。较新的内核（2.6.30及更高版本）包含了对内核中特定事件的检测。这些事件用tracepoint进行静态标记。systemtap中可用的一个tracepoint示例是kernel.trace("kfree_skb")，它表示每次在内核中释放网络缓冲区时的事件。
    - **module("module").function("function")**：允许你探测模块内的函数。例如：
      ```
        probe module("ext3").function("*") { } 
        probe module("ext3").function("*").return { }
      ```
      第一个探针指向ext3模块中所有函数的入口。第二个探针指向同一模块中所有函数的退出；.return后缀的使用与kernel.function()类似。请注意，示例3.2 “moduleprobe.stp” 中的探针在探针处理程序中不包含语句，因此不会打印任何有用的数据（与示例3.1 “wildcards.stp” 一样）。
      系统的内核模块通常位于/lib/modules/kernel_version中，其中kernel_version指的是当前加载的内核版本。模块使用.ko文件扩展名。

- **异步事件**：异步事件与代码中的特定指令或位置无关。这类探针点主要由计数器、定时器和类似的结构组成。

  异步事件的示例包括：
    - **begin**：SystemTap会话的启动；即，一旦SystemTap脚本开始运行。
    - **end**：SystemTap会话的结束。
    - **timer事件**：指定一个处理程序定期执行的事件。例如：
      ```bash
        probe timer.s(4) {
            printf("hello world\n")
        }
      ```
      示例3.3 “timer - s.stp” 是一个探针示例，它每4秒打印一次 “hello world”。也可以使用以下timer事件：
      ```bash
        timer.ms(milliseconds)
        timer.us(microseconds)
        timer.ns(nanoseconds)
        timer.hz(hertz)
        timer.jiffies(jiffies)
      ```
      当与其他收集信息的探针结合使用时，timer事件可以让你打印定期更新，并查看这些信息随时间的变化。

- **重要提示**：SystemTap支持大量的探针事件。有关支持的事件的更多信息，请参考man stapprobes。man stapprobes的 “SEE ALSO” 部分还包含指向其他man页面的链接，这些页面讨论了特定子系统和组件支持的事件。

#### 3.2.2 SystemTap处理程序/主体
考虑以下示例脚本：
```bash
probe begin {
  printf ("hello world\n")
  exit ()
}
```

在示例3.4 “helloworld.stp” 中，事件begin（即会话的开始）触发了花括号内的处理程序，该处理程序只是打印 “hello world” 并换行，然后退出。

SystemTap脚本会一直运行，直到exit()函数执行。如果用户想要停止脚本的执行，可以手动使用Ctrl + C中断。

- **printf()语句**：printf()语句是用于打印数据的最简单函数之一。printf()还可以使用各种SystemTap函数以以下格式显示数据：
  ```bash
    printf ("format string\n", arguments)
  ```
  格式字符串指定了参数应如何打印。示例3.4 “helloworld.stp” 的格式字符串指示SystemTap打印 “hello world”，并且不包含格式说明符。

  你可以在格式字符串中使用格式说明符%s（用于字符串）和%d（用于数字），具体取决于你的参数列表。格式字符串可以有多个格式说明符，每个说明符对应一个相应的参数；多个参数用逗号（,）分隔。

  从语义上讲，SystemTap的printf函数与C语言中的printf函数非常相似。上述SystemTap的printf函数的语法和格式与C风格的printf相同。

  为了说明这一点，考虑以下探针示例：
  ```bash
    probe syscall.open {
    printf ("%s(%d) open\n", execname(), pid())
    }
  ```

- **注意**：示例3.5 “variables - in - printf - statements.stp” 指示SystemTap探测所有对open系统调用的入口；对于每个事件，它打印当前的execname()（一个包含可执行文件名的字符串）和pid()（当前进程ID号），然后是单词 “open”。这个探针的输出片段可能如下所示：
  ```log
    hald(2360) open 
    vmware - guestd(2206) open 
    hald(2360) open 
    hald(2360) open 
    df(3433) open 
    df(3433) open 
    df(3433) open 
    hald(2360) open
  ```

- **SystemTap函数**：SystemTap支持多种函数，这些函数可用作printf()的参数。示例3.5 “variables - in - printf - statements.stp” 使用了SystemTap函数execname()（调用内核函数/执行系统调用的进程的名称）和pid()（当前进程ID）。

  以下是一些常用的SystemTap函数：
    - **tid()**：当前线程的ID。
    - **uid()**：当前用户的ID。
    - **cpu()**：当前CPU编号。
    - **gettimeofday_s()**：自UNIX纪元（1970年1月1日）以来的秒数。
    - **ctime()**：将自UNIX纪元以来的秒数转换为日期。
    - **pp()**：一个描述当前正在处理的探针点的字符串。
    - **thread_indent()**：这个函数在更好地组织打印结果方面非常有用。该函数接受一个参数，即缩进增量，它表示要在一个线程的 “缩进计数器” 中添加或删除多少个空格。然后它返回一个字符串，其中包含一些通用的跟踪数据以及适当数量的缩进空格。

      返回字符串中包含的通用数据包括一个时间戳（自线程首次调用thread_indent()以来的微秒数）、一个进程名称和线程ID。这使你能够识别调用了哪些函数、谁调用了它们以及每个函数调用的持续时间。

      如果函数调用的入口和出口紧挨着出现，很容易匹配它们。然而，在大多数情况下，在第一个函数调用入口之后，可能会有其他几个函数调用的入口和出口，然后第一个调用才会退出。缩进计数器通过对下一个函数调用进行缩进（如果它不是前一个函数的出口），帮助你将一个入口与其相应的出口匹配起来。

      考虑以下关于使用thread_indent()的示例：
      ```bash
        probe kernel.function("*@net/socket.c").call {
            printf ("%s -> %s\n", thread_indent(1), probefunc())
        }
        probe kernel.function("*@net/socket.c").return {
            printf ("%s <- %s\n", thread_indent(-1), probefunc())
        }
      ```
      示例3.6 “thread_indent.stp” 以以下格式在每个事件中打印thread_indent()和probe函数：
      ```log
        0 ftp(7223): -> sys_socketcall
        1159 ftp(7223): -> sys_socket
        2173ftp(7223): ->sys_socket
        2173 ftp(7223): -> __sock_create
        2286 ftp(7223): -> sock_alloc_inode
        2286ftp(7223): 
        3349 ftp(7223): -> sock_alloc 
        2737 ftp(7223): <- sock_alloc_inode
        2737 ftp(7223): 
        ->sock_alloc
        3417 ftp(7223): <-sock_alloc
        3389 ftp(7223): <- sock_alloc
        4117 ftp(7223): -> sock_create 
        3417 ftp(7223): <- __sock_create
        ->sock_create
        4160ftp(7223):
        4301 ftp(7223): -> sock_map_fd 
        4160 ftp(7223): <- sock_create
        4644 ftp(7223): ->sock_map_fd
        4644 ftp(7223): -> sock_map_file
        4715 ftp(7223): <- sock_map_fd 
        4699 ftp(7223): <- sock_map_file
        4699 ftp(7223):
        <-sock_map_fd
        4732 ftp(7223): <- sys_socket
        <-sys_socket
        4775 ftp(7223): <- sys_socketcall
      ```
      这个示例输出包含以下信息：
        - 自线程首次调用thread_indent()以来的时间（以微秒为单位，包含在thread_indent()返回的字符串中）。
        - 进行函数调用的进程名称（及其相应的ID，包含在thread_indent()返回的字符串中）。
        - 一个箭头，表示调用是入口（<-）还是出口（->）；缩进有助于你将特定的函数调用入口与其相应的出口匹配起来。
        - 进程调用的函数名称。
    - **name**：标识特定系统调用的名称。这个变量只能在使用事件syscall.system_call的探针中使用。
    - **target()**：与stap脚本的 -x process ID或stap脚本的 -c command结合使用。如果你想指定一个脚本接受一个进程ID或命令作为参数，可以在脚本中使用target()作为变量来引用它。例如：
      ```
        probe syscall.* { 
        if (pid() == target())
            printf("%s\n", name)
        }
      ```

      当示例3.7 “targetexample.stp” 以参数 -x process ID运行时，它会监视所有系统调用（由事件syscall.*指定），并打印出指定进程进行的所有系统调用的名称。

      这与每次想要针对特定进程时指定if (pid() == process ID) 的效果相同。然而，使用target()使你更容易复用脚本，让你能够在每次运行脚本时传递一个进程ID作为参数（即stap targetexample.stp -x process ID）。

      有关支持的SystemTap函数的更多信息，请参考man stapfuncs。

### 3.3 基本的SystemTap处理程序构造
SystemTap在处理程序中支持使用几种基本构造。这些处理程序构造的语法大多基于C和awk语法。本节介绍几种最有用的SystemTap处理程序构造，这些内容应该能为你提供足够的信息，让你编写简单但有用的SystemTap脚本。

#### 3.3.1 变量
变量可在处理程序中随意使用，只需选定一个名称，将函数或表达式的值赋给它，就能在表达式中使用。SystemTap会依据赋给变量的值的类型，自动判断该变量应被定义为字符串型还是整型。例如，如果将变量`foo`设为`gettimeofday_s()`（即`foo = gettimeofday_s()`），那么`foo`会被识别为数字型，可在`printf()`函数中使用整数格式说明符（`%d`）进行打印。

不过，默认情况下变量仅在其所在的探针内有效。这意味着，变量在每次探针处理程序调用时被初始化、使用，之后便会被释放。 **若要在多个探针间共享变量，需在探针外部使用`global`声明变量名。** 参考下面这个例子：

```bash
global count_jiffies, count_ms
probe timer.jiffies(100) { 
    count_jiffies ++ 
}
probe timer.ms(100) { 
    count_ms ++ 
}
probe timer.ms(12345) {
    hz=(1000*count_jiffies) / count_ms
    printf ("jiffies:ms ratio %d:%d => CONFIG_HZ=%d\n", count_jiffies, count_ms, hz)
    exit ()
}
```
在示例3.8 “timer-jiffies.stp” 中，脚本通过统计定时器记录的jiffies和毫秒数，来计算内核的`CONFIG_HZ`设置。`global`声明使得脚本能够在`timer.ms(12345)`探针中，使用在其他探针中设置的`count_jiffies`和`count_ms`变量。
- **注意**：在示例3.8 “timer-jiffies.stp” 中，`++`符号（即`count_jiffies ++`和`count_ms ++`）用于将变量的值自增1。在下面这个探针中，每100个jiffies，`count_jiffies`就会自增1：
  ```bash
    probe timer.jiffies(100) { 
        count_jiffies ++ 
    }
  ```

  在这种情况下，SystemTap会识别出`count_jiffies`是一个整数。由于没有给`count_jiffies`赋初始值，它的默认初始值为零。

#### 3.3.2 目标变量
映射到代码中实际位置的探针事件（例如`kernel.function("function")`和`kernel.statement("statement")`），允许使用目标变量来获取在代码中该位置可见的变量值。可以使用`-L`选项列出在某个探针点可用的目标变量。如果为正在运行的内核安装了调试信息，可运行以下命令来查看`vfs_read`函数有哪些可用的目标变量：
```bash
    stap -L 'kernel.function("vfs_read")'
```

这会输出类似下面的内容：

```bash
    kernel.function("vfs_read@fs/read_write.c:277") $file:struct file* $buf:char* $count:size_t $pos:loff_t*
```

每个目标变量前面都有一个`$`，目标变量的类型紧跟在“:”后面。内核的`vfs_read`函数在入口处有`$file`（指向描述文件的结构体的指针）、`$buf`（指向用于存储读取数据的用户空间内存的指针）、`$count`（要读取的字节数）和`$pos`（从文件中开始读取的位置）这些目标变量。

当目标变量并非探针点的局部变量时，比如全局外部变量，或者在其他文件中定义的文件局部静态变量，可以通过“@var("varname@src/file.c")”来引用它。也支持指定可执行文件或库文件路径作为第二个参数，如“@var("varname", "/path/to/exe/or/lib")”。

SystemTap会跟踪目标变量的类型信息，并且可以使用`->`操作符来查看结构体的字段。`->`操作符可以链式使用，用于查看包含在其他数据结构中的数据结构，以及跟随指针查看其他数据结构。无论访问子结构体中的字段，还是通过指针访问其他结构体，都使用`->`操作符来获取结构体字段中的值。例如，要访问定义在`fs/file_table.c`中的静态`files_stat`目标变量的一个字段（该变量保存了当前文件系统的一些sysctl可调参数），可以这样写：

```bash
    stap -e 'probe kernel.function("vfs_read") { printf ("current files_stat max_files: %d\n", @var("files_stat@fs/file_table.c")->max_files); exit(); }'
```

这会输出类似下面的内容：
```
current files_stat max_files: 386070
```

对于指向基本类型（如整数和字符串）的指针，有以下一些函数可用于访问内核空间数据。每个函数的第一个参数都是指向数据项的指针。在4.2节“访问用户空间目标变量”中，也有类似的函数用于访问用户空间代码中的目标变量。
- `kernel_char(address)`：从内核内存中的`address`处获取字符。
- `kernel_short(address)`：从内核内存中的`address`处获取短整型数据。
- `kernel_int(address)`：从内核内存中的`address`处获取整型数据。
- `kernel_long(address)`：从内核内存中的`address`处获取长整型数据。
- `kernel_string(address)`：从内核内存中的`address`处获取字符串。
- `kernel_string_n(address, n)`：从内核内存中的`address`处获取字符串，并将字符串长度限制为`n`字节。

##### 3.3.2.1 美化打印目标变量
SystemTap脚本常被用于观察代码内部的运行情况。在很多情况下，仅仅打印各种上下文变量的值就足够了。SystemTap提供了一些操作，能够为目标变量生成可打印的字符串：
- `$$vars`：扩展为一个字符字符串，等同于`sprintf("parm1=%x ... parmN=%x var1= %x ... varN=%x", parm1, ..., parmN, var1, ..., varN)`，其中包含探针点作用域内的每个变量。如果某些值的运行时位置无法找到，可能会被打印为“=?”。
- `$$locals`：扩展为`$$vars`的一个子集，仅包含局部变量。
- `$$parms`：扩展为`$$vars`的一个子集，仅包含函数参数。
- `$$return`：仅在返回探针中可用。如果被探测的函数有返回值，它会扩展为一个等同于`sprintf("return= %x", $return)`的字符串，否则为一个空字符串。

下面是一个命令行脚本，用于打印传递给`vfs_read`函数的参数值：

```bash
    stap -e 'probe kernel.function("vfs_read") {printf("%s\n", $$parms); exit(); }'
```

有四个参数被传递给`vfs_read`函数：`file`、`buf`、`count`和`pos`。`$$parms`会为传递给函数的参数生成一个字符串。在这个例子中，除了`count`参数外，其他参数都是指针。下面是上述命令行脚本的输出示例：
```
    file=0xffff8800b40d4c80 buf=0x7fff634403e0 count=0x2004 pos=0xffff8800af96df48
```
获取指针所指向的地址可能用处不大，而指针所指向的数据结构的字段可能更有用。使用`$`后缀可以美化打印数据结构。下面的命令行示例使用美化打印后缀，来打印传递给`vfs_read`函数的数据结构的更多详细信息：

```bash
    stap -e 'probe kernel.function("vfs_read") {printf("%s\n", $$parms$); exit(); }'
```

上述命令行将生成类似下面的输出，其中包含数据结构的字段信息：

```
    file={.f_u={...}, .f_path={...}, .f_op=0xffffffffa06e1d80, .f_lock={...}, .f_count={...}, .f_flags=34818, .f_mode=3
    buf="" count=8196 pos=-131938753921208
```

使用`$`后缀时，由数据结构组成的字段不会被展开。“$$”后缀则会打印嵌套数据结构中的值。下面是一个使用`$$`后缀的示例：

```bash
    stap -e 'probe kernel.function("vfs_read") {printf("%s\n", $$parms$$); exit(); }'
```

与所有字符串一样，`$$`后缀受最大字符串大小的限制。下面是上述命令行脚本的一个代表性输出，由于字符串大小限制，输出被截断：

```
    file={.f_u={.fu_list={.next=0xffff8801336ca0e8, .prev=0xffff88012ded0840}, .fu_rcuhead={.next=0xffff8801336c
```

##### 3.3.2.2 类型转换
在大多数情况下，SystemTap可以从调试信息中确定变量的类型。然而，代码可能会对变量使用`void`指针（例如内存分配例程），这时就没有类型信息。此外，在探针处理程序中可用的类型信息，在函数内部不可用；SystemTap函数的参数使用`long`类型来代替有类型的指针。SystemTap的`@cast`操作符（从SystemTap 0.9版本开始可用）可用于指定对象的正确类型。

示例3.9 “Casting Example” 来自`task.stp` tapset。该函数返回由`long`类型的`task`指向的`task_struct`结构体中`state`字段的值。`@cast`操作符的第一个参数`task`是指向对象的指针，第二个参数是要将对象转换的类型`task_struct`，第三个参数列出类型定义信息所在的文件，该参数是可选的。通过`@cast`操作符，可以访问这个特定`task_struct`结构体`task`的各个字段；在这个例子中，获取的是`state`字段的值。

```bash
    function task_state:long (task:long) {
        return @cast(task, "task_struct", "kernel<linux/sched.h>")->state
    }
```

##### 3.3.2.3 检查目标变量的可用性
随着代码的演进，可用的目标变量可能会发生变化。`@defined`操作符能更方便地处理目标变量可用性的变化。它用于测试某个特定的目标变量是否可用，测试结果可用于选择合适的表达式。

示例3.10 “Testing target variable available Example” 来自`memory.stp` tapset，它提供了一个探针事件别名。在被探测的内核函数的某些版本中，存在一个`$flags`参数。当该参数可用时，会用它来生成局部变量`write_access`。而在没有`$flags`参数的内核函数版本中，则使用`$write`参数来生成`write_access`局部变量。

```bash
probe vm.pagefault = kernel.function("__handle_mm_fault@mm/memory.c") ?,
kernel.function("handle_mm_fault@mm/memory.c") ? {
    write_access = (@defined($flags) ? $flags & FAULT_FLAG_WRITE : $write)
    name = "pagefault"
    address = $address
}
```

#### 3.3.3 条件语句
在某些情况下，SystemTap脚本的输出可能会过多。为了解决这个问题，需要进一步优化脚本逻辑，以便将输出限定为与探针更相关或更有用的内容。

可以通过在处理程序中使用条件语句来实现这一点。SystemTap支持以下几种条件语句：

##### If/Else语句
格式：

```
if (condition)
    statement1
else
    statement2
```

如果条件表达式的值非零，则执行`statement1`；如果条件表达式的值为零，则执行`statement2`。`else`子句（`else statement2`）是可选的。`statement1`和`statement2`都可以是语句块。

```bash
global countread, countnonread
probe kernel.function("vfs_read"),kernel.function("vfs_write") {
    if (probefunc()=="vfs_read")
        countread ++
    else
        countnonread ++
}
probe timer.s(5) { 
    exit() 
}
probe end {
    printf("VFS reads total %d\n VFS writes total %d\n", countread, countnonread)
}
```

示例3.11 “ifelse.stp” 是一个脚本，用于统计系统在5秒内执行的虚拟文件系统读取（`vfs_read`）和写入（`vfs_write`）操作的次数。运行该脚本时，如果探测到的函数名与`vfs_read`匹配（由条件`if (probefunc()=="vfs_read")`判断），则将变量`countread`的值增加1；否则，增加`countnonread`的值（`else {countnonread ++}`）。

##### While循环
格式：
```
    while (condition)
        statement
```

只要条件的值非零，就会执行`statement`中的语句块。`statement`通常是一个语句块，并且必须改变某个值，以便条件最终变为零。

##### For循环
格式：
```bash
    for (initialization; conditional; increment)
        statement
```

`for`循环是`while`循环的简写形式。以下是与之等价的`while`循环：

```bash
    initialization
    while (conditional) {
        statement
        increment
    }
```

##### 条件运算符
除了`==`（“等于”）之外，条件语句中还可以使用以下运算符：
- `>=`：大于或等于
- `<=`：小于或等于
- `!=`：不等于

#### 3.3.4 命令行参数
SystemTap脚本还可以接受简单的命令行参数，使用`$`或`@`，紧接着命令行参数的序号。如果期望用户输入整数作为命令行参数，使用`$`；如果期望输入字符串，则使用`@`。

```bash
probe kernel.function(@1) { }
probe kernel.function(@1).return { }
```

示例3.12 “commandlineargs.stp” 与示例3.1 “wildcards.stp” 类似，不同之处在于它允许将要探测的内核函数作为命令行参数传递（例如`stap commandlineargs.stp kernel function`）。也可以指定脚本接受多个命令行参数，按照用户输入的顺序，将它们记为`@1`、`@2`等。

### 3.4 关联数组
SystemTap还支持使用关联数组。普通变量代表单个值，而关联数组可以代表一组值。简单来说，关联数组是一组唯一的键，数组中的每个键都有一个与之关联的值。

由于关联数组通常在多个探针中处理（后面会演示），因此在SystemTap脚本中应将它们声明为全局变量。访问关联数组中元素的语法与awk类似，如下所示：

```
array_name[index_expression]
```

这里，`array_name`是数组使用的任意名称。`index_expression`用于引用数组中特定的唯一键。举例来说，假设要构建一个名为`foo`的数组，用于指定三个人（`tom`、`dick`和`harry`，这些是唯一键）的年龄。要分别给他们赋值为23、24和25，可以使用以下数组语句：

```bash
foo["tom"] = 23
foo["dick"] = 24
foo["harry"] = 25
```

在数组语句中，最多可以指定九个索引表达式，每个表达式用逗号（,）分隔。如果希望键包含多个信息，这会很有用。下面来自`disktop.stp`的代码行，使用了5个元素作为键：进程ID、可执行文件名、用户ID、父进程ID和字符串“W”，并将`devname`与该键关联起来：

```bash
device[pid(),execname(),uid(),ppid(),"W"] = devname
```

**重要提示**：所有关联数组都必须声明为全局变量，无论该关联数组在一个还是多个探针中使用。

### 3.5 SystemTap中的数组操作
本节列举了SystemTap中一些最常用的数组操作。

#### 3.5.1 分配关联值
使用`=`为索引的唯一键值对设置关联值，就像这样：

```bash
array_name[index_expression] = value
```

示例3.13“基本数组语句”展示了一个非常基础的示例，说明如何为唯一键设置明确的关联值。你还可以将处理函数同时用作索引表达式和值。例如，你可以使用数组将时间戳作为关联值与进程名关联起来（你希望将进程名作为唯一键），如下所示：

```bash
foo[tid()] = gettimeofday_s()
```

每当一个事件调用示例3.14“将时间戳关联到进程名”中的语句时，SystemTap会返回相应的`tid()`值（即线程的ID，它被用作唯一键）。同时，SystemTap还会使用`gettimeofday_s()`函数将相应的时间戳设置为`tid()`函数定义的唯一键的关联值。这就创建了一个由包含线程ID和时间戳的键值对组成的数组。

在同一个示例中，如果`tid()`返回的值在数组`foo`中已经存在，该操作符会丢弃原来的关联值，并用`gettimeofday_s()`当前的时间戳替换它。

#### 3.5.2 从数组读取值
你也可以像读取变量值一样从数组中读取值。为此，在数学表达式中包含`array_name[index_expression]`语句即可。例如：

```bash
delta = gettimeofday_s() - foo[tid()]
```

这个例子假设数组`foo`是使用示例3.14“将时间戳关联到进程名”（在3.5.1节“分配关联值”中）的结构构建的。这设置了一个时间戳作为参考点，用于计算`delta`。

示例3.15“在简单计算中使用数组值”中的结构通过从当前的`gettimeofday_s()`中减去键`tid()`的关联值来计算变量`delta`的值。这个结构通过从数组中读取`tid()`的值来实现这一点。这个特定的结构对于确定两个事件之间的时间非常有用，例如读取操作的开始和完成之间的时间。

如果索引表达式找不到唯一键，默认情况下，对于数值运算（如示例3.15“在简单计算中使用数组值”），它将返回0；对于字符串运算，它将返回空字符串。

#### 3.5.3 增加关联值
使用`++`来增加数组中唯一键的关联值，如下所示：

```bash
array_name[index_expression] ++
```

同样，你也可以将处理函数用作索引表达式。例如，如果你想统计特定进程对虚拟文件系统执行读取操作（使用事件`vfs.read`）的次数，可以使用以下探针：

```bash
probe vfs.read {
    reads[execname()] ++
}
```

在示例3.16“vfsreads.stp”中，当探针第一次返回进程名`gnome-terminal`（即`gnome-terminal`第一次执行VFS读取）时，该进程名被设置为唯一键`gnome-terminal`，关联值为1。下一次探针返回进程名`gnome-terminal`时，SystemTap会将`gnome-terminal`的关联值增加1。SystemTap会对探针返回的所有进程名执行此操作。

#### 3.5.4 处理数组中的多个元素
一旦你在数组中收集了足够的信息，就需要检索并处理该数组中的所有元素，使其发挥作用。以示例3.16“vfsreads.stp”为例，该脚本收集了每个进程执行VFS读取次数的信息，但没有说明如何处理这些信息。让示例3.16“vfsreads.stp”有用的一个明显方法是打印数组`reads`中的键值对，但该怎么做呢？
- **注意**：处理数组中所有键值对（作为迭代）的最佳方法是使用`foreach`语句。考虑以下示例：

```bash
global reads
probe vfs.read {
    reads[execname()] ++
}
probe timer.s(3) {
    foreach (count in reads) {
        printf("%s : %d \n", count, reads[count])
    }
}
```

在示例3.17“cumulative-vfsreads.stp”的第二个探针中，`foreach`语句使用变量`count`来引用数组`reads`中唯一键的每次迭代。同一探针中的`reads[count]`数组语句检索每个唯一键的关联值。

根据我们对示例3.17“cumulative-vfsreads.stp”中第一个探针的了解，该脚本每3秒打印一次VFS读取统计信息，显示执行VFS读取的进程名称以及相应的VFS读取计数。

现在，请记住，示例3.17“cumulative-vfsreads.stp”中的`foreach`语句会打印数组中所有进程名的迭代，且没有特定顺序。你可以使用`+`（升序）或`-`（降序）指示脚本按特定顺序处理迭代。此外，还可以使用`limit value`选项限制脚本需要处理的迭代次数。

例如，考虑以下替换探针：

```bash
probe timer.s(3) {
    foreach (count in reads- limit 10) {
        printf("%s : %d \n", count, reads[count])
    }
}
```

这个`foreach`语句指示脚本按关联值降序处理数组`reads`中的元素。`limit 10`选项指示`foreach`仅处理前10次迭代（即打印前10个，从最高值开始）。

#### 3.5.5 清除/删除数组和数组元素
有时，你可能需要清除数组元素中的关联值，或者重置整个数组以便在另一个探针中重新使用。3.5.4节“处理数组中的多个元素”中的示例3.17“cumulative-vfsreads.stp”可让你跟踪每个进程的VFS读取次数随时间的增长情况，但它不会显示每个进程每3秒进行的VFS读取次数。

要实现这一点，你需要清除数组中累积的值。你可以使用`delete`操作符删除数组中的元素或整个数组。考虑以下示例：

```bash
global reads
probe vfs.read {
    reads[execname()] ++
}
probe timer.s(3) {
    foreach (count in reads) {
        printf("%s : %d \n", count, reads[count])
    }
    delete reads
}
```

在示例3.18“noncumulative-vfsreads.stp”中，第二个探针仅打印在被探测的3秒内每个进程进行的VFS读取次数。`delete reads`语句在该探针内清除`reads`数组。

#### 3.5.6 在条件语句中使用数组
你也可以在`if`语句中使用关联数组。如果你希望在数组中的某个值满足特定条件时执行一个子例程，这会很有用。考虑以下示例：

```bash
global reads
probe vfs.read {
    reads[execname()] ++
}
probe timer.s(3) {
    printf("=======\n")
    foreach (count in reads-) {
        if (reads[count] >= 1024) {
            printf("%s : %dkB \n", count, reads[count]/1024)
        } else {
            printf("%s : %dB \n", count, reads[count])
        }
    }
}
```

每隔三秒，示例3.19“vfsreads-print-if-1kb.stp”会打印出所有进程的列表，以及每个进程执行VFS读取的次数。如果进程名的关联值大于或等于1024，脚本中的`if`语句会将其转换为以kB为单位并打印出来。

##### 测试成员资格
你还可以测试特定的唯一键是否是数组的成员。此外，数组成员资格可以在`if`语句中使用，如下所示：
```bash
if([index_expression] in array_name)
    statement
```

为了说明这一点，考虑以下示例：

```bash
global reads
probe vfs.read {
    reads[execname()] ++
}
probe timer.s(3) {
    printf("=======\n")
    foreach (count in reads+) {
        if(["stapio"] in reads) {
            printf("%s : %d \n", count, reads[count])
            printf("stapio read detected, exiting\n")
            exit()
        }
    }
}
```

`if(["stapio"] in reads)`语句指示脚本一旦唯一键`stapio`被添加到数组`reads`中，就打印`stapio read detected, exiting`。

#### 3.5.7 计算统计聚合
统计聚合用于收集数值统计信息，在需要快速大量累积新数据（即仅存储聚合的流统计信息）的场景中非常重要。统计聚合可用于全局变量或作为数组中的元素。

要向统计聚合中添加值，使用操作符`<<< value`。

```bash
global reads
probe vfs.read {
    reads[execname()] <<< $count
}
```

在示例3.21“stat-aggregates.stp”中，操作符`<<< $count`将`$count`返回的数量存储到`reads`数组中相应`execname()`的关联值中。请记住，这些值是存储起来的；它们不会被添加到每个唯一键的关联值中，也不会用于替换当前的关联值。可以这样理解，每个唯一键（`execname()`）都有多个关联值，每次探针处理程序运行时都会累积。
- **注意**：在示例3.21“stat-aggregates.stp”的上下文中，`count`返回由`execname()`返回的进程对虚拟文件系统读取的数据量。

要提取由统计聚合收集的数据，使用语法格式`@extractor(variable/array index expression)`。`extractor`可以是以下任何一个整数提取器：
- **count**：返回存储到变量/数组索引表达式中的所有值的数量。以示例3.21“stat-aggregates.stp”中的示例探针为例，表达式`@count(reads[execname()])`将返回数组`reads`中每个唯一键存储的值的数量。
- **sum**：返回存储到变量/数组索引表达式中的所有值的总和。同样以示例3.21“stat-aggregates.stp”中的示例探针为例，表达式`@sum(reads[execname()])`将返回数组`reads`中每个唯一键存储的所有值的总和。
- **min**：返回存储在变量/数组索引表达式中的所有值中的最小值。
- **max**：返回存储在变量/数组索引表达式中的所有值中的最大值。
- **avg**：返回存储在变量/数组索引表达式中的所有值的平均值。

使用统计聚合时，你还可以构建使用多个索引表达式（最多5个）的数组结构。这有助于在探针过程中捕获更多上下文信息。例如：

```bash
global reads
probe vfs.read {
    reads[execname(),pid()] <<< 1
}
probe timer.s(3) {
    foreach([var1,var2] in reads) {
        printf("%s (%d) : %d \n", var1, var2, @count(reads[var1,var2]))
    }
}
```

在示例3.22“多个数组索引”中，第一个探针跟踪每个进程执行VFS读取的次数。与前面的示例不同的是，这个数组将执行的读取操作同时关联到进程名及其相应的进程ID。

示例3.22“多个数组索引”中的第二个探针展示了如何处理和打印由数组`reads`收集的信息。注意`foreach`语句如何使用与第一个探针中数组`reads`首次实例相同数量的变量（即`var1`和`var2`）。

### 3.6 Tapsets
Tapsets是一种脚本，构成了预编写的探针和函数库，可在SystemTap脚本中使用。当用户运行SystemTap脚本时，SystemTap会根据tapset库检查脚本的探针事件和处理程序；然后在将脚本转换为C代码之前，加载相应的探针和函数（有关SystemTap会话中具体过程的信息，请参阅3.1节“架构”）。

与SystemTap脚本一样，tapsets使用.stp作为文件名扩展名。默认情况下，标准的tapset库位于/usr/share/systemtap/tapset/目录下。然而，与SystemTap脚本不同的是，tapsets并非用于直接执行；相反，它们构成了一个库，其他脚本可以从中提取定义。

tapset库是一个抽象层，旨在让用户更轻松地定义事件和函数。Tapsets为用户可能想要指定为事件的函数提供了有用的别名；在很大程度上，记住合适的别名比记住可能因内核版本而异的特定内核函数要容易得多。

在3.2.1节“事件”和SystemTap函数中，有几个处理程序和函数是在tapsets中定义的。例如，thread_indent()函数是在indent.stp中定义的。


## 第4章 用户空间探测
----
SystemTap最初专注于内核空间探测。由于在很多情况下，用户空间探测有助于诊断问题，SystemTap 0.6版本增加了对用户空间进程进行探测的支持。SystemTap可以探测用户空间进程中函数的进入和返回、探测用户空间代码中的预定义标记，以及监控用户进程事件。

SystemTap需要uprobes模块来执行用户空间探测。如果你的Linux内核版本为3.5或更高，它已经包含了uprobes。要验证当前内核是否原生支持uprobes，可运行以下命令：

```bash
grep CONFIG_UPROBES /boot/config-`uname -r`
```

如果uprobes已集成，此命令的输出如下：

```
CONFIG_UPROBES=y
```

### 4.1 用户空间事件
所有用户空间事件探针都以process开头。你可以通过指定进程ID将进程事件限制为特定的运行进程。也可以通过指定可执行文件的路径（PATH）来限制进程事件，以监控特定的可执行文件。SystemTap利用PATH环境变量，这使得你既可以使用在命令行中启动可执行文件时使用的名称，也可以使用可执行文件的绝对路径。

一些用户空间探针事件将其作用域限制为特定的可执行文件名（PATH），因为SystemTap必须使用调试信息来静态分析放置探针的位置。但对于许多用户空间探针事件，进程ID和可执行文件名是可选的。以下列出的任何包含进程ID或可执行文件路径的进程事件，都必须包含这些参数。而对于未列出这些参数的进程事件，进程ID和可执行文件路径是可选的：
- **process("PATH").function("function")**：可执行文件PATH中用户空间函数function的入口。此事件是kernel.function("function")事件在用户空间的对应事件。它允许在function中使用通配符，并支持.return后缀。
- **process("PATH").statement("statement")**：statement代码中的最早指令。这是kernel.statement("statement")在用户空间的对应事件。
- **process("PATH").mark("marker")**：PATH中定义的静态探针点marker。你可以在marker中使用通配符，通过单个探针指定多个标记。静态探针点可能还会有编号参数（`$`1、`$`2等）可供探针使用。
  多种用户空间软件包（如Java）包含这些静态探针点。大多数提供静态探针点的软件包也会为原始的用户空间标记事件提供别名。以下是x86_64架构的Java HotSpot JVM的一个此类别名示例：
  ```
  probe hotspot.gc_begin = process("/usr/lib/jvm/java-1.6.0-openjdk-1.6.0.0.x86_64/jre/lib/amd64/server/libjvm.so").mark("gc__begin")
  ```

- **process.begin**：一个用户空间进程被创建。你可以将其限制为特定的进程ID或可执行文件的完整路径。
- **process.thread.begin**：一个用户空间线程被创建。你可以将其限制为特定的进程ID或可执行文件的完整路径。
- **process.end**：一个用户空间进程终止。你可以将其限制为特定的进程ID或可执行文件的完整路径。
- **process.thread.end**：一个用户空间线程被销毁。你可以将其限制为特定的进程ID或可执行文件的完整路径。
- **process.syscall**：一个用户空间进程进行系统调用。系统调用号可在`$`syscall上下文变量中获取，前六个参数可在`$`arg1到`$`arg6中获取。.return后缀将探针放置在系统调用返回处。对于syscall.return，返回值可通过`$`return上下文变量获取。你可以将其限制为特定的进程ID或可执行文件的完整路径。

### 4.2 访问用户空间目标变量
你可以按照3.3.2节“目标变量”中描述的相同方式访问用户空间目标变量。然而，在Linux中，用户代码和内核代码有单独的地址空间。当使用->操作符时，SystemTap会访问相应的地址空间。

对于指向整数和字符串等基本类型的指针，有以下几个函数可用于访问用户空间数据。每个函数的第一个参数都是指向数据项的指针。
- **user_char(address)**：获取当前用户进程中address处的字符。
- **user_short(address)**：获取当前用户进程中address处的短整型。
- **user_int(address)**：获取当前用户进程中address处的整型。
- **user_long(address)**：获取当前用户进程中address处的长整型。
- **user_string(address)**：获取当前用户进程中address处的字符串。
- **user_string_n(address, n)**：获取当前用户进程中address处的字符串，并将字符串长度限制为n字节。

### 4.3 用户空间栈回溯
探针点（pp）函数指示是哪个特定事件触发了SystemTap事件处理程序。对函数入口的探针会列出函数名称。然而，在许多情况下，同一个探针点事件可能由程序中的多个不同模块触发；对于共享库中的函数来说，这种情况尤为常见。用户空间栈的SystemTap回溯可以提供关于探针点事件如何被触发的更多上下文信息。

用户空间栈回溯的生成较为复杂，因为编译器生成的优化代码可能会消除栈帧指针。不过，编译器也会在调试信息部分包含相关信息，以便调试工具生成栈回溯。SystemTap用户空间栈回溯机制利用这些调试信息来遍历栈，为32位和64位x86处理器生成栈跟踪；其他处理器架构目前还不支持使用调试信息来展开用户空间栈。为确保使用所需的调试信息来生成用户空间栈回溯，对于可执行文件使用-d executable选项，对于共享库使用--ldd选项。

例如，你可以使用用户空间回溯函数来查看ls命令是如何调用xmalloc函数的。在安装了ls命令的调试信息后，以下SystemTap命令会在每次调用xmalloc函数时提供回溯信息：

```bash
stap -d /bin/ls --ldd \
    -e 'probe process("ls").function("xmalloc") {print_usyms(ubacktrace())}' \
    -c "ls /"
```

执行此命令时，会生成类似以下的输出：

```
bin dev lib media net
boot etc lib64 misc op_session profilerc selinux tmp bin dev lib media net proc sbin sys var
cgroup home lost+found mnt opt root srv usr
root srv usr
0x4116c0 : xmalloc+0x0/0x20 [/bin/ls] 
0x4116fc : xmemdup+0x1c/0x40 [/bin/ls] 
0x40e68b : clone_quoting_options+0x3b/0x50 [/bin/ls]
0x4087e4 : main+0x3b4/0x1900 [/bin/ls] 
0x3fa441ec5d : __libc_start_main+0xfd/0x1d0 [/lib64/libc-2.12.so]
0x402799 : _start+0x29/0x2c [/bin/ls]
0x4116c0 : xmalloc+0x0/0x20 [/bin/ls]
0x4116fc : xmemdup+0x1c/0x40 [/bin/ls] 
0x40e68b : clone_quoting_options+0x3b/0x50 [/bin/ls]
0x40884a : main+0x41a/0x1900 [/bin/ls]
0x3fa441ec5d : __libc_start_main+0xfd/0x1d0 [/lib64/libc-2.12.so]
...
```

有关用户空间栈回溯可用函数的更多详细信息，请参阅ucontextsymbols.stp和ucontext-unwind.stp tapsets。你也可以在SystemTap Tapset参考手册中找到上述tapsets中函数的描述。

## 第5章 有用的SystemTap脚本
----
本章列举了几个可用于监控和调查不同子系统的SystemTap脚本。安装systemtap-testsuite RPM包后，所有这些脚本都可在/usr/share/systemtap/testsuite/systemtap.examples/目录中找到。

### 5.1 网络
以下各节展示了用于跟踪网络相关函数并构建网络活动概况的脚本。

#### 5.1.1 网络分析
本节介绍如何分析网络活动。nettop.stp脚本可以让你了解系统中每个进程产生的网络流量情况。

```bash
#! /usr/bin/env stap
global ifxmit, ifrecv
global ifmerged
probe netdev.transmit {
    ifxmit[pid(), dev_name, execname(), uid()] <<< length
    ifmerged[pid(), dev_name, execname(), uid()] <<< 1
}
probe netdev.receive {
    ifrecv[pid(), dev_name, execname(), uid()] <<< length
    ifmerged[pid(), dev_name, execname(), uid()] <<< 1
}
function print_activity() {
    printf("%5s %5s %-12s %7s %7s %7s %7s %-15s\n", "PID", "UID", "DEV", "XMIT_PK", "RECV_PK", "XMIT_KB", "RECV_KB", "COMMAND")
    foreach ([pid, dev, exec, uid] in ifmerged-) {
        n_xmit = @count(ifxmit[pid, dev, exec, uid])
        n_recv = @count(ifrecv[pid, dev, exec, uid])
        printf("%5d %5d %-12s %7d %7d %7d %7d %-15s\n",
               pid, uid, dev, n_xmit, n_recv,
               @sum(ifxmit[pid, dev, exec, uid])/1024,
               @sum(ifrecv[pid, dev, exec, uid])/1024,
               exec)
    }
    print("\n")
    delete ifxmit
    delete ifrecv
    delete ifmerged
}
probe timer.ms(5000), end, error {
    print_activity()
}
```

注意，函数print_activity()使用了以下表达式：

```bash
n_xmit ? @sum(ifxmit[pid, dev, exec, uid])/1024 : 0
n_recv ? @sum(ifrecv[pid, dev, exec, uid])/1024 : 0
```

这些表达式是if/else条件语句。第一个语句是以下伪代码的更简洁写法：

```bash
if n_recv != 0 then
    @sum(ifrecv[pid, dev, exec, uid])/1024
else
    0
```

nettop.stp脚本跟踪系统中哪些进程正在生成网络流量，并提供每个进程的以下信息：
- **PID**：列出的进程的ID。
- **UID**：用户ID。用户ID为0表示根用户。
- **DEV**：进程用于发送/接收数据的以太网设备（例如，eth0、eth1）。
- **XMIT_PK**：进程传输的数据包数量。
- **RECV_PK**：进程接收的数据包数量。
- **XMIT_KB**：进程发送的数据量，以千字节为单位。
- **RECV_KB**：进程接收的数据量，以千字节为单位。

nettop.stp每5秒提供一次网络分析采样。你可以通过相应地编辑probe timer.ms(5000)来更改此设置。示例5.1“nettop.stp示例输出”包含了nettop.stp在20秒内的输出节选：

```log
[...]
PID UID DEV
PID UID DEV XMIT_PK RECV_PK XMIT_KB RECV_KB COMMAND
0 0 eth0 0 5 0 0 swapper
11178 0eth0 2 0 0 0 synergyc
PID UID DEV
PID UID DEV XMIT_PK RECV_PK XMIT_KB RECV_KB COMMAND
2886 4eth0 79 0 5 0 cups-polld
11362 0 0eth0 0eth0 0 3 61 32 0 0 5 firefox 3 swapper
PID UID DEV
PID UID DEV XMIT_PK RECV_PK XMIT_KB RECV_KB COMMAND
0 0 eth0 0 6 0 0 swapper
2886 410 2 2 0 0 cups-polld
11178 0 eth0 3 0 0 0 synergyc
3611 0eth0 0 1 0 0 Xorg
PID UID DEV
PID UID DEV XMIT_PK RECV_PK XMIT_KB RECV_KB COMMAND
0 0eth0 3 42 0 2 swapper
11178 0etho 43 1 3 0 synergyc
11362 3897 0etho 0eth0 0 0 7 1 0 0 0 firefox 0 multiload-apple
[...]
```

#### 5.1.2 跟踪网络套接字代码中调用的函数
本节介绍如何跟踪内核的net/socket.c文件中调用的函数。此任务有助于你更详细地识别每个进程在内核级别与网络的交互方式。

```bash
#! /usr/bin/env stap
probe kernel.function("*@net/socket.c").call {
    printf ("%s -> %s\n", thread_indent(1), ppfunc())
}
probe kernel.function("*@net/socket.c").return {
    printf ("%s <- %s\n", thread_indent(-1), ppfunc())
}
```

socket-trace.stp与示例3.6“thread_indent.stp”相同，后者在SystemTap函数部分用于说明thread_indent()的工作原理。

示例5.2“socket-trace.stp示例输出”包含了socket-trace.stp在3秒内的输出节选。有关此脚本由thread_indent()提供的输出的更多信息，请参考SystemTap函数示例3.6“thread_indent.stp”。

```log
[...]
0 Xorg(3611): -> sock_poll 
3 Xorg(3611): <- sock_poll
0 Xorg(3611): -> sock_poll
3 Xorg(3611): <- sock_poll 
0 gnome-terminal(11106): -> sock_poll
5 gnome-terminal(11106): <- sock_poll
0 scim-bridge(3883): -> sys_socketcall 
3 scim-bridge(3883): <- sock_poll 
0 scim-bridge(3883): -> sock_poll
8 scim-bridge(3883): -> sys_recvfrom 
4 scim-bridge(3883): -> sys_recv
0 ->sys_recvfrom
12 scim-bridge(3883):-> sock_from_file
20 scim-bridge(3883):-> sock_recvmsg 
16 scim-bridge(3883):<- sock_from_file 
24 scim-bridge(3883):<- sock_recvmsg
28 scim-bridge(3883): <- sys_recvfrom
<-sys_recvfrom
31 scim-bridge(3883): <- sys_recv
35 scim-bridge(3883): <- sys_socketcall
[...]
```

#### 5.1.3 监控传入的TCP连接
本节展示如何监控传入的TCP连接。这一任务对于实时识别未经授权、可疑或其他不必要的网络访问请求非常有用。

```
#! /usr/bin/env stap
probe begin {
    printf("%6s %16s %6s %6s %16s\n",
           "UID", "CMD", "PID", "PORT", "IP_SOURCE")
}
probe kernel.{function("tcp_accept"),function("inet_csk_accept")}.return? {
    sock = $return
    if (sock != 0)
        printf("%6d %16s %6d %6d %16s\n", uid(), execname(), pid(),
               inet_get_local_port(sock), inet_get_ip_source(sock))
}
```

在tcp_connections.stp运行期间，它会实时打印系统接受的任何传入TCP连接的以下信息：
- 当前的UID。
- CMD - 接受连接的命令。
- 命令的PID。
- 连接使用的端口。
- TCP连接的源IP地址。

```
UID  CMD     PID  PORT  IP_SOURCE
0    sshd    3165 22    10.64.0.227
0    sshd    3165 22    10.64.0.227
```

#### 5.1.4 监控TCP数据包
本节展示如何监控系统接收的TCP数据包。这对于分析系统上运行的应用程序产生的网络流量很有帮助。

```bash
#! /usr/bin/env stap
// 一个类似TCP转储的示例
probe begin, timer.s(1) {
    printf("Source IP Dest IP SPort DPort U A P R S F\n")
    printf("-------------------------------------------------\n")
}
probe udp.recvmsg /*,udp.sendmsg */ {
    printf(" %15s %15s %5d %5d UDP\n", saddr, daddr, sport, dport)
}
probe tcp.receive {
    printf(" %15s %15s %5d %5d %d %d %d %d %d %d\n",
           saddr, daddr, sport, dport, urg, ack, psh, rst, syn, fin)
}
```

在tcpdumplike.stp运行时，它会实时打印关于任何接收到的TCP数据包的以下信息：
- 源IP地址和目的IP地址（分别为saddr和daddr）。
- 源端口和目的端口（分别为sport和dport）。
- 数据包标志。

为了确定数据包使用的标志，tcpdumplike.stp使用了以下函数：
- urg - 紧急标志。
- ack - 确认标志。
- psh - 推送标志。
- rst - 重置标志。
- syn - 同步标志。
- fin - 结束标志。

上述函数返回1或0来表示数据包是否使用了相应的标志。

```log
Source IP Dest IP SPort DPort U A P R S F
209.85.229.147 10.0.2.15 80 20373 0 1 1 0 0 0
92.122.126.240 10.0.2.15 80 53214 0 1 0 0 1 0
10.0.2.15 92.122.126.240 80 53214 0 1 0 0 0 0
209.85.229.118 10.0.2.15 80 63433 0 1 0 0 1 0
209.85.229.118 10.0.2.15 80 63433 0 1 0 0 0 0
209.85.229.147 10.0.2.15 80 21141 0 1 1 0 0 0
209.85.229.147 10.0.2.15 80 21141 0 1 1 0 0 0
209.85.229.147 10.0.2.15 80 21141 0 1 1 0 0 0
209.85.229.147 10.0.2.15 80 21141 0 1 1 0 0 0
209.85.229.147 10.0.2.15 80 21141 0 1 1 0 0 0
209.85.229.118 10.0.2.15 80 63433 0 1 1 0 0 0
[...]
```

#### 5.1.5 监控内核中的网络数据包丢弃
Linux的网络堆栈可能会由于各种原因丢弃数据包。一些Linux内核包含一个跟踪点`kernel.trace("kfree_skb")`，它可以轻松跟踪数据包丢弃的位置。dropwatch.stp使用`kernel.trace("kfree_skb")`来跟踪数据包丢弃情况；该脚本会总结每个五秒间隔内丢弃数据包的位置。

```bash
#! /usr/bin/env stap
############################################################
# Dropwatch.stp
# Author: Neil Horman <nhorman@redhat.com>
# http://fedorahosted.org/dropwatch
############################################################
# 一个模仿dropwatch工具行为的示例脚本
# 用于保存我们找到的丢弃点列表的数组
global locations
# 记录我们开启和关闭监控的时间
probe begin {
    printf("Monitoring for dropped packets\n")
}
probe end {
    printf("Stopping dropped packet monitor\n")
}
probe kernel.trace("kfree_skb") {
    locations[$location] <<< 1 # 为每个丢弃位置的计数器加1
}
# 每5秒报告一次我们的丢弃位置
probe timer.sec(5) {
    printf("\n%s\n", ctime(gettimeofday_s()))
    foreach (l in locations-) {
        printf("%d packets dropped at %s\n", @count(locations[l]), symdata(l))
    }
    delete locations
}
```

`kernel.trace("kfree_skb")`跟踪内核中哪些地方丢弃网络数据包。`kernel.trace("kfree_skb")`有两个参数：一个指向正在释放的缓冲区的指针（`$`skb）和缓冲区在 kernel 代码中被释放的位置（`$`location）。dropwatch.stp脚本尽可能提供包含`$`location的函数。默认情况下，检测中没有将`$`location映射回函数的信息。在SystemTap 1.4版本中，--all-modules选项将包含所需的映射信息，可以使用以下命令来运行该脚本：
```bash
stap --all-modules dropwatch.stp
```

在旧版本的SystemTap中，可以使用以下命令来模拟--all-modules选项：
```bash
stap -dkernel \
dropwatch.stp `cat /proc/modules | awk 'BEGIN { ORS = " " } {print "-d"$1}'` \
```

运行dropwatch.stp脚本15秒，输出结果会与示例5.5“dropwatch.stp示例输出”类似。输出会列出每个跟踪点位置的丢失数据包数量，以及函数名或地址。

```log
Monitoring for dropped packets
Tue Nov 17 00:26:51 2020
1762 packets dropped at unix_stream_recvmsg
4 packets dropped at tun_do_read
2 packets dropped at nf_hook_slow
Tue Nov 17 00:26:56 2020
467 packets dropped at unix_stream_recvmsg
20 packets dropped at nf_hook_slow
6 packets dropped at tun_do_read
Tue Nov 17 00:27:01 2020
4 packets dropped at nf_hook_slow
Stopping dropped packet monitor
446 packets dropped at unix_stream_recvmsg
4 packets dropped at tun_do_read
```
当脚本在一台机器上编译并在另一台机器上运行时，--all-modules和/proc/modules目录不可用；symname函数只会打印出原始地址。为了使数据包丢弃的原始地址更有意义，可以参考/boot/System.map-`uname -r`文件。该文件列出了每个函数的起始地址，使你能够将示例5.5“dropwatch.stp示例输出”中的地址映射到特定的函数名。根据/boot/System.map-`uname -r`文件的以下片段，地址0xffffffff8149a8ed映射到函数unix_stream_recvmsg：

```
[...]
ffffffff8149a420 t unix_dgram_poll
ffffffff8149a5e0 t unix_stream_recvmsg
ffffffff8149ad00 t unix_find_other
[...]
```

### 5.2 磁盘
以下各节展示了监控磁盘和I/O活动的脚本。

#### 5.2.1 汇总磁盘读写流量
本节介绍如何识别哪些进程对系统进行最频繁的磁盘读写操作。

```bash
#!/usr/bin/env stap 
# Copyright (C) 2007 Oracle Corp.
# 每5秒获取磁盘读写状态，输出前十个条目
# 这是自由软件，遵循GNU通用公共许可证（GPL）；
# 可以是版本2，或者（根据你的选择）任何更高版本。
# 使用方法：
# ./disktop.stp
global io_stat,device
global read_bytes,write_bytes
probe vfs.read.return {
    if (returnval()>0) {
        if (devname!="N/A") { # 跳过从缓存的读取
            io_stat[pid(),execname(),uid(),ppid(),"R"] += returnval()
            device[pid(),execname(),uid(),ppid(),"R"] = devname
            read_bytes += returnval()
        }
    }
}
probe vfs.write.return {
    if (returnval()>0) {
        if (devname!="N/A") { # 跳过更新缓存
            io_stat[pid(),execname(),uid(),ppid(),"W"] += returnval()
            device[pid(),execname(),uid(),ppid(),"W"] = devname
            write_bytes += returnval()
        }
    }
}
probe timer.ms(5000) {
    if (read_bytes+write_bytes) { # 跳过无读写操作的磁盘
        printf("\n%-25s, %-8s%4dKb/sec, %-7s%6dKb, %-7s%6dKb\n\n",
               ctime(gettimeofday_s()), "Average:", ((read_bytes+write_bytes)/1024)/5,
               "Read:",read_bytes/1024, "Write:",write_bytes/1024)
        # 打印表头
        printf("%8s %8s %8s %25s %8s %4s %12s\n", "UID","PID","PPID","CMD","DEVICE","T","BYTES")
        # 打印前十的I/O操作
        foreach ([process,cmd,userid,parent,action] in io_stat- limit 10)
            printf("%8d %8d %8d %25s %8s %4s %12d\n",
                   userid,process,parent,cmd, device[process,cmd,userid,parent,action], action,io_stat[process,cmd,userid,parent,action])
        # 清除数据
        delete io_stat
        delete device
        write_bytes = 0
        read_bytes = 0
    }
}
probe end{
    delete device
    delete read_bytes
    delete write_bytes
    delete io_stat
}
```

disktop.stp输出对磁盘进行最频繁读写操作的前十个进程。示例5.6“disktop.stp示例输出”展示了该脚本的示例输出，每个列出的进程都包含以下数据：
- UID - 用户ID。用户ID为0表示根用户。
- PID - 列出的进程的ID。
- PPID - 列出的进程的父进程的ID。
- CMD - 列出的进程的名称。
- DEVICE - 列出的进程正在读取或写入的存储设备。
- T - 列出的进程执行的操作类型；W表示写入，R表示读取。
- BYTES - 从磁盘读取或写入磁盘的数据量。

disktop.stp输出中的时间和日期由函数ctime()和gettimeofday_s()返回。ctime()根据自Unix纪元（1970年1月1日）以来经过的秒数得出日历时间。gettimeofday_s()计算自Unix纪元以来的实际秒数，为输出提供了一个相当准确的人类可读时间戳。

在这个脚本中，`$`return是一个局部变量，它存储每个进程从虚拟文件系统读取或写入的实际字节数。`$`return只能在返回探针（例如vfs.read.return和vfs.read.return）中使用。

```log
[...]
Mon Sep 29 03:38:28 2008 , Average: 19Kb/sec, Read: 7Kb, Write: 89Kb
UID  PID  PPID  CMD           DEVICE  T  BYTES
0    26319 26294 firefox     sda5    W  90229
0    2758  2757  pam_timestamp_c sda5    R  8064
0    2885  1     cupsd       sda5    W  1678
Mon Sep 29 03:38:38 2008 , Average: 1Kb/sec, Read: 7Kb, Write: 1Kb
UID  PID  PPID  CMD           DEVICE  T  BYTES
0    2758  2757  pam_timestamp_c sda5    R  8064
0    2885  1     cupsd       sda5    W  1678
```

#### 5.2.2 跟踪每个文件读写的I/O时间
本节介绍如何监控每个进程读取或写入任何文件所花费的时间。这对于确定给定系统上哪些文件加载缓慢很有用。

```bash
#! /usr/bin/env stap
/*
* Copyright (C) 2006-2018 Red Hat Inc.
* 本受版权保护的材料可供任何希望使用、修改、复制或重新分发的人使用，但需遵守GNU通用公共许可证v.2的条款和条件。
* 您应该已经随本程序收到了一份GNU通用公共许可证副本。如果没有，请访问<http://www.gnu.org/licenses/>。
* 当进程打开的每个文件关闭时，打印出在读写系统调用中花费的时间。请注意，SystemTap脚本需要在打开操作发生之前运行，以便脚本记录数据。
* 此脚本可用于找出机器上哪些文件加载缓慢。例如：
* stap iotime.stp -c 'firefox'
* 输出格式为：
* 时间戳 进程ID (可执行文件) 信息类型 路径 ...
* 200283135 2573 (cupsd) access /etc/printcap read: 0 write: 7063
* 200283143 2573 (cupsd) iotime /etc/printcap time: 69
*/
global start
global time_io
function timestamp:long() {
    return gettimeofday_us() - start
}
function proc:string() {
    return sprintf("%d (%s)", pid(), execname())
}
probe begin {
    start = gettimeofday_us()
}
global possible_filename, filehandles, fileread, filewrite
probe syscall.open, syscall.openat {
    possible_filename[tid()] = filename
}
probe syscall.open.return, syscall.openat.return {
    // 即使使用非dwarf系统调用返回探针，也能获取文件名
    filename = possible_filename[tid()]
    delete possible_filename[tid()]
    if (retval != -1) {
        filehandles[pid(), retval] = filename
    } else {
        printf("%d %s access %s fail\n", timestamp(), proc(), filename)
    }
}
global read_fds, write_fds
probe syscall.read {
    read_fds[tid()] = fd
}
probe syscall.read.return {
    p = pid()
    // 即使使用非dwarf系统调用返回探针，也能获取fd
    delete read_fds[tid()]
    fd = read_fds[tid()]
    bytes = retval
    time = gettimeofday_us() - @entry(gettimeofday_us())
    if (bytes > 0) {
        time_io[p, fd] <<< time
        fileread[p, fd] <<< bytes
    }
}
probe syscall.write {
    write_fds[tid()] = fd
}
probe syscall.write.return {
    p = pid()
    // 即使使用非dwarf系统调用返回探针，也能获取fd
    fd = write_fds[tid()]
    delete write_fds[tid()]
    bytes = retval
    time = gettimeofday_us() - @entry(gettimeofday_us())
    if (bytes > 0) {
        time_io[p, fd] <<< time
        filewrite[p, fd] <<< bytes
    }
}
probe syscall.close {
    if ([pid(), fd] in filehandles) {
        printf("%d %s access %s read: %d write: %d\n", timestamp(), proc(), filehandles[pid(), fd], @sum(fileread[pid(), fd]), @sum(filewrite[pid(), fd]))
        if (@count(time_io[pid(), fd])) {
            printf("%d %s iotime %s time: %d\n", timestamp(), proc(), filehandles[pid(), fd], @sum(time_io[pid(), fd]))
        }
        delete filewrite[pid(), fd]
        delete fileread[pid(), fd]
        delete filehandles[pid(), fd]
        delete time_io[pid(),fd]
    }
}
```
iotime.stp跟踪每次系统调用对文件的打开、关闭、读取和写入操作。对于任何系统调用访问的每个文件，iotime.stp计算读取或写入完成所需的微秒数，并跟踪读取或写入文件的数据量（以字节为单位）。

iotime.stp还使用局部变量`$count`来跟踪任何系统调用尝试读取或写入的数据量（以字节为单位）。请注意，`$return`（如5.2.1节 汇总磁盘读写流量中的disktop.stp所使用）存储实际读取/写入的数据量。`$count`只能在跟踪数据读取或写入的探针（即syscall.read和syscall.write）上使用。

```
[...] 
825946 3364 (NetworkManager) access /sys/class/net/eth0/carrier read: 8190 write: 0 
825955 3364 (NetworkManager) iotime /sys/class/net/eth0/carrier time: 9
[...]
117061 2460 (pcscd) access /dev/bus/usb/003/001 read: 43 write: 0
117065 2460 (pcscd) iotime /dev/bus/usb/003/001 time: 7
[...]
3973737 2886 (sendmail) access /proc/loadavg read: 4096 write: 0
3973744 2886 (sendmail) iotime /proc/loadavg time: 11 
[...]
```

示例5.7“iotime.stp示例输出”打印以下数据：
- 以微秒为单位的时间戳。
- 进程ID和进程名称。
- access或iotime标志。
- 被访问的文件。

如果一个进程能够读取或写入任何数据，应该会同时出现一对access和iotime行。access行的时间戳表示给定进程开始访问文件的时间；在该行末尾，它将显示读取/写入的数据量（以字节为单位）。iotime行将显示进程执行读取或写入操作所花费的时间（以微秒为单位）。

如果access行后面没有iotime行，则意味着该进程没有读取或写入任何数据。

#### 5.2.3 跟踪累积I/O
本节介绍如何跟踪系统的累积I/O量。

```bash
#! /usr/bin/env stap
# traceio.stp
# Copyright (C) 2007-2018 Red Hat, Inc., Eugene Teo <eteo@redhat.com>
# Copyright (C) 2009 Kai Meyer <kai@unixlords.com>
# 修复了一个允许此脚本长时间运行的错误
# 并添加了humanreadable函数
# 本程序是自由软件；您可以根据自由软件基金会发布的GNU通用公共许可证第2版的条款重新分发和/或修改它。
global reads, writes, total_io
probe vfs.read.return {
    if (returnval() > 0) {
        reads[pid(),execname()] += returnval()
        total_io[pid(),execname()] += returnval()
    }
}
probe vfs.write.return {
    if (returnval() > 0) {
        writes[pid(),execname()] += returnval()
        total_io[pid(),execname()] += returnval()
    }
}
function humanreadable(bytes) {
    if (bytes > 1024*1024*1024) {
        return sprintf("%d GiB", bytes/1024/1024/1024)
    } else if (bytes > 1024*1024) {
        return sprintf("%d MiB", bytes/1024/1024)
    } else if (bytes > 1024) {
        return sprintf("%d KiB", bytes/1024)
    } else {
        return sprintf("%d B", bytes)
    }
}
probe timer.s(1) {
    foreach([p,e] in total_io- limit 10) {
        printf("%8d %15s r: %12s w: %12s\n",
               p, e, humanreadable(reads[p,e]),
               humanreadable(writes[p,e]))
    }
    printf("\n") 
    # 因此，这些值是脚本启动以来的累积值。
    # 注意，我们不会清零reads、writes和total_io。
}
```

traceio.stp打印一段时间内产生I/O流量的前十个可执行文件。此外，它还跟踪这十个可执行文件所做的累积I/O读取和写入量。这些信息以1秒为间隔进行跟踪和打印，并按降序排列。


请注意，traceio.stp也使用了局部变量`$return`，5.2.1节“汇总磁盘读写流量”中的disktop.stp也使用了该变量。

```log
[...]
Xorg r: 583401KiB w: 0 KiB
floaters r: 96KiB W: 7130 KiB 
multiload-apple r: 538 KiB w: 537 KiB
sshd r: 138KiB W: 71 KiB 
pam_timestamp_c r: 138 KiB w: 0 KiB
staprun r: 51KiB W: 51 KiB
snmpd r: 46KiB W: 0KiB 
pcscd r: 28KiB W: 0KiB
irqbalance r: 27KiB w: 4KiB
cupsd r: 4KiB W: 18KiB
Xorg r: 588140 KiB W: 0KiB
floaters r: 97 KiB W: 7143 KiB
multiload-apple r: 543 KiB w: 542 KiB
sshd r: 543 KIB W: 72KiB 
pam_timestamp_c r: 138 KiB w: 0 KiB
staprun r: 51KiB W: 51 KiB
snmpdr: 46 KiB W: 0KiB
pcscd r: 28KiB W: 0KiB
irgbalance r: 27KiB W: 4KiB
cupsd r: 4KiB w: 18KiB
```

#### 5.2.4 I/O监控（按设备）
本节介绍如何监控特定设备上的I/O活动。
```bash
#! /usr/bin/env stap
global device_of_interest
probe begin { 
    /* 以下不是最有效的方法。
    dev = usrdev2kerndev($1)
    device_of_interest = MKDEV(MAJOR(dev), MINOR(dev))
    可以直接将usrdev2kerndev()的结果放入device_of_interest。
    但是，想要测试其他设备函数 */
}
probe vfs.{write,read} {
    if (dev == device_of_interest) {
        printf ("%s(%d) %s 0x%x\n", execname(), pid(), ppfunc(), dev)
    }
}
```

traceio2.stp接受1个参数：设备的完整设备号。要获取此编号，可以使用`stat -c "0x%D" directory`，其中directory位于要监控的设备中。

usrdev2kerndev()函数将完整设备号转换为内核能识别的格式。usrdev2kerndev()的输出与MKDEV()、MINOR()和MAJOR()函数一起使用，以确定特定设备的主设备号和次设备号。

traceio2.stp的输出包括执行读/写操作的任何进程的名称和ID、它正在执行的函数（即vfs_read或vfs_write）以及内核设备号。

以下是`stap traceio2.stp 0x805`完整输出的节选，其中0x805是/home的完整设备号。/home位于/dev/sda5上，这是我们要监控的设备。
  ```
    synergyc(3722) vfs_read 0x800005 
    synergyc(3722) vfs_read 0x800005 
    [...]
    cupsd(2889) vfs_write 0x800005 
    cupsd(2889) vfs_write 0x800005
    cupsd(2889) vfs_write 0x800005
    [...]
  ```

#### 5.2.5 监控文件的读写操作
本节介绍如何实时监控对文件的读取和写入操作。
  ```bash
    #! /usr/bin/env stap
    probe vfs.{write,read} {
        if (dev == MKDEV($1,$2) # 主/次设备号
            && ino == $3) # dev和ino由vfs.write和vfs.read定义
        printf ("%s(%d) %s 0x%x/%u\n", execname(), pid(), ppfunc(), dev, ino)
    }
  ```
inodewatch.stp在命令行中接受关于文件的以下信息作为参数：
- 文件的主设备号。
- 文件的次设备号。
- 文件的inode号。

要获取这些信息，可以使用`stat -c '%D %i' filename`，其中filename是文件的绝对路径。

例如：要监控/etc/crontab，首先运行`stat -c '%D %i' /etc/crontab`。这将给出以下输出：
  ```
  805 1078319
  ```

805是十六进制的设备号。低两位是次设备号，高位是主设备号。1078319是inode号。要开始监控/etc/crontab，可以运行`stap inodewatch.stp 0x8 0x05 1078319`（0x前缀表示十六进制值）。

此命令的输出包含执行读/写操作的任何进程的名称和ID、它正在执行的函数（即vfs_read或vfs_write）、设备号（十六进制格式）和inode号。示例5.10“inodewatch.stp示例输出”包含了`stap inodewatch.stp 0x8 0x05 1078319`的输出（在脚本运行时执行`cat /etc/crontab`）：
  ```
  cat(16437) vfs_read 0x800005/1078319
  cat(16437) vfs_read 0x800005/1078319
  ```

#### 5.2.6 监控文件属性变化
本节介绍如何实时监控是否有进程正在更改目标文件的属性。
- **inodewatch2.stp**
  ```bash
    #!/usr/bin/env stap
    global ATTR_MODE = 1
    probe kernel.function("notify_change") {
        dev_nr = $dentry->d_inode->i_sb->s_dev
        inode_nr = $dentry->d_inode->i_ino
        if (dev_nr == MKDEV($1,$2) // 设备的主/次设备号
            && inode_nr == $3
            && $attr->ia_valid & ATTR_MODE)
            printf ("%s(%d) %s 0x%x/%u %o %d\n", execname(), pid(), ppfunc(), dev_nr, inode_nr, $attr->ia_mode, uid())
    }
  ```
与5.2.5节 “监控文件的读写操作” 中的inodewatch.stp类似，inodewatch2.stp也将目标文件的设备号（整数格式）和inode号作为参数。有关如何获取这些信息的更多内容，请参考5.2.5节 “监控文件的读写操作”。

inodewatch2.stp的输出与inodewatch.stp相似，但它还包含被监控文件的属性变化，以及负责更改的用户ID（uid()）。示例5.11 “inodewatch2.stp示例输出” 展示了在监控/home/joe/bigfile时，用户joe执行chmod 777 /home/joe/bigfile和chmod 666 /home/joe/bigfile时inodewatch2.stp的输出。
- **示例5.11 inodewatch2.stp示例输出**
  ```
  chmod(17448) inode_setattr 0x800005/6011835 100777 500
  chmod(17449) inode_setattr 0x800005/6011835 100666 500
  ```

#### 5.2.7 定期打印I/O块时间
本节介绍如何跟踪每个块I/O请求等待完成所花费的时间。这有助于判断在任何给定时间是否存在过多未完成的块I/O操作。

- **ioblktime.stp**
  ```bash
    #!/usr/bin/env stap
    global req_time%[25000], etimes
    probe ioblock.request {
        req_time[$bio] = gettimeofday_us()
    }
    probe ioblock.end {
        t = gettimeofday_us()
        s = req_time[$bio]
        delete req_time[$bio]
        if (s) {
            etimes[devname, bio_rw_str(rw)] <<< t - s
        }
    }
    /* 暂时删除与其他请求合并的请求 */
    probe kernel.{trace("block_bio_frontmerge"), trace("block_bio_backmerge")} {
        delete req_time[$bio]
    }
    probe timer.s(10), end {
        ansi_clear_screen()
        printf("%10s %3s %10s %10s %10s\n", "device", "rw", "total (us)", "count", "avg (us)")
        foreach ([dev,rw] in etimes - limit 20) {
            printf("%10s %3s %10d %10d %10d\n", dev, rw, @sum(etimes[dev,rw]), @count(etimes[dev,rw]), @avg(etimes[dev,rw]))
        }
        delete etimes
    }
  ```
ioblktime.stp计算每个设备的块I/O平均等待时间，并每10秒打印一次列表。与往常一样，你可以通过编辑probe timer.s(10), end {}中的指定值来修改此刷新频率。

在某些情况下，可能会存在过多未完成的块I/O操作，此时脚本可能会超过默认的MAXMAPENTRIES数量。MAXMAPENTRIES是在声明数组时未显式指定数组大小时，数组的最大行数。如果脚本超过默认的MAXMAPENTRIES值2048，请使用stap选项 -DMAXMAPENTRIES=10000再次运行脚本。
- **示例5.12 ioblktime.stp示例输出**
  ```log
    device  rw    total (us)  count  avg (us)
    sda     W         9659       6      1609
    dm-0    W        20278       6      3379
    dm-0    R        20524       5      4104
    sda     R        19277       5      3855
  ```
示例5.12 “ioblktime.stp示例输出” 显示了设备名称、执行的操作（rw）、所有操作的总等待时间（total(us)）、操作数量（count）以及所有这些操作的平均等待时间（avg (us)）。脚本统计的时间单位为微秒。

### 5.3 性能分析
以下部分展示了通过监控函数调用来分析内核活动的脚本。

#### 5.3.1 统计函数调用次数
本节介绍如何确定系统在30秒的采样时间内调用特定内核函数的次数。根据通配符的使用情况，你还可以使用此脚本来针对多个内核函数。
- **functioncallcount.stp**
  ```bash
    #!/usr/bin/env stap
    # 以下命令将探测内核内存管理代码中的所有函数：
    # stap functioncallcount.stp "*@mm/*.c"
    probe kernel.function(@1).call {  # 探测命令行中列出的函数
        called[ppfunc()] <<< 1  # 高效地增加计数
        global called
    }
    probe end {
        foreach (fn in called-)  # 按调用次数（降序）排序
            printf("%s %d\n", fn, @count(called[fn]))  
        exit()
    }
  ```
  functioncallcount.stp将目标内核函数作为参数。该参数支持通配符，这使你能够在一定程度上针对多个内核函数。
  functioncallcount.stp的输出包含被调用函数的名称以及在采样时间内的调用次数（按字母顺序排列）。示例5.13 “functioncallcount.stp示例输出” 包含了stap functioncallcount.stp "\*@mm/\*.c"的输出节选。

- **示例5.13 functioncallcount.stp示例输出**
  ```log
    ...
    __vma_link 97
    __vma_link_file 66
    __vma_link_list 97
    __vma_link_rb 97
    __xchg 103
    add_page_to_active_list 102
    add_page_to_inactive_list 19
    add_to_page_cache 19
    add_to_page_cache_lru 7
    all_vm_events 6
    alloc_pages_node 4630
    alloc_slabmgmt 67
    anon_vma_alloc 62
    anon_vma_free 62
    anon_vma_lock 66
    anon_vma_prepare 98
    anon_vma_unlink 97
    anon_vma_unlock 66
    arch_get_unmapped_area_topdown 94
    arch_get_unmapped_exec_area 3
    arch_unmap_area_topdown 97
    atomic_add 2
    atomic_add_negative 97
    atomic_dec_and_test 5153
    atomic_inc 470
    atomic_inc_and_test 1
    ...
  ```

#### 5.3.2 调用图跟踪
本节介绍如何跟踪传入和传出的函数调用。
- **para-callgraph.stp**
  ```bash
    #!/usr/bin/env stap
    function trace(entry_p, extra) {
        %( $# > 1 %? if (tid() in trace) %)
            printf("%s%s%s %s\n", thread_indent (entry_p),
                    (entry_p>0?"->":"<-"),
                    ppfunc (),
                    extra)
        %( $# > 1 %? )
    }
    %( $# > 1 %? global trace
    probe $2.call {
        trace[tid()] = 1
    }
    probe $2.return {
        delete trace[tid()]
    }
    %( $# > 1 %? )
    probe $1.call {
        trace(1, $$parms)
    }
    probe $1.return {
        trace(-1, $$return)
    }
  ```

  para-callgraph.stp接受两个命令行参数：
    - 你想要跟踪其进入/退出调用的函数（`$1`）。
    - 第二个可选的触发函数（`$2`），用于在线程基础上启用或禁用跟踪。只要触发函数尚未退出，每个线程中的跟踪就会继续。

  para-callgraph.stp使用了thread_indent()函数；因此，其输出包含`$1`（即你正在跟踪的探测函数）的时间戳、进程名称和线程ID。有关thread_indent()的更多信息，请参考SystemTap函数中的相关条目。

  以下示例包含了stap para-callgraph.stp 'kernel.function("\*@fs/\*.c")' 'kernel.function("sys_read")'的输出节选。

- **示例5.14 para-callgraph.stp示例输出**
  ```log
    ...
    267 gnome-terminal(2921): <-do_sync_read return=0xfffffffffffffff5
    269 gnome-terminal(2921):<-vfs_read return=0xfffffffffffffff5
    0 gnome-terminal(2921):->fput file=0xffff880111eebbc0
    2 gnome-terminal(2921):<-fput
    0 gnome-terminal(2921):->fget_light fd=0x3 fput_needed=0xffff88010544df54
    3 gnome-terminal(2921):<-fget_light return=0xffff8801116ce980
    pos=0xffff88010544df48 ppos=0xffff88010544df48 count=0x1000 ppos=0xffff88010544df48
    15 gnome-terminal(2921): <-do_sync_read return=0xfffffffffffffff5
    12 gnome-terminal(2921): ->do_sync_read filp=0xffff8801116ce980 buf=0xc86504 len=0x1000
    0 gnome-terminal(2921):->vfs_read file=0xffff8801116ce980 buf=0xc86504 count=0x1000
    4 gnome-terminal(2921): ->rw_verify_area read_write=0x0 file=0xffff8801116ce980
    7 gnome-terminal(2921): <-rw_verify_area return=0x1000
    18 gnome-terminal(2921):<-vfs_read return=0xfffffffffffffff5
    0 gnome-terminal(2921):->fput file=0xffff8801116ce980
    ...
  ```

#### 5.3.3 确定内核态和用户态的耗时
本节说明如何确定任何给定线程在内核态或用户态所花费的时间。
- **thread-times.stp**
  ```bash
    #!/usr/bin/env stap
    probe perf.sw.cpu_clock!, timer.profile {
        // 注意：为避免在SMP机器上产生竞争，不使用全局标量/数组，
        // 仅使用无竞争的统计聚合。
        tid=tid(); e=execname()
        if (!user_mode())
            kticks[e,tid] <<< 1
        else
            uticks[e,tid] <<< 1
        ticks <<< 1
        tids[e,tid] <<< 1
    }
    global uticks%, kticks%, ticks
    global tids%
    probe timer.s(5), end {
        allticks = @count(ticks)
        printf ("%16s %5s %7s %7s (of %d ticks)\n", "comm", "tid", "%user", "%kernel", allticks)
        foreach ([e,tid] in tids- limit 20) { 
            // SystemTap仅执行整数运算。
            // 为避免精度损失，将小数点向右移动四位（*100000）。可以将原始结果值x.xxyy想象为变为xxxyy.0。
            // 通过除以100并进行取模100运算获得整数百分比xxx。
            uscaled = @count(uticks[e,tid])*10000/allticks 
            kscaled = @count(kticks[e,tid])*10000/allticks
            printf ("%16s %5d %3d.%02d%% %3d.%02d%%\n", e, tid, uscaled/100, uscaled%100, kscaled/100, kscaled%100)
        }
        printf("\n")
        delete uticks
        delete kticks
        delete ticks
        delete tids
    }
  ```

  thread-times.stp列出了在5秒采样时间内占用CPU时间最多的前20个进程，以及采样期间的总CPU时钟周期数。此脚本的输出还记录了每个进程使用的CPU时间百分比，以及该时间是在内核态还是用户态花费的。

  示例5.15 “thread-times.stp示例输出” 包含了thread-times.stp在5秒采样内的输出。
- **示例5.15 thread-times.stp示例输出**
  ```log
    comm             tid  %user  %kernel (of 20002 ticks)
    0                    0.00%  87.88%
    32169                5.24%   3.33%
    9815                 0.03%   0.36%
    11106                0.95%   0.62%
    3611                 0.56%   0.37%
    9859                 0.00%   0.12%
    9861                 0.01%   0.02%
    32167                0.08%   0.08%
    3897                 0.01%   0.08%
    3800                 0.03%   0.00%
    2886                 0.02%   0.00%
    3243                 0.00%   0.01%
    3862                 0.00%   0.00%
    21767                0.00%   0.00%
    3782                 0.00%   0.00%
    2522                 0.00%   0.00%
    3883                 0.00%   0.00%
    3775                 0.00%   0.00%
    3943                 0.00%   0.00%
    3873                 0.00%   0.00%
  ```

#### 5.3.4 监控轮询应用程序
本节将介绍如何识别和监控正在进行轮询的应用程序。这样做可以跟踪不必要或过度的轮询，有助于找出在CPU使用和节能方面可改进的地方。

- **timeout.stp**
  ```bash
    #! /usr/bin/env stap 
    # Copyright (C) 2009-2018 Red Hat, Inc.
    # Written by Ulrich Drepper <drepper@redhat.com> 
    # Modified by William Cohen <wcohen@redhat.com>
    global process, timeout_count, to
    global poll_timeout, epoll_timeout, select_timeout, itimer_timeout
    global nanosleep_timeout, futex_timeout, signal_timeout
    probe syscall.{poll,epoll_wait} {
    if (timeout) 
        to[pid()]=timeout
    }
    probe syscall.poll.return {
    if (retval == 0 && to[pid()] > 0 ) {
        poll_timeout[pid()]++
        timeout_count[pid()]++
        process[pid()] = execname()
        delete to[pid()]
    }
    }
    probe syscall.epoll_wait.return {
    if (retval == 0 && to[pid()] > 0 ) {
        epoll_timeout[pid()]++
        timeout_count[pid()]++
        process[pid()] = execname()
        delete to[pid()]
    }
    }
    probe syscall.select.return {
    if (retval == 0) {
        select_timeout[pid()]++
        timeout_count[pid()]++
        process[pid()] = execname()
    }
    }
    probe syscall.futex.return {
    if (errno_str(retval) == "ETIMEDOUT") {
        futex_timeout[pid()]++
        timeout_count[pid()]++
        process[pid()] = execname()
    }
    }
    probe syscall.nanosleep.return {
    if (retval == 0) {
        nanosleep_timeout[pid()]++
        timeout_count[pid()]++
        process[pid()] = execname()
    }
    }
    probe kernel.function("it_real_fn") {
    timeout_count[pid()]++
    process[pid()] = execname()
    itimer_timeout[pid()]++
    }
    probe syscall.rt_sigtimedwait.return {
    if (errno_str(retval) == "EAGAIN") {
        signal_timeout[pid()]++
        timeout_count[pid()]++
        process[pid()] = execname()
    }
    }
    probe syscall.exit {
    if (pid() in process) {
        delete process[pid()]
        delete timeout_count[pid()]
        delete poll_timeout[pid()]
        delete epoll_timeout[pid()]
        delete select_timeout[pid()]
        delete itimer_timeout[pid()]
        delete futex_timeout[pid()]
        delete nanosleep_timeout[pid()]
        delete signal_timeout[pid()]
    }
    }
    probe timer.s(1) {
    ansi_clear_screen()
    printf ("%5d |%7d %7d %7d %7d %7d %7d %7d| %-.38s\n", p, printf (" pid | poll select epoll itimer futex nanosle signal| process\n")
    poll_timeout[p], select_timeout[p],
    epoll_timeout[p], itimer_timeout[p], futex_timeout[p], nanosleep_timeout[p],
    signal_timeout[p], process[p])
    }
    global prom_arr
    probe prometheus {
    foreach (p in timeout_count- limit 20) {
        prom_arr[poll_timeout[p], select_timeout[p], futex_timeout[p], nanosleep_timeout[p], epoll_timeout[p], itimer_timeout[p],
        signal_timeout[p]] = process[p]
        @prometheus_dump_array7(prom_arr, "process_timeouts", "poll_timeout", "select_timeout", delete prom_arr "futex_timeout", "nanosleep_timeout", "signal_timeout") "epoll_timeout", "itimer_timeout",
    }
  ```

  timeout.stp脚本跟踪以下系统调用由于超时而不是实际事件发生而完成的次数：
    - poll
    - select
    - epoll
    - itimer
    - futex
    - nanosleep
    - signal

  示例5.16 “timeout.stp示例输出”展示了该脚本的输出。在这个特定示例中，由于插件模块的原因，firefox进行了过多的轮询。
- **示例5.16 timeout.stp示例输出**
  ```log
    22945 28937 uid 148793 poll select 0 56949 0 epo11 itimer 0 0 4727 1 37288 futex nanosle signal| 0 0 0 0 0 process scim-bridge firefox
    0 0 0 O 36414 0 0 0| swapper
    4275 23140 0 0 1 0 0 0| mixer_applet2
    22941 4191 7908 0 14405 1 0 0 62 0 0 0 0 0 0| scim-launcher 0 gnome-terminal
    4261 3483 3695 0 0 0 7206 0 0 0 0 0 0 2 0 0 0 0 7622 7622 0 0| gdm-binary 0 0 escd dhcdbd
    4189 6916 0 0 2 0 0 0 scim-panel-gtk
    1863 5767 0 0 0 0 0 0 iscsid
    2562 0 2881 0 1 0 1438 0| pcscd
    4257 4255 0 0 1 0 0 0 gnome-power-man
    4278 3921 4083 3876 1603 0 1331 0 0 0 0 0 1728 60 0 0 0 0 0 0 0 0 0| multiload-apple 01 Xorg gam_server
    4248 1591 0 0 0 0 0 0| nm-applet
    3165 0 1441 0 0 0 0 0 xterm
    29548 1862 0 0 1440 0 0 0 0 0 0 0 1438 0 0 0 httpd iscsid
  ```
  可以通过编辑第二个探测点（timer.s(1)）来增加采样时间。timeout.stp脚本的输出包含前20个进行轮询的应用程序的名称和UID，以及每个应用程序执行每个轮询系统调用的次数（随时间统计）。

#### 5.3.5 跟踪最常使用的系统调用
5.3.4节 “监控轮询应用程序” 中的timeout.stp脚本通过检查一小部分系统调用（poll、select、epoll、itimer、futex、nanosleep和signal）来帮助识别正在进行轮询的应用程序。然而，在某些系统中，这一小部分系统调用之外的大量系统调用可能是导致内核时间消耗的原因。如果你怀疑某个应用程序过度使用系统调用，就需要确定系统上最常使用的系统调用。为此，可以使用topsys.stp脚本。

- **topsys.stp**
  ```bash
    #! /usr/bin/env stap
    # 本脚本持续列出5秒间隔内系统中前20个最常使用的系统调用

    global syscalls_count
    probe syscall_any {
    syscalls_count[name] <<< 1
    }
    function print_systop () {
    printf ("%25s %10s\n", "SYSCALL", "COUNT")
    foreach (syscall in syscalls_count- limit 20) {
        printf("%25s %10d\n", syscall, @count(syscalls_count[syscall]))
    }
    delete syscalls_count
    }
    probe timer.s(5) {
    print_systop ()
    printf("--- --\n")
    }
    global prom_arr
    probe prometheus {
    foreach (syscall in syscalls_count- limit 20)
        prom_arr[syscall] = @count(syscalls_count[syscall])
    @prometheus_dump_array1(prom_arr, "top_syscall_count", "name")
    delete prom_arr
    }
  ```

  topsys.stp脚本列出系统每5秒内使用的前20个系统调用，并列出每个系统调用在该时间段内的使用次数。示例5.17 “topsys.stp示例输出”展示了一个示例输出。
- **示例5.17 topsys.stp示例输出**
  ```log
    SYSCALL COUNT 
    gettimeofday 1857
    read 1821
    ioctl 1568
    poll 1033
    close 638
    open 503
    select 455
    write 391
    writev 335
    futex 303
    recvmsg 251
    socket 137
    clock_gettime 124
    rt_sigprocmask 121
    sendto 120
    setitimer 106
    stat 90
    time 81
    sigreturn 72
    fstat 66
  ```

#### 5.3.6 跟踪每个进程的系统调用量
本节将说明如何确定哪些进程执行的系统调用量最大。在前面的章节中，已经介绍了如何监控系统随时间使用的最常使用的系统调用（5.3.5节 “跟踪最常使用的系统调用”），还介绍了如何识别哪些应用程序最常使用特定的 “可疑轮询” 系统调用（5.3.4节 “监控轮询应用程序”）。监控每个进程的系统调用量可以为调查系统中的轮询进程和其他资源占用者提供更多数据。

- **syscalls_by_proc.stp**
  ```bash
    #! /usr/bin/env stap
    # Copyright (C) 2006 IBM Corp. 
    # Copyright (C) 2018-2019 Red Hat, Inc.
    # 本文件是systemtap的一部分，属于自由软件。你可以在GNU通用公共许可证（GPL）的条款下重新分发和/或修改它；
    # 可以是版本2，或者（根据你的选择）任何更高版本。
    # 按进程名降序打印系统调用计数。
    global syscalls
    probe begin {
    print ("Collecting data... Type Ctrl-C to exit and display results\n")
    }
    probe syscall_any {
    syscalls[execname()] <<< 1
    }
    probe end {
    printf ("%-10s %-s\n", "#SysCalls", "Process Name")
    foreach (proc in syscalls-)
        printf("%-10d %-s\n", @sum(syscalls[proc]), proc)
    }
  ```

  syscalls_by_proc.stp脚本列出执行系统调用次数最多的前20个进程，并列出每个进程在该时间段内执行的系统调用次数。示例5.18 “topsys.stp示例输出”展示了一个示例输出。
- **示例5.18 topsys.stp示例输出**
  ```log
    Collecting data... Type Ctrl-C to exit and display results
    #SysCalls Process Name
    1577 multiload-apple
    692 synergyc
    408 pcscd
    376 mixer_applet2
    299 gnome-terminal
    293 Xorg
    206 scim-panel-gtk
    95 gnome-power-man
    90 artsd
    85 dhcdbd
    84 scim-bridge
    78 gnome-screensav
    66 scim-launcher
    ...
  ```

要显示进程ID而不是进程名称，可以使用以下脚本。
- **syscalls_by_pid.stp**
  ```bash
    #! /usr/bin/env stap
    # Copyright (C) 2006 IBM Corp.
    # 本文件是systemtap的一部分，属于自由软件。你可以在GNU通用公共许可证（GPL）的条款下重新分发和/或修改它；
    # 可以是版本2，或者（根据你的选择）任何更高版本。
    # 按进程ID降序打印系统调用计数。
    global syscalls
    probe begin {
    print ("Collecting data... Type Ctrl-C to exit and display results\n")
    }
    probe syscall_any {
    syscalls[pid()] <<< 1
    }
    probe end {
    printf ("%-10s %-s\n", "#SysCalls", "PID")
    foreach (pid in syscalls-)
        printf("%-10d %-d\n", @sum(syscalls[pid]), pid)
    }
  ```
  如输出中所示，需要手动退出脚本才能显示结果。可以通过简单地添加一个timer.s()探测点为任一脚本添加定时过期功能；例如，要使脚本在5秒后过期，可以向脚本中添加以下探测点：
  
  ```bash
    probe timer.s(5)
    exit()
  ```

### 5.4 识别用户空间中的竞争锁
本节介绍如何在特定时间段内识别系统中用户空间的竞争锁。识别用户空间的竞争锁，有助于排查因futex争用导致的程序性能不佳问题。

简单来讲，当多个进程试图同时访问同一个锁变量时，就会发生futex争用。这可能会导致性能下降，因为锁会使执行序列化——一个进程获取锁，而其他进程必须等待锁变量再次可用。

futexes.stp脚本通过探测futex系统调用来显示锁争用情况。
- **futexes.stp**
  ```bash
    #! /usr/bin/env stap
    # 本脚本通过挂钩futex系统调用，尝试识别用户空间中的竞争锁
    global FUTEX_WAIT = 0 /*, FUTEX_WAKE = 1 */ 
    global FUTEX_PRIVATE_FLAG = 128 /* linux 2.6.22+ */ 
    global FUTEX_CLOCK_REALTIME = 256 /* linux 2.6.29+ */
    global lock_waits # 长期统计(tid, lock)阻塞的耗时
    global process_names # 长期记录pid到execname的映射
    global entry_times%, uaddrs%
    probe syscall.futex {
        entry_times[tid()] = gettimeofday_us()
        if ((op & ~(FUTEX_PRIVATE_FLAG|FUTEX_CLOCK_REALTIME)) != FUTEX_WAIT) 
            next
        uaddrs[tid()] = futex_uaddr
    }
    probe syscall.futex.return {
        if (!(entry_times[tid()])) 
            next
        elapsed = gettimeofday_us() - entry_times[tid()]
        delete entry_times[tid()]
        lock_waits[pid(), uaddrs[tid()]] <<< elapsed
        delete uaddrs[tid()]
        if (!(pid() in process_names))
            process_names[pid()] = execname()
    }
    probe end {
        foreach ([pid+, lock] in lock_waits)
            printf ("%s[%d] lock %p contended %d times, %d avg us\n", process_names[pid], pid, lock, @count(lock_waits[pid,lock]), @avg(lock_waits[pid,lock]))
    }
    ```
  futexes.stp脚本需要手动停止；退出时，它会打印以下信息：
    - 造成争用的进程的名称和ID
    - 竞争锁变量的位置
    - 锁变量被争用的次数
    - 整个探测期间的平均争用时间

  示例5.19 “futexes.stp示例输出” 包含了脚本退出时（大约20秒后）的部分输出内容。
- **示例5.19 futexes.stp示例输出**
  ```log
  automount[2825] lock 0x00bc7784 contended 18 times, 999931 avg us 
  synergyc[3686] lock 0x0861e96c contended 192 times, 101991 avg us 
  ...
  synergyc[3758] lock 0x08d98744 contended 192 times, 101990 avg us 
  synergyc[3938] lock 0x0982a8b4 contended 192 times, 101997 avg us 
  ...
  ```

## 第6章 理解SystemTap错误
----
本章介绍使用SystemTap时可能遇到的常见错误。

### 6.1 解析和语义错误
解析和语义错误，发生在SystemTap将脚本解析并转换为C代码、生成内核模块之前。例如，类型错误通常源于为变量或数组赋予无效值的操作。
- **解析错误：预期为foo，却看到bar**（⁠parse error: expected foo, saw bar）：
  脚本包含语法或排版错误。SystemTap根据探测的上下文，检测到构造类型不正确。例如，下面这个无效的SystemTap脚本缺少探测处理程序：
  ```bash
  probe vfs.read
  probe vfs.write
  ```
  尝试运行这个SystemTap脚本时会失败，并显示以下错误消息，表明解析器在第2行第1列期望的不是probe关键字：

  ```
    parse error: expected one of '. , ( ? ! { = +='
    saw: keyword at perror.stp:2:1
    1 parse error(s).
  ```
- **解析错误：非特权脚本中包含嵌入式代码**（parse error: embedded code in unprivileged script）：
  脚本包含不安全的嵌入式C代码，即由%{和%}包围的代码块。SystemTap允许在脚本中嵌入C代码，如果没有合适的tapsets，这会很有用。但是，嵌入式C构造并不安全，如果脚本中出现此类构造，SystemTap会报告此错误以警告用户。如果你确定脚本中的类似构造是安全的，并且你是stapdev组的成员（或具有root权限），可以使用-g选项以 “专家” 模式运行脚本：
  ```
  stap -g script
  ```

- **语义错误：标识符'foo'的类型不匹配……字符串与长整型**（semantic error: type mismatch for identifier 'foo' ... string vs. long）：
  脚本中的函数foo使用了错误的类型（如%s或%d）。在下面的示例中，格式说明符应该是%s而不是%d，因为execname()函数返回的是字符串：
  ```bash
  probe syscall.open
  printf ("%d(%d) open\n", execname(), pid())
  ```

- **语义错误：标识符'foo'的类型未解析**（semantic error: unresolved type for identifier 'foo'）：
  使用了标识符（变量），但无法确定其类型（整数或字符串）。例如，在脚本从未为变量赋值的情况下，在printf语句中使用该变量时，就会出现这种情况。

- **语义错误：期望符号或数组索引表达式**（semantic error: Expecting symbol or array index expression）：
  SystemTap无法为变量或数组中的某个位置赋值。赋值的目标不是有效的目标。以下示例代码会生成此错误：
  ```bash
  probe begin { printf("x") = 1 }
  ```

- **语义错误：在搜索N元函数时，函数调用未解析**（⁠while searching for arity N function, semantic error: unresolved function call）：
  脚本中的函数调用或数组索引表达式使用了无效数量的参数。在SystemTap中，元数（arity）可以指数组的索引数量，也可以指函数的参数数量。

- **语义错误：不支持数组局部变量，是否缺少全局声明？**（⁠semantic error: array locals not supported, missing global declaration?）：
  脚本在未将数组声明为全局变量的情况下使用了数组操作（在SystemTap脚本中，全局变量可以在使用后声明）。如果使用数组时索引数量不一致，也会出现类似的消息。

- **语义错误：在'foreach'迭代期间修改了变量'foo'**（⁠semantic error: variable 'foo' modified during 'foreach' iteration
）：
  数组foo在活动的foreach循环中被修改（赋值或删除）。如果脚本中的某个操作在foreach循环中进行函数调用，也会显示此错误。

- **语义错误：在位置N探测点不匹配，解析探测点foo时出错**（⁠semantic error: probe point mismatch at position N, while resolving probe point foo
）：
  SystemTap不理解事件或SystemTap函数foo的含义。这通常意味着SystemTap在tapset库中找不到与foo匹配的项。N指的是错误所在的行和列。

- **语义错误：无法解析探测点，解析探测点foo时出错**（⁠semantic error: no match for probe point, while resolving probe point foo
）：
  由于多种原因，SystemTap无法解析事件或处理程序函数foo。当脚本包含事件kernel.function("something")，而something不存在时，就会出现此错误。在某些情况下，该错误也可能意味着脚本包含无效的内核文件名或源代码行号。

- **语义错误：未解析的目标符号表达式**（⁠semantic error: unresolved target-symbol expression
）：
  脚本中的处理程序引用了目标变量，但无法解析该变量的值。此错误也可能意味着处理程序在无效的上下文中引用了目标变量，这可能是生成代码的编译器优化导致的结果。

- **语义错误：libdwfl失败**（⁠semantic error: libdwfl failure
）：
  处理调试信息时出现问题。在大多数情况下，此错误是由于安装的kernel-debuginfo包的版本与被探测的内核不完全匹配，或者安装的kernel-debuginfo包本身可能存在一致性或正确性问题。

- **语义错误：找不到foo的调试信息**（⁠semantic error: cannot find foo debuginfo
）：
  SystemTap找不到合适的kernel-debuginfo包。

### 6.2 运行时错误和警告
运行时错误和警告，发生在SystemTap检测工具已安装并在系统上收集数据时。
- **警告：错误数量：N，跳过的探测：M**（⁠WARNING: Number of errors: N, skipped probes: M）：
  在本次运行期间发生了错误和 / 或跳过了探测。N和M表示由于某些条件（如在一段时间内执行事件处理程序所需时间过长）而未执行的探测数量。

- **除以零**（⁠division by 0）：
  脚本代码执行了无效的除法操作。

- **聚合元素未找到**（⁠aggregate element not found
）：
  在尚未累积任何值的聚合上，调用了除@count之外的统计提取函数，这类似于除以零的情况。

- **聚合溢出**（⁠aggregation overflow
）：
  此时，包含聚合值的数组包含了太多不同的键值对。

- **MAXNESTING超出限制**（⁠MAXNESTING exceeded
）：
  尝试的函数调用嵌套级别过多。默认允许的函数调用嵌套级别为10。

- **MAXACTION超出限制**（⁠MAXACTION exceeded
）：
  探测处理程序在探测处理程序中尝试执行的语句过多。默认情况下，探测处理程序中允许的操作数为1000。

- **在内核 / 用户空间字符串复制错误，地址为ADDR**（⁠kernel/user string copy fault at ADDR
）：
  探测处理程序试图在无效地址（ADDR）处从内核或用户空间复制字符串。

- **指针解引用错误**（⁠pointer dereference fault）：
  在指针解引用操作（如目标变量求值）期间遇到错误。


## 第7章 参考文献
----
本章列举了有关SystemTap的更多信息的参考资料。在编写高级探测和tapsets时，请参考这些资料。
- **SystemTap Wiki**：SystemTap Wiki是与SystemTap的部署、使用和开发相关的链接和文章的集合。可以在 http://sourceware.org/systemtap/wiki/HomePage 上找到它。

- **SystemTap教程**：本书的大部分内容来自SystemTap教程。SystemTap教程更适合具有C++和内核开发中级到高级知识的用户，可以在 http://sourceware.org/systemtap/tutorial/ 上找到它。

- **man stapprobes**：stapprobes(3stap)手册页列举了SystemTap支持的各种探测点，以及SystemTap tapset库定义的其他别名。手册页的底部列出了其他手册页，这些手册页列举了特定系统组件的类似探测点，如tapset::scsi、tapset::kprocess、tapset::signal等。

- **man stapfuncs**：stapfuncs(3stap)手册页列举了SystemTap tapset库支持的众多函数，以及每个函数的规定语法。不过，它并未提供所有支持函数的完整列表，还有更多未记录的函数可用。

- **SystemTap Tapset参考手册**：SystemTap Tapset参考手册更详细地描述了tapsets中预定义的函数和探测点。可以在 http://sourceware.org/systemtap/tapsets/ 上找到它。

- **SystemTap语言参考**：SystemTap语言参考是对SystemTap语言结构和语法的全面参考。建议具有C++和其他类似编程语言的基础到中级知识的用户使用，所有用户都可以在 http://sourceware.org/systemtap/langref/ 上访问它。

- **Tapset开发者指南**：当你具备足够的编写SystemTap脚本的能力后，可以尝试编写自己的tapsets。Tapset开发者指南描述了如何向tapset库中添加函数。

- **测试套件**：systemtap-testsuite软件包允许你测试整个SystemTap工具链，而无需从源代码构建它。此外，它还包含许多SystemTap脚本示例供学习和测试；其中一些脚本也在第5章 “有用的SystemTap脚本” 中进行了介绍。默认情况下，systemtap-testsuite中包含的示例脚本位于/usr/share/systemtap/testsuite/systemtap.examples/目录中。 


## 第8章 Appendix A. Revision History（修改历史）
----
Revision 2.0-1 Mon Jul 20 2009 includes 5.4 minor updates and additional script "dropwatch.stp"
Don Domingo ddomingo@redhat.com
Revision 1.0-1 Wed Jun 17 2009 Building+pushing to RHEL
Don Domingo ddomingo@redhat.com


## 第9章 Index（索引）
----
**Symbols（符号）**
`$`count
sample usage
local variables, 50
`$`return
sample usage
local variables, 47, 51
@avg (integer extractor)
computing for statistical aggregates
array operations, 34
@count (integer extractor)
computing for statistical aggregates
array operations, 33
@max (integer extractor)
computing for statistical aggregates
array operations, 33
@min (integer extractor)
computing for statistical aggregates
array operations, 33
@sum (integer extractor)
computing for statistical aggregates
array operations, 33
**A**
adding values to statistical aggregates
computing for statistical aggregates
array operations, 33
advantages of cross-instrumentation, 6
aggregate element not found
runtime errors/warnings
understainding SystemTap errors, 71
aggregates (statistical)
array operations, 32
aggregation overflow
runtime errors/warnings
understainding SystemTap errors, 72
algebraic formulas using arrays
reading values from arrays
array operations, 27
architecture notation, determining, 7
architecture of SystemTap, 11
array locals not supported
parse/semantics error
understanding SystemTap errors, 70
array operations
assigning associated values, 27
associating timestamps to process names, 27
associative arrays, 26
clearing arrays/array elements, 29
delete operator, 30
multiple array operations within the same
probe, 31
virtual file system reads (non-cumulative),
tallying, 30
computing for statistical aggregates, 32
@avg (integer extractor), 34
@count (integer extractor), 33
@max (integer extractor), 33
@min (integer extractor), 33
@sum (integer extractor), 33
adding values to statistical aggregates, 33
count (operator), 33
extracting data collected by statistical
aggregates, 33
conditional statements, using arrays in, 31
testing for array membership, 32
deleting arrays and array elements, 29
incrementing associated values, 28
tallying virtual file system reads (VFS reads),
28
multiple elements in an array, 28
processing multiple elements in an array, 28
cumulative virtual file system reads, tallying,
29
foreach, 28
iterations, processing elements in an array as,
28
limiting the output of foreach, 29
ordering the output of foreach, 29
reading values from arrays, 27
computing for timestamp deltas, 27
empty unique keys, 28
using arrays in simple computations, 27
arrays, 26
(see also associative arrays)
assigning associated values
array operations, 27
associating timestamps to process names, 27
associating timestamps to process names
array operations, 27
associated values
introduction
arrays, 26
associating timestamps to process names
assigning associated values
array operations, 27
associative arrays
introduction, 26
associated values, 26
example, 26
index expression, 26
key pairs, 26
syntax, 26
unique keys, 26
asynchronous events
Events, 14
**B**
begin
Events, 14
building instrumentation modules from SystemTap
scripts, 5
building kernel modules from SystemTap scripts, 5
**C**
call graph tracing
examples of SystemTap scripts, 57
capabilities of SystemTap
Introduction, 1
changes to file attributes, monitoring
examples of SystemTap scripts, 54
clearing arrays/array elements
array operations, 29
delete operator, 30
multiple array operations within the same
probe, 31
virtual file system reads (non-cumulative),
tallying, 30
command-line arguments
SystemTap handler constructs
handlers, 25
compiling instrumentation/kernel modules from
SystemTap scripts, 5
components
SystemTap scripts
introduction, 12
computing for statistical aggregates
array operations, 32
@avg (integer extractor), 34
@count (integer extractor), 33
@max (integer extractor), 33
@min (integer extractor), 33
@sum (integer extractor), 33
adding values to statistical aggregates, 33
count (operator), 33
extracting data collected by statistical
aggregates, 33
computing for timestamp deltas
reading values from arrays
array operations, 27
conditional operators
conditional statements
handlers, 25
conditional statements, using arrays in
array operations, 31
testing for array membership, 32
CONFIG_HZ, computing for, 20
contended user-space locks (futex contentions),
identifying
examples of SystemTap scripts, 66
copy fault
runtime errors/warnings
understainding SystemTap errors, 72
count operator
computing for statistical aggregates
array (operator), 33
counting function calls
examples of SystemTap scripts, 56
CPU ticks
examples of SystemTap scripts, 59
cpu()
functions, 17
cross-compiling, 5
cross-instrumentation
advantages of, 6
building kernel modules from SystemTap scripts,
5
configuration
host system and target system, 6
generating instrumentation from SystemTap
scripts, 5
host system, 6
instrumentation module, 6
target kernel, 6
target system, 6
ctime()
functions, 17
ctime(), example of usage
script examples, 47
cumulative I/O, tracking
examples of SystemTap scripts, 50
cumulative virtual file system reads, tallying
processing multiple elements in an array
array operations, 29
**D**
delete operator
78
clearing arrays/array elements
array operations, 30
determining architecture notation, 7
determining the kernel version, 4
determining time spent in kernel and user space
examples of SystemTap scripts, 58
device I/O, monitoring
examples of SystemTap scripts, 52
device number of a file (integer format)
examples of SystemTap scripts, 53
disk I/O traffic, summarizing
script examples, 46
division by 0
runtime errors/warnings
understainding SystemTap errors, 71
documentation goals
Introduction, 1
**E**
embedded code in unprivileged script
parse/semantics error
understanding SystemTap errors, 69
empty unique keys
reading values from arrays
array operations, 28
end
Events, 15
errors
parse/semantics error, 69
embedded code in unprivileged script, 69
expected symbol/array index expression, 70
grammatical/typographical script error, 69
guru mode, 69
invalid values to variables/arrays, 69
libdwfl failure, 71
no match for probe point, 71
non-global arrays, 70
probe mismatch, 70
type mismatch for identifier, 69
unresolved function call, 70
unresolved target-symbol expression, 71
unresolved type for identifier, 70
variable modified during 'foreach', 70
runtime errors/warnings, 71
aggregate element not found, 71
aggregation overflow, 72
copy fault, 72
division by 0, 71
MAXACTION exceeded, 72
MAXNESTING exceeded, 72
number of errors: N, skipped probes: M, 71
pointer dereference fault, 72
event types
Understanding How SystemTap Works, 11
Events
asynchronous events, 14
begin, 14
end, 15
examples of synchronous and asynchronous
events, 13
introduction, 13
kernel.function("function"), 13
kernel.trace("tracepoint"), 14
module("module"), 14
synchronous events, 13
syscall.system_call, 13
timer events, 15
user-space, 35
vfs.file_operation, 13
wildcards, 14
events and handlers, 11
events wildcards, 14
example
introduction
arrays, 26
example of multiple command-line arguments
examples of SystemTap scripts, 58
examples of synchronous and asynchronous
events
Events, 13
examples of SystemTap scripts, 39
call graph tracing, 57
CPU ticks, 59
ctime(), example of usage, 47
determining time spent in kernel and user space,
58
file device number (integer format), 53
futex (lock) contentions, 66
futex system call, 66
identifying contended user-space locks (futex
contentions), 66
if/else conditionals, alternative syntax, 40
inode number, 53
monitoring changes to file attributes, 54
monitoring device I/O, 52
monitoring I/O block time, 55
monitoring I/O time, 48
monitoring incoming TCP connections, 42
monitoring polling applications, 60
monitoring reads and writes to a file, 53

monitoring system calls, 63
monitoring system calls (volume per process),
64
monitoring TCP packets, 42
multiple command-line arguments, example of,
58
net/socket.c, tracing functions from, 41
network profiling, 39, 44
stat -c, determining file device number (integer
format), 53
stat -c, determining whole device number, 52
summarizing disk I/O traffic, 46
tallying function calls, 56
thread_indent(), sample usage, 58
timer.ms(), sample usage, 56
timer.s(), sample usage, 62, 64
tracing functions called in network socket code,
41
tracking cumulative I/O, 50
trigger function, 58
usrdev2kerndev(), 52
whole device number (usage as a command-line
argument), 52
exceeded MAXACTION
runtime errors/warnings
understainding SystemTap errors, 72
exceeded MAXNESTING
runtime errors/warnings
understainding SystemTap errors, 72
exit()
functions, 16
expected symbol/array index expression
parse/semantics error
understanding SystemTap errors, 70
extracting data collected by statistical aggregates
computing for statistical aggregates
array operations, 33
**F**
feedback
contact information for this manual, vii
file attributes, monitoring changes to
examples of SystemTap scripts, 54
file device number (integer format)
examples of SystemTap scripts, 53
file reads/writes, monitoring
examples of SystemTap scripts, 53
flight recorder mode, 9
file mode, 10
in-memory mode, 9
for loops
conditional statements
handlers, 25
foreach
processing multiple elements in an array
array operations, 28
format
introduction
arrays, 26
format and syntax
printf(), 16
SystemTap handler constructs
handlers, 19
SystemTap scripts
introduction, 12
format specifiers
printf(), 16
format strings
printf(), 16
function call (unresolved)
parse/semantics error
understanding SystemTap errors, 70
function calls (incoming/outgoing), tracing
examples of SystemTap scripts, 57
function calls, tallying
examples of SystemTap scripts, 56
functions, 17
cpu(), 17
ctime(), 17
gettimeofday_s(), 17
pp(), 17
SystemTap scripts
introduction, 12
target(), 19
thread_indent(), 17
tid(), 17, 17
uid(), 17
functions (used in handlers)
exit(), 16
functions called in network socket code, tracing
examples of SystemTap scripts, 41
futex (lock) contentions
examples of SystemTap scripts, 66
futex contention, definition
examples of SystemTap scripts, 66
futex contentions, identifying
examples of SystemTap scripts, 66
futex system call
examples of SystemTap scripts, 66

**G**
gettimeofday_s()
functions, 17
global
SystemTap handler constructs
handlers, 20
goals, documentation
Introduction, 1
grammatical/typographical script error
parse/semantics error
understanding SystemTap errors, 69
guru mode
parse/semantics error
understanding SystemTap errors, 69
**H**
handler functions, 17
handlers
conditional statements, 24
conditional operators, 25
for loops, 25
if/else, 24
while loops, 24
introduction, 15
SystemTap handler constructs, 19
command-line arguments, 25
global, 20
syntax and format, 19
variable notations, 26
variables, 19
target variables, 20
handlers and events, 11
SystemTap scripts
introduction, 12
heaviest disk reads/writes, identifying
script examples, 46
host system
cross-instrumentation, 6
host system and target system
cross-instrumentation
configuration, 6
**I**
I/O block time, monitoring
examples of SystemTap scripts, 55
I/O monitoring (by device)
examples of SystemTap scripts, 52
I/O time, monitoring
examples of SystemTap scripts, 48
I/O traffic, summarizing
script examples, 46
identifier type mismatch
parse/semantics error
understanding SystemTap errors, 69
identifying contended user-space locks (futex
contentions)
examples of SystemTap scripts, 66
identifying heaviest disk reads/writes
script examples, 46
if/else
conditional statements
handlers, 24
if/else conditionals, alternative syntax
examples of SystemTap scripts, 40
if/else statements, using arrays in
array operations, 31
incoming TCP connections, monitoring
examples of SystemTap scripts, 42
incoming/outgoing function calls, tracing
examples of SystemTap scripts, 57
incrementing associated values
array operations, 28
tallying virtual file system reads (VFS reads),
28
index expression
introduction
arrays, 26
initial testing, 5
inode number
examples of SystemTap scripts, 53
Installation
initial testing, 5
kernel information packages, 3
kernel version, determining the, 4
required packages, 3
Setup and Installation, 3
systemtap package, 3
systemtap-runtime package, 3
instrumentation module
cross-instrumentation, 6
instrumentation modules from SystemTap scripts,
building, 5
integer extractors
computing for statistical aggregates
array operations, 33
Introduction
capabilities of SystemTap, 1
documentation goals, 1
goals, documentation, 1

limitations of SystemTap, 1
performance monitoring, 1
invalid division
runtime errors/warnings
understainding SystemTap errors, 71
invalid values to variables/arrays
parse/semantics error
understanding SystemTap errors, 69
iterations, processing elements in an array as
processing multiple elements in an array
array operations, 28
**K**
kernel and user space, determining time spent in
examples of SystemTap scripts, 58
kernel information packages, 3
kernel modules from SystemTap scripts, building, 5
kernel version, determining the, 4
kernel.function("function")
Events, 13
kernel.trace("tracepoint")
Events, 14
key pairs
introduction
arrays, 26
**L**
libdwfl failure
parse/semantics error
understanding SystemTap errors, 71
limitations of SystemTap
Introduction, 1
limiting the output of foreach
processing multiple elements in an array
array operations, 29
local variables
name, 19
sample usage
$count, 50
$return, 47, 51
**M**
MAXACTION exceeded
runtime errors/warnings
understainding SystemTap errors, 72
MAXNESTING exceeded
runtime errors/warnings
understainding SystemTap errors, 72
membership (in array), testing for
conditional statements, using arrays in
array operations, 32
module("module")
Events, 14
monitoring changes to file attributes
examples of SystemTap scripts, 54
monitoring cumulative I/O
examples of SystemTap scripts, 50
monitoring device I/O
examples of SystemTap scripts, 52
monitoring I/O block time
examples of SystemTap scripts, 55
monitoring I/O time
examples of SystemTap scripts, 48
monitoring incoming TCP connections
examples of SystemTap scripts, 42
monitoring polling applications
examples of SystemTap scripts, 60
monitoring reads and writes to a file
examples of SystemTap scripts, 53
monitoring system calls
examples of SystemTap scripts, 63
monitoring system calls (volume per process)
examples of SystemTap scripts, 64
monitoring TCP packets
examples of SystemTap scripts, 42
multiple array operations within the same probe
clearing arrays/array elements
array operations, 31
multiple command-line arguments, example of
examples of SystemTap scripts, 58
multiple elements in an array
array operations, 28
**N**
name
local variables, 19
net/socket.c, tracing functions from
examples of SystemTap scripts, 41
network profiling
examples of SystemTap scripts, 39, 44
network socket code, tracing functions called in
examples of SystemTap scripts, 41
network traffic, monitoring
examples of SystemTap scripts, 39, 44
no match for probe point
parse/semantics error
understanding SystemTap errors, 71
non-global arrays
parse/semantics error
understanding SystemTap errors, 70
82
number of errors: N, skipped probes: M
runtime errors/warnings
understainding SystemTap errors, 71
**O**
operations
assigning associated values
associating timestamps to process names, 27
associative arrays, 26
clearing arrays/array elements, 29
delete operator, 30
multiple array operations within the same
probe, 31
virtual file system reads (non-cumulative),
tallying, 30
computing for statistical aggregates, 32
@avg (integer extractor), 34
@count (integer extractor), 33
@max (integer extractor), 33
@min (integer extractor), 33
@sum (integer extractor), 33
adding values to statistical aggregates, 33
count (operator), 33
extracting data collected by statistical
aggregates, 33
conditional statements, using arrays in, 31
testing for array membership, 32
deleting arrays and array elements, 29
incrementing associated values, 28
tallying virtual file system reads (VFS reads),
28
multiple elements in an array, 28
processing multiple elements in an array, 28
cumulative virtual file system reads, tallying,
29
foreach, 28
iterations, processing elements in an array as,
28
limiting the output of foreach, 29
ordering the output of foreach, 29
reading values from arrays, 27
computing for timestamp deltas, 27
empty unique keys, 28
using arrays in simple computations, 27
options, stap
Usage, 8
ordering the output of foreach
processing multiple elements in an array
array operations, 29
overflow of aggregation
runtime errors/warnings
understainding SystemTap errors, 72
**P**
packages required to run SystemTap, 3
parse/semantics error
understanding SystemTap errors, 69
embedded code in unprivileged script, 69
expected symbol/array index expression, 70
grammatical/typographical script error, 69
guru mode, 69
invalid values to variables/arrays, 69
libdwfl failure, 71
no match for probe point, 71
non-global arrays, 70
probe mismatch, 70
type mismatch for identifier, 69
unresolved function call, 70
unresolved target-symbol expression, 71
unresolved type for identifier, 70
variable modified during 'foreach', 70
performance monitoring
Introduction, 1
pointer dereference fault
runtime errors/warnings
understainding SystemTap errors, 72
polling applications, monitoring
examples of SystemTap scripts, 60
pp()
functions, 17
printf()
format specifiers, 16
format strings, 16, 16
syntax and format, 16
printing I/O activity (cumulative)
examples of SystemTap scripts, 50
printing I/O block time (periodically)
examples of SystemTap scripts, 55
probe mismatch
parse/semantics error
understanding SystemTap errors, 70
probe point (no match for)
parse/semantics error
understanding SystemTap errors, 71
probes
SystemTap scripts
introduction, 12
processing multiple elements in an array
array operations, 28
cumulative virtual file system reads, tallying

array operations, 29
foreach
array operations, 28
limiting the output of foreach
array operations, 29
ordering the output of foreach
array operations, 29
profiling the network
examples of SystemTap scripts, 39, 44
**R**
reading values from arrays
array operations, 27
empty unique keys, 28
using arrays in simple computations, 27
computing for timestamp deltas
array operations, 27
reads/writes to a file, monitoring
examples of SystemTap scripts, 53
required packages, 3
RPMs required to run SystemTap, 3
running scripts from standard input, 8
running SystemTap scripts
Usage, 7
runtime errors/warnings
understainding SystemTap errors, 71
aggregate element not found, 71
aggregation overflow, 72
copy fault, 72
division by 0, 71
MAXACTION exceeded, 72
MAXNESTING exceeded, 72
number of errors: N, skipped probes: M, 71
pointer dereference fault, 72
**S**
script examples
call graph tracing, 57
CPU ticks, 59
ctime(), example of usage, 47
determining time spent in kernel and user space,
58
file device number (integer format), 53
futex (lock) contentions, 66
futex system call, 66
identifying contended user-space locks (futex
contentions), 66
if/else conditionals, alternative syntax, 40
inode number, 53
monitoring changes to file attributes, 54
monitoring device I/O, 52
monitoring I/O block time, 55
monitoring I/O time, 48
monitoring incoming TCP connections, 42
monitoring polling applications, 60
monitoring reads and writes to a file, 53
monitoring system calls, 63
monitoring system calls (volume per process),
64
monitoring TCP packets, 42
multiple command-line arguments, example of,
58
net/socket.c, tracing functions from, 41
network profiling, 39, 44
stat -c, determining file device number (integer
format), 53
stat -c, determining whole device number, 52
summarizing disk I/O traffic, 46
tallying function calls, 56
thread_indent(), sample usage, 58
timer.ms(), sample usage, 56
timer.s(), sample usage, 62, 64
tracing functions called in network socket code,
41
tracking cumulative I/O, 50
trigger function, 58
usrdev2kerndev(), 52
whole device number (usage as a command-line
argument), 52
scripts
introduction, 11
components, 12
events and handlers, 12
format and syntax, 12
functions, 12
probes, 12
statement blocks, 12
sessions, SystemTap, 11
Setup and Installation, 3
Stack backtrace
user-space, 37
standard input, running scripts from
Usage, 8
stap
Usage, 7
stap options, 8
stapdev
Usage, 7
staprun
Usage, 7

stapusr
Usage, 8
stat -c, determining file device number (integer
format)
examples of SystemTap scripts, 53
stat -c, determining whole device number
examples of SystemTap scripts, 52
statement blocks
SystemTap scripts
introduction, 12
statistical aggregates
array operations, 32
summarizing disk I/O traffic
script examples, 46, 46
synchronous events
Events, 13
syntax
introduction
arrays, 26
syntax and format
printf(), 16
SystemTap handler constructs
handlers, 19
SystemTap scripts
introduction, 12
syscall.system_call
Events, 13
system calls volume (per process), monitoring
examples of SystemTap scripts, 64
system calls, monitoring
examples of SystemTap scripts, 63
SystemTap architecture, 11
SystemTap handlers
SystemTap handler constructs, 19
syntax and format, 19
systemtap package, 3
SystemTap script functions, 17
SystemTap scripts
introduction, 11
components, 12
events and handlers, 12
format and syntax, 12
functions, 12
probes, 12
statement blocks, 12
useful examples, 39
SystemTap scripts, how to run, 7
SystemTap sessions, 11
SystemTap statements
conditional statements, 24
conditional operators, 25
for loops, 25
if/else, 24
while loops, 24
SystemTap handler constructs
command-line arguments, 25
global, 20
variable notations, 26
variables, 19
systemtap-runtime package, 3
systemtap-testsuite package
sample scripts, 39
**T**
tallying function calls
examples of SystemTap scripts, 56
tallying virtual file system reads (VFS reads)
incrementing associated values
array operations, 28
Tapsets
definition of, 34
target kernel
cross-instrumentation, 6
target system
cross-instrumentation, 6
target system and host system
configuration, 6
target variables, 20
pretty printing, 22
typecasting, 23
user-space, 36
variable availability, 23
target()
functions, 19
target-symbol expression, unresolved
parse/semantics error
understanding SystemTap errors, 71
TCP connections (incoming), monitoring
examples of SystemTap scripts, 42
TCP packets, monitoring
examples of SystemTap scripts, 42, 42
testing for array membership
conditional statements, using arrays in
array operations, 32
testing, initial, 5
thread_indent()
functions, 17
thread_indent(), sample usage
examples of SystemTap scripts, 58
tid()

functions, 17
time of I/O
examples of SystemTap scripts, 48
time spent in kernel/user space, determining
examples of SystemTap scripts, 58
timer events
Events, 15
timer.ms(), sample usage
examples of SystemTap scripts, 56
timer.s(), sample usage
examples of SystemTap scripts, 62, 64
timestamp deltas, computing for
reading values from arrays
array operations, 27
timestamps, association thereof to process names
assigning associated values
array operations, 27
tracepoint, 14, 44
tracing call graph
examples of SystemTap scripts, 57
tracing functions called in network socket code
examples of SystemTap scripts, 41
tracing incoming/outgoing function calls
examples of SystemTap scripts, 57
tracking cumulative I/O
examples of SystemTap scripts, 50
trigger function
examples of SystemTap scripts, 58
type mismatch for identifier
parse/semantics error
understanding SystemTap errors, 69
typographical script error
parse/semantics error
understanding SystemTap errors, 69
**U**
uid()
functions, 17
uname -m, 7
uname -r, 4
understainding SystemTap errors
runtime errors/warnings, 71
aggregate element not found, 71
aggregation overflow, 72
copy fault, 72
division by 0, 71
MAXACTION exceeded, 72
MAXNESTING exceeded, 72
number of errors: N, skipped probes: M, 71
pointer dereference fault, 72
Understanding How SystemTap Works, 11
architecture, 11
event types, 11
events and handlers, 11
SystemTap sessions, 11
understanding SystemTap errors
parse/semantics error, 69
embedded code in unprivileged script, 69
expected symbol/array index expression, 70
grammatical/typographical script error, 69
guru mode, 69
invalid values to variables/arrays, 69
libdwfl failure, 71
no match for probe point, 71
non-global arrays, 70
probe mismatch, 70
type mismatch for identifier, 69
unresolved function call, 70
unresolved target-symbol expression, 71
unresolved type for identifier, 70
variable modified during 'foreach', 70
unique keys
introduction
arrays, 26
unprivileged script, embedded code in
parse/semantics error
understanding SystemTap errors, 69
unresolved function call
parse/semantics error
understanding SystemTap errors, 70
unresolved target-symbol expression
parse/semantics error
understanding SystemTap errors, 71
unresolved type for identifier
parse/semantics error
understanding SystemTap errors, 70
unsafe embedded code in unprivileged script
parse/semantics error
understanding SystemTap errors, 69
Usage
options, stap, 8
running SystemTap scripts, 7
standard input, running scripts from, 8
stap, 7
stapdev, 7
staprun, 7
stapusr, 8
useful examples of SystemTap scripts, 39
user and kernel space, determining time spent in
examples of SystemTap scripts, 58
86
using arrays in simple computations
reading values from arrays
array operations, 27
Using SystemTap, 3
usrdev2kerndev()
examples of SystemTap scripts, 52
**V**
values, assignment of
array operations, 27
variable modified during 'foreach'
parse/semantics error
understanding SystemTap errors, 70
variable notations
SystemTap handler constructs
handlers, 26
variables
SystemTap handler constructs
handlers, 19
variables (local)
name, 19
sample usage
`$`count, 50
`$`return, 47, 51
VFS reads, tallying of
incrementing associated values
array operations, 28
vfs.file_operation
Events, 13
virtual file system reads (cumulative), tallying
processing multiple elements in an array
array operations, 29
virtual file system reads (non-cumulative), tallying
clearing arrays/array elements
array operations, 30
**W**
while loops
conditional statements
handlers, 24
whole device number (usage as a command-line
argument)
examples of SystemTap scripts, 52
wildcards in events, 14
writes/reads to a file, monitoring
examples of SystemTap scripts, 53