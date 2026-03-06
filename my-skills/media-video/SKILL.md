---
name: media-video
description: "AI视频生成skill。文生视频、图生视频、首尾帧、多镜头、视频转视频。支持：Kling、Seedance、Wan、Sora2、Runway、Hailuo、Veo、Grok。调用 kie.ai API。"
metadata:
  {"openclaw": {"emoji": "🎬"}}
---

# Media Video Skill — kie.ai 视频生成

## ⚙️ 默认参数（用户未指定时使用）

| 参数 | 默认值 | 可选范围 |
|------|--------|---------|
| 分辨率 | 720P | 480P / 720P / 1080P |
| 比例 | 16:9 | 16:9 / 9:16 / 1:1 |
| 时长 | 5s | 4s / 5s / 6s / 8s / 10s / 12s / 15s |
| 音频 | 无 | no_audio / with_audio |
| 模式 | std | std / pro |

**每次生成前告知用户：**
> 默认 720P、16:9、5秒、无音频。1080P/带音频/更长时长费用会增加，请确认。

---

## 📋 完整模型表

### 🏢 Kling AI

| 模型 | API model 字段 | 时长 | 分辨率 | Credits | USD | 推荐场景 |
|------|---------------|------|--------|---------|-----|---------|
| Kling 3.0 | `kling-3.0/video` | 5s | 720P 无音频 | 20 | $0.10 | 最新旗舰 ⭐ |
| Kling 3.0 | `kling-3.0/video` | 5s | 720P 带音频 | 30 | $0.15 | 原生音频 |
| Kling 3.0 | `kling-3.0/video` | 5s | 1080P 无音频 | 27 | $0.135 | 高清旗舰 |
| Kling 3.0 | `kling-3.0/video` | 5s | 1080P 带音频 | 40 | $0.20 | 高清+音频 |
| Kling 3.0 | `kling-3.0/video` | 10s | 720P 无音频 | 40 | $0.20 | 长视频 |
| Kling 3.0 | `kling-3.0/video` | 10s | 1080P 带音频 | 80 | $0.40 | 长视频高清 |
| Kling 2.6 | `kling-2.6/text-to-video` | 5s | 720P 无音频 | 55 | $0.275 | 高质量叙事 |
| Kling 2.6 | `kling-2.6/text-to-video` | 5s | 1080P 带音频 | 110 | $0.55 | 高清叙事 |
| Kling 2.6 | `kling-2.6/text-to-video` | 10s | 720P 无音频 | 110 | $0.55 | 长叙事 |
| Kling 2.6 | `kling-2.6/text-to-video` | 10s | 1080P 带音频 | 220 | $1.10 | 长高清叙事 |
| Kling 2.6 Motion | `kling-2.6/motion-control` | 标准 | 720P | 6 | $0.03 | 运动控制 |
| Kling 2.6 Motion | `kling-2.6/motion-control` | 标准 | 1080P | 9 | $0.045 | 高清运动控制 |
| Kling v2.5 Turbo | `kling/v2-5-turbo-text-to-video-pro` | 5s | 1080P | 42 | $0.21 | 快速高质量 |
| Kling v2.5 Turbo | `kling/v2-5-turbo-text-to-video-pro` | 10s | 1080P | 84 | $0.42 | 快速长视频 |
| Kling v2.1 Master | `kling/v2-1-master-text-to-video` | 5s | 1080P | 160 | $0.80 | 最高质量 |
| Kling v2.1 Master | `kling/v2-1-master-text-to-video` | 10s | 1080P | 320 | $1.60 | 最高质量长 |
| Kling v2.1 Pro | `kling/v2-1-pro` | 5s | 1080P | 50 | $0.25 | 专业级 |
| Kling v2.1 Pro | `kling/v2-1-pro` | 10s | 1080P | 100 | $0.50 | 专业级长 |
| Kling v2.1 Standard | `kling/v2-1-standard` | 5s | 720P | 25 | $0.125 | 标准质量 |
| Kling v2.1 Standard | `kling/v2-1-standard` | 10s | 720P | 50 | $0.25 | 标准长视频 |
| Kling AI Avatar Std | `kling/ai-avatar-standard` | 标准 | 标准 | 8 | $0.04 | AI数字人标准 |
| Kling AI Avatar Pro | `kling/ai-avatar-pro` | 标准 | 标准 | 16 | $0.08 | AI数字人专业 |

