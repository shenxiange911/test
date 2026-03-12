# KIE 模型矩阵（优先支持的图片 / 视频 / 音频模型）

> 说明  
> KIE 的 Market 会持续更新模型，完整最新列表应以官方 Market 为准。  
> 本文档列的是 **最适合你当前 React Flow 项目优先接入** 的模型集合。  
> OpenClaw 写代码时，第一阶段只允许使用本文件中的模型 key。

---

## 1. 图片模型

### 1.1 4o Image API（专线）
**用途**
- 文生图
- 带参考图的生成 / 变体
- 快速原型

**创建接口**
- `POST /api/v1/gpt4o-image/generate`

**查询接口**
- `GET /api/v1/gpt4o-image/record-info?taskId=...`

**下载直链**
- `POST /api/v1/gpt4o-image/download-url`

**官方示例字段**
```json
{
  "filesUrl": ["https://example.com/image.png"],
  "prompt": "A beautiful sunset over the mountains",
  "size": "1:1",
  "callBackUrl": "https://your-callback-url.com/callback",
  "isEnhance": false,
  "uploadCn": false,
  "enableFallback": false,
  "fallbackModel": "FLUX_MAX"
}
```

**推荐前端映射**
```ts
type FourOImageConfig = {
  prompt: string;
  size: "1:1" | "3:2" | "2:3" | "16:9" | "9:16";
  filesUrl?: string[];
  isEnhance?: boolean;
  enableFallback?: boolean;
  fallbackModel?: "FLUX_MAX";
};
```

### 1.2 Flux Kontext（专线）
**用途**
- 文生图
- 图片编辑
- 复杂图像修改

**创建接口**
- `POST /api/v1/flux/kontext/generate`

**查询接口**
- `GET /api/v1/flux/kontext/record-info?taskId=...`

**关键规则**
- Text-to-image：提供 `prompt` + `aspectRatio`
- Image editing：提供 `prompt` + `inputImage`
- `aspectRatio` 可选；不传时保留原图比例
- 官方说明 prompt 只支持英文

**推荐映射**
```ts
type FluxKontextConfig = {
  model: "flux-kontext-pro" | "flux-kontext-max";
  prompt: string;
  aspectRatio?: "1:1" | "3:2" | "2:3" | "16:9" | "9:16";
  inputImage?: string;
};
```

### 1.3 GPT Image 1.5（Market）
**用途**
- 文生图
- 图生图

**推荐 model key**
- `gpt-image/1-5-text-to-image`
- `gpt-image/1-5-image-to-image`

**常见参数（来自官方示例）**
```json
{
  "model": "gpt-image/1-5-text-to-image",
  "input": {
    "prompt": "A cinematic poster of a futuristic city",
    "aspect_ratio": "1:1",
    "quality": "medium"
  }
}
```

图生图：
```json
{
  "model": "gpt-image/1-5-image-to-image",
  "input": {
    "image_urls": ["https://..."],
    "prompt": "Replace the clothes with a white sci-fi jacket",
    "aspect_ratio": "3:2",
    "quality": "medium"
  }
}
```

**推荐映射**
```ts
type GPTImage15Config = {
  prompt: string;
  aspect_ratio: "1:1" | "3:2" | "2:3" | "16:9" | "9:16";
  quality: "low" | "medium" | "high";
  image_urls?: string[];
};
```

### 1.4 Seedream 4.5（Market）
**用途**
- 高质量文生图
- 品宣视觉
- 摄影感 / 写实感

**推荐 model key**
- `seedream/4-5-text-to-image`
- `seedream/4-5-edit`

**官方示例常见字段**
- `prompt`
- `aspect_ratio`
- `quality`

**推荐映射**
```ts
type Seedream45Config = {
  prompt: string;
  aspect_ratio: "1:1" | "16:9" | "9:16" | "4:3" | "3:4";
  quality: "basic" | "standard" | "high";
  image_urls?: string[];
};
```

### 1.5 Google Imagen / Nano Banana（Market）
**推荐 model key**
- `google/imagen4-fast`
- `google/imagen4`
- `google/imagen4-ultra`
- `google/nano-banana`
- `google/nano-banana-edit`

