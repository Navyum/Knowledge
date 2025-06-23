---
title: HEIF编解码器安装
date: 2025-06-17 11:39:40
author: Navyum
tags: 
 - HEIF
 - 环境安装
categories: 
 - HEIF
 - 图片格式
article: true
index: true

headerDepth: 2
sticky: true
star: true
---


## HEIF编、解码器安装手册  by Navyum

### HEIF 编码、解码原理
![Img](https://raw.staticdn.net/Navyum/imgbed/main/IMG/21139a95b55bedab5c5a1eaf9a9c4f0b.png)

### 相关依赖库：
主要的第三方库：libx265、libde265、libaom、libvvenc、liblibheif、libvips
其他参考：libavif

### 相关编码标准：
H.264/MPEG-4、H.265/HEVC、AVIF（AV1/AOM、dav1d）、H.266/VVC

### 依赖安装
安装依赖时务必要注意安装顺序，前者是必要依赖，如果没有正确安装，后面的通用库可以正常编译通过，但是无法使用heif功能

### 关于编译工具：
这些库会使用到的编译工具包括：gcc-6、g++、make、 cmake-3.x、meson、ninja

#### Centos7 下安装vips且支持heif转换：
1. 安装其他图片格式库【必须】
    ``` bash
    yum install -y \
      libpng-devel \
      glib2-devel \
      libjpeg-devel \
      expat-devel \
      zlib-devel \
      giflib-devel \
      libtiff-devel \
      libexif-devel \
      libtool
    ```
2. 安装编译工具 【必须】
    ```bash
    yum install -y automake \
    gcc \
    make \
    gcc-c++ 
    ```
3. 源码安装webp【可选】
    * [google官方地址](https://chromium.googlesource.com/webm/libwebp)，可自行选择版本
    * 以当前最新版本tag-1.4.0为例（2024-10-16）
        ```bash
        git clone https://chromium.googlesource.com/webm/libwebp \
        && cd libwebp \
        && git checkout -b remotes/origin/1.4.0 \
        && ./autogen.sh \
        && ./configure --enable-libwebpmux --enable-libwebpdemux --enable-libwebpdecoder \
        && make \
        && make install \
        && cd ..
        ```
4. 源码安装libde265解码codec【必须】
    * [libde265地址](https://github.com/strukturag/libde265/releases)，自行选择版本
    * 以当前最新版本v1.0.15为例（2024-10-16）
        ```bash
        wget https://github.com/strukturag/libde265/releases/download/v1.0.15/libde265-1.0.15.tar.gz \
        && tar xzf libde265-1.0.15.tar.gz \
        && cd libde265-1.0.15 \
        && ./configure \
        && make \
        && make install \
        && cd ..
        ```
5. 源码安装libx265编码codec【必须】
    * [libx265官方地址](https://github.com/videolan/x265)
    * 以当前最新版本v3.4为例（2024-10-16）
        ```bash
        wget https://github.com/videolan/x265/archive/refs/tags/3.4.tar.gz \
        && tar xzf 3.4.tar.gz \
        && cd x265-3.4 \
        && cd x265/build/linux \
        && ./make-Makefiles.bash      # 键入 g，生成对应环境的Makefile

        make && make install \
        && cd ..
        ```
6. 源码安装libheif【必须】
    * [libheif官方地址](https://github.com/strukturag/libheif)
    * [nikia libheif解析](https://github.com/nokiatech/heif)
    * 以当前最新版本v1.18.2为例（2024-10-16）
    * 前置依赖 cmake 3.3解决【最新版libheif必须】
        * centos7 需要通过源码安装，yum无法安装3.x以上cmake（此过程30min起步）
            ```bash
            yum install openssl openssl-devel \
            && wget https://cmake.org/files/v3.26/cmake-3.26.4.tar.gz \
            && tar zxf cmake-3.26.4.tar.gz \
            && cd cmake-3.26.4 \
            && ./configure \
            && make && make install
            ```
    * 编译libheif：
        ```bash
        wget https://github.com/strukturag/libheif/releases/download/v1.18.2/libheif-1.18.2.tar.gz \
        && tar xzf libheif-1.18.2.tar.gz \
        && cd libheif-1.18.2 \
        && mkdir build && cd build && cmake --preset=release .. \
        && make && make install \
        cd ..
        ```
    * 检查对应依赖是否是否安装好：
        * ![Img](https://raw.staticdn.net/Navyum/imgbed/main/IMG/520dcda8bfa09a4d32d8b96103cea9d7.png){width="40%"}
        ```bash
        heif-enc --list-encoders
        outputs：
            HEIC encoders:
            - x265 = x265 HEVC encoder (0.0) [default]
            AVIF encoders:
            VVIC encoders:
            JPEG encoders:
            - jpeg = libjpeg-turbo 1.2.90 (libjpeg 6.2) [default]
            JPEG 2000 encoders:
            HT-J2K encoders:
            Uncompressed encoders:
            - uncompressed = uncompressed [default]
        ```
    * 使用libheif库中的工具进行转换【此时已经可以使用heif工具进行格式转换】：
        * heif信息查看： ./heif-info  ../../tests/data/x.heif
        * heif编码：    ./heif-enc   test.jpg  -o  test.heif
        * heif解码：    ./heif-dec   ../../tests/data/x.heif -o c.jpg

    * **进阶使用其他编解码器**：
        * libheif支持的其他编码、解码器：
        *    | Format       |  Decoders           |  Encoders                    |
            |:-------------|:-------------------:|:----------------------------:|
            | HEIC         | libde265, ffmpeg    | x265, kvazaar                |
            | AVIF         | AOM, dav1d          | AOM, rav1e, svt-av1          |
            | VVC          | vvdec               | vvenc, uvg266                |
            | AVC          | openh264            | -                            |
            | JPEG         | libjpeg(-turbo)     | libjpeg(-turbo)              |
            | JPEG2000     | OpenJPEG            | OpenJPEG                     |
            | uncompressed | built-in            | built-in                     |

        * 使用AVIF（AV1，一般使用aom的实现）：
            * ![Img](https://raw.staticdn.net/Navyum/imgbed/main/IMG/1b2e740f7714ff546c3a96a8c3c10eb3.png){width="60%"}
            * 安装对libaom：
                ```bash
                git clone -b v3.9.1 --depth 1 https://aomedia.googlesource.com/aom \
                && cd aom \
                && cmake -S . -B build.libavif -G Ninja \
                -DCMAKE_INSTALL_PREFIX="/usr/local"  \ # 安装路径，需要按需修改
                -DBUILD_SHARED_LIBS=1       \  # 设置同时编译动态链接库，否则生成静态库
                -DCMAKE_BUILD_TYPE=Release  \  # 编译类型
                -DAOM_TARGET_CPU=generic    \  #-DAOM_TARGET_CPU=generic 实际编译时，根据报错自己添加的参数
                -DENABLE_DOCS=0 \
                -DENABLE_EXAMPLES=0 \
                -DENABLE_TESTDATA=0 \
                -DENABLE_TESTS=0 \
                -DENABLE_TOOLS=0 
                
                ninja -C build.libavif && ninja -C build.libavif install \
                cd ..
                ```
             * 进行编、解码测试：
                * heif-enc --avif test.jpg -o test.heif
                * heif-dec --avif test.heif -o test.jpg

        * 使用VCC（H.266/VCC 字节在用）：
            * 依赖说明：
                * gcc-5.0、cmake-3.13以上版本
                * 安装高版本 gcc：
                    * 方式一：官网源码编译（所需时间60min起步）
                    * 方式二：使用红帽编译好的版本，centos-release-scl
                        1. 下载scl Repo
                            ```
                            yum install centos-release-scl centos-release-scl-rh -y
                            ```
                        2. 修改SCL源地址为阿里云（CentOS7的SCL源在2024年6月30日停止维护）
                                ```bash
                                cat >/etc/yum.repos.d/CentOS-SCLo-rh.repo <<EOF
                                [centos-sclo-rh]
                                name=CentOS-7 - SCLo rh
                                baseurl=https://mirrors.aliyun.com/centos/7/sclo/x86_64/rh/
                                gpgcheck=1
                                enabled=1
                                gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-SCLo
                                EOF
                                ```
                        3. 安装gcc-9和dev包：
                            ```bash
                            yum install devtoolset-9-gcc devtoolset-9-gcc-c++ devtoolset-9-binutils -y
                            ```
                        4. 启动并验证版本：
                            ```
                            scl enable devtoolset-9 bash && gcc -v
                            ```

            * 编码：[官网](https://github.com/fraunhoferhhi/vvenc)
                ```bash
                wget https://github.com/fraunhoferhhi/vvenc/archive/refs/tags/v1.12.0.tar.gz \
                && tar xvf v1.12.0.tar.gz 
                cd vvenc-1.12.0
                make install install-prefix=/usr/local # install-prefix设置是必须的。如果参数使用install-release 生成static库即.a文件
                cd ..
                ```
            * 解码：[官网](https://github.com/fraunhoferhhi/vvdec)
                ```bash
                wget https://github.com/fraunhoferhhi/vvdec/archive/refs/tags/v2.3.0.tar.gz \
                && tar xvf v2.3.0.tar.gz
                cd vvdec-2.3.0 && make install install-prefix=/usr/local  # install-prefix设置是必须的
                cd ..
                ```
            * **重新安装libheif，并设置额外参数**：必须安装libheif-1.18.1+版本，且必须通过参数手动开启（其他库可以自动发现）
                ```bash
                cmake -DWITH_VVDEC=ON -DWITH_VVENC=on ..
                ...

                vvenc VVC enc. (experimental)   : + built-in
                vvdec VVC dec. (experimental)   : + built-in

                === Supported formats ===
                format        decoding   encoding
                HEIC            YES        YES
                AVIF            YES        NO
                VVC             YES        YES
                ...

                ```
            * 进行编、解码测试：
                * heif-enc --vvc test.jpg -o test.heif
                * heif-dec test.heif -o test.jpg
        * 检查编解码器安装情况：
            * heif-dec --list-decoders
            * heif-enc --list-encoders


7. 源码安装libvips【管理各种图片互换时需要安装】
    * [官方地址](https://github.com/libvips/libvips)
    * 以**v8.15.3**为例（需要使用meson）
        ```bash
        yum install python3 \
        && pip3 install meson
        
        cd libvips-x.y.x 
        meson setup build --prefix /my/install/prefix
        cd build
        
        meson compile \
        && meson test \
        && meson install
        ```
    * 以**v8.12.2**为例（**此版本只能使用libheif v1.16及之前版本**，如果libheif是最新版，使用会出错）
        ```bash
        wget https://github.com/libvips/libvips/releases/download/v8.12.2/vips-8.12.2.tar.gz \
        && tar zxf vips-v8.12.2.tar.gz \
        cd vips-8.12.2 \
        && ./configure && make && make install \
        cd ..
        ```
    * 依赖安装结果检查：
        * ![Img](https://raw.staticdn.net/Navyum/imgbed/main/IMG/6fbe082e1a7b9c81db286da04d27d5f4.png){width="40%"}
        ```bash
        /usr/local/bin/vips --vips-config
        ```
        * 使用vips转换：
            * 编码为heif: vips copy test.jpg test.heif
            * 解码为jpg:  vips copy test.heif test.jpg
            * 编码为webp: vips copy test.jpg test.webp

### 在golang项目中使用heif 
* 通过[bimg](github.com/h2non/bimg)使用libvips的sample：
    ``` golang
    buffer, err := bimg.Read("image.jpg")
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
    }

    newImage, err := bimg.NewImage(buffer).Convert(bimg.HEIF)
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
    }

    outputFile, err := os.Create("test.heif")
    if err != nil {
        log.Fatalf("Error creating output file: %v", err)
    }

    defer outputFile.Close()

    if _, err := outputFile.Write(newImage); err != nil {
        log.Fatalf("Error saving image: %v", err)
    }
    ```

### 直接使用 Dockerfile、Image：
* 环境： centos7
* Github 地址：[https://github.com/Navyum/heif-tools](https://github.com/Navyum/heif-tools)
* heif：docker pull ghcr.io/navyum/heif-tools:heif-tool
* vips：docker pull ghcr.io/navyum/heif-tools:vips-tool


### 参考：
* [libvips安装问题](https://github.com/libvips/libvips/discussions/3173)
* [libvip和libheif版本兼容问题：heif_writer callback returned a null error text (5.2001)](https://github.com/libvips/libvips/discussions/3856)
* [libheif支持VVC相关讨论](https://github.com/strukturag/libheif/issues/519)
* [手淘HEIF、AVIF技术演进](https://tech.taobao.org/news/fo1d1l)
* [爱奇艺HEIF、AVIF技术演进](https://my.oschina.net/u/4484233/blog/11044121)
* [字节跳动ImageX的HEIF技术演进](https://developer.volcengine.com/articles/7195758069530230840)
* [FPGA 加速](https://mp.weixin.qq.com/s?__biz=MzU1NTEzOTM5Mw==&mid=2247495551&idx=1&sn=9fcbb6bd880807ce63f812642a8ee199&utm_source=tuicool&utm_medium=referral)
* [FPGA教程](https://xupsh.github.io/pp4fpgas-cn/PREFACE.html)






