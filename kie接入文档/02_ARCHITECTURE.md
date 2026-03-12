# 02_ARCHITECTURE

## 总体分层

### 前端层（React Flow UI）
负责：

- 展示节点
- 编辑参数
- 手动连线
- 手动执行
- 展示运行状态
- 展示生成结果
- 发请求给你自己的后端

### 编排层（Workflow / Orchestrator）
负责：

- OpenClaw 自动生成节点图
- 生成 `FlowPatch`
- 校验节点类型、参数、连接规则
- 决定某节点应该调用哪个 KIE family
- 决定是 callback 主导还是 polling 主导

### 服务层（KIE Adapter）
负责：

- 按模型家族组装 KIE 请求
- 发起任务
- 保存 `taskId`
- 解析回调
- 查询任务详情
- 归一化结果

### 持久化层
负责：

- workflow
- node run records
- task mapping
- local file metadata
- latest result snapshot

## 推荐目录

```txt
src/
  features/
    flow/
      components/
      hooks/
      store/
      schema/
    kie/
      registry/
      normalizers/
      dto/
  services/
    api/
    workflow/
server/
  routes/
  kie/
  webhooks/
  storage/
```

## 数据主线

1. 用户手动创建节点 或 OpenClaw 生成节点
2. 用户手动连线 或 OpenClaw 输出 `FlowPatch.edges`
3. 前端提交“运行节点”到后端
4. 后端根据 node type + selected model family 选择 KIE adapter
5. 后端调用 KIE 创建任务，得到 `taskId`
6. 后端把 `taskId` 写入本地 `node_run`
7. KIE 通过 webhook 回调，或后端主动轮询
8. 后端查询最终结果并归一化
9. 如果结果是图片 / 视频 / 音频，后端下载保存到本地
10. 前端刷新节点状态并显示最新媒体

## 任务实体建议

### WorkflowNode
- id
- type
- position
- config
- runtime
- latestResult
- latestTask

### NodeRun
- runId
- nodeId
- provider = "kie"
- family
- modelKey
- taskId
- submitPayload
- status
- error
- normalizedResult
- savedFiles

### SavedMedia
- mediaId
- kind
- sourceUrl
- localPath
- mimeType
- size
- createdAt
