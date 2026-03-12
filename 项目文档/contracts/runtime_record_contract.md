# Runtime Record Contract

## 功能定位
Runtime Record 负责持久化节点执行结果的元信息，保存任务 ID、模型、状态、结果 URLs 等关键信息到 JSON 文件。

## Skill/Tool 绑定

### skillName
`runtime-record-writer` / 内部工具

### toolName
- 当前阶段：`fetch` API（POST 到本地/远端服务）
- 文件系统：直接写入 JSON

### executionMode
`internal` - 异步写入，不阻塞主流程

## 输入 Schema

### RuntimeRecordPayload
```typescript
{
  kind: 'image' | 'video' | 'audio' | 'text';
  nodeId: string;
  taskId?: string;
  model?: string;
  status: 'success' | 'error' | 'pending';
  resultUrls: string[];
  createTime: string;       // ISO 8601 格式
  compiledPromptHash?: string;
  promptSnapshot?: {
    compiledPrompt: string;
    compiledPromptHash: string;
    compiledAt: string;
  };
}
```

## 输出 Schema

### 成功
```typescript
{
  success: true;
  recordPath: string;       // 保存的文件路径
}
```

### 失败
```typescript
{
  success: false;
  error: string;
}
```

## 保存路径规则

### 目录结构
```
titanLX/项目文档/runtime_records/
  ├── image/
  │   ├── image-01_20260310_190000.json
  │   └── image-02_20260310_190100.json
  ├── video/
  ├── audio/
  └── text/
```

### 文件命名
`{nodeId}_{timestamp}.json`

示例：`image-01_20260310_190523.json`

## JSON 格式

### 最小格式
```json
{
  "nodeId": "image-01",
  "taskId": "task_abc123",
  "model": "nano-banana-2",
  "status": "success",
  "resultUrls": [
    "https://kie.ai/results/xxx.jpg"
  ],
  "createTime": "2026-03-10T19:05:23+08:00"
}
```

### 完整格式
```json
{
  "nodeId": "image-01",
  "taskId": "task_abc123",
  "model": "nano-banana-2",
  "status": "success",
  "resultUrls": [
    "https://kie.ai/results/xxx.jpg",
    "https://kie.ai/results/yyy.jpg"
  ],
  "createTime": "2026-03-10T19:05:23+08:00",
  "compiledPromptHash": "hash:7a3f2b1c",
  "promptSnapshot": {
    "compiledPrompt": "A professional product photo...",
    "compiledPromptHash": "hash:7a3f2b1c",
    "compiledAt": "2026-03-10T19:05:20+08:00"
  }
}
```

## Writeback 目标

### 文件系统
- 保存到 `runtime_records/{kind}/` 目录
- 每次执行生成新文件（不覆盖）

### 节点状态（可选）
- 可选：更新节点的 `runtime.recordPath` 字段

## 前端展示要求

### 不直接展示
Runtime Record 是后台持久化，前端不直接展示文件内容。

### 间接展示
- 节点的 `runtime.taskId` 来自 record
- 节点的 `result.resultUrls` 来自 record

## 操作入口

### 自动触发
- 图片生成成功后
- 视频生成成功后
- 任何需要持久化结果的操作后

### 手动触发
- 不支持手动触发

### Skill 调用
```typescript
await writeRuntimeRecord({
  kind: 'image',
  nodeId: 'image-01',
  taskId: 'task_xxx',
  model: 'nano-banana-2',
  status: 'success',
  resultUrls: ['https://...'],
  createTime: new Date().toISOString(),
})
```

## API Contract

### Endpoint
`POST /v1/runtime/records/{kind}`

### Request Body
```json
{
  "nodeId": "image-01",
  "taskId": "task_xxx",
  "model": "nano-banana-2",
  "status": "success",
  "resultUrls": ["https://..."],
  "createTime": "2026-03-10T19:00:00+08:00"
}
```

### Response
```json
{
  "success": true,
  "recordPath": "runtime_records/image/image-01_20260310_190000.json"
}
```

## 依赖的共享模块
- `runtimeRecords.ts` - 核心实现
- `actions/imageGenerationActions.ts` - 调用写入

## 当前实现状态（以 `09_实现进度追踪.md` 为准）
- ✅ Runtime Record 的目标、目录结构与最小 JSON 格式已经定义清楚
- `IN_PROGRESS` 代码层已进入 runtime records 主线，但仍不能写成“持久化已闭环”
- `TODO` `generateImageWithAction` / 统一动作层对 `writeRuntimeRecord` 的真实接入仍需补齐
- `TODO` 真实文件写入、错误处理、最小可观测性仍需补齐
- `TODO` 若走服务端 API，则对应 endpoint 仍属于目标态而非既成事实

## 下一步
1. 在 `generateImageWithAction` 与后续统一动作层中真实接入 `writeRuntimeRecord`
2. 先落最小可用本地文件写入，再决定是否补服务端 API
3. 补充错误处理、记录路径写回与最小调试日志
