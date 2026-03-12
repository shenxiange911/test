# 严格实现规则（必须喂给 OpenClaw）

## 1. 语言与类型
- 必须使用 TypeScript
- `strict: true`
- 禁止 `any`
- 所有 provider payload / result 都必须有类型
- 所有 node data 都必须通过 schema 校验

## 2. React Flow 规则
- 必须使用 `@xyflow/react`
- 必须使用受控模式
- 父容器必须有明确高度
- 所有自定义节点必须通过 `nodeTypes` 注册
- 所有连接点必须使用 `Handle`
- 只允许通过统一 state 更新节点

## 3. 服务端规则
- KIE Key 只允许存在于服务端
- 回调验签必须启用
- 任何下载保存都只能在服务端做永久持久化
- 所有 KIE 响应必须先 normalize 再返给前端

## 4. 结构规则
目录建议：

```txt
src/
  features/flow/
    flow.store.ts
    flow.types.ts
    flow.schema.ts
    connection.rules.ts
  features/kie/
    kie.types.ts
    kie.schemas.ts
    kie.client.ts
    kie.normalizer.ts
    kie.model-map.ts
  components/nodes/
    TextNode.tsx
    ImageNode.tsx
    VideoNode.tsx
    AudioNode.tsx
    UploadNode.tsx
  server/
    routes/kie.run.ts
    routes/kie.task.ts
    routes/kie.webhook.ts
    services/kie.service.ts
    services/media.persist.ts
```

## 5. OpenClaw 禁止行为
- 禁止在节点组件里直接 `fetch("https://api.kie.ai/...")`
- 禁止绕过 schema 直接拼 payload
- 禁止把上传逻辑写死在 UI
- 禁止不区分 Market / 4o / Veo / Runway / Suno 的 response shape
- 禁止把 callback 当成可信请求而不验签
- 禁止把临时 URL 直接落永久数据库，不做持久化说明

## 6. 必须实现的能力
- 创建任务
- 查询任务
- callback 验签
- 上传文件
- 统一 normalize
- 节点结果显示
- 下载按钮
- 本地保存 / 服务端保存
- 自动连线 patch 校验

## 7. 兼容性连接规则
只允许以下边：

- `text -> image`
- `text -> video`
- `text -> audio`
- `upload(image) -> image`
- `upload(image) -> imageEditor`
- `upload(image) -> video`
- `upload(video) -> video`
- `upload(audio) -> audio`
- `image -> video`
- `image -> imageEditor`

不在白名单里的连接必须拒绝。

## 8. 任务执行策略
- 所有节点运行逻辑走统一 `runNode()`
- 根据 `modelKey` 路由到不同 KIE provider adapter
- 所有 adapter 返回统一 `SubmitTaskResult`
- 所有结果查询返回统一 `NormalizedKieResult`

## 9. 验收标准
- lint 通过
- typecheck 通过
- 断网 / KIE 报错时 UI 能进入 error 状态
- callback 成功后节点 UI 自动刷新
- 页面刷新后仍可恢复已有结果
