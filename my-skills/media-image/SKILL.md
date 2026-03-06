---
name: media-image
description: "AI图片生成/编辑/放大skill。用于：文生图、图生图、图片编辑、图片放大、去背景。支持模型：FLUX.2、Seedream、GPT-Image、Grok、Ideogram、Recraft、Qwen、Nano Banana、Topaz。调用 kie.ai API。"
metadata:
  {"openclaw": {"emoji": "🖼️"}}
---

# Media Image Skill — kie.ai 图片生成

## ⚙️ 默认参数（用户未指定时使用）

| 参数 | 默认值 | 可选范围 |
|------|--------|---------|
| 分辨率 | 1K (1024px) | 1K / 2K / 4K |
| 比例 | 1:1 | 1:1 / 16:9 / 9:16 / 4:3 / 3:4 |
| 模型 | seedream/5-lite-text-to-image | 见下方模型表 |
| 质量 | standard | standard / high |

**每次生成前告知用户：**
> 默认 1K 分辨率、1:1 比例，如需 2K/4K 或其他比例请说明（费用会增加）

---

## 📋 完整模型表

### 🏢 Black Forest Labs — FLUX 系列

| 模型名 | API model 字段 | 任务 | 分辨率 | Credits | USD | 推荐场景 |
|--------|---------------|------|--------|---------|-----|---------|
| FLUX.2 Flex | `flux-2/flex-text-to-image` | 文生图 | 1K | 14 | $0.07 | 写实风格 |
| FLUX.2 Flex | `flux-2/flex-text-to-image` | 文生图 | 2K | 24 | $0.12 | 高清写实 |
| FLUX.2 Flex | `flux-2/flex-image-to-image` | 图生图 | 1K | 14 | $0.07 | 图片改风格 |
| FLUX.2 Flex | `flux-2/flex-image-to-image` | 图生图 | 2K | 24 | $0.12 | 高清改风格 |
| FLUX.2 Pro | `flux-2/pro-text-to-image` | 文生图 | 1K | 5 | $0.025 | 专业写实 |
| FLUX.2 Pro | `flux-2/pro-text-to-image` | 文生图 | 2K | 7 | $0.035 | 专业高清 |
| FLUX.2 Pro | `flux-2/pro-image-to-image` | 图生图 | 1K | 5 | $0.025 | 精准编辑 |
| FLUX.2 Pro | `flux-2/pro-image-to-image` | 图生图 | 2K | 7 | $0.035 | 精准高清编辑 |
| Flux Kontext Pro | `flux-kontext-pro` | 图生图编辑 | 1K | 4 | $0.02 | 精准局部编辑 |
| Flux Kontext Max | `flux-kontext-max` | 图生图编辑 | 2K | 8 | $0.04 | 高质量编辑 |

### 🏢 ByteDance — Seedream 系列

| 模型名 | API model 字段 | 任务 | Credits | USD | 推荐场景 |
|--------|---------------|------|---------|-----|---------|
| Seedream 5.0 Lite | `seedream/5-lite-text-to-image` | 文生图 | 5.5 | $0.0275 | 日常生图，性价比最高 ⭐ |
| Seedream 5.0 Lite | `seedream/5-lite-image-to-image` | 图生图 | 5.5 | $0.0275 | 快速图片改造 |
| Seedream 4.5 | `bytedance/seedream-v4-text-to-image` | 文生图 | 5 | $0.025 | 高质量创意图 |
| Seedream 4.5 Edit | `bytedance/seedream-v4-edit` | 图片编辑 | 5 | $0.025 | 精准编辑 |
| Seedream 4.5 (2步) | `bytedance/seedream-v4-text-to-image` | 文生图 | 13~26 | $0.065~$0.13 | 超高质量 |

### 🏢 OpenAI — GPT-Image 系列

| 模型名 | API model 字段 | 任务 | 质量 | Credits | USD | 推荐场景 |
|--------|---------------|------|------|---------|-----|---------|
| GPT-Image 1.5 | `gpt-image/1.5-text-to-image` | 文生图 | medium | 4 | $0.02 | 精准文字渲染 |
| GPT-Image 1.5 | `gpt-image/1.5-text-to-image` | 文生图 | high | 22 | $0.11 | 超高质量 |
| GPT-Image 1.5 | `gpt-image/1.5-image-to-image` | 图生图 | medium | 4 | $0.02 | 图片编辑 |
| GPT-Image 1.5 | `gpt-image/1.5-image-to-image` | 图生图 | high | 22 | $0.11 | 高质量编辑 |

