# titanLX 节点体系与 Schema 总表

## 1. 节点分类

| 节点类型 | 用途 | 运行底座 |
|---|---|---|
| Image Node | 图片生成/图片编辑 | KIE |
| Video Node | 视频生成/视频编辑 | KIE |
| Text Analyze Node | 文本+附件分析理解 | Gemini |
| Audio Node | 音频生成/音频理解 | Audio / KIE / Gemini |

## 2. 节点输入输出总览

### Image Node
- 输入：text、image refs、camera config、style refs、focus-picked refs、tag chips、slash commands、`@Image N` references、model params
- 输出：image urls、preview、runtime state、multi-result primary/secondary state
- 写回：self
- 备注：Image Node 的实际输入编译分为三层
  - 用户显式输入 prompt
  - 相机参数 / 风格参考图的隐式全局提示词前缀
  - `@Image N` / 焦点提取 / 参考图带来的结构化片段

### Video Node
- 输入：text、image refs、video refs、model params
- 输出：video urls、cover、runtime state
- 写回：self

### Text Analyze Node
- 输入：text、image/video/audio/txt/pdf 附件、analysis prompt
- 输出：analysis text、structured summary
- 写回：self / downstream

### Audio Node
- 输入：text、mode(`tts`/`music`)、voice/model params、optional uploaded audio asset、optional upstream text ref
- 输出：audio url、waveform/player state、runtime state、optional transcript
- 写回：self
- 备注：Audio Node 当前至少分两条主语义
  - `tts`：文本转语音，模型会联动音色、语速、稳定性、相似度、风格强度等参数
  - `music`：文本转音乐，模型会联动纯音乐开关与 `Auto / 30s / 1m / 2m / 3m / 4m` 时长位
  - 上传本地音频后会切到素材浏览/结果分发态，只保留右输出口，可继续输出给 `Video` / `Digital Human`

## 3. 推荐连接关系
- Text → Image
- Text → Video
- Image → Image
- Image → Video
- Video → Text Analyze
- Image → Text Analyze
- Audio → Text Analyze
- Text Analyze → Image
- Text Analyze → Video
- 多上游汇入 Analysis / Storyboard
- 多分支汇入 Result

## 3.1 文件上传到节点的自适应映射
- `image/*` → Image Node
- `video/*` → Video Node
- `audio/*` → Audio Node
- `text/plain` / `.txt` → Text / Text Analyze Node
- 这条映射同时适用于：
  - 画布级上传
  - 左侧添加节点面板底部 `上传` 入口
- 上传行为默认应理解为“按类型创建节点”，而不是先进入统一素材池后再手动分配

## 4. 节点体系补充原则
- one-to-many branch generation 是一等工作流模式
- 每个生成节点拥有自己的 provider / model / params
- Manual + automatic 必须共存
- Result 节点负责汇总多分支输出
- Storyboard / Analysis 属于理解与规划层，不等于执行层

## 5. 通用 Schema 字段
- `nodeId`
- `type`
- `title`
- `status`
- `runtime`
- `result`
- `skillBinding`
- `upstream`
- `customPrompting`
- `templateRefs`
- `promptSnapshot`

## 6. 通用 Contract 字段
- `toolName`
- `inputSchemaRef`
- `outputSchemaRef`
- `writebackTarget`
- `retryPolicy`
- `executionMode`
- `provider`
- `model`
- `mergePolicy`
- `compiledPromptWriteback`

## 7. 当前阶段整合结论
- 当前最值得优先补齐的不是继续扩节点，而是把文档已定义的 `customPrompting`、模板引用、compiled prompt 追踪真正接入代码
- Image Node 仍是 v1 第一闭环节点，先完成真实 KIE 接入、payload builder、结果持久化，再复制模式到 Video / Audio
- 摄像机参数不能只停留在 UI；后续必须进入 Image adapter 的 payload builder
- 结果持久化不能只保存显示态，至少要写入 `taskId / model / status / resultUrls / createTime`，并预留 prompt/template snapshot 追踪字段
