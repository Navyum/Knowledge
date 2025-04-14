---
title: systemTap分析
date: 2025-04-11 14:52:58
author: Navyum
tags: 
 - systemtap、nginx源码、性能分析、TCP FIN、TCP RST
categories: 
 - 笔记
---
## systemTap分析
本文主要通过案例演示的方式，介绍个人在使用systemtap对nginx（openresty）进行网络相关的探测的使用过程、使用感受以及过程中遇到的问题

### 背景介绍：
问题： 分析openresty（nginx）在出现abort时，为什么FIN正常关闭TCP连接，而不是使用RST？

### 第一步：需要知道如何添加探测点
* 探测点跟断点的概念类似，就是在指定位置，进行debug信息的输出
* **重要！** 查看对应程序的所有function，以nginx为例
  ```bash
    # 查看Nginx可用的探针点
    sudo stap -L 'process("/usr/local/openresty/nginx/sbin/nginx").function("*")'(还有一种方式是：使用nm ./sbin/nginx，但是看不到参数和文件位置)

    # 看到的输出如下：
    ...
    process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_http_variables_add_core_vars@src/http/ngx_http_variables.c:2592") $cf:ngx_conf_t*
    process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_http_variables_init_vars@src/http/ngx_http_variables.c:2635") $cf:ngx_conf_t* $hash:ngx_hash_init_t
    process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_http_wait_request_handler@src/http/ngx_http_request.c:375") $rev:ngx_event_t*
    process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_http_weak_etag@src/http/ngx_http_core_module.c:1703") $r:ngx_http_request_t*
    process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_http_write_filter@src/http/ngx_http_write_filter_module.c:48") $r:ngx_http_request_t* $in:ngx_chain_t*
    process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_http_write_filter_init@src/http/ngx_http_write_filter_module.c:362") $cf:ngx_conf_t*
    process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_http_write_request_body@src/http/ngx_http_request_body.c:484") $r:ngx_http_request_t*
    process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_http_writer@src/http/ngx_http_request.c:2786") $r:ngx_http_request_t*
    process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_http_xss_body_filter@../xss-nginx-module-0.06/src/ngx_http_xss_filter_module.c:264") $r:ngx_http_request_t* $in:ngx_chain_t* $ll:ngx_chain_t**
  ```
* 找到需要添加探测点的函数、结构体、变量
    * 假设我们需要找nginx中，某个URI的函数调用栈信息
    * 添加探测点之前，我们需要一些基础知识。nginx关闭连接的标准函数为：`ngx_close_connection`
    * 通过如下命令，查看当前版本是否可以添加相应探测点
      ```bash
      sudo stap -L 'process("/usr/local/openresty/nginx/sbin/nginx").function("*")'|grep ngx_close_connection
      
      process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_close_connection@src/core/ngx_connection.c:1179") $c:ngx_connection_t*
      ```
      这样我们确认当前的nginx版本存在函数，且得到该函数的第一个参数为`$c`，属于结构体指针`ngx_connection_t*`


### 第二步：编写stp脚本
```tcp-close.stp
probe process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_close_connection") {
    if (target() == pid()) {
        printf("Close conn %d \n", $c->number)
        print_ubacktrace()
    }
}

probe kernel.function("tcp_reset") {
    if (pid() == target()) {
        printf("TCP RST sent%s",$sk$)
    }
}

probe kernel.function("tcp_send_fin") {
    if (pid() == target()) {
        printf("TCP FIN sent%s %s",$sk$, $skb$)
    }
}
```



### 第三步：执行并将结果可视化
* 执行：`stap tcp-close.stp -x <pid>`，同时使用curl请求url `curl $url` 