### 🏢 Google — Nano Banana / Imagen 系列

| 模型名 | API model 字段 | 任务 | Credits | USD | 推荐场景 |
|--------|---------------|------|---------|-----|---------|
| Nano Banana | `google/nano-banana` | 文生图 | 3 | $0.015 | 快速生图 |
| Nano Banana Edit | `google/nano-banana-edit` | 图生图 | 3 | $0.015 | 图片编辑 |
| Nano Banana Reframe | `google/nano-banana-reframe` | 图生图 | 4 | $0.02 | 比例重构 |
| Nano Banana Pro 1/2K | `nano-banana-pro` | 文生图 | 8 | $0.04 | 高清生图 |
| Nano Banana Pro 4K | `nano-banana-pro` | 文生图 | 14 | $0.07 | 超高清 4K |
| Imagen 4 Fast | `google/imagen4` | 文生图 | 4 | $0.02 | 快速高质量 |
| Imagen 4 Default | `google/imagen4` | 文生图 | 8 | $0.04 | 标准质量 |
| Imagen 4 Ultra | `google/imagen4` | 文生图 | 12 | $0.06 | 旗舰质量 |

### 🏢 Grok — xAI

| 模型名 | API model 字段 | 任务 | Credits | USD | 推荐场景 |
|--------|---------------|------|---------|-----|---------|
| Grok Imagine | `grok-imagine/text-to-image` | 文生图 | 4 | $0.02 | 快速生图 |
| Grok Imagine | `grok-imagine/image-to-image` | 图生图 | 4 | $0.02 | 图片改造 |
| Grok Upscale | `grok-imagine/upscale` | 图片放大 | 10 | $0.05 | 图片超分 |

### 🏢 Ideogram

| 模型名 | API model 字段 | 任务 | 质量 | Credits | USD | 推荐场景 |
|--------|---------------|------|------|---------|-----|---------|
| Ideogram V3 | `ideogram/v3-text-to-image` | 文生图 | TURBO | 3.5 | $0.0175 | 快速文字排版 |
| Ideogram V3 | `ideogram/v3-text-to-image` | 文生图 | BALANCED | 7 | $0.035 | 均衡质量 |
| Ideogram V3 | `ideogram/v3-text-to-image` | 文生图 | QUALITY | 10 | $0.05 | 高质量 |
| Ideogram V3 Edit | `ideogram/v3-edit` | 图生图 | TURBO | 3.5 | $0.0175 | 快速编辑 |
| Ideogram V3 Edit | `ideogram/v3-edit` | 图生图 | BALANCED | 7 | $0.035 | 均衡编辑 |
| Ideogram V3 Edit | `ideogram/v3-edit` | 图生图 | QUALITY | 10 | $0.05 | 高质量编辑 |
| Ideogram V3 Remix | `ideogram/v3-remix` | 图生图 | TURBO | 3.5 | $0.0175 | 快速混合 |
| Ideogram V3 Remix | `ideogram/v3-remix` | 图生图 | BALANCED | 7 | $0.035 | 均衡混合 |
| Ideogram V3 Remix | `ideogram/v3-remix` | 图生图 | QUALITY | 10 | $0.05 | 高质量混合 |
| Ideogram Reframe | `ideogram/reframe` | 图生图 | BALANCED | 7 | $0.035 | 比例重构 |
| Ideogram Reframe | `ideogram/reframe` | 图生图 | QUALITY | 10 | $0.05 | 高质量重构 |

### 🏢 Qwen

| 模型名 | API model 字段 | 任务 | Credits | USD | 推荐场景 |
|--------|---------------|------|---------|-----|---------|
| Qwen Z-Image | `qwen/z-image` | 文生图 | 0.8 | $0.004 | 极低成本生图 |
| Qwen Image | `qwen/image-to-image` | 图生图 | 4 | $0.02 | 风格转换 |
| Qwen Image Edit | `qwen/image-edit` | 图生图 | 5/MP | $0.03/MP | 精准编辑 |

### 🏢 Recraft

