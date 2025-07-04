---
title: RocketMQ原理
date: 2025-06-17 15:15:24
author: Navyum
tags: 
 - 消息队列
 - RocketMQ
categories: 
 - 常用软件
 - 消息队列
article: true
index: true

headerDepth: 2
sticky: false
star: true
icon: simple-icons:apacherocketmq
---

## 整体架构：
<img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/dd4853b7ddf4ae9a421ff728ccaad2c4.png" width =60% >

## 与kafka对比：
* 和Kafka相比，RocketMQ在架构上做了`减法`，在功能上做了`加法`

### 架构上的差异：做减法，对kafka做精简

#### nameserver替换zookeeper：
* 用一种更轻量的方式，管理消息队列的集群信息
* 生产者通过 nameserver 获取到 topic 和 broker 的路由信息，然后再与 broker 通信，实现服务发现和负载均衡的效果
<img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/aa624423f7fc2f3d143f192230a4e034.png" width =60% >

#### queue替换partition：
* 将topic拆分成了多个分区，但换了个名字，叫 Queue，也就是"队列"
* queue与partition相比：
    * queue不存储数据，只存储offset等一些简化信息
    * 消息完整数据则放到 `commitlog` 的文件上
    * `commitlog` 的文件跟`segment文件`一样，都是滚动写入
    * 查询方式跟es查询的两个阶段一样，先查索引，再查数据，都是使用数据和索引分离的方式
    * kafka因为数据存在partition，所以只需要查询一次
    <img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/700f62da1fd6f71e5871b7fca8867186.png" width =60% >
    <img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/02536c5af01f1617aa5b19f79de39f24.png" width =60% >

#### 底层存储的差异：
* kafka 对某个broker写数据，会找到broker上对应的topic，然后找对应的partition文件夹，然后顺序写入partition下的segment文件
* rocketmq 对某个broker写数据，不需要再根据topic、partition区分文件路径，然后顺序写到同一套的commitlog
<img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/a8ea2a26a4b8635fd647e9a43f8ed62d.png" width =60% >

#### 高可用的备份差异：
* kafka 以partition粒度，冗余多个replicas，主从同步的是segment文件
* rocketmq 以broker粒度，冗余多个broker，主从同步的是commitlog文件
* 原因：
    * 因为rocketmq上不同topic的数据都是写在同一套commitlog，如果要拆细，还得对commitlog做拆分
<img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/33dc316a68f9e8ba502ab3b44f40ca15.png" width =60% >

### 功能上的差异：做加法，支持更多功能

#### 支持消息过滤：
* 支持给消息打`tag`，消费者能根据 tag 过滤所需要的数据
* 通过topic进行业务类型分类，通过tag 进行二级更细粒度的分类

#### 支持更准确的事务：
* kafka的事务只能保证多个消息同时成功或失败
* rocketmq 支持生产者业务上，`功能逻辑` + `发消息`这两个操作的事务。即功能执行正常且发消息成功，则事务成功；否则事务失败，自动回滚。

#### 支持延时队列：
* 让消费者一定时延后，才能成功获取到对应消息

#### 支持死信队列：
* 将多次重试失败的消息放到死信队列，方便后续的人工干预

#### 消息回溯：
* 支持继续offset回溯
* 额外支持基于时间回溯