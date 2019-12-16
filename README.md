# Open API
Perfee Open API 开放平台是为商家、供应商等相关合作伙伴提供的一站式应用程序接口和数据解决方案，API 采用 RESTful 风格设计实现，并遵守被业界广泛应用的 OAuth 2.0 安全认证规范。

## 使用指南
API 定义技术文档: [https://apidocs.perfee.com](https://apidocs.perfee.com)

请使用带有公司域名的电子邮箱申请注册帐号，并致信 openapi@perfee.com 联系开通相关权限并获得相应的技术资料（APP_KEY、APP_SECRET等），信函内容请至少包含以下必要项目：
>
> 注册邮箱：（之前使用的公司域名邮箱，如：wangjg@abc.com）  
> 公司名称：（如：ABC电子商务有限公司）  
> 联络人：（如：王建国）  
> 职位 / 称谓：（如：产品总监）  
> 手机 / 电话：（如：+86 18912345678）  

## 示例代码
在正式使用前，请务必将代码中的 app_key 与 app_secret 替换成自己的真实数据！
### cURL
```shell
curl -X POST https://openapi.perfee.com/access_token \
    -H "Content-Type: application/json" \
    -d '{
        "appId": "r9g2f6vk",
        "appSecret": "7167bcc64be6e5d8b6a028f62deb3c3923bb3861",
        "storeId": 1
    }'
```
