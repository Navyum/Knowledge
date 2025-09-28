---
title: Electron macOS应用打包与发布完整指南
date: 2025-06-17 11:40:59
author: Navyum
tags: 
 - Electron
 - macOS
 - 应用打包
 - 代码签名
 - 发布
categories: 
 - Electron
 - 应用开发
 - 发布部署

article: true
index: true

headerDepth: 2
sticky: true
star: true
---

## Electron macOS应用打包与发布完整指南

本文详细介绍如何使用Electron打包和发布macOS应用程序，包括代码签名、公证、分发等完整流程。涵盖从开发环境配置到最终应用商店发布的各个环节。

### 概述

Electron应用在macOS上的发布需要经过以下关键步骤：
1. **代码签名**：使用Apple开发者证书对应用进行签名
2. **公证**：通过Apple的公证服务验证应用安全性
3. **分发**：通过App Store或直接分发方式发布应用

### 准备工作清单

在开始打包之前，需要准备以下内容：

1. **Apple ID账号**：用于开发者身份验证
2. **Apple App专用密码**：用于自动化流程的身份验证
3. **Apple开发者证书**：用于代码签名
4. **开发者账号**：Apple Developer Program会员资格（可选，用于App Store分发）

## 1. Apple ID账号配置

### 1.1 注册Apple ID
使用自己的Apple ID即可，如果没有可以注册新账号。

**注册地址：** [https://appleid.apple.com/](https://appleid.apple.com/)

### 1.2 设置Apple App专用密码
Apple App专用密码用于自动化工具（如GitHub Actions）进行身份验证，这是必需的步骤。

**操作步骤：**
1. 登录Apple ID管理页面：[https://appleid.apple.com/account/manage](https://appleid.apple.com/account/manage)
2. 在"安全"部分找到"APP 专用密码"
3. 点击"生成密码"并设置一个描述性名称（如"Electron打包"）
4. 记录生成的专用密码

**⚠️ 重要提醒：**
- 设置完成后立即保存到本地文件
- 专用密码只能查看一次，无法再次查看
- 如果忘记密码，只能重新创建

![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/b37c8ccf61de24109b8a501bdf8d1b10.png)

## 2. 申请开发者证书

开发者证书是代码签名的核心，有两种申请方式：

### 2.1 方式一：使用Xcode（推荐）

**适用场景：** 有Mac设备且需要图形界面操作

**操作步骤：**
1. **安装Xcode**
   - 从App Store安装Xcode
   - 确保Xcode版本支持最新的证书类型

2. **配置开发者账号**
   - 打开Xcode → Preferences（或Settings）
   - 点击"Accounts"标签
   - 如果未登录，点击"+"添加Apple ID账号
   - 登录前面申请的Apple ID

3. **申请证书**
   - 在Accounts页面选择你的Apple ID
   - 点击"Manage Certificates"
   - 点击"+"号，选择"Developer ID Application"
   - 设置证书密码（这个密码就是后续的`CSC_KEY_PASSWORD`）

   **⚠️ 重要提醒：**
   - 申请时设置的密码就是后续需要用到的`CSC_KEY_PASSWORD`
   - 必须妥善保管此密码
   - 如果未设置密码，则后续`CSC_KEY_PASSWORD`设置为空字符串

   ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/2ff9f323ad970b4e00a15f51c77c039e.png)

4. **导出证书**
   - 申请完成后，右键点击证书
   - 选择"Export"导出为PKCS12格式
   - 命名为`developerID_application.p12`
   - 设置导出密码（通常与申请时的密码相同）

   ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/f9dd7e68637a10f63deb44233dc3044e.png)

### 2.2 方式二：使用OpenSSL命令行

**适用场景：** 无Mac设备或需要自动化流程

**操作步骤：**

1. **加入Apple Developer Program**
   - 访问：[https://developer.apple.com/account](https://developer.apple.com/account)
   - 使用Apple ID登录并加入开发者计划

2. **本地生成证书请求**
   ```bash
   # 生成私钥
   openssl genrsa -out my.key 2048
   
   # 生成证书签名请求
   openssl req -new -sha256 -key my.key -out my.csr
   ```

   **⚠️ 重要提醒：**
   - 创建证书时设置的密码就是后续需要用到的`CSC_KEY_PASSWORD`
   - 必须妥善保管此密码
   - 如果未设置密码，则后续`CSC_KEY_PASSWORD`设置为空字符串

3. **上传到Apple开发者平台**
   - 访问：[https://developer.apple.com/account/resources/certificates/add](https://developer.apple.com/account/resources/certificates/add)
   - 选择"Developer ID Application"证书类型

   ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/40c91f2cadce9ab546bb12d14258abb9.png)

   - 选择"Previous SUB-CA"，然后点击"Choose File"上传刚才的`my.csr`文件

   ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/6a0d67e689a7400b0b646571339069e6.png)

   - 下载最终证书文件，文件名为`developerID_application.cer`

   ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/a107cd387db14603725f8ff0c9a9e8f3.png)

