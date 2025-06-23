---
title: paypal支付
date: 2025-01-15 18:29:28
author: Navyum
tags: 
 - paypal支付
categories: 
 - 编程
 - 技术方案

---
## paypal支付

### 流程图
[Drawio](../paypal.drawio){link-type="drawio"}

1. 用户选择点击"信用卡支付"
2. PC调用 `/api/pay/order/create/card?payway=paypal`创建paypal信用卡订单
3. 用户填写信用卡信息，一般会包含：卡号、有效期，CVV，以及姓名、地址、城市区域码等（第三方sdk）
4. PC提交信用卡信息、order_id给paypal，paypal返回对应状态
5. 上述成功后，PC捕获支付capture_order，调用 `/api/pay/order/capture/card?payway=paypal`。pending状态：可以loading并提示等待片刻
6. 同时间，paypal可能通知服务端扣款完成，此处服务端确保订单状态幂等，避免多次扣款。
7. PC轮训结果订单状态，调用 `/api/pay/order/query?payway=paypal`
    1. 查询到订单支付成功，跳转对应成果落地页
    2. 查询到订单支付失败，跳转失败落地页
8. 支付完成


### 高级信用卡支付（调研）：
* 问题：card-fields实际使用的是confirm-payment-source进行付款人信息更新，且内容明文
  ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/e379d59bd69478511ea8803d0ac5aab3.png)

