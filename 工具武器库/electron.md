---
title: 使用electron打包记录 
date: 2025-06-17 11:40:59
author: Navyum
tags: 
 - electron
 - 发布
categories: 
 - electron
 - 发布
 - 踩坑记录

article: true
index: true

headerDepth: 2
sticky: true
star: true
---

## electron 打包 mac程序环境配置：

### 需要准备的内容：
1. appleid（账号）
2. apple app password（app专用密码）
3. apple development cert（开发者证书）

### appleid（apple账号）
使用自己的appleid即可
注册地址：https://appleid.apple.com/

### 设置apple app专用密码
1. 登陆刚申请好的appleid。登陆地址：[https://appleid.apple.com/account/manage](https://appleid.apple.com/account/manage)
2. 点击 【APP 专用密码】，设置一个密码
    ⚠️：设置完成后立即保存到本地文件，后面无法再次查看，只能重新创建。
    ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/b37c8ccf61de24109b8a501bdf8d1b10.png)

### 申请开发者证书：
* 方式一：使用Mac Xcode
    1. Apple store 安装 Xcode
    2. 打开xcode->preference
    3. 点击 accounts（未登录则需要登录前面申请的appleid）
    4. 点击 Manage Certificates，并申请证书
        ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/2ff9f323ad970b4e00a15f51c77c039e.png)
        ⚠️：申请时设置的密码即后面需要用到的CSC_KEY_PASSWORD,需要保管好如果未设置，则后面CSC_KEY_PASSWORD设置为空字符串
    1. 申请完成后，右键申请的证书并导出pcks12证书，命名为developerID_application.p12
        ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/f9dd7e68637a10f63deb44233dc3044e.png)

* 方式二：openssl申请并提交到官网
    * 加入 Apple Developer Program [地址](https://developer.apple.com/account)
    * 本地生成证书
    ``` bash
    openssl genrsa -out my.key 2048
    openssl req -new -sha256 -key my.key -out my.csr
    ```
    ⚠️：创建证书时设置的密码即后面需要用到的CSC_KEY_PASSWORD,需要保管好。如果未设置，则后面CSC_KEY_PASSWORD设置为空字符串。
    * 上传到开发者平台 [地址](https://developer.apple.com/account/resources/certificates/add)
        * 选择：Developer ID Application
            * 如图：![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/40c91f2cadce9ab546bb12d14258abb9.png)
        * 选择Previous SUB-CA，然后点击Choose File上传刚才的my.csr文件
            * 如图：![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/6a0d67e689a7400b0b646571339069e6.png)
        * 下载最终证书文件，文件名为developerID_application.cer
            * 如图：![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/a107cd387db14603725f8ff0c9a9e8f3.png)
        * 通过shell进入到下载目录(Downloads)，执行如下命令生成pkcs12证书及对应的base64字符串
            ```bash
            openssl x509 -in developerID_application.cer -inform DER -outform PEM -out developerID_application.pem
            openssl pkcs12 -export -inkey ios.key -in developerID_application.pem -out developerID_application.p12
            ```

### Electron 设置打包环境：
* 本地构建：
    * 设置环境变量：
        ```bash
        ## 具体环境变量名称视你的项目而定
        export CSC_LINK=$HOME/Downloads/developerID_application.p12  #设置你自己的对应目录
        export CSC_KEY_PASSWORD="***" #设置你自己申请证书时输入的密码 
        export APPLEID="" # 你的appleid
        export APPLEPASSWD="" # 你的app专用密码
        ```
* github actions 构建：
    * 打开项目的 Settings-> secrets and variables -> Actions -> New repository secret
    * 具体环境变量名称视你的项目而定
        * 添加 CSC_KEY_PASSWORD、CSC_LINK、APPLEID、APPLEPASSWD
    ❌：踩坑：CSC_LINK设置错误：
        * 问题1: CSC_LINK设置时需要将pcks12密钥做base64编码为字符串才能设置
        * 解决：
            ```
            openssl base64 -in developerID_application.p12 -out certificate-base64.txt
            ```
        * 问题2：
            * 情况：上面生成的base64文件字符串设置到github action报错：
                * Error: Unable to process file command 'env' successfully.
                * Error: Invalid format '***'
                ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/0f3e0ce016f348e14a8e8064828b7be8.png)
            * 分析：根据执行情况和错误可以发现，生成的证书base64字符串有大量换行，导致通过echo 导入 GITHUB_ENV变量失败
            * 解决方案：
                * 去除base64的格式换行：
                    ```
                    openssl base64 < developerID_application.p12 | tr -d '\r\n' | tee certificate-base64.txt
                    ```
                * 重新复制并设置CSC_LINK，成功
    * 附github action workflow代码片段：
        ```
        - name: Set env
            if: matrix.platform == 'mac'
            run: |
                echo "APPLEID=${{ secrets.APPLEID }}" >> $GITHUB_ENV
                echo "APPLEIDPASS=${{ secrets.APPLEIDPASS }}" >> $GITHUB_ENV
                echo "CSC_LINK=${{ secrets.CSC_LINK }}" >> $GITHUB_ENV
                echo "CSC_KEY_PASSWORD=${{ secrets.CSC_KEY_PASSWORD }}" >> $GITHUB_ENV
        ```

