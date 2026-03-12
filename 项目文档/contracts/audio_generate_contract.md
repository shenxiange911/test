# Audio Generate Contract

## 功能定位
Audio Node 是 titanX 的音频生成节点，当前在 `titanX/app` 中覆盖 `tts` 与 `music` 两种模式，并统一接入 runtime/result/writeback 主链。

## Skill/Tool 绑定
- toolName: `tts` / `exec` / 后续统一 runtime
- provider: `ElevenLabs`
- executionMode: `provider_api`
- 当前前端验证形态：`generateAudio()` 本地 deterministic mock writeback

## 输入 Schema
```ts
{
  nodeId: string;
  nodeType: 'audio';
  mode: 'tts' | 'music';
  prompt: string;
  model: string;
  uploadedAudioUrl?: string;
  uploads?: UploadedAsset[];
  upstream?: {
    texts?: string[];
    audioUrls?: string[];
  };
  ttsConfig?: {
    voiceLabel?: string;
    speed?: number;
    stability?: number;
    similarity?: number;
    styleStrength?: number;
  };
  musicConfig?: {
    instrumentalOnly?: boolean;
    duration?: 'auto' | '30s' | '1m' | '2m' | '3m' | '4m';
  };
}
```

## 输出 Schema
```ts
{
  result: {
    previewUrl?: string;
    remoteUrl?: string;
    transcript?: string;
    resultUrls: string[];
  };
  resultState: {
    primaryResultId?: string;
    results: Array<{
      resultId: string;
      kind: 'audio';
      url?: string;
      previewUrl?: string;
      text?: string;
      duration?: number;
      model?: string;
      promptSnapshot?: string;
      createTime?: number;
    }>;
  };
  runtime: {
    executionMode: 'manual';
    provider: 'ElevenLabs';
    model: string;
    taskId?: string;
    submitStatus?: 'idle' | 'pending' | 'submitted' | 'error';
    providerState?: 'idle' | 'waiting' | 'success' | 'fail';
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
  - `record.operator.uploadedAudioUrl`
  - `record.shell.contentMode = 'generated' | 'asset'`
  - `record.shell.hasLeftInput = false`（素材态或生成后）
- `runtime_records/audio/*`
  - 当前前端只写 `runtime.lastRecordPath` 占位路径

## 当前代码映射
- `titanX/app/src/lib/compileNodeExecutionPlan.js`
- `titanX/app/src/lib/apiClient.js`
- `titanX/app/src/lib/applyExecutionWriteback.js`
- `titanX/app/src/components/nodes/TitanNode.jsx`

## 当前实现状态
- ✅ Audio node UI 已进入 `titanX/app`
- ✅ `tts` / `music` 模式切换已进入共享编辑器
- ✅ runtime/result/writeback 已接入统一主链
- ✅ 生成结果可作为下游 Video Node 音频引用
- ⚠️ 真实 ElevenLabs API 仍待接入，当前为本地 mock 结果验证 UI 主链
