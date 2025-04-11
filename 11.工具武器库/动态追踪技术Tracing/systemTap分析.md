## systemTap分析


### 分析的第一步，需要知道如何添加探测点
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
    * 添加探测点之前，我们需要一些基础知识。nginx处理URI的标准函数为：`ngx_http_process_request_uri`
    * 通过如下命令，查看当前版本是否可以添加相应探测点
      `sudo stap -L 'process("/usr/local/openresty/nginx/sbin/nginx").function("*")'|grep ngx_http_process_request_uri`
      `output: process("/usr/local/openresty/nginx/sbin/nginx").function("ngx_http_process_request_uri@src/http/ngx_http_request.c:1204") $r:ngx_http_request_t*`
      这样我们确认当前的nginx版本存在函数，且得到该函数的第一个参数为结构体指针`ngx_http_request_t`









### 常见的错误：
#### 1. no match
```
semantic error: while resolving probe point: identifier 'process' at test.stp:8:7
        source: probe process("/usr/local/openresty/nginx/sbin/nginx").mark("http_request_headers_filter") {
                      ^
semantic error: no match
```

错误原因：一般是process对应的探测点不存在，可能是源码版本不匹配等原因，或者是你的环境跟你抄的网上的别人的脚本环境不一致。
解决方案：自己使用stap -L 查找下正确的探测点




### 教程
https://sourceware.org/systemtap/documentation.html
https://sourceware.org/systemtap/tapsets/