| 模型名 | API model 字段 | 任务 | Credits | USD | 推荐场景 |
|--------|---------------|------|---------|-----|---------|
| Recraft 去背景 | `recraft/remove-background` | 图生图 | 1 | 免费 | 抠图去背景 |
| Recraft Crisp Upscale | `recraft/crisp-upscale` | 图片放大 | 0.5 | $0.0025 | 超低成本放大 |

### 🏢 Topaz — 专业放大

| 模型名 | API model 字段 | 任务 | 倍数 | Credits | USD | 推荐场景 |
|--------|---------------|------|------|---------|-----|---------|
| Topaz Image Upscale | `topaz/image-upscale` | 图片放大 | 2K | 10 | $0.05 | 标准放大 |
| Topaz Image Upscale | `topaz/image-upscale` | 图片放大 | 4K | 20 | $0.10 | 高清放大 |
| Topaz Image Upscale | `topaz/image-upscale` | 图片放大 | 8K | 40 | $0.20 | 超高清放大 |

---

## 🔌 API 调用规范

### 认证
```
POST https://api.kie.ai/api/v1/jobs/createTask
Authorization: Bearer {KIEAI_API_KEY}
Content-Type: application/json
```

### 文生图（Seedream 5.0 Lite，默认推荐）
```json
{
  "model": "seedream/5-lite-text-to-image",
  "input": {
    "prompt": "a beautiful sunset over mountains, photorealistic, 8k",
    "aspect_ratio": "1:1"
  }
}
```

### 文生图（FLUX.2 Pro 2K）
```json
{
  "model": "flux-2/pro-text-to-image",
  "input": {
    "prompt": "portrait of a woman, studio lighting",
    "image_size": "2k",
    "aspect_ratio": "3:4"
  }
}
```

### 图生图（Flux Kontext Pro）
```json
{
  "model": "flux-kontext-pro",
  "input": {
    "prompt": "change background to snowy mountain",
    "image_url": "https://example.com/image.jpg"
  }
}
```

### 图片放大（Topaz 4K）
```json
{
  "model": "topaz/image-upscale",
  "input": {
    "image_url": "https://example.com/image.jpg",
    "scale": "4k"
  }
}
```

### 去背景（Recraft，免费）
```json
{
  "model": "recraft/remove-background",
  "input": {
    "image_url": "https://example.com/image.jpg"
  }
}
```

### 查询任务结果
```
GET https://api.kie.ai/api/v1/jobs/getTask?taskId={taskId}
Authorization: Bearer {KIEAI_API_KEY}
```

### 结果字段
```json
{
  "data": {
    "taskId": "xxx",
    "state": "success",
    "result_urls": ["https://...image.png"]
  }
}
```

---

## 💰 费用速查

| 需求 | 推荐模型 | 单价 | 月100张预算 |
|------|---------|------|------------|
| 日常生图 1K | Seedream 5.0 Lite | $0.028 | ~$2.8 |
| 高质量 2K | FLUX.2 Pro | $0.035 | ~$3.5 |
| 精准编辑 | Flux Kontext Pro | $0.02 | ~$2.0 |
| 文字排版 | Ideogram V3 Turbo | $0.0175 | ~$1.75 |
| 超高清 4K | Nano Banana Pro | $0.07 | ~$7.0 |
| 去背景 | Recraft | 免费 | $0 |
| 图片放大 4K | Topaz | $0.10/张 | ~$10 |

---

## 🔄 使用流程

1. 判断任务类型：文生图 / 图生图 / 编辑 / 放大 / 去背景
2. 推荐模型 + 告知默认参数和价格
3. 用户确认 → 调用 createTask
4. 轮询结果（每3秒，最多60秒）
5. 返回图片URL

## ⚠️ 注意事项
- prompt 建议英文，效果更好
- image_url 需要公开可访问的 URL
- API Key 存在环境变量 `KIEAI_API_KEY`（值：`943650a08f4c9d76eb6991a8a5d23cfd`）
- 1 credit = $0.01 USD
- 当前余额：9218 credits（$92.18）

---

## 🖥️ 本地模型（优先使用，免费）

> 目前图片类暂无本地模型。以后添加新的本地图片模型，告诉 Leon：模型名、端口、任务类型，Leon 会同步更新此文件。

### 启动本地服务参考
```bash
systemctl --user list-units | grep -E "image|diffusion|comfy"
```
