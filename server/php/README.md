# CoinSummer LN PHP SDK

## 获取支付列表

```php
request('GET', '/v1/payment/');
```

## 查询支付详情

```php
request('GET', '/v1/payment/'.$payment_id);
```

## 创建支付订单

```php
request('POST', '/v1/payment/', [
    'amount' => 1024,
    'expiry' => 1800
]);
```

## 提交提现申请

```php
request('POST', '/v1/payment/', [
    'invoice' => 'xxxxxx'
]);
```

## 获取提现申请信息

```php
request('GET', '/v1/payment/'.$withdraw_id);
```
