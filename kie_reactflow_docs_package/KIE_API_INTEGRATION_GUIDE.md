# KIE API 完整接入指南（面向 React Flow 节点系统）

## 1. 这套项目的目标

你要做的是一个 **TapNow / Flowgram 风格** 的媒体工作流节点系统，要求同时支持：

- 用户手动创建节点
- 用户手动拖拽连线
- OpenClaw 自动生成节点
- OpenClaw 自动补全连线
- 节点触发 KIE API 生成图片 / 视频 / 音频
- 返回结果显示在节点 UI 里
- 支持下载结果 / 本地保存 / 服务端缓存

---

## 2. 官方 API 结构总览

KIE 现在不是单一一条 API，而是 **三类接入路线**：

### A. Market 统一模型路线
适合大多数图片 / 视频 / 音频模型。

- 创建任务：
  - `POST https://api.kie.ai/api/v1/jobs/createTask`
- 查任务：
  - `GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId=...`

适用于：
- Seedream
- GPT Image 1.5
- Imagen4 / Nano Banana
- Kling
- Wan
- Sora2
- ElevenLabs
- 以及 Market 下未来新增模型

### B. 专有产品 API 路线
某些产品线有自己的独立接口，字段不完全和 Market 一样。

#### 4o Image API
- 创建：
  - `POST https://api.kie.ai/api/v1/gpt4o-image/generate`
- 查详情：
  - `GET https://api.kie.ai/api/v1/gpt4o-image/record-info?taskId=...`
- 转直链：
  - `POST https://api.kie.ai/api/v1/gpt4o-image/download-url`

#### Flux Kontext API
- 创建 / 编辑：
  - `POST https://api.kie.ai/api/v1/flux/kontext/generate`
- 查详情：
  - `GET https://api.kie.ai/api/v1/flux/kontext/record-info?taskId=...`

#### Runway API
- 创建：
  - `POST https://api.kie.ai/api/v1/runway/generate`
- 查详情：
  - `GET https://api.kie.ai/api/v1/runway/record-info?taskId=...`

#### Veo 3.1 API
- 创建：
  - `POST https://api.kie.ai/api/v1/veo/generate`
- 查详情：
  - `GET https://api.kie.ai/api/v1/veo/record-info?taskId=...`

#### Suno API
- 生成音乐：
  - `POST https://api.kie.ai/api/v1/generate`
- 查音乐详情：
  - `GET https://api.kie.ai/api/v1/generate/record-info?taskId=...`

### C. 文件上传 API 路线
这是 **前置依赖**。凡是需要 `image_urls` / 上传音频 / 上传视频的模型，都应该先上传到 KIE 的临时文件服务。

上传基地址不是 `api.kie.ai`，而是：

- `https://kieai.redpandaai.co/api/file-base64-upload`
- `https://kieai.redpandaai.co/api/file-stream-upload`
- `https://kieai.redpandaai.co/api/file-url-upload`

---

## 3. 鉴权原则

所有 KIE 文档都要求 Bearer Token 鉴权。

### 绝对禁止
- 前端 React 组件里直接写 KIE Key
- 在浏览器里直接请求 KIE
- 在 GitHub 仓库明文写死 key

### 正确做法
- 浏览器 -> 你的后端 `/api/kie/...`
- 你的后端 -> KIE 官方接口
- 后端从环境变量读取：
  - `KIE_API_KEY`
  - `KIE_WEBHOOK_HMAC_KEY`

---

## 4. 节点系统和 KIE 的映射关系

推荐至少有这些节点类型：

### Text Node
用途：
- 作为 prompt / script / scene prompt 源头

不直接调用 KIE 时：
- 只负责输出文本给下游节点

也可以扩展：
- 接 Chat 模型
- 自动补 prompt
- 自动分镜

### Image Node
用途：
- 文生图
- 图生图
- 图片编辑
- 图片增强 / 去背景 / 放大