4. **生成PKCS12证书**
   ```bash
   # 进入下载目录
   cd ~/Downloads
   
   # 将CER格式转换为PEM格式
   openssl x509 -in developerID_application.cer -inform DER -outform PEM -out developerID_application.pem
   
   # 生成PKCS12证书
   openssl pkcs12 -export -inkey my.key -in developerID_application.pem -out developerID_application.p12
   ```

**证书类型说明：**
- **Developer ID Application**：用于在App Store外分发的应用签名
- **Mac App Store**：用于提交到App Store的应用签名
- **Development**：用于开发阶段的应用签名

## 3. Electron打包环境配置

### 3.1 本地构建环境配置

**设置环境变量：**
```bash
# 证书文件路径（根据你的实际路径调整）
export CSC_LINK=$HOME/Downloads/developerID_application.p12

# 证书密码（申请证书时设置的密码）
export CSC_KEY_PASSWORD="your_certificate_password"

# Apple ID账号
export APPLEID="your_apple_id@example.com"

# Apple App专用密码
export APPLEPASSWD="your_app_specific_password"
```

**验证环境变量：**
```bash
# 检查环境变量是否设置正确
echo $CSC_LINK
echo $CSC_KEY_PASSWORD
echo $APPLEID
echo $APPLEPASSWD
```

### 3.2 GitHub Actions构建环境配置

**配置步骤：**
1. 打开项目的Settings → Secrets and variables → Actions
2. 点击"New repository secret"
3. 添加以下密钥：

| 密钥名称 | 描述 | 示例值 |
|:---------|:-----|:-------|
| `CSC_LINK` | 证书文件的Base64编码 | 见下方说明 |
| `CSC_KEY_PASSWORD` | 证书密码 | 申请证书时设置的密码 |
| `APPLEID` | Apple ID账号 | your_apple_id@example.com |
| `APPLEPASSWD` | Apple App专用密码 | 生成的专用密码 |

**CSC_LINK配置说明：**
CSC_LINK需要将PKCS12证书文件转换为Base64编码字符串。

### 3.3 常见问题与解决方案

#### 问题1：CSC_LINK Base64编码
**问题描述：** CSC_LINK设置时需要将PKCS12密钥做Base64编码为字符串才能设置

**解决方案：**
```bash
# 生成Base64编码的证书文件
openssl base64 -in developerID_application.p12 -out certificate-base64.txt
```

#### 问题2：GitHub Actions环境变量格式错误
**问题描述：** 生成的Base64文件字符串设置到GitHub Action时报错：
- `Error: Unable to process file command 'env' successfully.`
- `Error: Invalid format '***'`

![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/0f3e0ce016f348e14a8e8064828b7be8.png)

**问题分析：** 
生成的证书Base64字符串包含大量换行符，导致通过`echo`导入`GITHUB_ENV`变量失败。

**解决方案：**
```bash
# 去除Base64的格式换行
openssl base64 < developerID_application.p12 | tr -d '\r\n' | tee certificate-base64.txt
```

**验证步骤：**
1. 重新复制生成的Base64字符串
2. 设置到GitHub Secrets中的`CSC_LINK`
3. 重新运行GitHub Actions构建

## 4. GitHub Actions Workflow配置

### 4.1 环境变量设置
```yaml
- name: Set macOS signing environment
  if: matrix.platform == 'mac'
  run: |
    echo "APPLEID=${{ secrets.APPLEID }}" >> $GITHUB_ENV
    echo "APPLEIDPASS=${{ secrets.APPLEIDPASS }}" >> $GITHUB_ENV
    echo "CSC_LINK=${{ secrets.CSC_LINK }}" >> $GITHUB_ENV
    echo "CSC_KEY_PASSWORD=${{ secrets.CSC_KEY_PASSWORD }}" >> $GITHUB_ENV
```

