---
title: wireshark抓包之目标主机不可达
date: 2025-10-15 15:11:11
author: Navyum
icon: lucide-lab:shark

tags: 
 - wireshark
 - 抓包
 - icmp
categories: 
 - wireshark
 - 工具

article: true
index: true

headerDepth: 2
sticky: true
star: true
---
## wireshark抓包

### wireshark抓包之目标主机不可达 Destination unreachable (3)
---

### 背景：
最近自己新购买了一台虚拟机，想要搭建一些web服务到这台机器上并通过互联网访问

### 出现问题：
机器购买后，添加了nginx对应的web服务，本地测试curl 'localhost' 正常，但是通过互联网的公网IP访问curl 'server-ip'则请求一直Pending直到超时。
另外该服务器上还有一个不依赖nginx直接暴露8000端口在公网的docker镜像服务，使用curl 'server-ip:8000/route'可以正常访问。


### 最终定位到原因：
直接原因：服务器网络存在无法访问的问题
根本原因：服务器的一些特定端口没有开放，存在默认的防火墙策略


### 分析过程：
1. 复现问题：
   <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/3883d164aa2c9ecf45af56d4ebd05973.png" width="80%"></p>

2. 因为服务本身3000端口正常，直接ping测试网络，网络连接正常。
   <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/5d2b987afda1677b00a4e044f1c3e109.png" width="80%"></p>

1. 此刻我已经蚌住了。只能采用tcpdump进行抓包，在wireshark中打开分析协议[firewall.pcap](firewall.pcap)
   * wireshark解析结果：
     <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/0ecf9df6125bc5e61d81d4e678e0c5e9.png" width="80%"></p>
   * 错误信息：
     <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/6b8ea5d9a4ba674e9857f68d898b7a99.png" width="80%"></p>

4. 解析抓包结果：
    1. 总共获取到两个包，1号包为客户端尝试TCP握手包（Seq=0），2号包为ICMP包。
    2. 根据常识，客户端TCP握手，你服务端应该给我返回TCP包，完成三次握手然后建立连接啊。
    3. 然后根据返回的错误信息，查询ICMP协议（互联网控制报文协议），这服务端网络不可达啊。从Host administratively prohibited可以猜测出，这感觉是个权限问题。
       ```bash
       Type: Destination unreachable (3)
       Code: 10 (Host administratively prohibited)
       ```
    4. 因为3000端口正常，此时我第一个就是怀疑是不是网络链路上存在限制导致的80端口无法访问。再次使用traceroute进行检查
       <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/a4f3281b16efce5b97fe969da75a7d78.png" width="80%"></p>
    5. 为了保持和curl中错误的一致性，所以我强制使用ICMP协议进行链路检测（备注：traceroute默认是使用UDP协议的）。结果证明，整个链路没有任何问题，抓包获取到的ICMP错误就是服务器返回的。此刻已经定位到出现问题的来源了。（备注：命令行中指定的80端口其实不生效，因为ICMP协议本身没有Port这个概念，这个和TCP、UDP不一样，指定ICMP时，命令自动忽略-p选项）
    6. 查找ICMP官方RFC资料
       
       相关资料：[rfc1122 官方文档](https://www.rfc-editor.org/rfc/rfc1122.html)
        > 3.2.2.1  Destination Unreachable: RFC-792
        > ...
        > **10 = communication with destination host administratively prohibited**
        >
        >    A Destination Unreachable message that is received MUST be
        >     reported to the transport layer.  The transport layer SHOULD
        >     use the information appropriately; for example, see Sections
        >     4.1.3.3, 4.2.3.9, and 4.2.4 below.  A transport protocol
        >     that has its own mechanism for notifying the sender that a
        >     port is unreachable (e.g., TCP, which sends RST segments)
        >     MUST nevertheless accept an ICMP Port Unreachable for the
        >     same purpose.
    1. 排查服务器防火墙，发现安装的是firewall-cmd，查询得知firewall-cmd默认关闭了所有的1～1023的端口（很多默认服务的端口）。而8000端口不属于这个范围内，默认是放开状态。（好坑爹啊）。另外firewall默认使用的是public这个zone [官方文档](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/8/html/configuring_and_managing_networking/controlling-network-traffic-using-firewalld_using-and-configuring-firewalld)
       ```bash
        firewall-cmd --get-services         # 获取所有知名服务
        firewall-cmd --query-service=http   # 获取http服务的开放状态
       ```

5. 两种解决方案，选择其一：
    * 通过services方式，对已定义的服务http、https，添加开放策略（对服务端协议理解一般的，直接开放http、https更省心）
       ```bash
        firewall-cmd --add-service=http  --permanent        # 永久开放http服务（即80端口）
        firewall-cmd --add-service=https --permanent        # 永久开放https服务（即443端口）
        firewall-cmd --reload                               # 重启后生效
        firewall-cmd --list-all                             # 查看services字段，http、https是否有开放成功
       ```
    * 通过ports方式，对指定协议+端口号方式，开放80、443端口（对动手强的更推荐这个方式，更透明些）
       ```bash
       firewall-cmd --add-port=80/tcp  --permanent
       firewall-cmd --add-port=443/tcp --permanent
        firewall-cmd --reload                               # 重启后生效
        firewall-cmd --list-all                             # 查看ports字段，http、https是否有开放成功
       ```

### 延伸：
#### 关于ICMP协议
* 即 Internet Control Message Protocol，互联网控制报文协议
![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/f0bf192a1cf0f08545024033e15b4ed5.png)

* 查询报文类型：
    - 8：主动查询
    - 0：主动查询回显

* 差错报文类型（Type）：
    - 3：终点不可达（地址不可达，本次抓包定位到的问题大类）
    - 4：源抑制（让源站放慢发送速度）
    - 5：重定向（让下次发给另一个路由器）
    - 11：超时（也就是超过网络包的生存时间还是没到）


* 具体应用：
    * `ping`：主动发送查询报文，获得查询回显报文
    * `traceroute`：默认发送udp数据包（也可指定其他类型），做网络探测：
        1. 探测沿途的路由（超时类型）：
            * 使用特殊的TTL，将TTL逐个累增，逐个获取链路上的路由器 IP
        2. 探测目的主机（不可达类型）：
            * 使用不可能UDP端口号，收到端口不可达回应，则表示成功到达目的主机 
        3. 确定整条路径的MTU（分片错误类型）：
            * 故意设置为不分片，每次收到该差错报文，则调小MTU，直到到达目的主机