* 得到结果：
    ```log
    ERROR Close conn 12090529 
    0x47cc10 : ngx_close_connection+0x0/0x330 [/usr/local/openresty/nginx/sbin/nginx]
    0x4af7ed : ngx_http_close_connection+0x4d/0xa0 [/usr/local/openresty/nginx/sbin/nginx]
    0x4ac97a : ngx_http_core_content_phase+0x2a/0x170 [/usr/local/openresty/nginx/sbin/nginx]
    0x4a6d45 : ngx_http_core_run_phases+0x25/0x50 [/usr/local/openresty/nginx/sbin/nginx]
    0x4b2d63 : ngx_http_process_request+0xa3/0x2d0 [/usr/local/openresty/nginx/sbin/nginx]
    0x4b3382 : ngx_http_process_request_headers+0x3f2/0x460 [/usr/local/openresty/nginx/sbin/nginx]
    0x4b3754 : ngx_http_process_request_line+0x364/0x400 [/usr/local/openresty/nginx/sbin/nginx]
    0x498099 : ngx_epoll_process_events+0x429/0x470 [/usr/local/openresty/nginx/sbin/nginx]
    0x48ce33 : ngx_process_events_and_timers+0x93/0x2a0 [/usr/local/openresty/nginx/sbin/nginx]
    0x495b05 : ngx_worker_process_cycle+0x45/0x1b0 [/usr/local/openresty/nginx/sbin/nginx]
    0x49447c : ngx_spawn_process+0x17c/0x510 [/usr/local/openresty/nginx/sbin/nginx]
    0x495e94 : ngx_start_worker_processes+0x74/0xe0 [/usr/local/openresty/nginx/sbin/nginx]
    0x496ec4 : ngx_master_process_cycle+0x444/0xae0 [/usr/local/openresty/nginx/sbin/nginx]
    0x46af59 : main+0x819/0xb38 [/usr/local/openresty/nginx/sbin/nginx]
    0x7fb422a43555 : __libc_start_main+0xf5/0x1c0 [/usr/lib64/libc-2.17.so]
    0x46b2a1 : _start+0x29/0x38 [/usr/local/openresty/nginx/sbin/nginx]

    TCP FIN sent{.__sk_common={...}, .sk_lock={...}, .sk_receive_queue={...}, .sk_backlog={...}, .sk_forward_alloc=0, 
    sk_rxhash=2678085662, .sk_napi_id=1, .sk_ll_usec=0, .sk_drops={...}, .sk_rcvbuf=1061488, .sk_filter=0x0, 
    .sk_wq=0xffff8e3c05e69900, .rh_reserved_sk_async_wait_queue={...}, .sk_policy=[...], .sk_flags=768, 
    .sk_rx_dst=0xffff8e3c21fe1600, .sk_dst_cache=0xffff8e3c21fe1600, .rh_reserved_sk_dst_lock={...}, 
    .sk_wmem_alloc={...}, .sk_omem_alloc={...}, .sk_sndbuf=2626560, .sk_write_queue={...}, .sk_shutdown=3, .sk

    ```

### 第四步：结合源码，添加必要的变量输出

* 源码解读：
  ```c
    void ngx_close_connection(ngx_connection_t *c)
    {
        // 关键标志位 1：fd 有效性
        if (c->fd != (ngx_socket_t) -1) {

            // 关键标志位 2：linger 延迟关闭
            if (c->read->timer_set) {
                ngx_del_timer(c->read);
            }

            if (c->write->timer_set) {
                ngx_del_timer(c->write);
            }

            // 关键标志位 3：socket 关闭方式
            if (ngx_close_socket(c->fd) == -1) { // 实际关闭操作
                ngx_log_error(NGX_LOG_ALERT, c->log, ngx_socket_errno,
                            "close() socket %d failed", c->fd);
            }

            c->fd = (ngx_socket_t) -1; // 标记 fd 已关闭
        }

        // 关键标志位 4：连接池回收
        if (c->pool) {
            ngx_destroy_pool(c->pool); // 正常关闭会回收内存
        }

        // 关键标志位 5：destroyed 标记
        c->destroyed = 1; // 标记连接已销毁
    }
  ```

* 修改脚本
  ```tcp-close.stp
  # tcp-close.stp
  ...
  修改第3行：printf("Close conn %d (fd:%d) error:%d destroyed:%d\n", $c->number, $c->fd, $c->log->action, $c->destroyed)
  ...
  ```

* 输出：
  ```log
    Close conn 12102682 (fd:17) error:8140054 destroyed:1
  ```

* 结论：<span style="color: rgb(255, 76, 65);">destroyed=1，表示nginx为正常退出</span>


### 总结：
* 使用systemtap时，需要知道探测点的具体位置，需要对当前程序、程序源码有比较深的理解
* 编写stp脚本，需要stp的基础语法认知，可以结合GPT编写（我测试下来，GPT对其语法掌握不是很全面，写完还需要手动修改，可能原因是太过于小众了）
* 编写脚本可能需要多次修改，最终才能获得满意的效果
* 对输出结果的理解，可以结合程序源码，一边看源码内容，一边看变量、程序栈情况，效果会更好。
* 使用感受：
    * 源码理解：   <span style="color: rgb(255, 76, 65);">要求高</span>
    * stp脚本语法：<span style="color: rgb(255, 76, 65);">要求高</span>

### 常见的错误：
#### 1. no match
```
semantic error: while resolving probe point: identifier 'process' at test.stp:8:7
        source: probe process("/usr/local/openresty/nginx/sbin/nginx").mark("http_request_headers_filter") {
                      ^
semantic error: no match
```

错误原因：一般是process对应的探测点不存在，可能是源码版本不匹配等原因，或者是你的环境跟你抄的网上的别人的脚本环境不一致。即`http_request_headers_filter`这个函数在当前版本的nginx不存在。
解决方案：自己使用stap -L 查找下正确的探测点



### systemtap 教程
* [documentation](https://sourceware.org/systemtap/documentation.html)
* [tapsets](https://sourceware.org/systemtap/tapsets/)
* [nginx 源码](https://github.com/nginx/nginx)