推荐对接：
- 4o Image
- Flux Kontext
- GPT Image 1.5
- Seedream
- Imagen4
- Nano Banana Edit

### Video Node
用途：
- 文生视频
- 图生视频
- 视频增强 / 扩展

推荐对接：
- Veo 3.1
- Runway
- Kling
- Wan
- Sora2

### Audio Node
用途：
- TTS
- 音效
- 音乐生成
- 音频风格转换

推荐对接：
- ElevenLabs
- Suno

### Upload Node
用途：
- 上传图片 / 视频 / 音频
- 输出给下游节点作为输入素材

---

## 5. 通用执行状态机

每个 React Flow 节点都必须实现统一状态：

```ts
type KieNodeRunState =
  | "idle"
  | "uploading"
  | "queued"
  | "generating"
  | "success"
  | "error";
```

节点 UI 里至少要显示：

- 当前状态
- 当前 taskId
- 最近一次错误
- 最近一次结果预览
- 下载按钮
- 重新运行按钮

---

## 6. 推荐后端流程

### 6.1 文生图 / 图生图 / 文生视频 / 图生视频

#### Step 1
浏览器点击节点 Run

#### Step 2
前端把节点数据发给自己的后端
例如：
- `POST /api/kie/run-node`

body:
```json
{
  "nodeId": "image-1",
  "nodeType": "image",
  "provider": "kie",
  "modelKey": "gpt-image-1.5-tti",
  "config": {
    "prompt": "A cinematic rainy street at night",
    "aspectRatio": "16:9",
    "quality": "medium"
  },
  "upstream": {
    "text": "来自 Text Node 的补充 prompt",
    "assets": []
  }
}
```

#### Step 3
后端判断是否需要先上传文件
例如：
- 图生图
- 图生视频
- 音频翻唱
- 视频转视频

如果需要，则调用 File Upload API，拿到 KIE file URL。

#### Step 4
后端按模型规范提交任务给 KIE
得到：
- `taskId`

#### Step 5
后端把 `taskId` 写回你自己的数据库 / KV / 任务表

#### Step 6
后端立即响应前端：
```json
{
  "ok": true,
  "taskId": "task_xxx",
  "providerTaskType": "market"
}
```

#### Step 7
结果返回有两条路线：

##### 路线 A：callback（推荐）
KIE 回调你的：
- `/api/kie/webhook/market`
- `/api/kie/webhook/4o-image`
- `/api/kie/webhook/runway`
- `/api/kie/webhook/veo`
- `/api/kie/webhook/suno`

##### 路线 B：polling（兜底）
前端 / 后端轮询你自己的：
- `GET /api/kie/task/:taskId`

你的后端再去查 KIE。

---

## 7. 不同接口的结果结构要统一归一化

不同 KIE 产品返回结构不完全一样。

### Market `recordInfo`
通常长这样：
- `data.taskId`
- `data.model`
- `data.state`
- `data.param`
- `data.resultJson`

其中 `resultJson` 往往还是一个 JSON 字符串，需要再次 `JSON.parse()`。

### 4o Image `record-info`
结果在：
- `data.response.resultUrls`

### Veo `record-info`
结果在：
- `data.response.resultUrls`
- `data.response.originUrls`
- `data.response.resolution`

### Suno `record-info`
结果在：
- `data.response.sunoData[]`
- 里面常见字段：
  - `audioUrl`
  - `streamAudioUrl`
  - `imageUrl`
  - `prompt`
  - `duration`

所以必须做统一归一化：

```ts
type NormalizedKieResult =
  | {
      kind: "image";
      urls: string[];
      previewUrl: string | null;
    }
  | {
      kind: "video";
      urls: string[];
      previewUrl: string | null;
      resolution?: string;
    }
  | {
      kind: "audio";
      urls: string[];
      previewUrl?: string | null;
      coverImageUrl?: string | null;
      streamUrl?: string | null;
    }
  | {
      kind: "text";
      text: string;
    };
```

