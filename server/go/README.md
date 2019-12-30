# CoinSummer LN GO SDK

## 获取支付列表

```go
Request("GET", "/v1/payment", map[string]string{
    page: 1,
    limit: 10
})
```

## 查询支付详情

```go
Request("GET", "/v1/payment/payment_id", map[string]string{})
```

## 创建支付订单

```go
Request("POST", "/v1/payment", map[string]string{
    amount: 1024,
    expiry: 1800
})
```

## 提交提现申请

```go
Request("POST", "/v1/withdraw", map[string]string{
    invoice: 'xxxxxxxx'
})
```

## 获取提现申请信息

```go
Request("GET", "/v1/withdraw/withdraw_id/", map[string]string{})
```
