# Audio Node Schema & Contract

## 1. 节点定位
Audio Node 用于音频生成、语音合成、音频理解或转写，作为独立节点族维护。

## 2. UI 要求
选中节点后，下方编辑框建议包含：
- 模型/语音选择
- 输入文本或音频来源
- 参数（语言、风格、速度、情绪等）
- 输出区（播放器 / 转写结果）

## 3. Schema
```ts
{
  nodeId: string;
  type: 'audioNode';
  model: string;
  mode: 'tts' | 'stt' | 'music';
  text?: string;
  uploads: UploadedAsset[];
  params?: Record<string, string | number | boolean>;
  runtime?: NodeRuntimeState;
  result?: {
    kind: 'audio' | 'text';
    remoteUrl?: string;
    localPath?: string;
    transcript?: string;
  };
}
```

## 4. Tool Contract
- tool: `tts` / `exec` / 后续统一 runtime
- provider: `Audio Skill / KIE / Gemini`
- input:
  - text or audio refs
  - model
  - params
- output:
  - audio url / transcript
- writebackTarget: `self`

## 5. 节点级 Analyze / 转写原则
- Audio Node 可承担音频理解、转写、语音结果写回
- 若作为理解节点使用，应把 transcript / summary 写回节点

## 6. 写回规则
- 音频 URL 写回 result
- 转写文本写回 result.transcript
- 如为在线生成，也需保存 URL 到项目 JSON 记录
