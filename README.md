# websocket-demo
 【全栈】Websocket 在 TB 使用的 demo 项目

## 模板使用文档
本 Repo 按照 TeaBreak DjangoTemplate 和 TeaBreak React 常用设置来创建

前端快速发布：
```
    yarn build
    scp -r ./react/build <user>@<host>:<path-to-folder>/react/
```

后端应急一秒部署（非紧急情况请使用git进行同步）
```
    # Mac/Linux：
    rsync -aP  --exclude-from=exclude.list ./django <user>@<host>:<path-to-folder>/
    # Windows
    scp -r ./django <user>@<host>:<path-to-folder>/django/
```