**建议**
- `imagen4-fast`：默认快速模型
- `imagen4`：平衡
- `imagen4-ultra`：高质量
- `nano-banana-edit`：编辑

---

## 2. 视频模型

### 2.1 Runway（专线）
**创建接口**
- `POST /api/v1/runway/generate`

**查询接口**
- `GET /api/v1/runway/record-info?taskId=...`

**官方示例**
```json
{
  "prompt": "A fluffy orange cat dancing energetically in a colorful room with disco lights",
  "imageUrl": "https://example.com/cat-image.jpg",
  "model": "runway-duration-5-generate",
  "waterMark": "kie.ai",
  "callBackUrl": "https://api.example.com/callback"
}
```

**推荐映射**
```ts
type RunwayConfig = {
  prompt: string;
  imageUrl?: string;
  model: "runway-duration-5-generate" | "runway-duration-10-generate";
  waterMark?: string;
};
```

### 2.2 Veo 3.1（专线）
**创建接口**
- `POST /api/v1/veo/generate`

**查询接口**
- `GET /api/v1/veo/record-info?taskId=...`

**官方能力**
- `TEXT_2_VIDEO`
- `FIRST_AND_LAST_FRAMES_2_VIDEO`
- `REFERENCE_2_VIDEO`
- 支持 `16:9` / `9:16`
- 支持 1080P / 4K（4K 需单独路线）
- 默认自带背景音轨

**官方示例**
```json
{
  "prompt": "A dog playing in a park",
  "imageUrls": [
    "http://example.com/image1.jpg",
    "http://example.com/image2.jpg"
  ],
  "model": "veo3_fast",
  "watermark": "MyBrand",
  "callBackUrl": "http://your-callback-url.com/complete",
  "aspect_ratio": "16:9",
  "seeds": 12345,
  "enableFallback": false,
  "enableTranslation": true,
  "generationType": "REFERENCE_2_VIDEO"
}
```

**推荐映射**
```ts
type VeoConfig = {
  prompt: string;
  imageUrls?: string[];
  model: "veo3_fast" | "veo3_quality";
  watermark?: string;
  aspect_ratio?: "16:9" | "9:16" | "auto";
  seeds?: number;
  enableFallback?: boolean;
  enableTranslation?: boolean;
  generationType:
    | "TEXT_2_VIDEO"
    | "FIRST_AND_LAST_FRAMES_2_VIDEO"
    | "REFERENCE_2_VIDEO";
};
```

### 2.3 Kling 3.0（Market）
**model key**
- `kling-3.0/video`

**官方示例**
```json
{
  "model": "kling-3.0/video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "In a bright rehearsal room, sunlight streams through the window@element_dog",
    "image_urls": ["https://...png"],
    "sound": true,
    "duration": "5",
    "aspect_ratio": "16:9",
    "mode": "pro",
    "multi_shots": false,
    "multi_prompt": [
      { "prompt": "a happy dog in running@element_cat", "duration": 3 },
      { "prompt": "a happy dog play with a cat@element_dog", "duration": 3 }
    ],
    "kling_elements": [
      {
        "name": "element_dog",
        "description": "dog",
        "element_input_urls": ["https://...", "https://..."]
      }
    ]
  }
}
```

**推荐映射**
```ts
type Kling30Config = {
  prompt: string;
  image_urls?: string[];
  sound?: boolean;
  duration: "5" | "10";
  aspect_ratio: "16:9" | "9:16" | "1:1";
  mode: "standard" | "pro";
  multi_shots?: boolean;
  multi_prompt?: Array<{ prompt: string; duration: number }>;
  kling_elements?: Array<{
    name: string;
    description: string;
    element_input_urls: string[];
  }>;
};
```

### 2.4 Wan 2.6（Market）
**推荐 model key**
- `wan/2-6-image-to-video`
- `wan/2-6-text-to-video`
- `wan/2-6-video-to-video`

**官方示例（图生视频）**
```json
{
  "model": "wan/2-6-image-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "Anthropomorphic fox singing in the rain",
    "image_urls": ["https://...webp"],
    "duration": "5",
    "resolution": "1080p"
  }
}
```

