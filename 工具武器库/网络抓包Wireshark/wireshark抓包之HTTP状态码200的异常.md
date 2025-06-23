---
title: wireshark抓包之HTTP状态码200的异常
date: 2025-04-08 17:55:36
author: Navyum
tags: 
 - wireshark
 - 抓包
 - chunk格式
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


### nginx server 以 content-type chunk格式返回的程序异常
---

### 背景：
业务需要通过脚本跑一批数据，数据有很多条，每条数据需要进行一次数据库查询、一次OSS下载，最终才能确定该记录的输出
```text
输出举例：
记录A： DB记录1 + OSS记录1
记录B： DB记录2 + OSS记录2
...
记录N： DB记录N + OSS记录N
```

### 业务方出现的问题：
在跑脚本时，使用curl命令行进行接口调用，对nginx的输出结果进行保存，但是出现报错：`curl: (18) transfer closed with outstanding read data remaining`。保存的结果文件里面记录正常。

<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/22236647388dc056bff4a58ab963567b.png" width="80%"></p>


### nginx配置
```nginx.conf
location = /test {
    content_by_lua_block {
    for i=1, 1000 do
        -- 1. get result 
        ...
        -- 2. print result

        ngx.say(result)

        end
    end
    ngx.exit()
    }
}
```

### 最终定位到原因：
直接原因：服务端主动断开了TCP连接，导致未完整发送chunk的终止块`0\r\n\r\n`，导致客户端接收时解析协议出错。
根本原因：服务端程序出现异常中断，但是因为按照chunk格式返回时，HTTP 200的头在首个tcp包中已经发送无法修改。


### 分析过程：
#### 1. 通过tcpdump进行抓包，在wireshark中打开
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/d0a0640c241eb51617709e57acd76b73.png" width="80%"></p>

#### 2. 解读
* 30号包显示，最终由服务端（10.8.4.199）主动发送FIN断开TCP连接
* 从30、31号包可以看出，整个挥手过程中，Seq、Ack的值都是正常的，说明TCP挥手也是正常进行的
* 28号包存在问题点在于：Protocol根据Info来看，应该是`HTTP`才对，但是实际展示的是`TCP`

#### 3. 搜索网上资料
* 在网上搜索相关资料，并结合实际代码，猜测是ngx.say导致的该问题。
* 初步判断：ngx.say 必须结合ngx.eof 一起使用，但是实际设置后，没有作用，问题依然存在。

