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
