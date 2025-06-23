---
title: systemTap安装
date: 2025-04-03 10:32:17
author: Navyum
tags: 
 - SystemTap
 - 性能分析

categories: 
 - 工具
 - 性能分析
 - Systemtap
---
## systemTap安装

## 当前环境：cenos7
```bash
$cat /etc/redhat-release
 CentOS Linux release 7.9.2009 (Core) # 查看操作系统版本

$uname -r
 3.10.0-1160.53.1.el7.x86_64      # 查看内核版本
```

## 安装：
### 安装systemtap
```bash
$ yum install -y systemtap systemtap-runtime
```

### 安装依赖
依赖项：
    * `kernel-devel-$(uname -r)、kernel-debuginfo-$(uname -r)、kernel-debuginfo-common-$(uname -r)`
    * 依赖项一定要和内核版本一致，否则无法成功。如果不一致，则需要安装kernel、kernel-devel。

#### 一、自动安装
```bash
$ stap-prep # 一般安装都会报错，需要手动安装
```
#### 二、手动安装
1. yum 直接安装
   ```bash
   $ sudo yum install -y kernel-devel-$(uname -r) kernel-debuginfo-$(uname -r) kernel-debuginfo-common-$(uname -r)
   ```
   如果报错：`No package kernel-xx available，则需要使用下面的手动下载对应rpm，然后安装

2. yum 离线安装
   * **离线安装kernel、kernel-devel**
     * 如何找离线包： 
        * 镜像地址1：`https://mirrors.aliyun.com/centos-vault/$your_centos_version/updates/x86_64/Packages/kernel-$(uname -r).rpm`    
        * 镜像地址2：`https://mirror.tuna.tsinghua.edu.cn/centos-vault/$your_centos_version/updates/x86_64/Packages/kernel-$(uname -r).rpm`
        * 注意⚠️：vault表示过期的镜像，因为7系列已经不在维护了，所以对应系统的包只能到这个里面找
     * 找到后右键复制下载地址
     * 下载离线包 `$ sudo wget 下载地址`
     * 安装离线包 `$ sudo rpm -ivh kernel-xxx.rpm`
   * **kernel-debuginfo 的另一种安装方式**：
     ```bash
     $ sudo debuginfo-install -y kernel-$(uname -r)
     ```

#### 验证systemtap
```bash
$ sudo stap -v -e 'probe vfs.read {printf("read performed\n"); exit()}'

Pass 1: parsed user script and 476 library scripts using 272304virt/69548res/3500shr/66148data kb, in 670usr/40sys/714real ms.
Pass 2: analyzed script: 1 probe, 1 function, 7 embeds, 0 globals using 439692virt/232156res/4832shr/233536data kb, in 1970usr/460sys/2424real ms.
Pass 3: using cached /root/.systemtap/cache/3a/stap_3acbc48da4d846dbd13b2e55b382b10f_2806.c
Pass 4: using cached /root/.systemtap/cache/3a/stap_3acbc48da4d846dbd13b2e55b382b10f_2806.ko
Pass 5: starting run.
read performed
Pass 5: run completed in 0usr/30sys/342real ms.
```

看到 run completed 则表示安装成功