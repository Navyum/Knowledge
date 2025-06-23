---
title: github action 踩坑记录
date: 2025-06-17 11:41:40
author: Navyum
tags: 
 - github工作流
 - github Action
categories: 
 - 踩坑记录

article: true
index: true

headerDepth: 2
sticky: false
star: true
---


### 问题一：工作流互相触发异常的
* 主要任务：
    1. 使用【自动生成工作流】通过定时任务触发，生产内容并推送到分支
    2. 使用【构建工作流】通过push事件监听，将新生产的内容构建成待发布内容
    3. 使用【pages发布工作流】将构建好的内容发布到Pages

* 遇到的问题：
    * 1号工作流执行完成后，不会自动触发2号工作流进行build
    * 1号工作流的定时触发配置：
        ```
        # 触发机制
        name: Generate Daily Markdown
        on:
            schedule:
            - cron: '01 8 * * *'
        
        jobs:
            build:
                ...省略...

                # 向main分支推送修改
                - name: Push changes
                    uses: ad-m/github-push-action@master
                    with:
                        github_token: ${{ secrets.GITHUB_TOKEN }}
                        branch: ${{ github.ref }}
        ```
    * 2号工作流的push触发配置：
        ```
        name: docs build
        on:
            push:
                branches:
                    - main
        ```
    * 1号触发任务会向main分支进行推送，理应会触发2号工作流，但是实际无法触发

* 排查过程：
    * 官方说明：
    ![](https://raw.staticdn.net/Navyum/imgbed/main/IMG/2bde3c0d77c9beeeaecf5e32b1b3e9c7.png){width="60%"}
    * 官方主要是出于防止循环依赖导致资源浪费考虑所以这样设计。(`请确保不要创建递归或意外的工作流程`)


* 解决方案：
    * 方案1：使用workflow_run监听【工作流1】
        * 具体操作，修改2号工作流触发机制：
        ```
        name: docs build
        on:
            workflow_run:
            workflows: "Generate Daily Markdown"    # 需要监听的流程名字
            types: completed
        ```
    * 方案2：使用personal access token，替代GITHUB_TOKEN
        * 具体操作，修改1号工作流的push方式：
        ```
        - name: Push changes
            uses: ad-m/github-push-action@master
            with:
                github_token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
                branch: ${{ github.ref }}
        ```
