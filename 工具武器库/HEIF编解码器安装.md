---
title: HEIF编解码器安装与配置指南
date: 2025-06-17 11:39:40
author: Navyum
tags: 
 - HEIF
 - 环境安装
 - 图片格式
 - 编解码器
categories: 
 - HEIF
 - 图片格式
 - 工具配置
article: true
index: true

headerDepth: 2
sticky: true
star: true
---

## HEIF编解码器安装与配置指南

HEIF（High Efficiency Image Format）是一种高效的图像格式，基于HEVC（H.265）编码标准，相比JPEG格式能够提供更好的压缩率和图像质量。本文详细介绍如何在CentOS 7环境下安装和配置HEIF编解码器，支持多种编码格式的转换。

### 技术背景

#### HEIF编码解码原理
![Img](https://raw.staticdn.net/Navyum/imgbed/main/IMG/21139a95b55bedab5c5a1eaf9a9c4f0b.png)

#### 支持的编码标准
- **H.264/MPEG-4 AVC**：传统视频编码标准
- **H.265/HEVC**：高效视频编码，HEIF的主要编码标准
- **AVIF**：基于AV1编码的图像格式（AV1/AOM、dav1d）
- **H.266/VVC**：下一代视频编码标准

#### 核心依赖库
**主要编解码库：**
- `libx265`：HEVC编码器
- `libde265`：HEVC解码器
- `libaom`：AV1编码器
- `libvvenc`：VVC编码器
- `libheif`：HEIF格式处理核心库
- `libvips`：图像处理库

**其他参考库：**
- `libavif`：AVIF格式处理库

#### 编译工具要求
安装过程中需要以下编译工具：
- `gcc-6+`、`g++`：C/C++编译器
- `make`：构建工具
- `cmake-3.x`：跨平台构建系统
- `meson`：现代构建系统
- `ninja`：快速构建工具

### 安装前准备

**重要提醒：** 安装依赖时必须严格按照顺序进行，前面的库是后续库的必要依赖。如果依赖安装不正确，虽然后续库可能编译通过，但无法正常使用HEIF功能。

### CentOS 7 环境安装步骤

#### 1. 安装基础图片格式库【必须】
```bash
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

#### 2. 安装编译工具【必须】
```bash
yum install -y \
  automake \
  gcc \
  make \
  gcc-c++
```
#### 3. 源码安装WebP库【可选】
WebP是Google开发的现代图像格式，提供更好的压缩率。

**官方地址：** [Google WebP](https://chromium.googlesource.com/webm/libwebp)

**安装步骤（以v1.4.0为例）：**
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

#### 4. 源码安装libde265解码器【必须】
libde265是开源的HEVC解码器，用于解码HEIF格式图像。

**官方地址：** [libde265 Releases](https://github.com/strukturag/libde265/releases)

**安装步骤（以v1.0.15为例）：**
```bash
wget https://github.com/strukturag/libde265/releases/download/v1.0.15/libde265-1.0.15.tar.gz \
&& tar xzf libde265-1.0.15.tar.gz \
&& cd libde265-1.0.15 \
&& ./configure \
&& make \
&& make install \
&& cd ..
```
#### 5. 源码安装libx265编码器【必须】
libx265是开源的HEVC编码器，用于将图像编码为HEIF格式。

**官方地址：** [libx265 GitHub](https://github.com/videolan/x265)

**安装步骤（以v3.4为例）：**
```bash
wget https://github.com/videolan/x265/archive/refs/tags/3.4.tar.gz \
&& tar xzf 3.4.tar.gz \
&& cd x265-3.4 \
&& cd x265/build/linux \
&& ./make-Makefiles.bash      # 键入 g，生成对应环境的Makefile
make && make install \
&& cd ../..
```
#### 6. 源码安装libheif【必须】
libheif是HEIF格式处理的核心库，提供编码、解码和格式转换功能。

**官方地址：** 
- [libheif GitHub](https://github.com/strukturag/libheif)
- [Nokia HEIF解析](https://github.com/nokiatech/heif)

**前置依赖：** 需要cmake 3.3+版本

**6.1 安装CMake 3.26.4（CentOS 7需要源码安装）**
```bash
yum install openssl openssl-devel \
&& wget https://cmake.org/files/v3.26/cmake-3.26.4.tar.gz \
&& tar zxf cmake-3.26.4.tar.gz \
&& cd cmake-3.26.4 \
&& ./configure \
&& make && make install
```

**6.2 编译安装libheif（以v1.18.2为例）**
```bash
wget https://github.com/strukturag/libheif/releases/download/v1.18.2/libheif-1.18.2.tar.gz \
&& tar xzf libheif-1.18.2.tar.gz \
&& cd libheif-1.18.2 \
&& mkdir build && cd build \
&& cmake --preset=release .. \
&& make && make install \
&& cd ../..
```
**6.3 验证安装结果**
检查编解码器是否正确安装：
```bash
heif-enc --list-encoders
```

**预期输出：**
```
HEIC encoders:
- x265 = x265 HEVC encoder (0.0) [default]
AVIF encoders:
VVC encoders:
JPEG encoders:
- jpeg = libjpeg-turbo 1.2.90 (libjpeg 6.2) [default]
JPEG 2000 encoders:
HT-J2K encoders:
Uncompressed encoders:
- uncompressed = uncompressed [default]
```

**6.4 基础使用示例**
此时已经可以使用heif工具进行格式转换：

```bash
# 查看HEIF文件信息
./heif-info ../../tests/data/x.heif

# 将JPEG转换为HEIF
./heif-enc test.jpg -o test.heif

# 将HEIF转换为JPEG
./heif-dec ../../tests/data/x.heif -o c.jpg
```

### 高级编解码器配置

#### 支持的编解码器列表
libheif支持多种格式的编解码器：

| 格式 | 解码器 | 编码器 |
|:-----|:------:|:------:|
| HEIC | libde265, ffmpeg | x265, kvazaar |
| AVIF | AOM, dav1d | AOM, rav1e, svt-av1 |
| VVC | vvdec | vvenc, uvg266 |
| AVC | openh264 | - |
| JPEG | libjpeg(-turbo) | libjpeg(-turbo) |
| JPEG2000 | OpenJPEG | OpenJPEG |
| uncompressed | built-in | built-in |

#### 7. 安装AVIF编解码器（可选）
AVIF是基于AV1编码的图像格式，提供更好的压缩效率。

**7.1 安装libaom（AV1编码器）**
```bash
git clone -b v3.9.1 --depth 1 https://aomedia.googlesource.com/aom \
&& cd aom \
&& cmake -S . -B build.libavif -G Ninja \
-DCMAKE_INSTALL_PREFIX="/usr/local" \
-DBUILD_SHARED_LIBS=1 \
-DCMAKE_BUILD_TYPE=Release \
-DAOM_TARGET_CPU=generic \
-DENABLE_DOCS=0 \
-DENABLE_EXAMPLES=0 \
-DENABLE_TESTDATA=0 \
-DENABLE_TESTS=0 \
-DENABLE_TOOLS=0 

ninja -C build.libavif && ninja -C build.libavif install \
&& cd ..
```

**7.2 AVIF编解码测试**
```bash
# 编码为AVIF格式
heif-enc --avif test.jpg -o test.avif

# 解码AVIF格式
heif-dec --avif test.avif -o test.jpg
```

#### 8. 安装VVC编解码器（H.266/VVC，实验性功能）
VVC是下一代视频编码标准，目前处于实验阶段。

**8.1 依赖要求**
- gcc-5.0+、cmake-3.13+版本
- 需要安装高版本gcc

**8.2 安装高版本GCC**
**方式一：源码编译（耗时60分钟以上）**

**方式二：使用红帽SCL版本（推荐）**
```bash
# 1. 安装SCL仓库
yum install centos-release-scl centos-release-scl-rh -y

# 2. 修改SCL源为阿里云（CentOS7的SCL源在2024年6月30日停止维护）
cat >/etc/yum.repos.d/CentOS-SCLo-rh.repo <<EOF
[centos-sclo-rh]
name=CentOS-7 - SCLo rh
baseurl=https://mirrors.aliyun.com/centos/7/sclo/x86_64/rh/
gpgcheck=1
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-SCLo
EOF

# 3. 安装gcc-9开发包
yum install devtoolset-9-gcc devtoolset-9-gcc-c++ devtoolset-9-binutils -y

# 4. 启用并验证版本
scl enable devtoolset-9 bash && gcc -v
```

**8.3 安装VVC编码器**
**官方地址：** [vvenc GitHub](https://github.com/fraunhoferhhi/vvenc)

```bash
wget https://github.com/fraunhoferhhi/vvenc/archive/refs/tags/v1.12.0.tar.gz \
&& tar xvf v1.12.0.tar.gz \
&& cd vvenc-1.12.0 \
&& make install install-prefix=/usr/local \
&& cd ..
```

**8.4 安装VVC解码器**
**官方地址：** [vvdec GitHub](https://github.com/fraunhoferhhi/vvdec)

```bash
wget https://github.com/fraunhoferhhi/vvdec/archive/refs/tags/v2.3.0.tar.gz \
&& tar xvf v2.3.0.tar.gz \
&& cd vvdec-2.3.0 \
&& make install install-prefix=/usr/local \
&& cd ..
```

**8.5 重新编译libheif支持VVC**
必须使用libheif-1.18.1+版本，并通过参数手动启用VVC支持：

```bash
cd libheif-1.18.2/build
cmake -DWITH_VVDEC=ON -DWITH_VVENC=ON ..
make && make install
```

**预期输出：**
```
vvenc VVC enc. (experimental)   : + built-in
vvdec VVC dec. (experimental)   : + built-in

=== Supported formats ===
format        decoding   encoding
HEIC            YES        YES
AVIF            YES        NO
VVC             YES        YES
```

**8.6 VVC编解码测试**
```bash
# 编码为VVC格式
heif-enc --vvc test.jpg -o test.heif

# 解码VVC格式
heif-dec test.heif -o test.jpg
```

**8.7 验证编解码器安装**
```bash
# 查看所有解码器
heif-dec --list-decoders

# 查看所有编码器
heif-enc --list-encoders
```


#### 9. 安装libvips图像处理库【可选】
libvips是一个高性能的图像处理库，支持多种格式转换。

**官方地址：** [libvips GitHub](https://github.com/libvips/libvips)

**9.1 安装libvips v8.15.3（推荐，使用meson构建）**
```bash
# 安装Python3和meson
yum install python3 \
&& pip3 install meson

# 下载并编译libvips
cd libvips-x.y.x 
meson setup build --prefix /usr/local
cd build

meson compile \
&& meson test \
&& meson install
```

**9.2 安装libvips v8.12.2（兼容版本）**
**注意：** 此版本只能使用libheif v1.16及之前版本，如果libheif是最新版会出错。

```bash
wget https://github.com/libvips/libvips/releases/download/v8.12.2/vips-8.12.2.tar.gz \
&& tar zxf vips-8.12.2.tar.gz \
&& cd vips-8.12.2 \
&& ./configure && make && make install \
&& cd ..
```

**9.3 验证libvips安装**
```bash
/usr/local/bin/vips --vips-config
```

**9.4 使用vips进行格式转换**
```bash
# 编码为HEIF格式
vips copy test.jpg test.heif

# 解码为JPEG格式
vips copy test.heif test.jpg

# 编码为WebP格式
vips copy test.jpg test.webp
```

### 应用开发集成

#### 在Golang项目中使用HEIF
通过[bimg](https://github.com/h2non/bimg)库使用libvips进行HEIF处理：

```golang
package main

import (
    "fmt"
    "log"
    "os"
    "github.com/h2non/bimg"
)

func main() {
    // 读取图像文件
    buffer, err := bimg.Read("image.jpg")
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        return
    }

    // 转换为HEIF格式
    newImage, err := bimg.NewImage(buffer).Convert(bimg.HEIF)
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        return
    }

    // 保存转换后的图像
    outputFile, err := os.Create("test.heif")
    if err != nil {
        log.Fatalf("Error creating output file: %v", err)
    }
    defer outputFile.Close()

    if _, err := outputFile.Write(newImage); err != nil {
        log.Fatalf("Error saving image: %v", err)
    }
    
    fmt.Println("Image converted to HEIF successfully!")
}
```

#### Docker容器化部署
**环境：** CentOS 7

**GitHub地址：** [heif-tools](https://github.com/Navyum/heif-tools)

**可用镜像：**
```bash
# HEIF工具镜像
docker pull ghcr.io/navyum/heif-tools:heif-tool

