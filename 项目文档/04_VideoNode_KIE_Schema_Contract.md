# KIE Video Node Schema & Contract

## 1. 节点定位
视频节点必须独立成族，不能塞进 Image Node。

## 2. UI 要求
选中节点后，下方编辑框建议包含：
- 模型型号
- 时长
- 比例
- 分辨率/质量
- motion / camera / style 等视频参数
- 当前输入文本
- 上游图片/视频/文本

## 3. Schema
```ts
{
  nodeId: string;
  type: 'videoNode';
  model: string;
  duration: string;
  aspectRatio: string;
  quality?: string;
  prompt: string;
  uploads: UploadedAsset[];
  upstream?: {
    texts?: string[];
    imageUrls?: string[];
    videoUrls?: string[];
  };
  params?: Record<string, string | number | boolean>;
  runtime?: NodeRuntimeState;
  result?: {
    kind: 'video';
    previewUrl?: string;
    remoteUrl?: string;
    localPath?: string;
    coverUrl?: string;
  };
}
```

## 4. Tool Contract
- tool: `exec` / 后续服务端 runtime API
- provider: `KIE`
- input:
  - prompt
  - model
  - duration
  - aspectRatio
  - input image/video refs
  - params
- output:
  - taskId
  - status
  - resultUrls[]
  - previewUrl / coverUrl
- writebackTarget: `self`

## 5. 运行时 Contract 补充
标准 runtime request 需要能表达：
- node_id
- node_type
- execution_mode
- provider
- model
- params
- input_refs
- project_id

标准 runtime state 至少包含：
- execution_mode
- provider
- model
- task_id
- queued_at
- started_at
- finished_at
- last_error

## 6. 写回规则
- 视频 URL 写回 result
- 封面图写回 preview/cover
- runtime 状态写回节点
- 保存 URL 到项目 JSON 记录

## 7. KIE URL 保存 JSON
推荐保存到：
`项目文档/runtime_records/video/`
