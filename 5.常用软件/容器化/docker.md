# docker
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
* 可以将container的状态打包到一个新的Image中
* 特性：
    * 自给自足（Self-contained）：不依赖于主机，自身拥有一切所需
    * 隔离性（Isolated）：容器隔离运行，相互之间几乎没有影响
    * 独立性（Independent）：每个容器可以独立管理，不影响其他容器
    * 可移植性（Portable）：容器可以在任何地方运行
* 相关命令：
    ```bash
    $ docker run     --name=app-container -it IMAGE_NAME [COMMAND] [ARG...]   //新建container
    $ docker exec    CONTAINER_ID [COMMAND] [ARG...]                         //对运行中的container执行命令
    $ docker rm      CONTAINER_ID
    $ docker inspect CONTAINER_ID         // 查看container详细信息
    $ docker commit  -m "message" -c "CMD node app.js" <容器ID> <新镜像名称>  //将容器ID保存为新镜像，并设置默认CMD为node app.js。不推荐，推荐使用dockerfile
    ```

### Volumes/bind mounts/tmpfs
* 作用：将容器中的数据持久化，volumes不会随着container销毁而消失
* 图解：
![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/385b08ca5b077a3bf9bced726581755b.png)
* 差异对比：
|方式|管理方式中文名|目录位置|数据隔离|使用场景|
|:----|:----|:----|:----|:----|
|Bind Mount|host管理|自定义磁盘位置，依赖host文件系统|容器和主机共享|需要直接访问主机文件系统时，共享代码、共享主机配置|
|Volume|docker管理|/var/lib/docker/volumes/<volume-name>|容器和主机通过Docker存储驱动进行交互|需要数据持久化、多容器间共享数据时、云存储、远程存储，IO要求高，volumes存储在Linux VM中，而不是主机|
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
    // 其中 source 可以简写为 src
    // 其中 target 可以用 destination 或者 dst 代替
    // -v/--volume 和 --mount的一个区别，前者如果host对应文件夹不存在，会自动创建，后者会报错
    ```
#### Storage Driver
* 作用：存储本地镜像、Layer和对应cache
* 路径：/var/lib/docker/<storage-driver>，此处storage-driver通常为overlay2
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
$ docker inspect NETWORK_ID                                  // 查看NETWORK_ID网络信息
```


### Plugins

### 其他命令：
#### inspect
```
$ docker inspect centos-8 --format '{{ json .MacAddress }}'
```