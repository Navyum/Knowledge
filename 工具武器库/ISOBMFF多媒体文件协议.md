---
title: ISOBMFF多媒体文件协议
date: 2025-06-17 11:40:22
author: Navyum
tags: 
 - HEIF
 - 规范
categories: 
 - HEIF
 - 图片格式
article: true
index: true

headerDepth: 2
sticky: false
star: false
---

## ISOBMFF多媒体文件协议

## 多媒体文件

### 多媒体文件规范
* 规范范围：
    * 容器格式规范：定义文件结构和元数据存储
    * 编码格式规范：定义如何对数据进行压缩、编码、解码（涉及图片、音频、视频、字幕等）
    * 传输协议规范：定义流媒体协议

### ISOBMFF ISO基本媒体文件格式
ISO/IEC 14496-12 标准的实现

ISO Base Media File Format 是一种高度可扩展的容器文件格式，它定义了多媒体文件的通用结构

用途：
* 用于视频、音频文件的封装、支持如HEIF图像文件格式
* 是现代流媒体技术如DASH（Dynamic Adaptive Streaming over HTTP）和HLS（HTTP Live Streaming）的基础

ISOBMFF文件由称为“box” 的组件组成
* ftyp box来标识文件类型
* mdat box来存储媒体数据
* trak box来组织单个媒体流
* moov box来存储元数据

具体应用：
| 文件类型 | 互联网媒体类型（MIME） | 常用扩展名 |
| :---- | :-- | :-- |
| QuickTime | video/quicktime | .mov, .movie, .qt |
| HEIF | image/heif, image/heic | .heif, .heifs; .heic, .heics; .avci, .avcs; .HIF |
| MP4 | video/mp4, audio/mp4 | .mp4, .m4a, .m4p, .m4b, .m4r, .m4v |
| 3GP | video/3gpp | .3gp, 3g2 |
| JPEG 2000 | image/jp2, image/jpx | .jp2, .j2k, .jpf, .jpm, .jpg2, .j2c, .jpc, .jpx, .mj2 |
| Flash Video | video/x-flv | .flv, .fla, .f4v, .f4a, .f4b, .f4p |

ISOBMFF 文件结构：
HEIF容器格式/HEIF标准，基于ISOBMFF 标准