### 4.2 完整的macOS构建配置示例
```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Set macOS signing environment
      if: matrix.os == 'macos-latest'
      run: |
        echo "APPLEID=${{ secrets.APPLEID }}" >> $GITHUB_ENV
        echo "APPLEIDPASS=${{ secrets.APPLEIDPASS }}" >> $GITHUB_ENV
        echo "CSC_LINK=${{ secrets.CSC_LINK }}" >> $GITHUB_ENV
        echo "CSC_KEY_PASSWORD=${{ secrets.CSC_KEY_PASSWORD }}" >> $GITHUB_ENV
    
    - name: Build application
      run: npm run build
    
    - name: Build and sign macOS app
      if: matrix.os == 'macos-latest'
      run: npm run dist:mac
    
    - name: Upload macOS artifacts
      if: matrix.os == 'macos-latest'
      uses: actions/upload-artifact@v3
      with:
        name: macos-app
        path: dist/*.dmg
```

## 5. Electron Builder配置

### 5.1 package.json配置示例
```json
{
  "name": "your-app",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "build": "electron-builder",
    "dist:mac": "electron-builder --mac",
    "dist:win": "electron-builder --win",
    "dist:linux": "electron-builder --linux"
  },
  "build": {
    "appId": "com.yourcompany.yourapp",
    "productName": "Your App Name",
    "directories": {
      "output": "dist"
    },
    "mac": {
      "category": "public.app-category.productivity",
      "target": [
        {
          "target": "dmg",
          "arch": ["x64", "arm64"]
        }
      ],
      "hardenedRuntime": true,
      "gatekeeperAssess": false,
      "entitlements": "build/entitlements.mac.plist",
      "entitlementsInherit": "build/entitlements.mac.plist"
    },
    "dmg": {
      "title": "Your App Name",
      "icon": "build/icon.icns"
    },
    "afterSign": "build/notarize.js"
  }
}
```

### 5.2 公证配置（notarize.js）
```javascript
const { notarize } = require('@electron/notarize');

exports.default = async function notarizing(context) {
  const { electronPlatformName, appOutDir } = context;
  
  if (electronPlatformName !== 'darwin') {
    return;
  }

  const appName = context.packager.appInfo.productFilename;

  return await notarize({
    appBundleId: 'com.yourcompany.yourapp',
    appPath: `${appOutDir}/${appName}.app`,
    appleId: process.env.APPLEID,
    appleIdPassword: process.env.APPLEIDPASS,
  });
};
```

## 6. 故障排除

### 6.1 常见错误及解决方案

#### 错误1：证书验证失败
**错误信息：** `Code signing failed: The identity "Developer ID Application: Your Name" doesn't match any valid certificate`

**解决方案：**
1. 检查证书是否正确安装到钥匙串
2. 验证证书是否过期
3. 确认证书类型为"Developer ID Application"

#### 错误2：公证失败
**错误信息：** `Notarization failed: Invalid credentials`

**解决方案：**
1. 检查Apple ID和App专用密码是否正确
2. 确认Apple ID已加入开发者计划
3. 验证网络连接是否正常

#### 错误3：应用无法启动
**错误信息：** `"App" cannot be opened because the developer cannot be verified`

**解决方案：**
1. 确保应用已正确签名
2. 完成公证流程
3. 在系统偏好设置中允许应用运行

### 6.2 调试技巧

#### 验证签名状态
```bash
# 检查应用签名
codesign -dv --verbose=4 /path/to/your/app.app

# 验证签名
codesign --verify --verbose /path/to/your/app.app

# 检查公证状态
spctl --assess --verbose /path/to/your/app.app
```

#### 查看详细日志
```bash
# 启用详细日志
export DEBUG=electron-builder
npm run dist:mac
```

## 7. 最佳实践

### 7.1 安全建议
1. **保护证书安全**：不要将证书文件提交到版本控制系统
2. **使用环境变量**：敏感信息通过环境变量传递
3. **定期更新证书**：证书有有效期，需要定期更新

### 7.2 性能优化
1. **并行构建**：使用GitHub Actions的矩阵策略并行构建多平台
2. **缓存依赖**：利用npm缓存减少构建时间
3. **增量构建**：只构建变更的部分

### 7.3 发布流程
1. **版本管理**：使用语义化版本号
2. **自动化发布**：通过GitHub Actions自动发布
3. **发布说明**：提供详细的更新日志

---

**总结：** 本文详细介绍了Electron macOS应用打包的完整流程，从证书申请到最终发布。通过遵循这些步骤和最佳实践，您可以成功构建和发布专业的macOS应用程序。

