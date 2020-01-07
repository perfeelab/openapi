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