### 🏢 ByteDance — Seedance 系列

| 模型 | API model 字段 | 时长 | 分辨率 | Credits | USD | 推荐场景 |
|------|---------------|------|--------|---------|-----|---------|
| Seedance 1.5 Pro | `bytedance/seedance-1.5-pro` | 4s | 480P 无音频 | 7 | $0.035 | 低成本测试 |
| Seedance 1.5 Pro | `bytedance/seedance-1.5-pro` | 4s | 720P 无音频 | 14 | $0.07 | 标准质量 |
| Seedance 1.5 Pro | `bytedance/seedance-1.5-pro` | 4s | 1080P 无音频 | 30 | $0.15 | 高清 |
| Seedance 1.5 Pro | `bytedance/seedance-1.5-pro` | 4s | 1080P 带音频 | 60 | $0.30 | 高清+音频 |
| Seedance 1.5 Pro | `bytedance/seedance-1.5-pro` | 8s | 720P 无音频 | 28 | $0.14 | 中长视频 |
| Seedance 1.5 Pro | `bytedance/seedance-1.5-pro` | 8s | 1080P 无音频 | 60 | $0.30 | 高清中长 |
| Seedance 1.5 Pro | `bytedance/seedance-1.5-pro` | 8s | 1080P 带音频 | 120 | $0.60 | 高清中长+音频 |
| Seedance 1.5 Pro | `bytedance/seedance-1.5-pro` | 12s | 720P 带音频 | 84 | $0.42 | 长视频+音频 |
| Seedance 1.5 Pro | `bytedance/seedance-1.5-pro` | 12s | 1080P 带音频 | 180 | $0.90 | 高清长+音频 |
| Seedance V1 Pro | `bytedance/v1-pro-text-to-video` | 5s | 480P | 14 | $0.07 | 低成本 |
| Seedance V1 Pro | `bytedance/v1-pro-text-to-video` | 5s | 720P | 30 | $0.15 | 标准 |
| Seedance V1 Pro | `bytedance/v1-pro-text-to-video` | 10s | 1080P | 140 | $0.70 | 高清长 |
| Seedance V1 Lite | `bytedance/v1-lite-text-to-video` | 5s | 480P | 10 | $0.05 | 极低成本 |
| Seedance V1 Lite | `bytedance/v1-lite-text-to-video` | 10s | 1080P | 100 | $0.50 | 高清 |
| Seedance V1 Pro Fast | `bytedance/v1-pro-fast-image-to-video` | 5s | 720P | 16 | $0.08 | 快速图生视频 |
| Seedance V1 Pro Fast | `bytedance/v1-pro-fast-image-to-video` | 10s | 1080P | 72 | $0.36 | 快速高清 |

### 🏢 Wan 系列

| 模型 | API model 字段 | 时长 | 分辨率 | Credits | USD | 推荐场景 |
|------|---------------|------|--------|---------|-----|---------|
| Wan 2.6 T2V | `wan/2-6-text-to-video` | 5s | 720P | 70 | $0.35 | 长视频生成 |
| Wan 2.6 T2V | `wan/2-6-text-to-video` | 10s | 1080P | 210 | $1.05 | 高清长视频 |
| Wan 2.6 T2V | `wan/2-6-text-to-video` | 15s | 1080P | 315 | $1.575 | 超长视频 |
| Wan 2.6 I2V | `wan/2-6-image-to-video` | 5s | 720P | 70 | $0.35 | 图生视频 |
| Wan 2.6 I2V | `wan/2-6-image-to-video` | 10s | 1080P | 210 | $1.05 | 高清图生视频 |
| Wan 2.6 Flash T2V | `wan/2-6-flash-text-to-video` | 5s | 720P | 20 | $0.10 | 快速版 ⭐ |
| Wan 2.6 Flash I2V | `wan/2-6-flash-image-to-video` | 5s | 720P 无水印 | 40 | $0.20 | 快速图生视频 |
| Wan 2.6 Flash I2V | `wan/2-6-flash-image-to-video` | 10s | 1080P 无水印 | 120 | $0.60 | 快速高清 |
| Wan 2.6 V2V | `wan/2-6-video-to-video` | 5s | 1080P | 105 | $0.525 | 视频转视频 |
| Wan 2.6 V2V | `wan/2-6-video-to-video` | 10s | 1080P | 210 | $1.05 | 长视频转换 |
| Wan 2.5 T2V | `wan/2-5-text-to-video` | 5s | 720P | 60 | $0.30 | 稳定版 |
| Wan 2.5 T2V | `wan/2-5-text-to-video` | 10s | 1080P | 200 | $1.00 | 稳定高清 |
| Wan 2.2 Animate | `wan/2-2-animate-move` | 标准 | 480P | 6 | $0.03 | 图片动画化 |
| Wan 2.2 Animate | `wan/2-2-animate-move` | 标准 | 720P | 12.5 | $0.0625 | 高清动画 |
| Wan 2.2 A14B Turbo | `wan/2-2-a14b-image-to-video-turbo` | 标准 | 480P | 6 | $0.03 | 极速图生视频 |
| Wan 2.2 A14B Turbo | `wan/2-2-a14b-image-to-video-turbo` | 标准 | 720P | 12 | $0.06 | 极速高清 |

