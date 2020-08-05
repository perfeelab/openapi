## PerFee卖家用户授权介绍

如果您的应用和PerFee平台对接时需要获取卖家用户数据（如商品、订单等），为保证卖家用户数据的安全，您的应用需要取得用户的授权，即获取访问卖家用户数据的授权令牌 Access Token。这种情况下，您的应用需要引导卖家用户完成使用PerFee帐号录授权”的流程。该流程采用国际通用的OAuth2.0标准协议作为用户身份验证与授权协议。目前PerFee OAuth2.0服务支持采用授模式（authorization code）获取Access Token（授权令牌），详见如下说明。


### 1. 请求入口地址

#### 1) 获取授权码（code）

* 测试环境：[https://openapi-dev.perfee.com/oauth/authorize](https://openapi-dev.perfee.com/oauth/authorize)
* 正式环境：[https://openapi.perfee.com/oauth/authorize](https://openapi.perfee.com/oauth/authorize)

#### 2) 获取访问令牌（access_token）

* 测试环境：[https://openapi-dev.perfee.com/oauth/token](https://openapi-dev.perfee.com/oauth/token)
* 正式环境：[https://openapi.perfee.com/oauth/token](https://openapi.perfee.com/oauth/token)

### 2. 授权操作步骤

#### 1) 拼接授权url

拼接用户授权需访问的url ，示例及参数说明如下：

* 示例:

```
https://openapi-dev.perfee.com/oauth/authorize?response_type=code&client_id=client_id_test&redirect_uri=http://www.oauth.net&state=1212&scope=seller
```
* 参数说明

| 参数名称 | 是否必须 | 示例 | 备注 |
| --- | --- | --- | --- |
| client_id | 是 | client_id_test | 创建应用时获得。 |
| redirect_uri | 是 | http://www.oauth.net | redirect_uri指的是应用发起请求时，所传的回调地址是，在用户授权后应用会跳转至redirect_uri。要求与应用注册时填写的回调地址域名一致。 |
| state | 是 | 1212 | 随机字符串，传入值与返回值保持一致。 |
| scope | 是 | seller | 申请权限范围，可选值：1、seller。 |
| response_type | 是 | code | 授权类型，可选值：1、code。 |

#### 2) 引导用户登录授权

* 引导卖家用户通过浏览器访问以上授权url，如果卖家用户未处于登录状态，将弹出登录页面。卖家用户输入账号、密码登录，即可进入授权页面。

#### 3) 获取code

* 卖家用户进入授权页面后，选择需要授权的店铺store, 点击确认授权后，PerFee授权服务将会把授权码code返回到回调地址上。应用可以获取并使用该code去换取access_token（注意code的有效期很短）
* 若用户未点授权而是点了“取消”按钮，则返回如下结果，其中error为错误码，error_description为错误描述。

#### 4) 换取access_token

* 换取access_token请求参数说明

| 名称 | 是否必须 | 示例 | 备注 |
| --- | --- | --- | --- |
| client_id | 是 | client_id_test | 创建应用时获得。 |
| client_secret | 是 | client_secret_test | 创建应用时获得。 |
| redirect_uri | 是 | http://www.oauth.net | redirect_uri指的是应用发起请求时，所传的回调地址参数，在用户授权后应用会跳转至redirect_uri。要求与应用注册时填写的回调地址域名一致。 |
| grant_type | 是 | authorization_code | 授权类型 ，可选值为authorization_code、refresh_token。当grant_type为authorization_code，应带上可选参数code；当grant_type为refresh_token时，应带上可选参数refresh_token。	 |
| code | 否 |  | 上个步骤授权回调获取的code。 |
| refresh_token | 否 |  | 使用authorization_code方式授权时返回的refresh_token。 |

* code换取access_token示例
```
curl -i -d "code=6e0e89bed6987e9e2b540b42e91f5e77&grant_type=authorization_code&client_id=client_id_test&client_secret=client_secret_test&redirect_uri=http://www.oauth.net" https://openapi-dev.perfee.com/oauth/token
```

* code换取access_token返回值示例
```
{
    "token_type": "bearer",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZWxsZXJfaWQiOjEsInN0b3JlX2lkIjoxLCJyZWdpb25faWRfb2Zfc2VsbGVyIjoyLCJyZWdpb25faWRfb2Zfc3RvcmUiOjEsImNsaWVudF9pZCI6Imhza3Rlc3QiLCJyZWRpcmVjdF91cmkiOiJodHRwOi8vMTI3LjAuMC4xOjUwMDAvcGVyZmVlL2F1dGhvcml6ZSIsImV4cCI6MTU5NjYyMDI5Nn0.VaDy0gfGfTpU3x_25wwSjQtj5KHiw4G8uvcz28K4KPo",
    "expires_in": 7200,
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZWxsZXJfaWQiOjEsInN0b3JlX2lkIjoxLCJyZWdpb25faWRfb2Zfc2VsbGVyIjoyLCJyZWdpb25faWRfb2Zfc3RvcmUiOjEsImNsaWVudF9pZCI6Imhza3Rlc3QiLCJyZWRpcmVjdF91cmkiOiJodHRwOi8vMTI3LjAuMC4xOjUwMDAvcGVyZmVlL2F1dGhvcml6ZSIsImV4cCI6MTYyNzcxNzA5Nn0.XOdwFl7MOHqtRU0CQkQCwXio7tD3rAweWVh2jt6hotw",
    "refresh_token_expires_in": 31104000
}
```
* refresh_token换取access_token示例
```
curl -i -d "grant_type=refresh_token&client_id=client_id_test&client_secret=client_id_test&redirect_uri=http://127.0.0.1:5000/perfee/authorize&refresh_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZWxsZXJfaWQiOjEsInN0b3JlX2lkIjoxLCJyZWdpb25faWRfb2Zfc2VsbGVyIjoyLCJyZWdpb25faWRfb2Zfc3RvcmUiOjEsImNsaWVudF9pZCI6Imhza3Rlc3QiLCJyZWRpcmVjdF91cmkiOiJodHRwOi8vMTI3LjAuMC4xOjUwMDAvcGVyZmVlL2F1dGhvcml6ZSIsImV4cCI6MTYyNzcxNzA5Nn0.XOdwFl7MOHqtRU0CQkQCwXio7tD3rAweWVh2jt6hotw" https://openapi-dev.perfee.com/oauth/token
```

* refresh_token换取access_token返回值示例
```
{
    "token_type": "bearer",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZWxsZXJfaWQiOjEsInN0b3JlX2lkIjoxLCJyZWdpb25faWRfb2Zfc2VsbGVyIjoyLCJyZWdpb25faWRfb2Zfc3RvcmUiOjEsImNsaWVudF9pZCI6Imhza3Rlc3QiLCJyZWRpcmVjdF91cmkiOiJodHRwOi8vMTI3LjAuMC4xOjUwMDAvcGVyZmVlL2F1dGhvcml6ZSIsImV4cCI6MTU5NjYyMDI5Nn0.VaDy0gfGfTpU3x_25wwSjQtj5KHiw4G8uvcz28K4KPo",
    "expires_in": 7200
}
```

# Open API
Perfee Open API 开放平台是为商家、供应商等相关合作伙伴提供的一站式应用程序接口和数据解决方案，API 采用 RESTful 风格设计实现，并遵守被业界广泛应用的 OAuth 2.0 安全认证规范。

## 使用指南
API 定义技术文档: [https://apidocs.perfee.com](https://apidocs.perfee.com)

请使用带有公司域名的电子邮箱申请注册帐号，并致信 openapi@perfee.com 联系开通相关权限并获得相应的技术资料（APP_ID、APP_SECRET等），信函内容请至少包含以下必要项目：
>
> 注册邮箱：（之前使用的公司域名邮箱，如：wangjg@abc.com）  
> 公司名称：（如：ABC电子商务有限公司）  
> 联络人：（如：王建国）  
> 职位 / 称谓：（如：产品总监）  
> 手机 / 电话：（如：+86 18912345678）  

## 示例代码
在正式使用前，请务必将代码中的 appId 与 appSecret 替换成自己的真实数据！
### [cURL (shell)](samples/shell/get_orders.sh)
```shell
curl -v -X POST https://openapi.perfee.com/access-token \
    -H "Content-Type: application/json" \
    -d '{
        "appId": "your_app_id",
        "appSecret": "your_app_secret",
        "storeId": your_store_id
    }'

curl -v -G https://openapi.perfee.com/sale-orders \
    -H "AccessToken: your_access_token" \
    -d "regionId=1&status=0&page=1&limit=10" \
    -d "startTimestamp=1576771200&endTimestamp=1575907200" \
    -d "payMethod=1&payStatus=1"
```
### [python3](samples/shell/get_orders.py)
```python3
from requests import request

# 获取token
response = request(
    "post", "https://openapi-dev.perfee.com/access-token",
    headers={'Content-type': 'application/json'},
    data='{"appId": "your_app_id", "appSecret": "your_app_secret", "storeId": you_storeId}'
)
resp_json = response.json()
token = resp_json["data"]["token"]
refresh_token = resp_json["data"]["refreshToken"]
print(token)


# 使用RefreshToken获取token
response = request(
    "post", "https://openapi-dev.perfee.com/token-refresh",
    headers={'RefreshToken': refresh_token}
)
resp_json = response.json()
token = resp_json["data"]["token"]
print(token)


# 获取单个order信息
response = request(
    "get", "https://openapi-dev.perfee.com/sale-orders/123456",
    headers={'AccessToken': token}
)
resp_json = response.json()
print(resp_json)


# 获取订单列表
response = request(
    "get", "https://openapi-dev.perfee.com/sale-orders",
    headers={'AccessToken': token},
    params={
        "regionId": 1, "status": 0, "page": 1, "limit": 20,
        "startTimestamp": 1570000000, "endTimestamp": 1570432000
    }
)
resp_json = response.json()
print(resp_json)

```
