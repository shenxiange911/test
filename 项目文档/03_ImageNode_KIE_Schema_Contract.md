# KIE Image Node Schema & Contract

## 1. 节点定位
图片节点严格按 KIE 图片模型族实现，不允许混入视频逻辑。

## 2. UI 要求
打开节点编辑器后，下方编辑框必须包含：
- 模型型号
- 比例
- 大小
- 当前输入文本
- 上游文本
- 上游图片
- 摄像机型号
- 镜头型号
- 焦段
- 光圈
- 动态模型参数区

当前阶段可继续预留但不强制首批落地：
- ISO
- 快门速度
- 参数预设（Preset）

## 3. Schema
```ts
{
  nodeId: string;
  type: 'imageNode';
  model: string;
  ratio: string;
  size: string;
  prompt: string;
  cameraModel: string;
  lensModel: string;
  focalLength: string;
  aperture: string;
  uploads: UploadedAsset[];
  upstream?: {
    texts?: string[];
    imageUrls?: string[];
  };
  customPrompting?: {
    enabled?: boolean;
    userPrompt?: string;
    styleTags?: string[];
    negativePrompt?: string;
    mergeMode?: 'append' | 'prepend' | 'replace_section';
  };
  cameraParams?: {
    cameraModel?: string;
    lensModel?: string;
    focalLength?: string;
    aperture?: string;
    iso?: number;
    shutterSpeed?: string;
  };
  templateRefs?: Array<{
    templateId: string;
    scope: 'local' | 'type' | 'project';
    mergeMode: 'fill_empty' | 'merge' | 'replace';
  }>;
  promptSnapshot?: {
    compiledPrompt?: string;
    compiledPromptHash?: string;
    templateSnapshot?: Record<string, unknown>;
    compiledAt?: string;
  };
  params?: Record<string, string | number | boolean>;
  runtime?: NodeRuntimeState;
  result?: {
    kind: 'image';
    previewUrl?: string;
    remoteUrl?: string;
    localPath?: string;
  };
}
```

## 4. Tool Contract
- tool: `exec`（当前本地代理开发形态）/ 后续可切服务端 API
- provider: `KIE`
- input:
  - prompt
  - model
  - ratio
  - size
  - inputImageUrls
  - params
  - camera config
  - customPrompting
  - templateRefs
  - compiledPrompt
- output:
  - taskId
  - status
  - resultUrls[]
  - previewUrl
  - compiledPromptHash
- writebackTarget: `self`
- mergePolicy: `fill_empty | merge | replace`
- compiledPromptWriteback: `runtime | result | both`

## 5. 运行时 Contract 补充
标准 runtime request 需要能表达：
- node_id
- node_type
- execution_mode
- provider
- model
- params
- input_refs
- template_refs
- custom_prompting
- compiled_prompt
- project_id

标准 runtime state 至少包含：
- execution_mode
- provider
- model
- task_id
- queued_at
- started_at
- finished_at
- compiled_prompt_hash
- last_error

## 6. Model Registry 要求
- 模型选择不应继续在节点组件中硬编码 option 列表
- `modelRegistry` 应作为当前唯一模型入口，至少负责：
  - 模型显示名
  - family
  - endpoint
  - UI 字段配置
  - 参数转换器 `parameterTransformer`
- 节点 UI 只消费 registry，不直接写死 provider 细节

## 7. Adapter / Payload Builder 要求
- Image Node 应尽快拆出独立 `kieAdapter`，而不是把 provider 细节继续堆在 UI 层
- `buildKIEImagePayload()` 必须负责把以下字段统一编译到执行请求：
  - 上游 text/image refs
  - 节点主 prompt
  - templateRefs
  - customPrompting
  - cameraParams
  - model / ratio / size / params
- 摄像机参数不能只停留在编辑器输入框，必须真实进入 payload builder
- 当前阶段可先把 `cameraModel / lensModel / focalLength / aperture` 作为首批稳定参数；`iso / shutterSpeed` 预留后续接入

## 8. Runtime 可靠性要求
- `runtimeClient` 后续应补结构化错误处理，不只抛裸字符串
- 可加入有限重试，但默认必须是可控、小范围、可观测的重试
- 多节点并发执行时，后续应补执行队列或并发上限控制，避免无节制并发提交
- 请求/响应日志可以保留轻量调试钩子，但不要把示例里的完整拦截器模板原样搬进正式规范
- 当前阶段优先采用轻量 Prompt Compiler，不急于一次性引入完整模板 DSL（`if` / `each` / `unless`）；先保证 compiled prompt 单一真相来源

## 9. 写回规则
- preview 写回 `data.previewUrl`
- 远端 URL 写回 `data.result.remoteUrl`
- runtime 元信息写回 `data.runtime`
- prompt 追踪写回 `data.promptSnapshot`
- 并保存 URL 到项目 JSON 记录

## 10. KIE URL 保存 JSON
推荐保存到：
`项目文档/runtime_records/image/`

最少字段：
```json
{
  "nodeId": "image-01",
  "taskId": "task_xxx",
  "model": "nano-banana-2",
  "status": "success",
  "resultUrls": ["https://..."],
  "createTime": "2026-03-10T17:00:00+08:00"
}
```
