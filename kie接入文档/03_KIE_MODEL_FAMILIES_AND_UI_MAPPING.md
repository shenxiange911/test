# 03_KIE_MODEL_FAMILIES_AND_UI_MAPPING

## 先说结论

KIE 不是只有一个统一的“图片接口”或“视频接口”。
对你的项目，应该按 **模型家族 family** 做映射，而不是把所有模型都塞到一个巨大 switch 里。

推荐的 family：

- `market-image`
- `market-video`
- `market-audio`
- `gpt4o-image`
- `flux-kontext`
- `runway-video`
- `veo31-video`
- `suno-audio`

## 节点 UI -> family 映射

### Text Node
用途：
- 输入文本 prompt
- 作为上游 prompt 源头
- 不直接调用 KIE 生成媒体
- 可以驱动下游 Image / Video / Audio 节点

必有字段：
- title
- prompt
- language
- tags
- negativePrompt（可选，仅传给支持的下游）

### Image Node
默认支持 family：
- `gpt4o-image`
- `flux-kontext`
- `market-image`

UI 下拉项：
- Provider Family
- Model
- Aspect Ratio / Size
- Enhance / Translate / Fallback
- Output Format
- Upload image（可选，用于编辑类或参考图）

推荐下拉：
- Provider Family: `gpt4o-image | flux-kontext | market-image`
- 当 family = `gpt4o-image`
  - Model 固定为 `gpt4o-image`
  - Size 先给：`1:1`
  - 高级项：`isEnhance`, `uploadCn`, `enableFallback`
- 当 family = `flux-kontext`
  - Model：`flux-kontext-pro | flux-kontext-max`
  - Aspect Ratio：`1:1 | 16:9 | 9:16 | 4:3 | 3:4`
  - Output Format：`jpeg | png`
  - Enable Translation：`true | false`
- 当 family = `market-image`
  - Model 从 `model-registry.ts` 读取
  - 输入参数由 registry 决定
  - 常见模型分组：
    - Google Imagen
    - GPT Image
    - Qwen
    - Ideogram
    - Recraft
    - Topaz
    - Flux-2
    - Seedream
    - Grok Imagine
    - Z-image

### Image Editor Node
默认支持 family：
- `flux-kontext`
- `market-image`

用途：
- 图片编辑
- 背景替换
- 图像增强 / 去背 / 放大
- 输入图 + prompt

必有字段：
- inputImageUrl / uploadedAssetId
- prompt
- model
- aspectRatio（可选）
- outputFormat（按 family 支持）

### Video Node
默认支持 family：
- `runway-video`
- `veo31-video`
- `market-video`

UI 下拉项：
- Provider Family
- Model
- Aspect Ratio
- Duration
- Quality / Resolution
- Enable Fallback
- Enable Translation
- Input Image / Input Video

当 family = `runway-video`
- Model：`runway-gen`
- Duration：`5 | 10`
- Aspect Ratio：`16:9 | 9:16`
- Quality：`720p | 1080p`
- Image URL：可选
- Watermark：可选

当 family = `veo31-video`
- Model：`veo3 | veo3_fast`
- Aspect Ratio：优先 `16:9`
- Seeds：整数
- Enable Fallback：布尔
- Enable Translation：布尔
- Generation Type：
  - `TEXT_2_VIDEO`
  - `IMAGE_2_VIDEO`
  - `REFERENCE_2_VIDEO`
- Image URLs：0~N

当 family = `market-video`
- Model 从 registry 读取
- 具体 `input` 字段以模型文档为准
- 常见模型组：
  - Kling
  - Bytedance / Seedance
  - Hailuo
  - Sora2
  - Wan
  - Topaz video upscale
  - Infinitalk
  - Grok Imagine Video

### Audio Node
默认支持 family：
- `suno-audio`
- `market-audio`

当 family = `suno-audio`
- Model：`V3_5 | V4 | V4_5 | V4_5PLUS | V4_5ALL | V5`
- customMode：`true | false`
- instrumental：`true | false`
- prompt
- style
- title
- negativeTags（可选）

当 family = `market-audio`
- 目前优先挂载 ElevenLabs Market 模型
- 具体字段由 registry 决定

### Upload Node
用途：
- 上传本地图片 / 视频 / 音频
- 通过你的后端上传到 KIE File Upload API 或你自己的存储
- 给其他节点提供可引用的资产 URL

字段：
- assetKind
- localFileName
- fileUrl
- downloadUrl
- expiresAt
- mimeType
- size

## 强制映射规则

- 节点 UI 不能直接写死原始接口字段
- 节点 UI 使用**统一业务字段**
- family adapter 再把业务字段转成具体 KIE 请求字段

例如：

### 统一业务字段
```ts
type CommonImageConfig = {
  prompt: string;
  ratio?: string;
  format?: 'png' | 'jpeg';
  inputImageUrl?: string;
  enhance?: boolean;
  translate?: boolean;
  fallback?: boolean;
};
```

### gpt4o-image 转换
```ts
{
  prompt,
  size: ratio,
  filesUrl: inputImageUrl ? [inputImageUrl] : [],
  isEnhance: enhance ?? false,
  enableFallback: fallback ?? false
}
```

### flux-kontext 转换
```ts
{
  prompt,
  aspectRatio: ratio,
  inputImage: inputImageUrl,
  outputFormat: format ?? 'jpeg',
  enableTranslation: translate ?? false
}
```

## 模型注册策略

必须维护 `templates/model-registry.ts`。
OpenClaw 不能临时硬编码模型名。

`model-registry.ts` 每项至少包含：

- `uiLabel`
- `family`
- `modelKey`
- `kind`
- `officialDocUrl`
- `adapter`
- `inputMode`
- `uiFields`
- `defaults`
