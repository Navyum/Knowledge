---
title: docker
date: 2025-06-17 15:18:52
author: Navyum
tags: 
 - Docker
categories: 
 - 容器技术
article: true
index: true

headerDepth: 2
sticky: false
star: true
icon: simple-icons:docker
---

* client-server 架构
* `docker client`使用REST API，通过UDS或者network，与`dockerd`进行通信
![Img](https://raw.staticdn.net/Navyum/imgbed/main/IMG/a2959a6248c161ea2a84e671c8a5d38d.png)

## Docker Registries
* 用来存储Docker Images
* 默认使用Docker Hub Registries
* 常用的registries：
    * [Docker Hub](https://hub.docker.com/)
    * [ECR](https://aws.amazon.com/ecr/)
    * [GCR](https://cloud.google.com/artifact-registry)
    * [ACR](https://azure.microsoft.com/en-in/products/container-registry)
    * 自建：Harbor, JFrog Artifactory, GitLab Container registry 
* 相关命令：
    ```bash
    $ docker search IMAGE_NAME  // 从registies查找镜像
    $ docker pull DOCKER_USERNAME/IMAGE_NAME // 从registries拉镜像到本地
    $ docker tag YOUR_DOCKER_USERNAME/IMAGE_NAME YOUR_DOCKER_USERNAME/IMAGE_NAME:1.0 //将本地镜像重命名
    $ docker push YOUR_DOCKER_USERNAME/IMAGE_NAME:1.0 // 将镜像推送到registries
    ```

## Docker Objects

### Images
* Docker Images是用来创建docker container的一组只读的指令集
* Dockerfile 里面的每一条指令都会创建一个层Layer
* 特性：
    * 不可改变（immutable）：image创建后只能通过新建进行修改
    * 层（layers）：镜像由层构成，每一层代表文件系统的变更
* 相关命令：
    ```bash
    $ docker image ls                   // 罗列本地image
    $ docker image history IMAGE_NAME   // 查看image修改记录
    $ docker rmi   IMAGE_NAME             // 删除image
    $ docker tag    SOURCE_IMAGE_NAME[:TAG] TARGET_IMAGE_NAME[:TAG]    // 给指定image重命名并打上TAG
    $ docker inspect IMAGE_NAME         // 查看image详细信息
    $ docker ps -s                       // 查看镜像大小，size为实际占用大小，virtual size为虚拟内存占用，有一个算一个
    ```
#### Image layers
* Image构建时，对Layer做了缓存处理。由此实现多个Image之间对已经构建的好的Layer的复用。
* 如何利用好Layer Cache：编写dockerfile时，要尽可能考虑layer的层级先后关系，提高复用

### Containers
* Docker Containers是Docker Images的可运行的实例（类比类和实例）
* 容器是运行在主机上的一个进程
* 可以将container的状态打包到一个新的Image中
* 特性：
    * 自给自足（Self-contained）：不依赖于主机，自身拥有一切所需
    * 隔离性（Isolated）：容器隔离运行，相互之间几乎没有影响
    * 独立性（Independent）：每个容器可以独立管理，不影响其他容器
    * 可移植性（Portable）：容器可以在任何地方运行
* 相关命令：
    ```bash
    $ docker run     --name=app-container -it IMAGE_NAME [COMMAND] [ARG...]   //新建container，并以交互形式运行 COMMAND ARG。-i即--interactive -t即--tty，it一般搭配 sh 使用
    $ docker exec    CONTAINER_ID [COMMAND] [ARG...]                         //对运行中的container执行命令
    $ docker exec  -it testcentos  sh -c 'echo "xxx" >> /data/a'
    $ docker rm      CONTAINER_ID
    $ docker inspect CONTAINER_ID         // 查看container详细信息
    $ docker commit  -m "message" -c "CMD node app.js" <容器ID> <新镜像名称>  //将容器ID保存为新镜像，并设置默认CMD为node app.js。不推荐，推荐使用dockerfile
    $ docker run -it -m 100M --oom-kill-disable ubuntu:22.04 /bin/bash    // 关闭OOM killer时，必须要限制内存使用，否则会导致host内存耗尽
    ```
* 其他参数flag：
    * --entrypoint      覆盖Dockerfile ENTRYPOINT指令
    * --publish / -p    暴露指定ip和端口
    * --env  / -e       设置容器环境变量
    * --user / -u       设置容器内第一个进程的运行用户，默认为root
    * --workdir /-w     设置容器内，程序运行的工作目录
    * --memory-xx /-m   设置容器内存使用相关参数，用于性能调优
    * --cpu-xx /-c      设置容器CPU使用相关参数，用于性能调优
    * --gpus            设置容器可使用的GPU
    * --restart         设置容器自动重启策略

### Volumes/bind mounts/tmpfs
* 作用：将容器中的数据持久化，volumes不会随着container销毁而消失
* 图解：
![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/385b08ca5b077a3bf9bced726581755b.png)
* 差异对比：
|方式|管理方式中文名|目录位置|数据隔离|使用场景|
|:----|:----|:----|:----|:----|
|Bind Mount|host管理|自定义磁盘位置，依赖host文件系统|容器和主机共享|需要直接访问主机文件系统时，共享代码、共享主机配置|
|Volume|docker管理|/var/lib/docker/volumes/\<volume-name\>|容器和主机通过Docker存储驱动进行交互|需要数据持久化、多容器间共享数据时、云存储、远程存储，IO要求高，volumes存储在Linux VM中，而不是主机|
|tmpfs|docker管理|存储在主机内存中|隔离性好，多容器之间不共享|不想数据被持久化时，存储密钥等敏感信息|
* 相关命令：
    ``` bash
    $ docker volume create VOLUME_NAME //创建卷
    $ docker volume prune VOLUME_NAME  // 删除卷
    $ docker run -d -v VOLUME_NAME:/path/in/container IMAGE_NAME  // -v 方式挂载
    $ docker run -d --mount type=volume,source=VOLUME_NAME,target=/path/in/container IMAGE_NAME  // 挂载 volume
    $ docker run -d --mount type=bind,source=/path/on/host,target=/path/in/container IMAGE_NAME  // bind mount
    $ docker run -d --mount type=tmpfs,target=/path/in/container IMAGE_NAME  // tmpfs
    $ docker inspect CONTAINER_ID --format '{{ json .Mounts }}'
    $ docker inspect VOLUME_NAME
    // 其中 source 可以简写为 src
    // 其中 target 可以用 destination 或者 dst 代替
    // -v/--volume 和 --mount的一个区别，前者如果host对应文件夹不存在，会自动创建，后者会报错
    ```
#### Storage Driver
* 作用：存储本地镜像、Layer和对应cache
* 路径：/var/lib/docker/\<storage-driver\>，此处storage-driver通常为overlay2
* 常见的storage driver
    * overlay2、fuse-overlayfs、btrfs/zfs、vfs

### Networks
* 作用：用于容器之间、容器外部的通信（communicate）
* 网络驱动比较
|驱动|说明|使用场景|
|:----|:----|:----|
|bridge|桥接网络，相同主机的同网络容器之间进行通信，不同网络容器进行隔离|默认的网络驱动，生产环境不建议使用默认的bridge，可以用户自己创建bridge网络|
|host|直接使用host的网络，host和容器无网络隔离|使用host的namespace、容器不会被分配IP，高性能场景，仅在linux容器下支持|
|none|完全和其他容器、主机隔离|无网络通信的场景|
|overlay|连接多个docker守护进程|主要用于Swarm services、或者多个doc´ker host的独立容器通信；当然也可以通过管理host的网络实现service通信|
|ipvlan|由用户自主控制容器IP|提供对ipv4、ipv6的完全控制|
|macvlan|由用户自主控制容器MAC地址|给容器分配MAC地址|

|桥接模式|默认bridge|用户自定义bridge|
|:----|:----|:----|
|DNS设置|只能通过IP访问|IP 或者 Name|
|端口开放|容器必须指定开放端口，其他容器才能访问|所有容器的端口默认开放|
|隔离性|容器在不指定时默认使用bridge，存在风险|需要明确指定对应bridge名称|
|热插拔|使用默认bridge的容器需要停止才能加入新网络|可以直接加入或者断开对应自定义网络|
|灵活性|所有容器使用相同的网络配置，例如防火墙等配置修改不方便|可以自定义多个用户网络，配置独立|
|环境变量共享|使用--link flag共享|可以选择 volume、compose file、swarm services|

* 相关命令：
``` bash
$ docker network create -d bridge my-net                    // 创建my-net网络
$ docker network rm  my-net                                 // 删除my-net网络
$ docker network create -d overlay --attachable my-overlay   // --attachable 实现非swarm service的连接
$ docker run --network=my-net -itd --name=container3  busybox // 直接使用my-net网络运行容器
$ docker network connect my-net my-container                 // 将容器连接到my-net网络
$ docker network disconnect my-net my-container              // 将容器从my-net网络断开
$ docker inspect NETWORK_NAME                                // 查看NETWORK_NAME网络信息
```


### Plugins
* 用来扩展docker功能
* 常用的Plugins分类：
    * Network plugins   方便网络管理
    * Volume plugins    实现卷的云存储
    * Authorization plugins 权限管理
    * Logging plugins   日志管理
* 常用命令：
```bash
$ docker plugin install PLUGIN_NAME
$ docker plugin ls
$ docker plugin enable
$ docker plugin set
```



### 其他命令：
#### inspect 信息检查
```bash
$ docker inspect centos-8 --format '{{ json .MacAddress }}'
```

#### stats 容器运行时metrics获取
```bash
$ docker stats CONTAINER_NAME
```

### 格式化输出 --filter 和 --format
``` bash
$ docker COMMAND --filter "KEY=VALUE"  //过滤结果仅展示key
$ docker inspect --format '{{join .Args " , "}}'
```

## Build 镜像
* client-server架构图：
![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/83843a52e15b6b08952df8a8999ce5e3.png)
### 传统build VS buildx
* docker build 是 Docker 的标准构建命令
* ✅ docker buildx build 是使用`docker buildkit`进行构建，支持多平台构建、并行构建，是下一代构建工具
### buildx构建过程：
1. 创建builder：`$ docker buildx create --name=BUILDR --driver=DRIVER ... `
    * driver类型选择：docker、docker-container、kubernetes、remote
        ```bash
        # docker driver：默认的driver，不需要参数指定
        `$ docker buildx build -t <registry>/<image> . ` // 直接build
        # docker-container driver：注意末尾的 container，使用container进行构建
        `$ docker buildx create --name=BUILDR --driver=docker-container --driver-opt=[key=value,...] --use --bootstrap BUILDR `
        # kubernetes driver：使用k8s进行构建
        `$ docker buildx create --name=BUILDR --driver=kubernetes --driver-opt=[key=value,...] --use `
        # remote driver：使用远程driver进行构建
        `$ docker buildx create --name=BUILDR --driver=remote --use tcp://localhost:1234 `
        ```
2. 使用builder构建：
    ```bash
    # platform 指定平台架构，.从当前目录找dockerfile
    $ docker buildx build --builder=container --platform=linux/amd64,linux/arm64  -t <registry>/<image> .
    ```

### Dockerfile：
#### 语法相关 syntax
* 语法解析器指令，必须位于dockerfile第一行
``` 
# syntax=docker/dockerfile:1 
``` 
* 转义问题：windos下文件路径反斜杠问题
```
# escape=`
```

#### 命令：[参考](https://docs.docker.com/reference/dockerfile/)
* FROM
    * 初始化一个新的构建阶段（build stage），并为后续指令提供基础镜像
    ``` dockerfile
    FROM [--platform=<platform>] <image>[:<tag>] [AS <name>] 
    ```
* WORKDIR
    * 给RUN, CMD, ENTRYPOINT, COPY ,ADD 设置工作目录
    ``` dockerfile
    WORKDIR path
    ```
    * 注意事项：
        * WORKDIR可以重复多次，第一次必须要绝对路径
        * 如果后续的WORKDIR是相对路径，那么它则是相对于上次的WORKDIR的值
* ARG
    * 定义用户build构建过程中使用的变量，不会被持久化到镜像中。
    * `docker build` 时通过 `--build-arg <name>=<value>` 传入值或者覆盖默认值
    ``` dockerfile
    ARG <name>[=<default value>]
    ```
    * 注意事项：
        * 变量的作用域
        * docker中有大量预置的变量，全局变量
* ENV
    * 定义镜像内部后续使用时需要的环境变量，会被持久化到镜像中。
    * `docker run` 时，通过 `--env <key>=<value>` 传入值或者覆盖默认值
    ```dockerfile
    ENV <key>=<value> ... # 支持一次定义多个
    ```
    * 注意事项：
        * 密钥等敏感信息不要通过ENV传入，推荐使用 `RUN --mount=type=secret`
* ADD
    * 从src拷贝数据到镜像中的dst路径
    ```dockerfile
    ADD [OPTIONS] <src> ... <dst>          # 不支持带空格的路径
    ADD [OPTIONS] ["<src>", ... "<dst>"]   # 支持带空格的路径
    ```
    * 注意事项：
        * 支持一次拷贝多个src到dst，此时最后一个位置为dst，并且必须是目录（参考cp命令）
        * 如果dst不存在，会自动创建
        * dst如果是文件夹，末尾一定要加"/"
        * ADD命令会自动判断src的类型
            * file/directory：直接完整拷贝到dst
            * tar压缩包：解压后拷贝到dst
            * url：下载url内容后拷贝到dst
            * git仓库：仓库被克隆到dst
* COPY
    * 从src拷贝数据到镜像中的dst路径
    ```dockerfile
    COPY [OPTIONS] <src> ... <dst>          # 不支持带空格的路径
    COPY [OPTIONS] ["<src>", ... "<dst>"]   # 支持带空格的路径
    COPY [--from=<image|stage|context>] <src> ... <dest>  # 重要‼️ 从镜像、阶段、上下文拷贝数据
    ```
    * 注意事项：
        * COPY 命令主要用于：
            * build context 用法同ADD
            * build stage 构建阶段 `COPY --from=build /myapp /usr/bin/` //将build阶段生成的/myapp 拷贝到当前阶段
            * named context 从自定义上下文拷贝
            * image 从镜像拷贝数据
        * 使用COPY --from 时，路径必须是绝对路径

* **CMD**
    * 容器启动时，定义默认参数和选项；镜像构建时不会起任何作用
    ```dockerfile
    # shell form：
    CMD command param1 param2

    # exec form：
    CMD ["executable","param1","param2"]

    # exec form： 作为ENTRYPOINT的默认参数使用，此时必须搭配ENTRYPOINT使用
    CMD ["param1","param2"]
    ```
    * 注意事项：
        * CMD只能有一个；如果有多个，则只有最后一个生效
        * 推荐用法 exec form形式作为ENTRYPOINT 默认参数
        * shell 模式，默认使用shell，存在字符串修改问题，例如转义、空格等
        * exec 模式，可以自己定义程序，对字符串参数处理较好，仍需要处理好转义问题

* **ENTRYPOINT**
    * 容器启动时，定义启动命令；镜像构建过程中不会起任何作用。（多阶段构建中可以有多个ENTRYPOINT）
    ```dockerfile
    # shell form：
    ENTRYPOINT command param1 param2

    # exec form：
    ENTRYPOINT ["executable", "param1", "param2"]
    ```
    * 注意事项：
        * 通过docker run --entrypoint 可以覆盖镜像中的ENTRYPOINT
        * 如果使用shell模式的 ENTRYPOINT
            * 则CMD会全部失效，包括run对应的命令行参数；
            * 并且会先启动shell作为1号进程，然后在shell环境下执行对应命令
            * docker stop 不够优雅，docker内的程序并不能基于外部的退出信号优雅退出
    * `CMD 和 ENTRYPOINT的组合`：
    ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/832031b8fb17ede21a4e43cd2b00fdd0.png)

* **RUN**
    * 通过执行命令，解决镜像构建过程中的依赖
    ```dockerfile
    # Shell form:
    RUN [OPTIONS] <command> ...
    
    # Exec form:
    RUN [OPTIONS] [ "<command>", ... ]
    ```
    * 注意事项：
        * 每一个RUN都会生成镜像的一层Layer
        * RUN 的 OPTIONS有三个：
            * --mount       build过程中需要访问的挂载点
            * --network     build过程中需要使用的网络
            * --security    稳定版尚未提供
* EXPOSE
    * 定义由该IMAGE生成的CONTAINER，在运行时的监听端口和协议
    ```dockerfile
    EXPOSE <port> [<port>/<protocol>...]
    ```
    * 注意事项：
        * EXPOSE需要搭配 -p 使用，EXPOSE只定义了容器内部的可用端口，并没有做外部的端口映射并暴露出去。
* VOLUME
    * 将镜像中的某个目录变成卷
    ```dockerfile
    RUN mkdir /data
    VOLUME ["/data"]
    ```
* USER
    * 给RUN, CMD, ENTRYPOINT 设置执行者
    ```dockerfile
    USER <user>[:<group>]
    ```
* LABEL
    * 给镜像添加元数据metadata，例如维护者信息、版本号、镜像描述等
    ```dockerfile
    LABEL <key>=<value>  ...
    ```
* SHELL
    * 修改默认shell从/bin/sh 改为指定shell，windows下常用。例如改为powershell和cmd
    * 一般用于 RUN 指令的shell模式下
    ```dockerfile
    SHELL ["executable", "parameters"]
    ```
* HEALTHCHECK
    * 用于检查container运行是否健康，通过在容器内运行CMD 检查命令
    ```dockerfile
    HEALTHCHECK [OPTIONS] CMD command
    ```
#### 多阶段构建
* 作用：
    * 通过 docker build --target=<stage_name>，用同一个dockerfile，构建某阶段的镜像
    * 通过 FROM scratch，利用阶段生成的二进制文件，降低最终镜像大小
    * buildx通过buildkit构建时，只构建依赖的阶段；传统build会构建所有阶段；
* 使用：
    * 给stage定义别名： FROM \<base_image\>:\<tag\> AS \<name\>
    * 通过COPY使用外部镜像的文件 COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
    * 通过COPY使用前面阶段的文件 COPY --from=pre_stage result /src
    * 构建指定的阶段：docker build -t IMAGE_NAME --target=stage_name .  // 从dockerfile构建stage_name对应阶段做为IMAGE_NAME镜像
* 例子：
    ```dockerfile
    # syntax=docker/dockerfile:1
    FROM golang:1.21-alpine AS base
    WORKDIR /src
    COPY go.mod go.sum /src/
    RUN go mod download
    COPY . .

    # build client
    FROM base AS build-client
    RUN go build -o /bin/client ./cmd/client

    # build server
    FROM base AS build-server
    RUN go build -o /bin/server ./cmd/server

    # copy client binary to client image
    FROM scratch AS client
    COPY --from=build-client /bin/client /bin/
    ENTRYPOINT [ "/bin/client" ]

    # copy server binary to server image
    FROM scratch AS server
    COPY --from=build-server /bin/server /bin/
    ENTRYPOINT [ "/bin/server" ]
    ```