### 🏢 Sora 2（OpenAI）

| 模型 | API model 字段 | 时长 | 质量 | Credits | USD | 推荐场景 |
|------|---------------|------|------|---------|-----|---------|
| Sora 2 Stable | `sora-2/stable-video` | 10s | 标准 | 20 | $0.10 | 高质量稳定 |
| Sora 2 Stable | `sora-2/stable-video` | 15s | 标准 | 30 | $0.15 | 长稳定 |
| Sora 2 Video | `sora-2/video` | 10s | 无水印 | 3 | $0.015 | 低成本 |
| Sora 2 Video | `sora-2/video` | 15s | 无水印 | 5 | $0.025 | 低成本长 |
| Sora 2 Pro Standard | `sora-2/pro-standard` | 10s | 标准 | 75 | $0.375 | 专业级 |
| Sora 2 Pro Standard | `sora-2/pro-standard` | 15s | 标准 | 135 | $0.675 | 专业长 |
| Sora 2 Pro High | `sora-2/pro-high` | 10s | 高质量 | 165 | $0.825 | 旗舰质量 |
| Sora 2 Pro High | `sora-2/pro-high` | 15s | 高质量 | 315 | $1.575 | 旗舰长视频 |
| Sora 2 Remix | `sora-2/remix` | 10s | 无水印 | 6 | $0.03 | 视频混剪 |
| Sora 2 Storyboard | `sora-2/pro-storyboard` | 10s | 标准 | 75 | $0.375 | 多镜头故事板 |

### 🏢 Runway

| 模型 | API model 字段 | 时长 | 分辨率 | Credits | USD | 推荐场景 |
|------|---------------|------|--------|---------|-----|---------|
| Runway Gen4 Turbo | `runway/gen4-turbo` | 5s | 720P | 15 | $0.075 | 快速生成 |
| Runway Gen4 Turbo | `runway/gen4-turbo` | 10s | 720P | 30 | $0.15 | 快速长视频 |
| Runway Gen4 | `runway/gen4` | 5s | 1080P | 30 | $0.15 | 高清生成 |
| Runway Gen4 | `runway/gen4` | 8s | 720P | 30 | $0.15 | 中长视频 |
| Runway Gen4 | `runway/gen4` | 10s | 1080P | 60 | $0.30 | 高清长视频 |
| Runway Extend | `runway/extend` | +5s | 720P | 12 | $0.06 | 视频延伸 |
| Runway Extend | `runway/extend` | +5s | 1080P | 30 | $0.15 | 高清延伸 |
| Runway Aleph | `runway/aleph` | 标准 | 标准 | 90 | $0.45 | 高级生成 |

### 🏢 Hailuo（MiniMax）

