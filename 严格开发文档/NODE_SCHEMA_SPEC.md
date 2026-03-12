# NODE_SCHEMA_SPEC.md

> ⚠️ 说明  
> 本文档包含 titanLX 的完整 schema 方向，但**当前阶段并未实现全部节点类型**。  
> 当前阶段最小主线请优先按 Text / Image 阅读。  
> 若 schema 与当前实现状态冲突，请以 `../项目文档/IMPLEMENTATION_REDLINES.md` 和 `./ACCEPTANCE_CHECKLIST.md` 解释当前阶段事实。

## 当前阶段范围（v1）
### 当前重点已进入主线的节点
- `textInput`
- `imageGenNode`

### 已定义但属于后续扩展/未来规划的节点
- `imageInput`
- `videoInput`
- `audioInput`
- `urlInput`
- `uploadNode`
- `analysisNode`
- `storyboardNode`
- `videoGenNode`
- `audioGenNode`
- `resultNode`

---

## 基础枚举
```ts
export type RunStatus =
  | 'idle'
  | 'configured'
  | 'queued'
  | 'running'
  | 'success'
  | 'error'
  | 'downloaded'
  | 'synced';

export type Controllability =
  | 'manual'
  | 'hybrid'
  | 'skill'
  | 'acp'
  | 'local_runtime'
  | 'provider_api'
  | 'result';

export type NodeCategory =
  | 'input'
  | 'analysis'
  | 'planning'
  | 'generation'
  | 'result';
```

## Prompt / Template 扩展
```ts
export interface PromptDirectives {
  cameraDirectives?: {
    cameraModel?: string;
    lensModel?: string;
    focalLength?: string;
    aperture?: string;
    shotType?: string;
    movement?: string;
  };
}

export interface CustomPrompting extends PromptDirectives {
  enabled?: boolean;
  mode?: 'append' | 'prepend' | 'replace_section';
  userPrompt?: string;
  styleTags?: string[];
  negativePrompt?: string;
  locked?: boolean;
  lastCompiledPrompt?: string;
}

export interface TemplateRef {
  templateId: string;
  scope: 'local' | 'type' | 'project';
  mergeMode: 'fill_empty' | 'merge' | 'replace';
}
```

## BaseNodeData
```ts
export interface BaseNodeData {
  nodeId: string;
  title: string;
  description?: string;
  status: RunStatus;
  controllability: Controllability;
  tags?: string[];
  uploads?: UploadedAsset[];
  result?: NodeResult | null;
  runtime?: NodeRuntimeState;
  analysisSummary?: string;
  skillBinding?: SkillBinding;
  customPrompting?: CustomPrompting;
  templateRefs?: TemplateRef[];
}
```

## SkillBinding
```ts
export interface SkillBinding {
  skillName: string;
  toolName: string;
  inputSchemaRef?: string;
  outputSchemaRef?: string;
  writebackTarget?: 'self' | 'downstream' | 'resultNode';
  mergePolicy?: 'fill_empty' | 'merge' | 'replace';
  compiledPromptWriteback?: 'runtime' | 'result' | 'both';
}
```

## v1 节点类型（完整方向）
```ts
export type NodeType =
  | 'textInput'
  | 'imageInput'
  | 'videoInput'
  | 'audioInput'
  | 'urlInput'
  | 'uploadNode'
  | 'analysisNode'
  | 'storyboardNode'
  | 'imageGenNode'
  | 'videoGenNode'
  | 'audioGenNode'
  | 'resultNode';
```

## 当前阶段最重要的两个节点
### TextInputNodeData
```ts
export interface TextInputNodeData extends BaseNodeData {
  type: 'textInput';
  text: string;
  language?: string;
}
```

### ImageGenNodeData（当前主线重点）
```ts
export interface ImageGenNodeData extends BaseNodeData {
  type: 'imageGenNode';
  providerFamily?: 'gpt4o-image' | 'flux-kontext' | 'market-image';
  prompt?: string;
  boundText?: string;
  model: string;
  size: string;
  ratio: string;
  format?: 'png' | 'jpeg';
  inputImages?: string[];
  enhance?: boolean;
  translate?: boolean;
  fallback?: boolean;
  cameraParams?: {
    cameraModel?: string;
    lensModel?: string;
    focalLength?: string;
    aperture?: string;
  };
  previewUrl?: string;
}
```