**推荐映射**
```ts
type Wan26ImageToVideoConfig = {
  prompt: string;
  image_urls: string[];
  duration: "5" | "10";
  resolution: "720p" | "1080p";
};
```

### 2.5 Sora2（Market）
**推荐 model key**
- `sora-2-image-to-video`
- `sora-2-text-to-video`
- `sora-2-pro-image-to-video`
- `sora-2-pro-text-to-video`

**官方示例**
```json
{
  "model": "sora-2-image-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "progressCallBackUrl": "https://your-domain.com/api/v1/jobs/progressCallBackUrl",
  "input": {
    "prompt": "A claymation conductor leads an orchestra",
    "image_urls": ["https://...jpg"],
    "aspect_ratio": "landscape",
    "n_frames": "10",
    "remove_watermark": true,
    "character_id_list": ["example_123456789"]
  }
}
```

**推荐映射**
```ts
type Sora2Config = {
  prompt: string;
  image_urls?: string[];
  aspect_ratio: "landscape" | "portrait" | "square";
  n_frames: string;
  remove_watermark?: boolean;
  character_id_list?: string[];
};
```

---

## 3. 音频模型

### 3.1 ElevenLabs TTS（Market）
**推荐 model key**
- `elevenlabs/text-to-speech-multilingual-v2`
- `elevenlabs/text-to-speech-turbo-2-5`
- `elevenlabs/text-to-dialogue-v3`

**官方示例**
```json
{
  "model": "elevenlabs/text-to-speech-multilingual-v2",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "text": "Unlock powerful API with Kie.ai!",
    "voice": "Rachel",
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0,
    "speed": 1,
    "timestamps": false,
    "previous_text": "",
    "next_text": "",
    "language_code": ""
  }
}
```

**推荐映射**
```ts
type ElevenLabsTTSConfig = {
  text: string;
  voice: string;
  stability?: number;
  similarity_boost?: number;
  style?: number;
  speed?: number;
  timestamps?: boolean;
  previous_text?: string;
  next_text?: string;
  language_code?: string;
};
```

### 3.2 Suno Music（专线）
**创建接口**
- `POST /api/v1/generate`

**查询接口**
- `GET /api/v1/generate/record-info?taskId=...`

**模式**
- `customMode: false`
  - 只要 `prompt`
- `customMode: true`
  - 如果 `instrumental: true`：`style` + `title` 必填
  - 如果 `instrumental: false`：`style` + `prompt` + `title` 必填

**官方示例**
```json
{
  "prompt": "A calm and relaxing piano track with soft melodies",
  "customMode": true,
  "instrumental": true,
  "model": "V4",
  "callBackUrl": "https://api.example.com/callback",
  "style": "Classical",
  "title": "Peaceful Piano Meditation",
  "negativeTags": "Heavy Metal, Upbeat Drums",
  "vocalGender": "m",
  "styleWeight": 0.65,
  "weirdnessConstraint": 0.65,
  "audioWeight": 0.65,
  "personaId": "persona_123",
  "personaModel": "style_persona"
}
```

**推荐映射**
```ts
type SunoConfig = {
  prompt: string;
  customMode: boolean;
  instrumental: boolean;
  model: "V4" | "V4_5" | "V4_5PLUS" | "V4_5ALL" | "V5";
  style?: string;
  title?: string;
  negativeTags?: string;
  vocalGender?: "m" | "f";
  styleWeight?: number;
  weirdnessConstraint?: number;
  audioWeight?: number;
  personaId?: string;
  personaModel?: string;
};
```

---

## 4. 你项目第一阶段允许的 modelKey

```ts
type SupportedModelKey =
  | "4o-image"
  | "flux-kontext-pro"
  | "flux-kontext-max"
  | "gpt-image-1.5-tti"
  | "gpt-image-1.5-iti"
  | "seedream-4.5-tti"
  | "seedream-4.5-edit"
  | "imagen4-fast"
  | "nano-banana-edit"
  | "runway-generate"
  | "veo3-fast"
  | "veo3-quality"
  | "kling-3-video"
  | "wan-2.6-i2v"
  | "sora2-i2v"
  | "elevenlabs-tts-multi-v2"
  | "elevenlabs-dialogue-v3"
  | "suno-generate";
```
