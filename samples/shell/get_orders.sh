#!/bin/sh

curl -v -X POST https://openapi.perfee.com/access_token \
    -H "Content-Type: application/json" \
    -d '{
        "appId": "your_app_id",
        "appSecret": "your_app_secret",
        "storeId": your_store_id
    }'

curl -v -G https://openapi.perfee.com/orders \
    -H "AccessToken: your_access_token" \
    -d "regionId=1&status=0&page=1&limit=10" \
    -d "startTimestamp=1576771200&endTimestamp=1575907200" \
    -d "payMethod=1&payStatus=1"
