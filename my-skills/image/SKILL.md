---
name: image
description: "AI图片生成/编辑/放大。用于：文生图、图生图、图片编辑、图片放大、去背景。按模型名调用，供应商无关。"
metadata:
  {"openclaw": {"emoji": "🖼️"}}
---

# Image Skill

## ⚙️ 默认参数
| 参数 | 默认值 | 可选 |
|------|--------|------|
| 分辨率 | 1K | 1K / 2K / 4K |
| 比例 | 1:1 | 1:1 / 16:9 / 9:16 / 4:3 / 3:4 |

**生成前告知用户：** 默认 1K、1:1，如需 2K/4K 或其他比例请说明。

---

## 📌 换供应商说明
每个模型块内有 `provider` 字段。换供应商时只改该模型的 provider 块：
- `base_url`：新供应商的 API 地址
- `auth`：新供应商的认证方式
- `model_id`：新供应商对应的模型名
- `input`：新供应商的请求字段

---

## 🖼️ 文生图模型

### Seedream 5.0 Lite
- 用途：日常文生图，性价比最高 ⭐
- 默认比例：1:1，支持 1:1 / 16:9 / 9:16 / 4:3 / 3:4
- 价格：$0.0275/张

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "seedream/5-lite-text-to-image",
  "input": {
    "prompt": "a beautiful sunset, photorealistic",
    "aspect_ratio": "1:1"
  }
}
```

---

### Seedream 4.5
- 用途：高质量创意图
- 价格：$0.025（1步）/ $0.065~$0.13（2步）

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "bytedance/seedream-v4-text-to-image",
  "input": {
    "prompt": "portrait of a woman, studio lighting",
    "aspect_ratio": "3:4"
  }
}
```

---

### FLUX.2 Pro
- 用途：专业写实图片
- 价格：1K $0.025 / 2K $0.035

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "flux-2/pro-text-to-image",
  "input": {
    "prompt": "cinematic landscape, golden hour",
    "image_size": "1k",
    "aspect_ratio": "16:9"
  }
}
```

---

### FLUX.2 Flex
- 用途：写实风格，高性价比
- 价格：1K $0.07 / 2K $0.12

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "flux-2/flex-text-to-image",
  "input": {
    "prompt": "futuristic city at night",
    "image_size": "1k",
    "aspect_ratio": "16:9"
  }
}
```

---

### GPT-Image 1.5
- 用途：精准文字渲染、复杂构图
- 价格：medium $0.02 / high $0.11

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "gpt-image/1.5-text-to-image",
  "input": {
    "prompt": "a poster with text 'Hello World'",
    "quality": "medium"
  }
}
```

---

### Ideogram V3
- 用途：文字排版、设计图
- 价格：TURBO $0.0175 / BALANCED $0.035 / QUALITY $0.05

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "ideogram/v3-text-to-image",
  "input": {
    "prompt": "minimalist logo design",
    "style_type": "DESIGN",
    "magic_prompt_option": "AUTO",
    "rendering_speed": "BALANCED"
  }
}
```

---

### Grok Imagine
- 用途：快速生图
- 价格：$0.02/张

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "grok-imagine/text-to-image",
  "input": {
    "prompt": "a cat sitting on a cloud",
    "aspect_ratio": "1:1"
  }
}
```

---

### Nano Banana Pro
- 用途：超高清 1K~4K
- 价格：1K/2K $0.04 / 4K $0.07

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "nano-banana-pro",
  "input": {
    "prompt": "ultra detailed landscape",
    "image_size": "4k",
    "aspect_ratio": "16:9"
  }
}
```

---

## 🖼️ 图生图 / 编辑模型

### Flux Kontext Pro（精准局部编辑）
- 用途：图片局部精准编辑
- 价格：$0.02/张

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "flux-kontext-pro",
  "input": {
    "prompt": "change background to snowy mountain",
    "image_url": "https://example.com/image.jpg"
  }
}
```

---

### Flux Kontext Max（高质量编辑）
- 用途：高质量图片编辑
- 价格：$0.04/张

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "flux-kontext-max",
  "input": {
    "prompt": "make it look like oil painting",
    "image_url": "https://example.com/image.jpg"
  }
}
```

---

### Seedream 5.0 Lite（图生图）
- 用途：快速图片改造
- 价格：$0.0275/张

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "seedream/5-lite-image-to-image",
  "input": {
    "prompt": "same scene but in anime style",
    "image_url": "https://example.com/image.jpg",
    "aspect_ratio": "1:1"
  }
}
```

---

### Qwen Image（风格转换）
- 用途：图片风格转换
- 价格：$0.02/张

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "qwen/image-to-image",
  "input": {
    "prompt": "convert to watercolor style",
    "image_url": "https://example.com/image.jpg"
  }
}
```

---

## 🖼️ 图片放大 / 处理

### Topaz Image Upscale（专业放大）
- 用途：图片超分放大
- 价格：2K $0.05 / 4K $0.10 / 8K $0.20

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "topaz/image-upscale",
  "input": {
    "image_url": "https://example.com/image.jpg",
    "scale": "4k"
  }
}
```

---

### Recraft 去背景（免费）
- 用途：抠图去背景
- 价格：免费

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "recraft/remove-background",
  "input": {
    "image_url": "https://example.com/image.jpg"
  }
}
```

---

### Grok Upscale
- 用途：图片超分
- 价格：$0.05/张

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "grok-imagine/upscale",
  "input": {
    "image_url": "https://example.com/image.jpg"
  }
}
```

---

## 🖥️ 本地模型
> 目前无本地图片模型。添加时告知：模型名、端口、任务类型，Leon 同步更新。

---

## 🔌 通用 API 规范

### 创建任务
```
POST {base_url}
Authorization: Bearer {KIEAI_API_KEY}
Content-Type: application/json

{
  "model": "{model_id}",
  "callBackUrl": "",
  "input": { ... }
}
```

### 查询结果
```
POST https://api.kie.ai/api/v1/playground/pageRecordListByDoris
# body: {"pageNum":1,"pageSize":5}
# 用 taskId 匹配 records[].taskId，state=="success" 时取 resultJson
Authorization: Bearer {KIEAI_API_KEY}
```

### 结果字段
```json
{
  "code": 200,
  "data": {
    "taskId": "xxx",
    "state": "success",
    "resultJson": "{\"result_urls\":[\"https://...image.png\"]}"
  }
}
```

---

## 💰 费用速查
| 用途 | 推荐模型 | 单价 |
|------|---------|------|
| 日常生图 | Seedream 5.0 Lite | $0.028 |
| 高质量 2K | FLUX.2 Pro | $0.035 |
| 精准编辑 | Flux Kontext Pro | $0.02 |
| 文字排版 | Ideogram V3 Turbo | $0.0175 |
| 超高清 4K | Nano Banana Pro | $0.07 |
| 去背景 | Recraft | 免费 |
| 放大 4K | Topaz | $0.10 |

## ⚠️ 注意
- prompt 建议英文
- image_url 需公开可访问
- KIEAI_API_KEY = `943650a08f4c9d76eb6991a8a5d23cfd`
- 1 credit = $0.01 USD
