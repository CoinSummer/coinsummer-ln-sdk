# CoinSummer LN Java SDK

## 获取支付列表

```java
Map<String, Object> params = new HashMap<String, Object>();
params.put("page", 1);
params.put("limit", 10);
String res = request("GET", "/v1/payment", params);
```

## 查询支付详情

```java
String payment_id = "unique_123456"
Map<String, Object> params = new HashMap<String, Object>();
String res = request("GET", "/v1/payment" + payment_id, params);
```

## 创建支付订单

```java
Map<String, Object> params = new HashMap<String, Object>();
params.put("amount", 1024);
params.put("expiry", 1800);
String res = request("POST", "/v1/payment", params);
```

## 提交提现申请

```java
Map<String, Object> params = new HashMap<String, Object>();
params.put("invoice", "xxxxxx");
String res = request("POST", "/v1/withdraw", params);
```

## 获取提现申请信息

```java
String withdraw_id = "unique_123456"
Map<String, Object> params = new HashMap<String, Object>();
String res = request("GET", "/v1/withdraw" + withdraw_id, params);
```
