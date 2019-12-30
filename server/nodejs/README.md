# CoinSummer LN Node.js SDK

## 获取支付列表

```js
coinsummerLN('GET', '/v1/payment', 
        {
            page: 1,
            limit: 10
        },
        api_key, api_secret, host
    ).then(res => {
        res.json().then((data)=>{
            console.log(JSON.stringify(data, null, 4))
        })
    }).catch(err => {
        console.log(err)
    })
```

## 查询支付详情

```js
coinsummerLN('GET', `/v1/payment/${paymentId}`, {}, api_key, api_secret, host)
    .then(res => {
        res.json().then((data)=>{
            console.log(JSON.stringify(data, null, 4))
        })
    }).catch(err => {
        console.log(err)
    })
```

## 创建支付订单

```js
coinsummerLN('POST', '/v1/payment', 
        {
            amount: 1024,
            expiry: 1800
        },
        api_key, api_secret, host
    ).then(res => {
        res.json().then((data)=>{
            console.log(JSON.stringify(data, null, 4))
        })
    }).catch(err => {
        console.log(err)
    })
```

## 提交提现申请

```js
coinsummerLN('POST', '/v1/withdraw', 
        {
            invoice: 'xxxxxxxx'
        },
        api_key, api_secret, host
    ).then(res => {
        res.json().then((data)=>{
            console.log(JSON.stringify(data, null, 4))
        })
    }).catch(err => {
        console.log(err)
    })
```

## 获取提现申请信息

```js
coinsummerLN('GET', '/v1/withdraw', 
        {
            withdrawId: 'unique_123456'
        }, 
        api_key, api_secret, host
    ).then(res => {
        res.json().then((data)=>{
            console.log(JSON.stringify(data, null, 4))
        })
    }).catch(err => {
        console.log(err)
    })
```