* 样例代码实现：
    ```html
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Checkout Page</title>
        </head>
        <body>
            <div id="checkout-form">
            <div id="card-name-field-container"></div>
            <div id="card-number-field-container"></div>
            <div id="card-expiry-field-container"></div>
            <div id="card-cvv-field-container"></div>
            <button id="multi-card-field-button" type="button">Pay now with Card Fields</button>
            </div>
        </body>
        <script src="https://www.paypal.com/sdk/js?client-id=AWrnnAVEr4D51bgZfP77TM4THK1f-Y4QMmqRtuqHswVpfpbG4oVolewqZiPHocOcDT3P3HaxGQ8Pxs5m&components=card-fields"></script>
        <script>
        // Custom styles object (optional)
            const styleObject = {
                input: {
                    "font-size": "16 px",
                    "font-family": "monospace",
                    "font-weight": "lighter",
                    color: "blue",
                },
                ".invalid": {
                color: "purple",
                },
                ":hover": {
                    color: "orange",
                },
                ".purple": {
                    color: "purple",
                },
            };
            // Create the card fields component and define callbacks

            const token='xxx'
            const cardField = paypal.CardFields({
                style: styleObject,
                createOrder: function (data, actions) {
                    return fetch(`https://mindshow.fun/api/pay/order/create/card?payway=paypal&product_id=ONE_MONTH&token=${token}&env=test`, {
                    method: "get",
                    })
                    .then((res) => {
                        return res.json();
                    })
                    .then((orderData) => {
                        orderID = orderData.data.oid; // Store oid
                        return orderData.data.trade_no; // Return trade_no
                    });
                },
                onApprove: function (data, actions) {
                    const tradeNo = data; // Get trade_no from createOrder
                    return fetch(`https://mindshow.fun/api/pay/order/capture/card?payway=paypal&oid=${orderID}&token=${token}&env=test&trade_no=${tradeNo}`, {
                    method: "get",
                    })
                    .then((res) => {
                        return res.json();
                    })
                    .then((orderData) => {
                        // Redirect to success page
                    });
                },
                inputEvents: {
                    onChange: function (data) {
                        // Handle a change event in any of the fields
                    },
                    onFocus: function(data) {
                        // Handle a focus event in any of the fields
                    },
                    onBlur: function(data) {
                        // Handle a blur event in any of the fields
                    },
                    onInputSubmitRequest: function(data) {
                        // Handle an attempt to submit the entire card form
                        // while focusing any of the fields
                    }
                },
            });
            // Define the container for each field and the submit button
            const cardNameContainer = document.getElementById("card-name-field-container"); // Optional field
            const cardNumberContainer = document.getElementById("card-number-field-container");
            const cardCvvContainer = document.getElementById("card-cvv-field-container");
            const cardExpiryContainer = document.getElementById("card-expiry-field-container");
            const multiCardFieldButton = document.getElementById("multi-card-field-button");
            // Render each field after checking for eligibility
            if (cardField.isEligible()) {
                const nameField = cardField.NameField();
                nameField.render(cardNameContainer);
                const numberField = cardField.NumberField();
                numberField.render(cardNumberContainer);
                const cvvField = cardField.CVVField();
                cvvField.render(cardCvvContainer);
                const expiryField = cardField.ExpiryField();
                expiryField.render(cardExpiryContainer);
                // Add click listener to the submit button and call the submit function on the CardField component
                multiCardFieldButton.addEventListener("click", () => {
                    cardField
                    .submit()
                    .then(() => {
                        // Handle a successful payment
                    })
                    .catch((err) => {
                        // Handle an unsuccessful payment
                    });
                });
            }
        </script>
    </html>
    ```

### 标准信用卡支付（确定方案）：
* JS SDK components 选择为 `Buttons`
* 参考：[https://developer.paypal.com/sdk/js/reference/#buttons](https://developer.paypal.com/sdk/js/reference/#buttons)
* 存在的问题：
    * 跳转页用户待填写内容过多
      ![Img](https://raw.staticdn.net/Navyum/imgbed/pic/IMG/b55ddffd98683307a4e70f5dfd4a4d22.png)

* 样例代码：
  ```html
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>PayPal JS SDK Standard Integration</title>
        </head>
        <body>
            <div id="paypal-button-container"></div>
            <p id="result-message"></p>

            
            <!-- Initialize the JS-SDK -->
            <script
                src="https://www.paypal.com/sdk/js?client-id=AVjJgDoTZYEE2ARMk21PTTYVhBFZX3eawV8J-PqdRW1pIBFeAPuvDbgGkOo0yVG0KNc-3AEO3l6BE-bV&components=buttons&enable-funding=card"
                data-sdk-integration-source="developer-studio"
            ></script>
            <script>
                var CARD_FUNDING_SOURCES = [
                    paypal.FUNDING.CARD
                ];

                var token = "xxx" //4A4A677A2C2E442DB43901DE9EB18B64

                // Loop over each funding source / payment method
                CARD_FUNDING_SOURCES.forEach(function (fundingSource) {
                    // Initialize the buttons
                    var button = paypal.Buttons({
                        fundingSource: fundingSource,
                        expandCardForm:true,

                        createOrder: function (data, actions) {
                            return fetch(`https://mindshow.fun/api/pay/order/create/card?payway=paypal&product_id=ONE_MONTH&token=${token}&env=prod`, {
                                method: "get",
                            })
                            .then((res) => {
                                console.log(res)
                                return res.json();
                            })
                            .then((orderData) => {
                                orderID = orderData.data.oid; // Store oid
                                return orderData.data.trade_no; // Return trade_no
                            });
                        },

                        // Call your server to finalize the transaction
                        onApprove: function (data, actions) {
                            console.log(orderID)
                            console.log(data)
                            return fetch(`https://mindshow.fun/api/pay/order/capture/card?payway=paypal&oid=${orderID}&token=${token}&trade_no=${data.trade_no}&env=prod`, {
                                method: "get",
                            })
                            .then(function (res) {
                                return res.json();
                            })
                            .then(function (orderData) {

                                // Successful capture! For demo purposes:
                                console.log('Capture result:', orderData, JSON.stringify(orderData, null, 2));
                                alert('Transaction was successful!');
                            });
                        }
                    });

                    // Check if the button is eligible
                    if (button.isEligible()) {
                        // Render the standalone button for that funding source
                        button.render('#paypal-button-container');
                    }
                });
            </script>
            
        </body>
    </html>
  ``` 

### 接口说明：

#### 1.创建订单
* 请求地址:
    * /api/pay/order/create/card
* 请求方法:
    * GET
* 请求query参数:
    * payway：支付方式
        * 可选值: paypal
    * product_id：购买项id
        * 具体值从购买项列表接口获取
        * e.g. ONE_MONTH
    * env ：调用环境
        * 可选值：prod （生产）、test（测试）
    * token：登录 token

* 接口响应：
    * header   content-type：application/json
* 响应内容：
    * code ：业务错误码
        * 0: 正常, 其他：异常
    * msg：业务错误信息
        * success: 正常
    * data：业务具体数据
        * oid： 商户内部订单号（用于后续查询支付状态）
        * payway：当前选择的支付方式
        * trade_no 支付渠道的订单号，第三方SDK需要用到

* 接口举例：
    * request： https://mindshow.fun/api/pay/order/create/card?payway=paypal&product_id=ONE_MONTH&env=test&token=1
    * reponse： 
      ```json
      {"msg": "success","data": {"oid": "2312021537588946764E299F2EA","payway": "paypal","trade_no":"XXXXXXXX"},"code": 0}
      ```
 
#### 2.确认扣款（onApprove事件触发后回调）
* 请求地址:
    * /api/pay/order/capture/card
* 请求方法:
    * GET
* 请求query参数:
    * payway：支付方式
        * 可选值: paypal
    * oid：商户内部订单号
        * 由create/order 返回
    * trade_no：支付渠道订单号
        * 由create/order 返回
    * env ：调用环境
        * 可选值：prod （生产）、test（测试）
    * token：登录 token

* 接口响应：
    * header   content-type：application/json
* 响应内容：
    * code ：业务错误码
        * 0: 正常, 其他：异常
    * msg：业务错误信息
        * success: 正常
    * data：业务具体数据
        * status： 订单状态
        * oid： 商户内部订单号（用于后续查询支付状态）

* 接口举例：
    * request： https://mindshow.fun/api/pay/order/capture/card?payway=paypal&oid=ooooo&env=test&token=1&trade_no=tttt
    * reponse： 
      ```json
      {"msg": "success","data": {"status": "INPAY","payway": "paypal","oid":"XXXXXXXX"},"code": 0}
      {"msg": "success","data": {"status": "PENDDING","payway": "paypal","oid":"XXXXXXXX"},"code": 0}
      {"msg": "success","data": {"status": "PAID","payway": "paypal","oid":"XXXXXXXX"},"code": 0}
      ```

#### 3.查询订单
* 参考原逻辑： https://www.mubu.com/doc/onoPIKobnL