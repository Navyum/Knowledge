---
title: minikube
date: 2025-06-17 15:19:11
author: Navyum
tags: 
 - minikube
categories: 
 - 踩坑笔记
 - 容器技术
article: true
index: true

headerDepth: 2
sticky: false
star: true
---

# minikube安装踩坑笔记

* **步骤一**：minikube 执行文件下载（linux x86-64为例子）：
    * 官方地址：(https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)´
    ```
        curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
        sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
    ```
* **步骤二** minikube 运行：
    * 官方命令： `minikube start`
    * 我们需要做如下改动：
        ```
        minikube start --vm-driver=docker --base-image="anjone/kicbase" --force --kubernetes-version=1.23.0
        ```
    * **问题一**：因为政策等原因，dokcer-hub无法拉取到base镜像
        * 错误信息（阻塞在镜像下载）：
            ```
            Pending：   Pulling base image v0.0.44 ...
                        > index.docker.io/kicbase/sta...:  0 B
                        E0811 15:29:59.503923   16810 cache.go:189] Error downloading kic artifacts:  failed to download kic base image or any fallback image

            ```
        * 解决方案1：
            * 使用命令行参数修改镜像源为阿里云
            ```
             minikube start --image-mirror-country='cn' --image-repository='registry.cn-hangzhou.aliyuncs.com/google_containers
            ``` 
            * 测试结果：❌未通过，猜测大部分云厂商的源站失效
        * 解决方案2：
            * 修改镜像源，并将 base-image `anjone/kicbase` 拉到本地
            ```
                $ sudo vi /etc/docker/daemon.json
                $ 修改registry-mirrors：
                {
                    "registry-mirrors": [
                        "https://hub.uuuadc.top",
                        "https://dockerpull.com",
                        "https://docker.1panel.live"
                    ]
                }
                $ sudo systemctl restart docker
                $ docker pull anjone/kicbase
            ```
            * 测试结果：✅ 通过
            * 源站来源：https://github.com/Navyum/CF-Workers-docker.io
                * 自己搭建
                * 使用别人搭建好的
    * **问题二**：默认会使用最新版kubernetes（测试时为v1.30.0），不支持docker
        * 错误信息（提示需要使用cri-docker）：
            ```
            ❌  Exiting due to RT_DOCKER_MISSING_CRI_DOCKER_NONE: sudo systemctl enable cri-docker.socket: Process exited with status 1
            ```
        * 解决方案1：
            * 使用ci-dockerd[github地址](https://github.com/Mirantis/cri-dockerd/releases)
            * 测试结果：未测试
        * 解决方案2: 
            * 使用支持docker的低版本kubernetes，例如1.23.0
            ```
             --kubernetes-version=1.23.0
            ```
            * 测试结果：✅ 通过
        * --vm-driver 参数说明：
            * 指定为docker，即通过docker运行minikube环境。我是在EC2环境中使用
        * --force 参数说明：
            * 使用root运行，不推荐
    * 运行成功截图：
        * 
* **步骤三** 检查minikube 运行状态：
    ```
    $ kubectl get nodes
        NAME       STATUS   ROLES                  AGE   VERSION
        minikube   Ready    control-plane,master   16h   v1.23.0
    $ minikube status
        minikube
        type: Control Plane
        host: Running
        kubelet: Running
        apiserver: Running
        kubeconfig: Configured
    ```
* **步骤四** 安装kubectl、kubeadm、kubelet：
    * 解决方案1：
        * 使用官方地址下载可执行文件：
            * 本例子使用的kubenetes版本为1.23.0，需要下载对应版本的kubectl
            * KUBERNETES_VERSION 替换为你需要的版本，本例子为1.23.0
            ```
            $ curl -LO https://dl.k8s.io/release/KUBERNETES_VERSION/bin/linux/amd64/kubectl
            ```
        * 测试结果：❌ 未通过，速度太慢
    * 解决方案2：
        * 使用yum源下载指定版本（centos）
            * 添加k8s仓库源
            ```
            cat << EOF > /etc/yum.repos.d/kubernetes.repo 
                [kubernetes]
                name=Kubernetes
                baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
                enabled=1
                gpgcheck=1
                repo_gpgcheck=1
                gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
            EOF
            ```
            * 下载1.23.0 版本kubectl
            
            ```
            $ yum install -y kubectl-1.23.0
            ```
        * 测试结果：✅通过
* **步骤四** 创建Deployment：
    * 官方推荐的yaml，拉取image太慢，使用阿里云的测试即可
    ```
    $ kubectl create deployment hello-minikube --image=registry.aliyuncs.com/google_containers/echoserver:1.10
    ```
* **步骤五** expose到外网：
    * 如果使用的是阿里云、腾讯云主机，需要在控制台开启对应端口号，否则可能无法访问，本例子需要手动开启Port 8080
    * expose 到8080端口
    ```
    $ kubectl expose deployment hello-minikube --type=NodePort --port=8080
    ```
    * 查看服务：
    ```
    $ kubectl get pod -o wide
        NAME                              READY   STATUS    RESTARTS   AGE     IP           NODE       NOMINATED NODE   READINESS GATES
        hello-minikube-6899fcbcf5-qdb2p   1/1     Running   0          2m28s   172.17.0.3   minikube   <none>           <none>
    
    $ kubectl get svc -o wide
        NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE     SELECTOR
        hello-minikube   NodePort    10.109.145.31   <none>        8080:32484/TCP   100s    app=hello-minikube
        kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP          2m38s   <none>
    ```


