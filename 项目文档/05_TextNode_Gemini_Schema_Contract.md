# Gemini Text Analyze Node Schema & Contract

## 1. 节点定位
文本节点不是普通文本框，而是 Gemini 附件分析节点。

## 2. UI 要求
选中节点后，下方编辑框应包含：
- 输入文本
- 分析提示词
- 附件上传区
- 附件列表/预览
- 模型选择（Gemini family）
- 输出结果区

## 3. Schema
```ts
{
  nodeId: string;
  type: 'textNode';
  text: string;
  analysisPrompt: string;
  model: string;
  uploads: UploadedAsset[];
  upstream?: {
    texts?: string[];
    imageUrls?: string[];
    videoUrls?: string[];
    audioUrls?: string[];
  };
  customPrompting?: {
    enabled?: boolean;
    userPrompt?: string;
    styleTags?: string[];
    mergeMode?: 'append' | 'prepend' | 'replace_section';
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
  runtime?: NodeRuntimeState;
  result?: {
    kind: 'text';
    content?: string;
    structured?: Record<string, unknown>;
  };
}
```

## 4. Tool Contract
- tool: `image` / `pdf` / 后续 Gemini 统一 runtime
- provider: `Gemini`
- input:
  - text
  - analysisPrompt
  - uploads
  - upstream refs
  - customPrompting
  - templateRefs
  - compiledPrompt
- output:
  - analysis text
  - structured summary
  - compiledPromptHash
- writebackTarget:
  - `self`
  - 或 `downstream`

## 5. 节点级 Analyze 原则
- Text Analyze Node 是模型驱动的理解节点
- 可分析当前节点自己的文本和附件
- 分析动作应写回：
  - analysis summary
  - tags
  - style cues
  - recommendations
  - last analysis model/provider

## 6. 当前阶段整合要求
- Text Node 不应继续只是本地 mock 文本工具，应逐步对齐 Gemini 附件分析节点定位
- Analyze 前需要先编译 prompt：原始输入/附件 -> 上游 refs -> `analysisPrompt` -> 模板片段 -> `customPrompting.userPrompt`
- 后续应补 `Compiled Prompt Preview`，避免用户看不到最终分析指令

## 7. 写回规则
- 主要文本结果写回 `result.content`
- prompt 追踪写回 `promptSnapshot`
- 可注入回当前输入框
- 可发送给下游 Image / Video Node
