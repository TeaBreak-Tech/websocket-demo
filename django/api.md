# API


## `user/` 
* uid 用户唯一标识
* token 令牌验证
* expired_date token 过期时间
* is_active 是否通过邮箱验证
* created_time 账号创建时间

### POST:/register/ 继承自[UserSystem](https://github.com/TeaBreak-Tech/UserSystem/blob/master/api.md)
用户注册  
注册成功会刷新token并设置cookie

        response.set_cookie("token", user.token, max_age=SESSION_AGE)
        response.set_cookie("is_login", "true", max_age=SESSION_AGE)
        response.set_cookie("uid", user.uid, max_age=SESSION_AGE)

* ```school_id``` 和 ```email``` 二选一必填，否则无法登陆
* ```password``` 必填且经过哈希加密
* Request(application/json)

        {
            "school_id":"119010115",
            "password":"5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"
        }

* response
    * http响应值为200即成功响应
    ```
    {
        "uid": 7,
        "is_active": false,
        "identity": "S"
    }
    ```
    * ```HttpResponse(content="Not satisfy unique constraint", status=403, reason="N-UNI")``` ```school_id``` 或 ```email``` 已注册

### POST:/login/ 继承自[UserSystem](https://github.com/TeaBreak-Tech/UserSystem/blob/master/api.md)
用户登陆  
登陆成功后会刷新token并设置cookie
```
response.set_cookie("token", user.token, max_age=SESSION_AGE)
response.set_cookie("is_login", "true", max_age=SESSION_AGE)
response.set_cookie("uid", user.uid, max_age=SESSION_AGE)
```
* ```school_id``` 和 ```email``` 二选一必填，否则无法登陆
* ```password``` 必填且经过哈希加密
* Request(application/json)

        {
            "school_id":"119010115",
            "password":"5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"
        }

* response
    * http响应值为200即成功响应
    ```
    {
        "uid": 7,
        "created_time": "2021-01-10T20:38:17.496",
        "is_active": false,
        "identity": "S"
    }
    ```
    * ```HttpResponse(content="Wrong password", status=403, reason="W-PWD")``` 密码错误
    * ```HttpResponse(content="User do not exist", status=404, reason="U-DNE")``` 不存在对应的用户
    * ```HttpResponse(content="No registered email address", status=403,reason="U-INA")``` 未填邮箱

### POST:/email/send/ 继承自[UserSystem](https://github.com/TeaBreak-Tech/UserSystem/blob/master/api.md)
发送验证邮箱的邮件
* ```uid``` 必填
* ```email``` 选填，用于更改邮箱地址
* Request(application/json)

        {
            "uid":7
        }
* Response
    * http响应值为200即成功响应
        ```
        {
            "uid": 7,
            "created_time":"2021-01-10T20:38:17.496",
            "is_active": false,
            "identity": "student"
        }
        ```
    * ```HttpResponse(content="User do not exist", status=404, reason="U-DNE")``` 不存在对应的用户

### POST:/email/code/ 继承自[UserSystem](https://github.com/TeaBreak-Tech/UserSystem/blob/master/api.md)
验证邮箱验证码
* ```uid``` 必填
* ```email_code``` 验证码必填
* Request

        {
            "uid":7，
            "email_code":"764390"
        }
* Response
    * http响应值为200即成功响应
        ```
        {
            "uid": 7,
            "created_time":"2021-01-10T20:38:17.496",
            "is_active": true,
            "identity": "student"
        }
        ```
    * ```HttpResponse(content="Wrong email code", status=403, reason="W-EMC")``` 验证码错误
    * ```HttpResponse(content="User do not exist", status=404, reason="U-DNE")``` 不存在对应的用户

### POST:/read/
用户 ```uid``` 从cookie中获取
标记当前用户已阅读声明
### GET:/read/
* Response
    * 200 用户已阅读声明
    * 403 用户未阅读声明
### GET:/is_login/
根据 ```uid``` 和 ```token``` 判断当前用户是否登录
验证成功后会刷新token并设置cookie

        response.set_cookie("token", user.token, max_age=SESSION_AGE)
        response.set_cookie("is_login", "true", max_age=SESSION_AGE)
        response.set_cookie("uid", user.uid, max_age=SESSION_AGE)
* Response
    * http响应值为200即成功响应
    * ```HttpResponse(content="Token does not match user", status=403, reason="T-DNM")```
    * ```HttpResponse(content="Token expire", status=403, reason="T-EXP")```
    * ```HttpResponse(content="User do not exist", status=404, reason="U-DNE")``` 不存在对应的用户
