# CoinSummer LN Python SDK

## 获取支付列表

```python
request(
    "GET", 
    "/open/v1/payment", 
    {
        page: 1,
        limit: 10
    },
    api_key, api_secret, host
)
```

## 查询支付详情

```python
request(
    "POST", 
    "/open/v1/payment/" + payment_id, 
    {},
    api_key, api_secret, host
)
```

## 创建支付订单

```python
request(
    "POST", 
    "/open/v1/payment", 
    {
        amount: 1024,
        expiry: 1800
    },
    api_key, api_secret, host
)
```

## 提交提现申请

```python
request(
    "POST", 
    "/open/v1/withdraw/", 
    {
        invoice: "xxxxxxxx"
    },
    api_key, api_secret, host
)
```

## 获取提现申请信息

```python
request(
    "GET",
    "/open/v1/withdraw/withdraw_id",
    {},
    api_key, api_secret, host
)
```
