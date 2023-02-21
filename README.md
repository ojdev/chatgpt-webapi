# chatgpt-webapi
使用[acheong08/ChatGPT](https://github.com/acheong08/ChatGPT)进行二次开发webapi接口

## 编译

### 直接运行

安装依赖`pip install --upgrade pip && pip install flask gevent revChatGPT`

修改 chatgpt-webapi.py 中的`access_token =` 值为[https://chat.openai.com/api/auth/session](https://chat.openai.com/api/auth/session)获取到access_token，

**注意：[acheong08/ChatGPT](https://github.com/acheong08/ChatGPT)包中使用用户名密码登录会有status code错误，原因未知。所以采用access_token，目前发现已经4天了，还没有过期。

保存后直接使用 `python3 chatgpt-webapi.py` 运行,默认端口80

### 本地docker

`docker build -t chatgpt-webapi .`

docker-compose.yml
```
version: "3"
services:
  chatgpt-webapi:
    image: chatgpt-webapi:latest
    container_name: chatgpt-webapi
    environment:
      - access_token=不要带双引号
      restart: always
```

### 现有镜像

docker-compose.yml
```
version: "3"
services:
  chatgpt-webapi:
    image: luacloud/chatgpt-webapi:latest
    container_name: chatgpt-webapi
    environment:
      - access_token=不要带双引号
      restart: always
```

#### nginx转发

```conf
server {

    server_name 域名;

    listen 443 ssl; 

    ssl_certificate /etc/letsencrypt/live/域名/fullchain.pem; 
    ssl_certificate_key /etc/letsencrypt/live/域名/privkey.pem; 
    error_page 497  https://$host$request_uri;
    location / {
        proxy_pass       http://chatgpt-webapi;
        proxy_redirect             off;
        proxy_http_version         1.1;
        proxy_set_header Upgrade   $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host      $http_host;
    }
}
```

## 使用方法

### 首次对话 [POST] https://域名/ask'

#### PostBody
```json
{
    "msg": "你的名字"
}
```

#### Result

```json
{
    "code": 0,
    "data": {
        "message": "我的名字是ChatGPT。",
        "parent_id": "24523875-a668-4246-a6b2-e70e1a3d69fb",
        "conversation_id": "6d91e084-8e2c-4bea-a96f-879f5d38f801"
    }
}
```

### 后续对话 [POST] https://域名/ask'

带上首次对话返回的`parent_id`与`conversation_id`

#### PostBody
```json
{
    "parent_id": "24523875-a668-4246-a6b2-e70e1a3d69fb",
    "conversation_id": "6d91e084-8e2c-4bea-a96f-879f5d38f801",
    "msg": "你的名字"
}
```

### 删除对话 [POST] https://域名/conversation/{conversation_id}/delete

- conversation_id 首次对话返回的conversation_id

#### PostBody
```json
{
}
```


### 获取历史记录 [GET] https://域名/conversation/{conversation_id}

- conversation_id 首次对话返回的conversation_id


### 后续扩展

参考 [https://github.com/acheong08/ChatGPT/wiki/V1](https://github.com/acheong08/ChatGPT/wiki/V1)自行添加