| 模型 | API model 字段 | 时长 | 分辨率 | Credits | USD | 推荐场景 |
|------|---------------|------|--------|---------|-----|---------|
| Hailuo 02 T2V Std | `hailuo/02-text-to-video-standard` | 6s | 标准 | 30 | $0.15 | 标准质量 |
| Hailuo 02 T2V Std | `hailuo/02-text-to-video-standard` | 10s | 标准 | 50 | $0.25 | 长视频 |
| Hailuo 02 T2V Pro | `hailuo/02-text-to-video-pro` | 标准 | 标准 | 57 | $0.285 | 专业级 |
| Hailuo 02 I2V Std | `hailuo/02-image-to-video-standard` | 6s | 512P | 12 | $0.06 | 低成本图生视频 |
| Hailuo 02 I2V Std | `hailuo/02-image-to-video-standard` | 6s | 768P | 30 | $0.15 | 标准图生视频 |
| Hailuo 02 I2V Std | `hailuo/02-image-to-video-standard` | 10s | 768P | 50 | $0.25 | 长图生视频 |
| Hailuo 02 I2V Pro | `hailuo/02-image-to-video-pro` | 标准 | 标准 | 57 | $0.285 | 专业图生视频 |
| Hailuo 2.3 I2V Std | `hailuo/2-3-image-to-video-standard` | 6s | 768P | 25 | $0.125 | 新版标准 |
| Hailuo 2.3 I2V Pro | `hailuo/2-3-image-to-video-pro` | 6s | 768P | 40 | $0.20 | 新版专业 |

### 🏢 Google — Veo

| 模型 | API model 字段 | 时长 | 比例 | Credits | USD | 推荐场景 |
|------|---------------|------|------|---------|-----|---------|
| Veo Fast | `veo/video-fast-generate` | 标准 | 16:9 | 20 | $0.10 | 快速生成 |
| Veo Fast | `veo/video-fast-generate` | 标准 | 9:16 | 20 | $0.10 | 竖版快速 |
| Veo Quality | `veo/video-generate` | 标准 | 16:9 | 150 | $0.75 | 高质量 |
| Veo Quality | `veo/video-generate` | 标准 | 9:16 | 150 | $0.75 | 竖版高质量 |
| Veo Extend | `veo/video-extend` | +标准 | 标准 | 20 | $0.10 | 视频延伸 |
| Veo Material Fast | `veo/material-video-fast-generate` | 标准 | 标准 | 20 | $0.10 | 素材生成 |
| Veo 1080P | `veo/get-1080p-video` | 标准 | 标准 | 5 | $0.025 | 获取1080P版本 |
| Veo 4K | `veo/get-4k-video` | 标准 | 标准 | 40 | $0.20 | 获取4K版本 |

### 🏢 Grok — xAI

| 模型 | API model 字段 | 时长 | 分辨率 | Credits | USD | 推荐场景 |
|------|---------------|------|--------|---------|-----|---------|
| Grok T2V | `grok-imagine/text-to-video` | 6s | 480P | 10 | $0.05 | 低成本 |
| Grok T2V | `grok-imagine/text-to-video` | 6s | 720P | 20 | $0.10 | 标准 |
| Grok T2V | `grok-imagine/text-to-video` | 10s | 720P | 30 | $0.15 | 长视频 |
| Grok I2V | `grok-imagine/image-to-video` | 6s | 480P | 10 | $0.05 | 低成本图生视频 |
| Grok I2V | `grok-imagine/image-to-video` | 6s | 720P | 20 | $0.10 | 标准图生视频 |
| Grok I2V | `grok-imagine/image-to-video` | 10s | 720P | 30 | $0.15 | 长图生视频 |

### 🏢 Luma

| 模型 | API model 字段 | 任务 | Credits | USD | 推荐场景 |
|------|---------------|------|---------|-----|---------|
| Luma Modify | `luma/modify` | 视频修改 | 30 | $0.15 | 视频风格修改 |

### 🏢 Topaz — 视频增强

| 模型 | API model 字段 | 倍数 | Credits | USD | 推荐场景 |
|------|---------------|------|---------|-----|---------|
| Topaz Video Upscale | `topaz/video-upscale` | 2x | 8 | $0.04 | 视频超分2倍 |
| Topaz Video Upscale | `topaz/video-upscale` | 4x | 14 | $0.07 | 视频超分4倍 |

### 🏢 InfiniTalk — 数字人/唇形同步