#### 4. 重新从协议的角度重新分析
* 根据以往经验，之前有一次手动设置content-length，但是因为计算错误导致的请求异常。
* 我们重新结合 Content-Type为 `application/octet-stream`以及Transfer-Encoding为：<span style="color: rgb(255, 76, 65);">chunked的基础知识</span>：
  * 当前HTTP 响应体没有Content-Length，client端无法根据字节判断tcp包什么时候结束
  * 此时基于TCP粘包理论，此时只能通过应用层的一些特殊的结束符号来判断包的结束位置
    * 查询[MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Transfer-Encoding#chunked)的相关知识：
        > [!TIP] chunked：
        > Data is sent in a series of chunks. Content can be sent in streams of unknown size to be transferred as a sequence of length-delimited buffers, so the sender can keep a connection open, and let the recipient know when it has received the entire message. 
        > The Content-Length header must be omitted, and at the beginning of each chunk, a string of hex digits indicate the size of the chunk-data in octets, followed by \r\n and then the chunk itself, followed by another \r\n. The terminating chunk is a zero-length chunk.
    * 讲人话就是：
        chunk格式固定为：
        ```
        [chunk size] 8字节 \r\n       -- 表示chunk data的实际大小
        [chunk data] \r\n            -- 实际chunk data
        ```
        `终止块`格式固定为：
        ```
        0\r\n\r\n (对应16进制 30 0d 0a 0d 0a)
        ```
#### 5. 排查wireshark中stream 是否有正确的块结束符
* 在wireshark中，选择对应的记录。右键 -> 【Follow】-> 【TCP Stream】
  ```
    ...
    00002ED4  45 36 25 41 43 25 42 45  25 45 35 25 38 37 25 41   E6%AC%BE %E5%87%A
    00002EE4  44 25 45 38 25 41 46 25  38 31 26 75 73 65 72 5f   D%E8%AF% 81&user_
    00002EF4  69 64 3d 34 32 39 38 31  31 31 30 30 0a 0d 0a      id=42981 1100...
  ```
* 末尾为0a 0d 0a，即\n\r\n。第一个\n是查询逻辑中的换行符，末尾的\r\n 表示，当前chunk的结束符。
* 最终该TCP Stream 并没有发现chunk块结束符

#### 6. 基于以上的信息，得知请求要么超时、要么是发生了异常
* 超时的情况、或者发生异常时，按照常应该是由客户端或者服务端发送`RST`
* 但是这个案例里面，缺少了chunk结束块。服务端依然正常发送FIN包结束当前的TCP连接

#### 7. 带着上面疑问，进一步排查看是否nginx哪里有问题
* 查看nginx的error.log，发现存在错误：
    ```
    [error] 22145#22145: *4985236 lua entry thread aborted: runtime error: .../openresty/nginx/conf/internal/xxxx-script.lua:3485: attempt to concatenate 'pages' (a nil value)
    stack traceback:
    coroutine 0:
    .../openresty/nginx/conf/internal/xxxx-script.lua: in main chunk, client: 127.0.0.1, server: , request: "POST /xxx/xxx?x=xxxxxxxxHTTP/1.1", host: "localhost"
    ```
* 可以看到因为是变量异常导致的`Abort`。这里存在一个疑问，程序abort，连接应该使用RST关闭才对，具体原因后面会使用bt trace 工具进行分析。
* 先排查代码，查看对应行的记录，判断对应变量在某个记录查询时，会是空值nil，导致nginx流式输出中断。

#### 8. 结合已知的情况，尝试复现问题
* 使用有问题的nginx配置：
  ```nginx.conf
   location = /test {
        content_by_lua_block {
            for i=1, 1000 do
                ngx.say(string.rep(tostring(i), i))   -- 将i重复i次，并正常打印
                
                -- 3. set error case
                if i == 999 then
                ngx.say(no_data)                    -- 故意打印不存在的变量no_data
                end

            end
            
            ngx.exit()
        }
    }
  ```
* 使用curl命令复现该问题：`curl localhost/test`
    * 问题得到复现 `curl: (18) transfer closed with outstanding read data remaining`


### 修复方案：
* 针对出现问的的pages变量，添加更健壮的代码逻辑进行判断是否为nil


### 回顾：
* 该问题比较隐蔽，因为curl的响应头中HTTP状态码为 200，但是出现错误，这个现象颠覆了正常的认知,所以一开始没有怀疑程序出现问题。如果能更早的查看nginx的error.log，也许可以更快的定位问题。
* 搜索网上的资料时，对类似的问题都是说是需要设置 ngx.eof()、ngx.fulsh()，直接误导了排查的方向
* 在分析抓包的结果时，很长时间都无法直接判断是哪里除了问题，因为从TCP的层面排查，所有的包都是没有任何问题的。唯一露出的马脚就是应该展示为HTTP的协议实际展示为了TCP。
* 该问题排查时，每次curl的结果都是一样的（因为pages为nil的就是有问题的那条记录），每次都能稳定复现。但是在测试环境，因为数据的差异，却无法直接复现问题，增加了排查的难度，尤其是测试环境构造数据进行测试时。

### 延伸：
* 问题1：nginx环境中，当请求发生异常，什么情况下会使用`RST`中断，什么时候使用`FIN`优雅中断？
* 问题2：为什么当前的案例，nginx使用的是FIN优雅关闭连接？
  * FIN：
    * FIN 正常关闭连接的场景：
        * 正常处理完请求
        * 保活时间（TCP Keep-Alive）内没有新请求
    * 源码：
        ```src/http/ngx_http_request.c
        函数 ngx_http_close_connection
        // ... existing code ...
        if (c->read->timer_set) {
            ngx_del_timer(c->read);
        }
        ngx_close_connection(c);
        // ... existing code ...
        ```
  * RST：
    * RST 异常关闭的场景：
        * 客户端发送非法请求（client prematurely closed connection）
        * upstream异常（upstream connection error）
        * 握手失败（SSL handshake failed）
        * 内存崩溃、主动断开、超时等异常（connection reset by peer）
    * 源码：
        ```src/event/ngx_event.c
        函数 ngx_connection_error：
        // ... existing code ...
        if (err == NGX_ECONNRESET || err == NGX_ENOTCONN) {
            c->error = 1;
            ngx_close_connection(c);
            return;
        }
        // ... existing code ...
        ```
  * 本案例的函数调用栈获取：
    ```
    ```


* 感受：在分析抓包时，使用大模型进行pcap的分析的探索遇到的问题：
  * 即使是过滤的数据，pcap文件还是比较大，大模型的上下文有限
  * 当前的case中，大模型无法深入的分析，只停留在TCP层面，因为TCP层面都是正确的，分析不出问题
  * 业务代码、抓包请求、环境介绍、报错信息，这些都需要使用者提供给大模型，后续wireshark是否能使用MCP的方式，由大模型自行按需读取需要的数据？