# VIPS工具镜像
docker pull ghcr.io/navyum/heif-tools:vips-tool
```


### 故障排除与常见问题

#### 常见安装问题
1. **libvips安装问题**
   - 参考：[libvips安装问题讨论](https://github.com/libvips/libvips/discussions/3173)

2. **版本兼容性问题**
   - libvips和libheif版本兼容问题：`heif_writer callback returned a null error text (5.2001)`
   - 参考：[版本兼容性讨论](https://github.com/libvips/libvips/discussions/3856)

3. **VVC支持问题**
   - libheif支持VVC相关讨论：[VVC支持问题](https://github.com/strukturag/libheif/issues/519)

#### 性能优化建议
1. **编译优化**：使用`-O3`优化级别编译
2. **硬件加速**：考虑使用FPGA加速（参考下方链接）
3. **内存管理**：合理设置缓冲区大小

### 参考资料

#### 技术文档
- [libvips安装问题](https://github.com/libvips/libvips/discussions/3173)
- [libvips和libheif版本兼容问题](https://github.com/libvips/libvips/discussions/3856)
- [libheif支持VVC相关讨论](https://github.com/strukturag/libheif/issues/519)

#### 企业实践案例
- [手淘HEIF、AVIF技术演进](https://tech.taobao.org/news/fo1d1l)
- [爱奇艺HEIF、AVIF技术演进](https://my.oschina.net/u/4484233/blog/11044121)
- [字节跳动ImageX的HEIF技术演进](https://developer.volcengine.com/articles/7195758069530230840)

#### 硬件加速
- [FPGA加速技术](https://mp.weixin.qq.com/s?__biz=MzU1NTEzOTM5Mw==&mid=2247495551&idx=1&sn=9fcbb6bd880807ce63f812642a8ee199&utm_source=tuicool&utm_medium=referral)
- [FPGA教程](https://xupsh.github.io/pp4fpgas-cn/PREFACE.html)

---

**总结：** 本文详细介绍了在CentOS 7环境下安装和配置HEIF编解码器的完整流程，包括基础依赖安装、核心库编译、高级编解码器配置以及应用开发集成。通过遵循本文的安装步骤，您可以成功搭建支持多种图像格式转换的HEIF处理环境。






