# Text Analyze Contract

## 功能定位
Text Node 是 Gemini 附件分析节点，负责理解文本、图片、视频、音频、PDF 等附件内容。

## Skill/Tool 绑定

### skillName
`analysis-skill` / `gemini-analyze`

### toolName
- 当前阶段：`image`（OpenClaw image tool，支持图片分析）
- 后续扩展：`pdf`（PDF 分析）
- 最终目标：统一 Gemini runtime adapter

### provider
`Gemini`

### executionMode
`skill` / `provider_api`

## 输入 Schema

### 必需字段
```typescript
{
  nodeId: string;           // 节点业务 ID，如 text-01
  text: string;             // 用户输入文本
  analysisPrompt: string;   // 分析任务描述
  uploads: UploadedAsset[]; // 附件列表
}
```

### 可选字段
```typescript
{
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
  model?: string;           // Gemini 模型选择
}
```

## 输出 Schema

### 成功输出
```typescript
{
  result: {
    kind: 'text';
    content: string;        // 分析结果文本
    structured?: {          // 结构化摘要（可选）
      tags?: string[];
      styleCues?: string[];
      recommendations?: string[];
    };
  };
  promptSnapshot: {
    compiledPrompt: string;
    compiledPromptHash: string;
    compiledAt: string;
    upstreamSummary: string[];
  };
  runtime: {
    executionMode: 'skill' | 'provider_api';
    provider: 'Gemini';
    model: string;
    finishedAt: string;
  };
}
```

### 错误输出
```typescript
{
  runtime: {
    lastError: string;      // 错误信息
    finishedAt: string;
  };
  status: 'error';
}
```

## Writeback 目标

### 主要写回：self
- `result.content` - 分析结果文本
- `result.structured` - 结构化摘要
- `promptSnapshot` - prompt 追踪
- `runtime` - 运行时元信息
- `status` - 节点状态

### 可选写回：downstream
- 通过 `sendTextToConnected` 动作将分析结果发送给下游节点
- 下游节点的 `upstream.texts` 会包含此分析结果

## 前端展示要求

### 节点缩略图
- 显示节点 ID（text-01）
- 显示状态图标
- 显示简短摘要

### 编辑器区域
- 输入文本框
- 分析提示词输入框
- 附件上传区
- 附件列表/预览
- 模型选择下拉框
- 分析结果展示区
- Compiled Prompt Preview（只读）

### 必须展示的字段
- `text` - 原始输入
- `analysisPrompt` - 分析任务
- `uploads` - 附件列表
- `result.content` - 分析结果
- `promptSnapshot.compiledPrompt` - 编译后的 prompt
- `runtime.model` - 使用的模型
- `status` - 当前状态

## 操作入口

### 手动操作
- 点击 "Analyze" 按钮 → `analyzeTextAction()`

### 自动操作
- Skill 调用：`analyzeTextAction({ nodeId: 'text-01' })`
- 必须通过稳定 nodeId 执行

## Retry Policy
`manual` - 失败后需要用户手动重试

## Merge Policy
`fill_empty` - 上游内容不覆盖本地已有输入

## 依赖的共享模块
- `promptCompiler.ts` - 编译 prompt
- `upstreamResolver.ts` - 解析上游内容
- `actions/textAnalysisAction.ts` - 执行分析

## 当前实现状态
- ✅ UI 字段已对齐
- ✅ promptSnapshot 已生成
- ⚠️ 未真实接入 Gemini API（当前是 mock 实现）
- ⚠️ analysisPrompt 未进入 compiled prompt
- ❌ 结构化摘要未实现

## 下一步
1. 将 analysisPrompt 纳入 promptCompiler
2. 真实接入 Gemini API
3. 实现结构化摘要输出
