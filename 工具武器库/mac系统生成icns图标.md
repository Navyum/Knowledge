---
title: mac系统生成icns图标
date: 2025-06-17 11:43:15
author: Navyum
tags: 
 - icns图标
 - iconutil
categories: 
 - 踩坑记录
article: true
index: true

headerDepth: 2
sticky: false
star: true
---


### 生成合适的icon png图片
* 使用豆包等大模型的文生图功能生成符合需要的icon
* 这里推荐尺寸为1024*1024，且需要导出四周透明的png格式，名称修改为`icon.png`

### 通去除背景，抠图操作
* 使用在线工具 https://www.remove.bg/upload

### 在mac上创建icns
* 创建icons.iconset文件
  ```bash
  mkdir icons.iconset
  ``` 
* 导出各尺寸的png到icons.iconset中（名称后缀必须为.iconset，不要擅自修改，踩了坑就知道了）
  ```
    Sips -z 16 16 icon.png -o icons.iconset/icon_16x16.png
    Sips -z 32 32 icon.png -o icons.iconset/icon_16x16@2x.png
    Sips -z 32 32 icon.png -o icons.iconset/icon_32x32.png
    Sips -z 64 64 icon.png -o icons.iconset/icon_32x32@2x.png
    Sips -z 128 128 icon.png -o icons.iconset/icon_128x128.png
    Sips -z 256 256 icon.png -o icons.iconset/icon_128x128@2x.png
    Sips -z 256 256 icon.png -o icons.iconset/icon_256x256.png
    Sips -z 512 512 icon.png -o icons.iconset/icon_256x256@2x.png
    Sips -z 512 512 icon.png -o icons.iconset/icon_512x512.png
    Sips -z 1024 1024 icon.png -o icons.iconset/icon_512x512@2x.png
  ```

* 使用iconutil将iconset生成为icns文件
  ```bash
  iconutil -c icns icons.iconset -o icon.icns
  ```
  
