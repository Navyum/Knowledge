---
title: API压测框架-locust
date: 2025-03-20 17:41:00
author: Navyum
tags: 
 - 压力测试
 - 瓶颈分析
 - P99X
 - Locust
 - 性能测试
 - API测试
categories: 
 - 工具
 - 压测

article: true
index: true

headerDepth: 2
sticky: true
star: true
---
## 概述

性能测试是软件开发生命周期中的一个关键阶段，旨在识别潜在的瓶颈，并确保应用程序在预期的用户负载下满足其性能标准。本文详细介绍如何使用Locust进行API压力测试，包括性能测试指标、可视化工具、测试案例和最佳实践。

---

## 一、性能测试指标
* 响应时间
    - ❌ 平均响应时间（ART）意义不大
    - ✅ 最大响应时间（MRT）
    - ✅ 百分位响应时间：P50、P90、P99
* 吞吐量
    - ✅ 请求速率（RPS）
    - ✅ 网络吞吐量（MB/s）
    - ❌ 事务速率（TPS）
* 容量指标
    - ✅ 最大并发用户数（MCU）
    - ✅ 系统承载峰值

---

## 二、性能测试中关键可视化工具

### 2.1 退化曲线（Degradation Curve）
* 说明：描绘`系统的负载`（用户数量）与`响应时间`之间的关系
* 坐标说明：以横轴上的区间代表`系统负载/用户数量`，纵轴上的点表示对应负载下的`响应时间`
* 作用：
    1. 确定系统的负载极限 
* 关键区域：
    * 单用户区域：最佳性能基准
    * 性能平稳区：没有明显性能下降的情况下实现最佳性能
    * 压力区域：负载增加后系统开始优雅地降级，标志着性能问题的开始
    * 性能拐点：性能下降突变的地方
* 样例：
  <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/ce7e841d4b98bc0e8f75da0a4486a1a6.png" width="80%"></p>

### 2.2 直方图（Histograms）
* 说明：描绘测试数据的分布情况，将数据分成多个区间，显示每个区间的频数或频率。
* 作用：
    1. 很好地说明响应时间的集中和分散情况
    2. 对极值/蜂刺值的洞察
* 坐标说明：以横轴上的区间代表`数据范围`，纵轴上的条形表示这些范围内数据的`频率`，性能测试的直方图通常呈现为正态分布
* 关键区域：
    * 最长的矩形：表示大多数数据点聚集在此处
* 样例：
  <p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/fe38d150664fe996b004c0b1ede3b7b0.png" width="80%"></p>

---

## 三、性能测试工具选择
| 测试工具 | Locust | wrk | ab  | JMeter |
| -- | -- | -- | -- | -- |
| 并发模型 | 协程（gevent） | 多线程 + Epoll | 多进程 | 线程组 |
| 协议支持 | <span style="color: rgb(255, 41, 65);">全协议</span>（需代码实现） | HTTP | HTTP | 多协议（支持插件扩展） |
| 测试脚本 | Python 代码 | Lua 脚本 | 无脚本 | GUI+XML |
| 分布式 | <span style="color: rgb(255, 41, 65);">原生支持</span> | 需第三方工具 | 不支持 | 需插件 |
| 报告能力 | Web UI+CSV | 基础控制台输出 | 基础控制台输出 | 丰富 HTML + 图表 |
| 学习曲线 | 中等（需 Python 基础） | 低（基础使用） | 极低 | 高（功能复杂） |

**结论**：如果要系统性的测试，在可视化呈现效果、上手度上，推荐使用Locust

---

## 四、实战案例

### 案例1：比较两个接口的性能

#### 背景
新、旧服务入参为不同的图片格式（HEIF、JPG），输出OCR结果，需要对新、旧两个接口进行测试，评估在耗时上的差异。

已知条件：
- HEIF格式图片大小更小，传输更快
- JPG图片解码库速度更快
- 需要比较传输、解码最终对接口的影响哪个更大

#### 测试思路
1. 控制新、旧服务使用相同内容、不同格式的图片
2. 控制测试的API在同一个时间、同样的服务器
3. 选择业务场景的常用尺寸，另外选择一些其他不同尺寸

#### 为什么选择Locust
- **并发测试**：Locust脚本可以通过权重设置，同时进行两个接口的测试（同时测试这样可以排除服务器压力等因素干扰）
- **报告能力**：Locust的报告可以同时显示两个接口的分析结果（不需要额外进行数据的加工、展示）
- **协议支持**：Locust支持的协议更好，可以直接使用内部写好的Class（脚本更便捷）

