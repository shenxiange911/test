# Image Generate Contract

## 功能定位
Image Node 是 KIE 图片生成节点，负责根据文本描述、上游图片、摄像机参数生成高质量图片。

## Skill/Tool 绑定

### skillName
`multimedia-skill` / `kie-image-generate`

### toolName
- 当前阶段：`exec`（本地代理开发形态）
- 后续目标：服务端 API / `kieAdapter`

### provider
`KIE`

### executionMode
`provider_api`

## 输入 Schema

### 必需字段
```typescript
{
  nodeId: string;           // 节点业务 ID，如 image-01
  prompt: string;           // 生成描述
  model: string;            // KIE 模型名称
  ratio: string;            // 比例，如 16:9
  size: string;             // 尺寸，如 1K
}
```

### 可选字段
```typescript
{
  upstream?: {
    texts?: string[];
    imageUrls?: string[];
  };
  cameraParams?: {
    cameraModel?: string;
    lensModel?: string;
    focalLength?: string;
    aperture?: string;
    iso?: number;
    shutterSpeed?: string;
  };
  customPrompting?: {
    enabled?: boolean;
    userPrompt?: string;
    styleTags?: string[];
    negativePrompt?: string;
    mergeMode?: 'append' | 'prepend' | 'replace_section';
  };
  templateRefs?: Array<{
    templateId: string;
    scope: 'local' | 'type' | 'project';
    mergeMode: 'fill_empty' | 'merge' | 'replace';
  }>;
  params?: Record<string, string | number | boolean>;
  uploads?: UploadedAsset[];
  count?: string;           // 生成数量
}
```

## 输出 Schema

### 成功输出
```typescript
{
  result: {
    kind: 'image';
    previewUrl?: string;    // 预览图 URL
    remoteUrl?: string;     // 远端结果 URL
    resultUrls?: string[];  // 多张图片 URLs
    localPath?: string;     // 本地路径（可选）
  };
  promptSnapshot: {
    compiledPrompt: string;
    compiledPromptHash: string;
    compiledAt: string;
    upstreamSummary: string[];
    templateSnapshot?: Record<string, unknown>;
  };
  runtime: {
    executionMode: 'provider_api';
    provider: 'KIE';
    model: string;
    taskId?: string;
    queuedAt?: string;
    startedAt?: string;
    finishedAt?: string;
    compiledPromptHash?: string;
  };
}
```

### 错误输出
```typescript
{
  runtime: {
    lastError: string;
    finishedAt: string;
  };
  status: 'error';
}
```

## Writeback 目标

### 主要写回：self
- `result.previewUrl` - 预览图
- `result.remoteUrl` - 远端 URL
- `result.resultUrls` - 结果 URLs
- `promptSnapshot` - prompt 追踪
- `runtime` - 运行时元信息
- `status` - 节点状态

### 持久化写回：runtime_records
保存到 `项目文档/runtime_records/image/{nodeId}_{timestamp}.json`：
```json
{
  "nodeId": "image-01",
  "taskId": "task_xxx",
  "model": "nano-banana-2",
  "status": "success",
  "resultUrls": ["https://..."],
  "createTime": "2026-03-10T19:00:00+08:00",
  "compiledPromptHash": "hash:abc123"
}
```

## 前端展示要求

### 节点缩略图
- 显示节点 ID（image-01）
- 显示预览图
- 显示状态图标

### 编辑器区域
- Prompt 输入框
- 模型选择下拉框
- 比例选择
- 尺寸选择
- 数量选择
- 摄像机控制区：
  - 摄像机型号
  - 镜头型号
  - 焦段
  - 光圈
- 上游文本预览
- 上游图片预览
- Compiled Prompt Preview（只读）
- 生成结果预览

### 必须展示的字段
- `prompt` - 原始 prompt
- `model` - 模型名称
- `ratio` - 比例
- `size` - 尺寸
- `cameraModel` / `lensModel` / `focalLength` / `aperture` - 摄像机参数
- `upstream.texts` - 上游文本摘要
- `upstream.imageUrls` - 上游图片列表
- `promptSnapshot.compiledPrompt` - 编译后的 prompt
- `result.previewUrl` - 生成结果
- `runtime.taskId` - 任务 ID
- `status` - 当前状态

## 操作入口

### 手动操作
- 点击 "Generate" 按钮 → `generateImageWithAction()`

### 自动操作
- Skill 调用：`generateImageWithAction({ nodeId: 'image-01' })`
- 必须通过稳定 nodeId 执行

## Execution Payload

通过 `executionPayloadBuilder()` 构建：
```typescript
{
  projectId: string;
  nodeId: string;
  prompt: string;           // 使用 compiledPrompt
  model: string;
  ratio: string;
  size: string;
  params: {
    size: string;
    aspectRatio: string;
    cameraModel?: string;
    lensModel?: string;
    focalLength?: string;
    aperture?: string;
    ...其他模型参数
  };
  inputImageUrls?: string[];
  upstreamText?: string[];
  compiledPrompt: string;
  templateRefs?: unknown[];
  customPrompting?: unknown;
  cameraParams?: unknown;
}
```

## Retry Policy
`manual` - 失败后需要用户手动重试

## Merge Policy
`fill_empty` - 上游内容不覆盖本地已有输入

## 依赖的共享模块
- `promptCompiler.ts` - 编译 prompt
- `executionPayloadBuilder.ts` - 构建执行 payload
- `upstreamResolver.ts` - 解析上游内容
- `modelRegistry.ts` - 模型配置
- `kieAdapter.ts` - KIE API 适配器
- `runtimeClient.ts` - 运行时客户端
- `runtimeRecords.ts` - 结果持久化
- `actions/imageGenerationActions.ts` - 执行生成

## 当前实现状态（以 `IMPLEMENTATION_REDLINES.md` 与 `09_实现进度追踪.md` 为准）
- ✅ Image Node 基础 UI 字段与编辑区结构方向已明确，模型 / 比例 / 尺寸 / 摄像机参数入口已进入主线
- `IN_PROGRESS` runtime 调用链已接入原型，但不能据此写成“Image Generate 真闭环已完成”
- `IN_PROGRESS` `executionPayloadBuilder` 已进入主线，但仍需继续核实它是否已经成为唯一执行 payload 真相来源
- `TODO` `promptSnapshot / compiledPrompt / templateRefs / customPrompting` 的真实编译链仍需继续做实，不能只看类型或占位字段
- `TODO` 摄像机参数真实映射到 KIE payload 仍需继续验收，不能只因 UI 字段存在就判定完成
- `TODO` 任务提交 / 轮询 / 结果写回 / runtime_records 持久化仍未真正闭环

## 下一步
1. 把 `compileNodePrompt()` 与 `executionPayloadBuilder()` 收口成唯一真实输入来源
2. 真实接入 KIE API，完成任务提交 → 轮询状态 → 写回结果
3. 把 camera params、upstream、templateRefs、customPrompting 全部纳入统一 payload 编译链
4. 实现 `runtime_records` 持久化与结构化错误处理
