#!/bin/sh

curl -v -G https://openapi-test.otoku-world.com/sale-orders \
    -H "Authorization: Bearer your_access_token" \
    -d "regionId=1&status=0&page=1&limit=10" \
    -d "startTimestamp=1576771200&endTimestamp=1575907200" \
    -d "payMethod=1&payStatus=1"