---

## 8. 下载与保存策略

### 8.1 千万不要把 KIE 的临时结果 URL 当永久资源
因为不同接口保留期不同：
- Market 通用结果 URL 建议尽快下载
- 4o Image 图片保留 14 天
- 4o / Common download-url 生成的直链只保留 20 分钟
- 上传文件只保留 3 天

### 8.2 推荐双层保存策略

#### A. 服务端永久缓存
后端在拿到成功结果后，立刻：
1. 调 KIE download-url（如果需要）
2. 用 Node.js stream 下载文件
3. 存到你自己的对象存储 / 本地磁盘 / S3 / R2
4. 返回你自己的永久 URL 给前端

#### B. 浏览器本地下载
在节点结果卡上提供：
- Download 按钮
- Export 按钮

支持：
- `<a download>`
- `fetch + blob + URL.createObjectURL`
- `showSaveFilePicker`（可选）

**最佳实践：**
浏览器只负责“让用户下载”，永久保存仍然由你自己的后端存储系统负责。

---

## 9. React Flow UI 更新规则

节点运行完后，不要直接把原始 KIE response 整坨塞进节点 data。

应该只塞归一化结果：

```ts
node.data = {
  ...node.data,
  runState: "success",
  taskId,
  result: normalized,
  preview: normalized.previewUrl ?? null,
  lastCompletedAt: Date.now(),
  providerMeta: {
    provider: "kie",
    rawResultRef: taskId
  }
}
```

### Image Node UI
显示：
- 大图预览
- model / aspect ratio / quality
- taskId
- Download
- Re-run

### Video Node UI
显示：
- `<video controls>`
- 分辨率
- 时长（如果有）
- Download
- Re-run

### Audio Node UI
显示：
- `<audio controls>`
- 封面图（如果有）
- 标题 / tags（如果有）
- Download
- Re-run

---

## 10. 手动连线与 OpenClaw 自动连线

你的系统要同时支持：

### 手动模式
用户自己拖线：
- Text -> Image
- Text -> Video
- Upload(image) -> Image Edit
- Upload(image) -> Video(image-to-video)
- Upload(audio) -> Audio Cover / Music / Speech-to-video

### 自动模式
OpenClaw 根据任务目标自动规划：
- 建节点
- 选模型
- 补默认参数
- 自动创建 edges
- 自动布局

但 OpenClaw 输出的不能直接改画布，必须先生成：

```ts
type FlowPatch = {
  nodesToAdd: NodeDraft[];
  edgesToAdd: EdgeDraft[];
  nodesToUpdate: NodeUpdatePatch[];
};
```

然后服务端或前端按规则校验：
- schema 是否合法
- 连接类型是否兼容
- modelKey 是否受支持
- 参数是否符合当前模型要求

---

## 11. 推荐的模型路由策略

### 图片
- 首选通用：`gpt-image-1.5` / `seedream4.5`
- 首选编辑：`flux-kontext-max` / `google/nano-banana-edit`
- 首选简单专线：`4o-image`

### 视频
- 高质量主线：`veo3_fast` / `veo3_quality`
- 多镜头 / 元素参考：`kling-3.0/video`
- 图生视频稳定线：`wan/2-6-image-to-video`
- 角色动画：`sora-2-image-to-video`

### 音频
- TTS：`elevenlabs/text-to-speech-multilingual-v2`
- 音乐：`Suno V4/V4_5/V5`
- 对话：`elevenlabs/text-to-dialogue-v3`

---

## 12. 最重要的严格约束

1. KIE key 永不进前端
2. React Flow 严格受控模式
3. 所有任务都有 `taskId`
4. 所有结果都做归一化
5. 所有 callback 都做 HMAC 验签
6. 所有下载都走你自己的后端缓存流程
7. 上传节点统一先走 KIE File Upload API
8. OpenClaw 只能输出 patch，不能直接写死 UI 状态
