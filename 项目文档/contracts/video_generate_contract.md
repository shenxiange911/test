# Video Generate Contract

## 功能定位
Video Node 是 titanX 的视频生成节点，当前在 `titanX/app` 中按统一 node shell + runtime/result/writeback 主链实现，承接文本、图片、视频、音频上游引用。

## Skill/Tool 绑定
- toolName: `exec` / 后续 `kieAdapter`
- provider: `KIE` / `Veo`
- executionMode: `provider_api`
- 当前前端验证形态：`generateVideo()` 本地 deterministic mock writeback

## 输入 Schema
```ts
{
  nodeId: string;
  nodeType: 'video';
  prompt: string;
  model: string;
  mode: 'text-to-video' | 'image-to-video' | 'video-to-video';
  duration: string;
  aspectRatio: string;
  resolution: string;
  quality?: string;
  multiShots?: boolean;
  generateAudio?: boolean;
  uploads?: UploadedAsset[];
  upstream?: {
    texts?: string[];
    imageUrls?: string[];
    videoUrls?: string[];
    audioUrls?: string[];
    resultRefs?: Array<{
      sourceNodeId: string;
      sourceBusinessId: string;
      sourceNodeType: 'text' | 'image' | 'video' | 'audio';
      resultId?: string;
      role: 'text' | 'image' | 'video' | 'audio';
      url?: string;
      text?: string;
      isPrimary: boolean;
    }>;
  };
}
```

## 输出 Schema
```ts
{
  result: {
    previewUrl?: string;
    remoteUrl?: string;
    coverUrl?: string;
    resultUrls: string[];
  };
  resultState: {
    primaryResultId?: string;
    results: Array<{
      resultId: string;
      kind: 'video';
      url?: string;
      previewUrl?: string;
      thumbnailUrl?: string;
      duration?: number;
      model?: string;
      promptSnapshot?: string;
      createTime?: number;
    }>;
  };
  runtime: {
    executionMode: 'manual';
    provider: string;
    model: string;
    taskId?: string;
    submitStatus?: 'idle' | 'pending' | 'submitted' | 'error';
    providerState?: 'idle' | 'waiting' | 'success' | 'fail';
    startedAt?: string;
    finishedAt?: string;
    lastWritebackAt?: string;
    lastRecordPath?: string;
  };
}
```

## Writeback 目标
- `self`
  - `record.compiled`
  - `record.runtime`
  - `record.result`
  - `record.resultState`
  - `record.shell.contentMode = 'generated'`
  - `record.shell.runtimeStatus = 'success' | 'error'`
- `runtime_records/video/*`
  - 当前前端只写 `runtime.lastRecordPath` 占位路径
  - 后续由真实 adapter / runtime record writer 落文件

## 当前代码映射
- `titanX/app/src/lib/compileNodeExecutionPlan.js`
- `titanX/app/src/lib/apiClient.js`
- `titanX/app/src/lib/applyExecutionWriteback.js`
- `titanX/app/src/components/nodes/TitanNode.jsx`

## 当前实现状态
- ✅ Video node UI 已进入 `titanX/app`
- ✅ 统一 `contentMode / runtimeStatus / resultState` 已接入
- ✅ 上游 `texts / imageUrls / videoUrls / audioUrls` 已进入 compiled plan
- ✅ 结果主次切换与 writeback 已接入共享主链
- ⚠️ 真实 KIE/Veo 视频 API 仍待接入，当前为本地 mock 结果验证 UI 主链
