from requests import request

token = "your_access_token"

# 获取单个order信息
response = request(
    "get", "https://openapi-test.perfee.com/sale-orders/123456",
    headers={'Authorization': 'Bearer %s' % token}
)
resp_json = response.json()
print(resp_json)


# 获取订单列表
response = request(
    "get", "https://openapi-test.perfee.com/sale-orders",
    headers={'Authorization': 'Bearer %s' % token},
    params={
        "regionId": 1, "status": 0, "page": 1, "limit": 20,
        "startTimestamp": 1570000000, "endTimestamp": 1570432000
    }
)
resp_json = response.json()
print(resp_json)