#### Locust脚本实现
```python
from locust import HttpUser, task, between
import os

class OCRUser(HttpUser):
    wait_time = between(1, 3)
    
    # 定义测试文件集及对应权重 [文件路径, 权重]
    test_files = [
        ("./sample/1.jpg", 1),   # 1启用的测试用例
        ("./sample/1.heif", 1),
        ("./sample/2.jpg", 1),
        ("./sample/2.heif", 1),
        ("./sample/3.jpg", 1),
        ("./sample/3.heif", 1),
        ("./sample/4.jpg", 1),
        ("./sample/4.heif", 1),
        ("./sample/5.jpg", 1),
        ("./sample/5.heif", 1),
    ]

    def on_start(self):
        """检查所有测试文件是否存在"""
        for path, _ in self.test_files:
            if not os.path.exists(path):
                raise FileNotFoundError(f"测试文件 {path} 不存在")

    @task
    def perform_ocr_test(self):
        """参数化测试入口"""
        for file_path, weight in self.test_files:
            if weight <= 0:
                continue
            self._execute_ocr_test(file_path)

    def _execute_ocr_test(self, file_path):
        """通用测试执行逻辑"""
        file_size = os.path.getsize(file_path) // 1024
        file_type = os.path.splitext(file_path)[1][1:].upper()
        
        with self._post_file(file_path, file_type) as res:
            self._validate_response(res, file_path)

    def _post_file(self, file_path, file_type):
        """统一封装文件上传操作"""
        task_name = f"{os.path.basename(file_path)}-{os.path.getsize(file_path)//1024}k-{file_type}"
        return self.client.post(
            "/recognize/document",
            files={"image": (
                os.path.basename(file_path), 
                open(file_path, "rb"),
                self._get_mime_type(file_type)
            )},
            name=task_name,
            catch_response=True
        )

    def _validate_response(self, response, file_path):
        """统一响应验证逻辑"""
        if response.status_code != 200:
            response.failure(f"[{file_path}] 状态码异常: {response.status_code}")
        elif not response.json():
            response.failure(f"[{file_path}] 无效的JSON响应")

    def _get_mime_type(self, file_type):
        """MIME类型映射保持不变"""
        file_type = file_type.lower()
        return {
            "jpg": "image/jpeg",
            "heif": "image/heif"
        }.get(file_type, "application/octet-stream")
```

#### 测试配置
**注意**：因为是要对比两个接口的性能，所以我选择的是`最佳性能基准`，选择单个用户的测试场景

<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/44b0f5203e636da73346e6d160066ac4.png" width="80%"></p>

#### 测试结果可视化
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/0a4390c21d9dbb3793e9203e0e2d6cbc.png" width="80%"></p>

#### 测试结论
- 在常见的300～500kb的图片内，对应接口的HEIF格式比JPG格式耗时大约高200ms左右
- 随着尺寸变大，超过1000kb，HEIF的传输优势才变明显
- 后续可以选择更多的大尺寸进行测试，观察HEIF的优异表现是否一致

### 案例2：对新、旧接口进行压力测试，评估其可支持的RPS

#### 测试目标
选择业务常用尺寸的HEIF和JPG大小，评估接口的最大RPS承载能力。

#### 脚本配置
复用上述脚本，分别开启 1.jpg和1.heif：

```python
("./sample/1.jpg", 1),   # 启用的测试用例
("./sample/1.heif", 1),
```

#### 负载配置
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/73f832c4bb5aa117f4280509b0b44b45.png" width="80%"></p>

#### 测试结果可视化
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/ed5a369c68cd91066c3f79c2e8ac2dfc.png" width="80%"></p>

#### 测试结论
- 对应接口的最高RPS为2.4，即使用户数量增加
- 在RPS为1.5时，耗时开始明显增加，即出现性能骤降的拐点
- 进一步验证：设置用户数量为2，RPS为2，耗时比较稳定。表明系统的最佳负载是RPS为2左右

---

## 五、总结与最佳实践

### 关键要点
1. **性能指标选择**：重点关注P90、P99响应时间，而非平均响应时间
2. **可视化分析**：使用退化曲线识别性能拐点，使用直方图分析响应时间分布
3. **工具选择**：Locust在可视化效果和上手度方面具有明显优势
4. **测试策略**：根据测试目标选择合适的负载配置和测试场景

### 建议
- 定期进行性能测试，建立性能基线
- 关注性能拐点，合理设置系统容量
- 结合业务场景设计测试用例
- 重视测试结果的可视化分析