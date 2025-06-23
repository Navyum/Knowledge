---
title: options函数选项模式
author: navyum
date: 2025-06-21 22:25:29

article: true
index: true

headerDepth: 2
sticky: false
star: false

category:
  - 笔记
tag:
  - 笔记
---

1. 作用：解决多参数配置问题
2. 优点：
    1. API 具有可扩展性，高度可配置化，新增参数不会破坏现有代码；
    2. 参数列表非常简洁，并且可以使用默认的参数；
    3. option 函数使参数的含义非常清晰，易于开发者理解和使用；
    4. 如果将 options 结构中的参数设置为小写，还可以限制这些参数的权限，防止这些参数在 package 外部使用。
3. 具体实施：
    1. 我们要对 schedule 结构进行改造，把可以配置的参数放入到options 结构中。定义options 支持的配置的功能模块。
```plain

type Schedule struct {
  requestCh chan *collect.Request
  workerCh  chan *collect.Request
  out       chan collect.ParseResult
  options
}

type options struct {
  WorkCount int
  Fetcher   collect.Fetcher
  Logger    *zap.Logger
  Seeds     []*collect.Request
}

```
    2. 书写一系列的闭包函数，这些函数的返回值是一个参数为 options 的函数
```plain
type Option func(opts *options)

func WithLogger(logger *zap.Logger) Option {
  return func(opts *options) {
    opts.Logger = logger
  }
}

func WithFetcher(fetcher collect.Fetcher) Option {
  return func(opts *options) {
    opts.Fetcher = fetcher
  }
}
```
    3. 创建一个生成 schedule 的新函数，函数参数为 Option 的可变参数列表。defaultOptions 为默认的 Option，代表默认的参数列表，然后循环遍历可变函数参数列表并执行
```plain

func NewSchedule(opts ...Option) *Schedule {
  options := defaultOptions
  for _, opt := range opts {
    opt(&options)
  }
  s := &Schedule{}
  s.options = options
  return s
}
```
    4. 在 main 函数中调用 NewSchedule
```plain

func main(){
  s := engine.NewSchedule(
      engine.WithFetcher(f),
      engine.WithLogger(logger)
    )
  s.Run()
}
```