* MP4文件
![Img](https://raw.staticdn.net/Navyum/imgbed/main/IMG/a5358213a7bd310ccc5c958e840907bb.png){width="60%"}
* HEIC文件
![Img](https://raw.staticdn.net/Navyum/imgbed/main/IMG/24111dab3038b2ed6f74cb98b73f5ca6.png){width="60%"}

### 容器格式规范：

#### 图片容器：
* TIFF（Tagged Image File Format） 打印相关
* GIF（Graphics Interchange Format） 很老，且存储效率低。协议甚至比JPEG还早
* RIFF（Resource Interchange File Format）webp文件的存储容器格式
* HEIF（High Efficiency Image File Format）高效压缩

### HEIF容器/HEIF标准
ISO/IEC 23000-12 标准，又称 HEIF，与编解码器无关的通用图像容器[wiki](https://www.iso.org/obp/ui/en/#iso:std:iso-iec:23000:-12:ed-1:v1:en)

#### 目标
- 替代JPEG，提供更小的文件大小和更高的图像质量，尤其是在存储高分辨率图像。
- 是ISOBMFF在图片领域的的特化
- HEIF也可以存储音频、图像序列等，`在HEIF中，照片、视频、音频可以封装成单一文件`

#### 特性
- 支持存储单个图像或图像序列，并且可以包含额外的媒体流，如音频和文本。
- 高压缩率。

#### 支持的文件类型扩展名

| 扩展名 | 描述 |
| :--- | :--- |
| `.heif` | HEIF容器格式的通用扩展名 |
| `.heifs` | 标识包含多个图像的通用扩展名 |
| `.heic` | 苹果公司使用的基于HEVC进行编码的图片 |
| `.heics` | 苹果公司使用的基于HEVC编码的图像序列 |
| `.avci` | 标识使用H.264/MPEG-4 AVC编码的视频 |
| `.avcs` | 标识使用H.264/MPEG-4 AVC编码的多个图像或图像序列 |
| `.avif` | 标识使用AV1视频编码的图像文件格式 |

#### 图像序列（Image Sequence）
是指一系列按特定顺序排列的静态图像，这些图像通常用于创建动态效果或动画。

#### HEIF图片的两种不同的编码：

HEIC：High Efficiency Image Codec（基于HEVC视频编码）
AVIF：AV1 Image File Format（基于AV1视频编码）

#### HEIC和AVIF的比较

**相同点：**
- 都旨在提供比传统JPEG格式更高的压缩效率和图像质量。

**区别：**

1. **目标：**
   - HEIC：基于H.265/HEVC视频压缩标准，旨在替代JPEG。
   - AVIF：基于AV1视频压缩标准，旨在提供比HEVC更高的压缩效率。

2. **兼容性：**
   - HEIC：由MPEG标准组织开发，主要被苹果设备支持，在Android和Windows设备上的支持有限。
   - AVIF：由开放媒体联盟（AOMedia）开发，作为一个开放标准，它被设计为跨平台兼容，适用于各种设备和操作系统。

3. **色彩和透明度：**
   - HEIC：支持高动态范围（HDR）和宽色域，但不支持透明度。
   - AVIF：支持HDR、宽色域以及透明度，使其在需要透明背景的图像中非常有用。

4. **版权和许可：**
   - HEIC：基于H.265/HEVC，可能涉及专利许可费用。
   - AVIF：是开放标准，不受专利许可费用的限制。


### 常见的图像文件格式的特征比较
| 特性 | HEIF (.heic) | JPEG/Exif | PNG | GIF (89a) | WebP | JPEG-XR / TIFF | JPEG-XR / JPX | BPG |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 格式和可扩展性 | ISOBMFF | TIFF | - | - | RIFF | TIFF | - | - |
| 有损压缩 | 是 (HEVC) | 是 (JPEG) | 否 | 否 | 是 (VP8) | 是 | 是 | 是 (HEVC) |
| 无损压缩 | 是 (HEVC) | 是 (TIFF Rev 6.0) | 是 (PNG) | 是 (GIF) | 是 (VP8L) | 是 | 是 | 是 (HEVC) |
| 可扩展至其他编码格式 | 是 | 是 | 否 | 否 | 否 | 是 | 是 | 否 |
| 元数据格式（在内部、顶部） | Exif, XMP, MPEG-7 | Exif | - | - | Exif, XMP | Exif, XMP | JPX, (XMP) | Exif，XMP |
| 可扩展至其他元数据格式 | 是 | 否 | 否 | 否 | 否 | 否 | 是（基于XML） | 是 |
| 其他媒体类型（音频、文本等） | 是 | Audio| 否 | 否 | 否 | 否 | 是 | 否 |
| 多图像特性 |
| 同一个文件中多个图像 | 是 | 否 | 否 | 是 | 是 | 否 | 是 | 是 |
| 图像序列/动画 | 是 | 否 | 否 | 是 | 是 | 否 | 是 | 是 |
| 图像编码 | 是 | 否 | 否 | 否 | 否 | 否 | 否 | 是 |
| 派生图像 |
| 多次90度旋转 | 是 | 是 | 否 | 否 | 否 | 是 | 是 | 否 |
| 裁剪 | 是 | 否 | 否 | 否 | 否 | 否 | 是 | 否 |
| 平铺/堆叠 | 是 | 否 | 否 | 否 | 是 | 否 | 是 | 否 |
| 可扩展至其他编辑操作 | 是 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| 辅助图片信息 |
| 透明度（alpha通道） | 是 | 否 | 是 | 否 | 是 | 是 | 是 | 是 |
| 深度映射 | 是 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| 缩略图 | 是 | 是 | 否 | 否 | 否 | 是 | 是 | 是 |


在线解析工具：
[Tool](https://gpac.github.io/mp4box.js/test/filereader.html)
[github](https://github.com/gpac/mp4box.js)

参考：
[wikipedia](https://en.wikipedia.org/wiki/ISO_base_media_file_format)
[isobmff](https://www.iso.org/obp/ui/en/#iso:std:iso-iec:14496:-12:ed-7:v1:en)
[avif](https://netflixtechblog.com/avif-for-next-generation-image-coding-b1d75675fe4)
[avif腾讯翻译](https://cloud.tencent.com/developer/news/583326)
[libavif AOM官方](https://github.com/AOMediaCodec/libavif)
[heif](https://github.com/nokiatech/heif)
[libheif](https://github.com/strukturag/libheif)