## 其他节点（后续扩展方向）
```ts
export interface ImageInputNodeData extends BaseNodeData {
  type: 'imageInput';
  imageUrl?: string;
  localPath?: string;
}

export interface VideoInputNodeData extends BaseNodeData {
  type: 'videoInput';
  videoUrl?: string;
  localPath?: string;
}

export interface AudioInputNodeData extends BaseNodeData {
  type: 'audioInput';
  audioUrl?: string;
  localPath?: string;
}

export interface UrlInputNodeData extends BaseNodeData {
  type: 'urlInput';
  url: string;
}

export interface UploadNodeData extends BaseNodeData {
  type: 'uploadNode';
  accept: 'image' | 'video' | 'audio' | 'any';
  assetKind?: 'image' | 'video' | 'audio' | 'text' | 'other';
  previewUrl?: string;
}

export interface AnalysisNodeData extends BaseNodeData {
  type: 'analysisNode';
  provider?: string;
  model?: string;
  analysisMode?: string;
  analysisPrompt?: string;
  structuredSummary?: string;
}

export interface StoryboardNodeData extends BaseNodeData {
  type: 'storyboardNode';
  provider?: string;
  model?: string;
  prompt?: string;
  aspectRatio?: string;
  outputCount?: number;
  planSummary?: string;
}

export interface VideoGenNodeData extends BaseNodeData {
  type: 'videoGenNode';
  prompt?: string;
  boundText?: string;
  model: string;
  ratio: string;
  duration: string;
  previewUrl?: string;
}

export interface AudioGenNodeData extends BaseNodeData {
  type: 'audioGenNode';
  prompt?: string;
  boundText?: string;
  model: string;
  voice: string;
  previewUrl?: string;
}

export interface ResultNodeData extends BaseNodeData {
  type: 'resultNode';
  branchSummaries?: string[];
  resultItems?: NodeResult[];
}
```

## AppNodeData
```ts
export type AppNodeData =
  | TextInputNodeData
  | ImageInputNodeData
  | VideoInputNodeData
  | AudioInputNodeData
  | UrlInputNodeData
  | UploadNodeData
  | AnalysisNodeData
  | StoryboardNodeData
  | ImageGenNodeData
  | VideoGenNodeData
  | AudioGenNodeData
  | ResultNodeData;
```

## Edge Schema
```ts
export interface FlowEdgeData {
  semantic?:
    | 'text_flow'
    | 'media_flow'
    | 'analysis_ref'
    | 'storyboard_ref'
    | 'image_ref'
    | 'video_ref'
    | 'audio_ref'
    | 'asset';
  auto?: boolean;
  locked?: boolean;
}
```

## ID-first 节点约束
- 每个节点创建时必须立刻获得稳定 `nodeId`
- 节点业务 ID 必须按类型独立编号，例如：`text-01`、`image-01`
- 删除节点后，新建同类型节点必须复用最小缺失编号
- 手动创建与自动创建必须共享同一个 allocator

## Runtime Request
```ts
export interface NodeRuntimeRequest {
  nodeId: string;
  nodeType: NodeType;
  executionMode: Controllability;
  provider?: string;
  model?: string;
  params?: Record<string, unknown>;
  inputRefs?: string[];
  templateRefs?: TemplateRef[];
  customPrompting?: CustomPrompting;
  compiledPrompt?: string;
  projectId: string;
}
```

## Runtime State
```ts
export interface NodeRuntimeState {
  executionMode?: Controllability;
  provider?: string;
  model?: string;
  taskId?: string;
  queuedAt?: string | null;
  startedAt?: string | null;
  finishedAt?: string | null;
  lastError?: string | null;
  compiledPromptHash?: string | null;
}
```

## Prompt / Template 约束
- 具备提示词意义的节点必须持有 `customPrompting`
- `customPrompting` 属于 operator-facing 字段，禁止只存在于本地 UI 临时状态
- `templateRefs` 只引用模板，不直接复制 runtime 结果字段
- 运行后应在 `result` 或 `runtime` 侧保留 prompt snapshot / template snapshot / compiledPromptHash 用于追踪
