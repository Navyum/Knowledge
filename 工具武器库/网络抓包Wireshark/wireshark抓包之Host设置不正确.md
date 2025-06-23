---
title: wireshark抓包之Host设置不正确
author: Navyum
date: 2025-06-18 19:40:32

article: true
index: true

headerDepth: 2
sticky: true
star: true

tags: 
 - wireshark
 - 抓包
 - host错误
categories: 
 - wireshark
 - 工具

---

## wireshark抓包

### Sling 请求k8s负载均衡器，导致的404错误
---

### 背景：
在一次业务开发中，业务中需要请求k8s服务地址。但是业务逻辑中的请求总是提示HTTP 404错误，使用curl 命令又是正确的。

### 出现问题：
在golang项目中，使用[Sling库](https://github.com/dghubble/sling)作为clinet，进行网络请求以获取服务响应结果

### 出错的关键golang代码如下
```golang

    response:=new(Response)

	// 构建请求
	request := srv.sling.New().
		POST(Path).
		QueryStruct(params).
		Set("Host", custom-host)    // 线上环境为k8s，需要强制设置host

    // 发送请求
	resp, err := request.Body(bytes.NewReader(pdfContent)).ReceiveSuccess(response)

    if err != nil {
      // handle error
    }

```

### 最终定位到原因：
直接原因：通过上述 Sling 的 Set 方法设置自定义的 Host 到 header 中，没有实际生效

根本原因：
- Sling 底层使用的是基础库 net/http 中的 http.Request 进行 HTTP 请求。在 Sling 的[Request](https://github.com/dghubble/sling/blob/main/sling.go)方法中，仅仅通过addHeaders设置了http.Request的Header对象：
```golang
func addHeaders(req *http.Request, header http.Header) {
	for key, values := range header {
		for _, value := range values {
			req.Header.Add(key, value)
		}
	}
}
```
- 而在 Go 的 net/http 标准库中，HTTP 请求的 Host 头部（Host header）是由 http.Request.Host 字段决定的，而不是 http.Request.Header["Host"]。
如果只是设置了req.Header.Set("Host", ...)，Go 的 HTTP 客户端在发送请求时会忽略 Header 里的 "Host" 字段，而是只看 req.Host 字段。
只有当 req.Host 为空时，Go 才会自动用 req.URL.Host 作为 Host 头。<span style="color: rgb(255, 76, 0);">巨坑啊巨坑！！！</span>

> 官方文档说明：
> For client requests, Host optionally overrides the Host header to send. If empty, the Request.Write method uses the value of URL.Host.
> [参考地址](https://pkg.go.dev/net/http#Request)


### 分析过程：
1. 分析出现 404 的可能原因：
    1. HTTP method 限制必须要是 POST 方式；如果设置为 GET，可能直接返回404
    2. HTTP 的 body没有成功读取到
    3. HTTP 的文件传输格式可能无法使用raw binary stream方式，而是要使用multipart/form-data格式
    4. 因为上游服务是k8s Ingress，服务使用了虚拟主机（Virtual Host）路由机制，在同一个 Ingress Controller 下，通过不同的 Host 访问同的后端服务；如果 Host 设置不正确，往往会404
2. 因为改代码的代价最小，所以先通过改代码逻辑的方式，逐个确认是否可以解决问题；很不幸没有解决（包括使用Sling.Set 设置 Host）。
3. 直接通过tcpdump进行抓包，在wireshark中打开
   * 请求失败 404
     <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/1d72e52a50f04678e1ec0d3085361f99.png" width="80%"></p>
   * 请求头信息
     <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/57b6203b94dcbf4549510f08a036ce54.png" width="80%"></p>
4. 解析抓包结果：
   直接就可以看出实际请求的 Host 跟我们在代码中设置的不符合，即代码的设置没有生效！！

5. 解决方案：
   排查为什么Sling在设置Host时，与实际请求存在偏差，最终定位到原因，Sling的实现没有支持单独设置 http.Request.Host，当使用 sling.Set 设置Host时，仅仅修改了http.Request.Header["Host"]的值；这与实际的Host存在明显偏差。
   1. 修改设置Host的逻辑，更改http.Request.Host的值
      ```golang
        req, err := sling.New().Post("https://example.com/api").Request()
        if err != nil {
            // handle error
        }
        req.Host = "custom-host"
        resp, err := http.DefaultClient.Do(req)
      ```
    2. 提交了 PR 给 Sling 库，支持Set方法设置 Host [merge request](https://github.com/dghubble/sling/pull/120)
       主要改动：
       ```golang
            func addHeaders(req *http.Request, header http.Header) {
                for key, values := range header {
                    if key == "Host" && len(values) > 0 {
                        // For Host header, only set the Host field directly
                        req.Host = values[0]
                    } else {
                        // For all other headers, add them to the request header
                        for _, value := range values {
                            req.Header.Add(key, value)
                        }
                    }
                }
            }
       ```

### 延伸：
为什么 k8s ingress 需要设置不同的 Host？

- 虚拟主机（Virtual Host）路由机制
Kubernetes Ingress 允许你在同一个 Ingress Controller（比如 nginx-ingress、traefik、alb-ingress 等）下，配置多个域名（Host）指向不同的后端服务。这种机制叫做“基于 Host 的路由”或“虚拟主机路由”。

- 示例：
  ```yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
    name: example-ingress
    spec:
    rules:
    - host: app1.example.com
        http:
        paths:
        - path: /
            backend:
            service:
                name: app1-service
                port:
                number: 80
    - host: app2.example.com
        http:
        paths:
        - path: /
            backend:
            service:
                name: app2-service
                port:
                number: 80
  ```

- 如果你访问 Ingress Controller 的外部地址（比如 ELB、NLB、LoadBalancer IP），但 Host 头不是你配置的域名，Ingress Controller 就无法正确路由到目标服务。

其他请求地址和Host不一致的场景：
- API Gateway ： 例如Kong、APISIX、AWS API Gateway 等 API 网关
- 多租户 SaaS 平台：使用Host区分租户
- 云负载均衡（Cloud Load Balancer）：AWS ELB/ALB、GCP Load Balancer、Azure Application Gateway 等，支持基于 Host 的路由
- 反向代理（Reverse Proxy）：Nginx/Apache/HAProxy 等反向代理服务器常常根据 Host 头来做虚拟主机路由

总结：
只要有"统一入口+多后端"或"虚拟主机"需求的地方，Host 头和实际请求地址（地址只是个统一入口）就可能不一样。这也是为什么很多云原生、微服务、SaaS、测试、代理等场景都需要手动设置 Host 头。