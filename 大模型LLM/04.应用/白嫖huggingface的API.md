---
title: 白嫖huggingface的API
date: 2025-02-06 19:31:15
author: Navyum
tags: 
 - LLM
 - Prompt
categories: 
 - LLM
 - AI
---
## 白嫖huggingface的API

### 背景：
众所周知，hugging face中很多space资源都是可以直接使用的，那么如何将这些资源用在自己的项目中呢？

### 经过：
在使用Yank Note的 AI Extension时，发现文本转图片的端点是可以免费使用的，我忽然对此产生了兴趣
免费的配置：
<img  src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/e1e56ea562c1d8593a2bd9842d9d62eb.png" width="40%" />

带着好奇，我直接打开对应的端点[https://black-forest-labs-flux-1-schnell.hf.space](https://black-forest-labs-flux-1-schnell.hf.space)：
端点地址：
<img  src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/af902ebd4e64aa4bd9632a6fe14f85f0.png" width="40%" />

好家伙，发现了老朋友gradio（huggingface上大部分的space应该都是基于gradio实现的界面吧🙂）

直接F12打开开发者模式，跑一边，查看下网络请求
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/2dd79c98e1950e7539509a224eb9fc50.png" width="60%"></p>

此时发现domain就是对应的端点地址：https://black-forest-labs-flux-1-schnell.hf.space/queue/data?session_hash=iy3znn5avof
，并且后面携带了path：/queue/data以及session信息。这些先不管，后面看gradio官方文档可以看到


我们从huggingface首页，搜索其他的文生图的space
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/cba1851e98c2153905c218918a51d715.png" width="60%"></p>

我对MIDJOURNEY比较感兴趣，所以就直接打开它[https://huggingface.co/spaces/mukaist/Midjourney](https://huggingface.co/spaces/mukaist/Midjourney)

直接F12打开开发者模式，跑一边，查看下网络请求
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/8364c25597acd584ab20ac27a847f22a.png" width="60%"></p>

此时我们看到，midJourney的这个也是基于SSE协议，并且可以找到对应的端点为：https://mukaist-midjourney.hf.space
该地址的后面也携带了path：/queue/data以及session信息

接下来，我们对比下这两个SSE协议返回的EventStream的差异
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/ac95291fa37db887231d839b16137305.png" width="60%"></p>
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/c4fe9d7aec8aa9f021e4b6281b876d6a.png" width="60%"></p>

直接找到msg为`process_completed`的这条stream，右键copy message，直接复制出来
```json 
{
    "msg": "process_completed",
    "event_id": "ac428a8daed3438392629275fe3c9b4f",
    "output": {
        "data": [
            {
                "path": "/tmp/gradio/2c4badcaf6aa37a7b2622117446ad2ac105d291e/image.webp",
                "url": "https://black-forest-labs-flux-1-schnell.hf.space/file=/tmp/gradio/2c4badcaf6aa37a7b2622117446ad2ac105d291e/image.webp",
                "size": null,
                "orig_name": "image.webp",
                "mime_type": null,
                "is_stream": false,
                "meta": {
                    "_type": "gradio.FileData"
                }
            },
            708694447
        ],
        "is_generating": false,
        "duration": 12.627551317214966,
        "average_duration": 11.79129842745821,
        "render_config": null,
        "changed_state_ids": [

        ]
    },
    "success": true
}
```
```json
{
    "msg": "process_completed",
    "event_id": "7f8054f0b4cc41688c91c4ae4e26bce0",
    "output": {
        "data": [
            [
                {
                    "image": {
                        "path": "/tmp/gradio/10fdc145d2e6dde65d2d8b1189cd54a2a34db4b3/c69b8380-6a65-4e0f-9a1f-5b5f4fb696c7.png",
                        "url": "https://mukaist-midjourney.hf.space/file=/tmp/gradio/10fdc145d2e6dde65d2d8b1189cd54a2a34db4b3/c69b8380-6a65-4e0f-9a1f-5b5f4fb696c7.png",
                        "size": null,
                        "orig_name": "c69b8380-6a65-4e0f-9a1f-5b5f4fb696c7.png",
                        "mime_type": null,
                        "is_stream": false,
                        "meta": {
                            "_type": "gradio.FileData"
                        }
                    },
                    "caption": null
                },
                {
                    "image": {
                        "path": "/tmp/gradio/211d3417c08b99d4d381096c1e5e4138a7aa81dd/6d26fa25-e52b-485c-86f7-30b8c4f387ac.png",
                        "url": "https://mukaist-midjourney.hf.space/file=/tmp/gradio/211d3417c08b99d4d381096c1e5e4138a7aa81dd/6d26fa25-e52b-485c-86f7-30b8c4f387ac.png",
                        "size": null,
                        "orig_name": "6d26fa25-e52b-485c-86f7-30b8c4f387ac.png",
                        "mime_type": null,
                        "is_stream": false,
                        "meta": {
                            "_type": "gradio.FileData"
                        }
                    },
                    "caption": null
                }
            ],
            47063601
        ],
        "is_generating": false,
        "duration": 21.571749687194824,
        "average_duration": 19.764927463950933,
        "render_config": null,
        "changed_state_ids": [

        ]
    },
    "success": true
}
```

我们可以看到url即生成的结果，但是两者的返回稍有差异。flux为 result?.data?.[0]?.url，midjouney为 result?.data?.[0]?.[0]?. image?.url，且midjourney一次生成了两个


那么接下来，我们只需要在yank note 的高级设置中，修改端点地址以及请求相应的结构即可使用midjourney作为免费的适配器了。
```js
const { state: { width, height, apiToken, instruction, endpoint } } = data

const client = await env.gradio.Client.connect(endpoint, { hf_token: apiToken })

const submission = await client.submit('/infer', {
  prompt: instruction,
  seed: 0,
  width,
  height,
  randomize_seed: true,
  num_inference_steps: 4,
}, undefined, undefined, true)

let result
for await (const msg of submission) {
  if (msg.type === 'data') {
    result = msg
    break
  }

  if (msg.type === 'status' && msg.stage !== 'error') {
    const status = msg.progress_data?.map(
      item => `${item.desc || item.unit}: ${item.index}/${item.length}`
    ).join('\n') || msg.stage || ''

    env.updateStatus(status)
  }
}

const url = result?.data?.[0]?.[0]?. image?.url  //修改url获取的结构

if (!url) {
  throw new Error(JSON.stringify(result))
}

return { url, method: 'GET' }
```

然后，尝试生成一个图片，结果报错了
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/5c25a986c5b4da4ce9da18590cda2435.png" width="60%"></p>

从错误信息看，提示对应端点没有对应的fn_index。

我的第一反应是，是不是fn_index设置的有问题，我查看了gradio中的请求，发现两者确实有差异：
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/ce4a00f834d85acb8abbc66e9997ebf2.png" width="60%"></p>
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/2ff39765f9b67616dd1b0bd9a8553e48.png" width="60%"></p>

其中一个是fn_index为2，另一个fn_index为3

第一直觉是，如何修改fn_index，从3改为2呢？我们先看下yank note的代码实现

其中下面的代码引起了我的注意：
```
const submission = await client.submit('/infer', {
  prompt: instruction,
  seed: 0,
  width,
  height,
  randomize_seed: true,
  num_inference_steps: 4,
}, undefined, undefined, true)
```

我们可以看到这段代码实际使用submit方法，请求了path为/infer。尝试找一下gradio的submit的参数说明
官方地址：[https://www.gradio.app/docs/js-client](https://www.gradio.app/docs/js-client)
仅找到一点信息：
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/d528d39711a5b4c4d77ad7c305d14a2f.png" width="60%"></p>

搜索官方文档没有找到任何fn_index相关的信息

但在官方文档中，发现了submit相似的方法predict，尝试使用client.predict("/predict")、client.submit("/predict")均失败。

在重新审视一下之前的错误，`提示对应端点没有对应的fn_index`，以及flux中使用的/infer方法，在gradio官方文档搜索时也没有任何信息，于是猜测：不同的平台对应的方法明应该存在差异。重新查看gradio的官方文档，发现了一个方法：view_api
> view_api
> The view_api method provides details about the API you are connected to. It returns a JavaScript object of all named endpoints, unnamed endpoints and what values they accept and return. This method does not accept arguments.
> ```
> import { Client } from "@gradio/client";
> const app = await Client.connect("user/space-name");
> const api_info = await app.view_api();
> console.log(api_info);
> ```

这个方法应该可以获取到对应端点提供的方法名，（这不就是类似于SOAP协议么？）

通过client.view_api()，获取到flux和midjourney各自实现的方法：

<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/f5ddf4154012718ab7442196a4c438a1.png" width="60%"></p>
<p align="center"><img src="https://raw.staticdn.net/Navyum/imgbed/pic/IMG/38666ebff36dfb4430ebd5a1d1af9d17.png" width="60%"></p>

果然如所料，各自的实现接口存在差异，flux的是`/infer`，而midjourney为`/run`。另外新的发现就是parameters的一些额外说明，这样我们在调用接口是就可以按照这个说明来实现了。

重新修改yank note中的高级设置：
```js
const { state: { width, height, apiToken, instruction, endpoint } } = data

const client = await env.gradio.Client.connect(endpoint, { hf_token: apiToken })


const submission = await client.submit('/run', {    //修改方法
  prompt: instruction,
  seed: 0,
  width,
  height,
  randomize_seed: true,
  // num_inference_steps: 4,         //去除不支持的parameter参数
}, undefined, undefined, true)

let result
for await (const msg of submission) {
  if (msg.type === 'data') {
    result = msg
    break
  }

  if (msg.type === 'status' && msg.stage !== 'error') {
    const status = msg.progress_data?.map(
      item => `${item.desc || item.unit}: ${item.index}/${item.length}`
    ).join('\n') || msg.stage || ''

    env.updateStatus(status)
  }
}

const url = result?.data?.[0]?.[0]?. image?.url  //修改url获取的结构

if (!url) {
  throw new Error(JSON.stringify(result))
}

return { url, method: 'GET' }
```

最后大功告成！！



### 总结：
* 同样的方法，只需要掌握方法，就可以使用到任何工具中，白嫖huggingface的资源（这里仅以yank note为例子）
* 如何使用hugging face上的免费space，具体步骤：
    1. 找到你想白嫖的的space
    2. 打开对应space，打开F12开发者模式，执行一次任务
    3. 找到刚刚你执行任务触发的请求（一般是SSE）
    4. 找出端点（SSE的url地址）
    5. 通过client.connect，连接到对应端点
    6. 通过client.view_api，查看端点实现方法和协议详细内容
    7. 通过client.sumbit，调用对应的端点，并传递参数（设置参数、prompt等）

### 完整代码实现
```js
import { Client } from "@gradio/client";

// setting、config
const endpoint = 'xxx-hf.spcae'
const method = '/infer'
const hf_token = 'xxx'
const prompt = 'your prompt'
const width = 512
const height = 512


const client = await Client.connect(endpoint, { hf_token: hf_token })

const submission = await client.submit(method, {
  prompt: prompt,
  seed: 0,
  width,
  height,
  randomize_seed: true,
}, undefined, undefined, true)

let result
for await (const msg of submission) {
  if (msg.type === 'data') {
    result = msg
    break
  }

  if (msg.type === 'status' && msg.stage !== 'error') {
    const status = msg.progress_data?.map(
      item => `${item.desc || item.unit}: ${item.index}/${item.length}`
    ).join('\n') || msg.stage || ''

    env.updateStatus(status)
  }
}

const url = result?.data?.[0]?.[0]?. image?.url

if (!url) {
  throw new Error(JSON.stringify(result))
}

return { url, method: 'GET' }
```


### 参考：
[gradio js sdk](https://www.gradio.app/docs/js-client)
[gradio guides](https://www.gradio.app/guides/getting-started-with-the-js-client)
