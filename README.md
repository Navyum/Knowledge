<p align="center">
  <img src=".website/logo.svg" alt="Navyum's blog logo" width="100" height="auto" />
</p>

<h1 align="center">学习文档</h1>


## Computer Science
- [💻 计算机网络](01.计算机网络/01.网络模型.md)
- [🕹️ 操作系统 TODO](/README)
- [⛵️ 算法、数据结构](03.算法、数据结构/0.学习路径.md)
- [📑 编程语言](04.编程语言/golang/golang学习笔记.md)
- [📁 常用软件](05.常用软件/0.学习路径.md)
  - [Mysql](05.常用软件/数据库/mysql/01.Mysql逻辑架构.md)
  - [Redis](05.常用软件/数据库/redis/01.数据类型、底层数据结构.md)
  - [Docker](05.常用软件/容器化/docker.md)
- [🌡️ 架构设计](06.架构设计/02.分布式与架构/01.分布式设计总纲.md)

## Large Language Model
- [🤖 大模型LLM](07.大模型LLM/00.概念/01.Transformer.md)

## Job Interview
- [❌ 问答 TODO](/README)
- [❌ 编程实战 TODO](/README)
- [👩 面试经验](10.面试经验/Ready4Interview.md)
- [🤔 个人思考](12.个人思考/职业规划.md)

## Effective tools
- [🔧 工具](11.工具武器库/electron.md)

## Reading Books
- [📚 读书笔记](https://www.notion.so/navyum/1c42fcd1fefa4e948d8514761b2ab8c7?v=0ca5dc6ee29e4c2787dbd0f1055b4ed0)

```js
// --echarts--
const option = {
        title: {
            text: 'APP、PC分享查看 PV 折线图'
        },
        tooltip: {},
        xAxis: {
            type: 'category',
            data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        },
        yAxis: {
            type: 'value'
        },
        series: [{
            name: 'PV',
            type: 'line',
            data: [7829, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        }]
    };
chart.setOption(option, true)

```

```js
// --echarts--
const option = {
    grid: {
        left: '10%',
        right: '10%',
        bottom: '10%',
        top: '10%',
        containLabel: true
    },
    title: {
        text: '2024 时间分配',
        left: 'center',
        top: 'bottom'
    },

    label: {
        show: true, // 显示标签
        formatter: '{d}%'
    },
    // 图例配置
    legend: {
        orient: 'vertical', // 图例排列方向，这里设置为垂直方向
        left: 'left', // 图例位置在图表左边
        data: [
        { name:'业务开发'},
        { name:'技术升级'},
        { name:'功能优化'},
        { name:'工作流程'},
        ]
    },
    series: [
    {
      data: [
        { name:'业务开发', value: 20  },
        { name:'技术升级', value: 40  },
        { name:'功能优化', value: 30  },
        { name:'工作流程', value: 10  },
        ],
      type: "pie",
    }
  ]
};
chart.setOption(option, true)
```