| 模型 | API model 字段 | 分辨率 | Credits | USD | 推荐场景 |
|------|---------------|--------|---------|-----|---------|
| InfiniTalk from Audio | `infinitalk/from-audio` | 480P | 3 | $0.015 | 音频驱动数字人 |
| InfiniTalk from Audio | `infinitalk/from-audio` | 720P | 12 | $0.06 | 高清数字人 |
| InfiniTalk from Text | `infinitalk/from-text` | 480P | 0.15 | $0.00075 | 文字驱动数字人 |
| InfiniTalk from Text | `infinitalk/from-text` | 720P | 0.3 | $0.0015 | 高清文字数字人 |

---

## 🔌 API 调用规范

### 认证
```
POST https://api.kie.ai/api/v1/jobs/createTask
Authorization: Bearer {KIEAI_API_KEY}
Content-Type: application/json
```

### 文生视频（Kling 3.0，默认推荐）
```json
{
  "model": "kling-3.0/video",
  "callBackUrl": "",
  "input": {
    "mode": "std",
    "prompt": "A cat walking in a garden, cinematic lighting",
    "duration": "5",
    "aspect_ratio": "16:9",
    "with_audio": false
  }
}
```

### 图生视频（首尾帧控制）
```json
{
  "model": "kling-3.0/video",
  "input": {
    "mode": "std",
    "prompt": "smooth transition",
    "image_urls": ["https://start.jpg", "https://end.jpg"],
    "multi_shots": false,
    "duration": "5",
    "aspect_ratio": "16:9"
  }
}
```

### 多镜头模式（Kling 3.0）
```json
{
  "model": "kling-3.0/video",
  "input": {
    "mode": "std",
    "prompt": "Scene 1: @element_dog runs. Scene 2: @element_dog jumps.",
    "image_urls": ["https://start.jpg"],
    "multi_shots": true,
    "duration": "10"
  }
}
```

### 视频转视频（Wan 2.6）
```json
{
  "model": "wan/2-6-video-to-video",
  "input": {
    "prompt": "anime style",
    "video_url": "https://example.com/video.mp4",
    "duration": "5",
    "resolution": "1080p"
  }
}
```

### 查询任务结果
```
GET https://api.kie.ai/api/v1/jobs/getTask?taskId={taskId}
Authorization: Bearer {KIEAI_API_KEY}
```

---

## 💰 费用速查

| 需求 | 推荐模型 | 单价 | 月50条预算 |
|------|---------|------|-----------|
| 日常短视频 5s 720P | Kling 3.0 无音频 | $0.10 | ~$5 |
| 带音频 5s 720P | Kling 3.0 带音频 | $0.15 | ~$7.5 |
| 高清 5s 1080P | Seedance 1.5 Pro | $0.15 | ~$7.5 |
| 快速出片 | Wan 2.6 Flash | $0.10 | ~$5 |
| 顶级质量 10s | Kling v2.1 Master | $1.60 | ~$80 |
| 数字人唇同步 | InfiniTalk from Text 720P | $0.0015/s | 极低 |

---

## 🔄 使用流程

1. 判断任务类型：文生视频 / 图生视频 / 首尾帧 / 多镜头 / 视频转视频 / 延伸 / 数字人
2. 推荐模型 + 告知默认参数和价格
3. 用户确认 → 调用 createTask
4. 轮询结果（每5秒，最多3分钟）
5. 返回视频URL

## ⚠️ 注意事项
- 视频生成耗时 1-3 分钟，需异步等待
- 带音频比无音频贵约 50%
- 1080P 比 720P 贵约 50%
- 15s 比 5s 贵约 3 倍
- 首尾帧：image_urls=[首帧URL, 尾帧URL]
- 多镜头：image_urls=[首帧URL]，multi_shots=true
- prompt 建议英文，最多 2500 字符
- API Key 存在环境变量 `KIEAI_API_KEY`（值：`943650a08f4c9d76eb6991a8a5d23cfd`）
- 1 credit = $0.01 USD

---

## 🖥️ 本地模型（优先使用，免费）

> 目前视频类暂无本地模型。以后添加新的本地视频模型，告诉 Leon：模型名、端口、任务类型，Leon 会同步更新此文件。

### 本地 GPU 信息
- GPU: RTX 3080 Ti 12GB，CUDA 13.1
- nvidia-smi: `/usr/lib/wsl/lib/nvidia-smi`

### 启动本地服务参考
```bash
systemctl --user list-units | grep -E "video|wan|kling"
```
