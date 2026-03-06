---
name: video
description: "AI视频生成/编辑。用于：文生视频、图生视频、首尾帧控制、多镜头、视频转视频、视频延伸、数字人唇同步。按模型名调用，供应商无关。"
metadata:
  {"openclaw": {"emoji": "🎬"}}
---

# Video Skill

## ⚙️ 默认参数
| 参数 | 默认值 | 可选 |
|------|--------|------|
| 分辨率 | 720p | 480p / 720p / 1080p |
| 比例 | 16:9 | 16:9 / 9:16 / 1:1 |
| 时长 | 5s | 4s/5s/6s/8s/10s/12s/15s（视模型） |
| 音频 | 无 | sound:false / sound:true |
| 模式 | std | std / pro |

**生成前告知用户：** 默认 720p、16:9、5秒、无音频。1080p/带音频/更长时长费用会增加，请确认。

---

## 📌 换供应商说明
每个模型块内有 provider 字段。换供应商时只改该模型的 provider 块（base_url / auth / model_id / input 字段名）。

---

## 🎬 文生视频模型

### Kling 3.0（旗舰，多镜头+原生音频）
- 用途：最新旗舰，支持多镜头叙事、原生音频、首尾帧 ⭐
- 默认：720p / 5s / 无音频
- 价格：720p-5s-无音频 $0.10，720p-5s-带音频 $0.15，1080p-5s-带音频 $0.20

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "kling-3.0/video",
  "input": {
    "mode": "std",
    "prompt": "A cat walking in a garden, cinematic lighting",
    "duration": "5",
    "aspect_ratio": "16:9",
    "sound": false
  }
}
```

**图生视频（首尾帧）：**
```json
{
  "model": "kling-3.0/video",
  "input": {
    "mode": "std",
    "prompt": "smooth transition",
    "image_urls": ["https://start.jpg", "https://end.jpg"],
    "multi_shots": false,
    "duration": "5",
    "aspect_ratio": "16:9",
    "sound": false
  }
}
```

**多镜头模式：**
```json
{
  "model": "kling-3.0/video",
  "input": {
    "mode": "std",
    "prompt": "Scene 1: @element_dog runs. Scene 2: @element_dog jumps.",
    "image_urls": ["https://start.jpg"],
    "multi_shots": true,
    "duration": "10",
    "kling_elements": [
      {
        "name": "element_dog",
        "description": "dog",
        "element_input_urls": ["https://dog1.jpg", "https://dog2.jpg"]
      }
    ]
  }
}
```

---

### Kling v2.1 Master（最高质量）
- 用途：最高质量，适合商业级输出
- 价格：5s $0.80 / 10s $1.60

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "kling/v2-1-master-text-to-video",
  "input": {
    "duration": "5",
    "aspect_ratio": "16:9",
    "prompt": "cinematic scene description"
  }
}
```

**图生视频（首尾帧）：**
```json
{
  "model": "kling/v2-1-master-image-to-video",
  "input": {
    "duration": "5",
    "image_url": "https://start.jpg",
    "tail_image_url": "https://end.jpg",
    "prompt": "smooth transition"
  }
}
```

---

### Kling v2.1 Pro
- 用途：专业级
- 价格：5s $0.25 / 10s $0.50

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "kling/v2-1-pro",
  "input": {
    "duration": "5",
    "aspect_ratio": "16:9",
    "prompt": "scene description"
  }
}
```

---

### Kling v2.1 Standard
- 用途：标准质量，性价比
- 价格：5s $0.125 / 10s $0.25

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "kling/v2-1-standard",
  "input": {
    "duration": "5",
    "aspect_ratio": "16:9",
    "prompt": "scene description"
  }
}
```

---

### Kling v2.5 Turbo（快速高质量）
- 用途：快速生成，质量好
- 价格：5s $0.21 / 10s $0.42

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "kling/v2-5-turbo-text-to-video-pro",
  "input": {
    "duration": "5",
    "aspect_ratio": "16:9",
    "prompt": "scene description"
  }
}
```

---

### Kling 2.6（高质量叙事）
- 用途：高质量叙事视频
- 价格：5s-720p-无音频 $0.275，10s-1080p-带音频 $1.10

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "kling-2.6/text-to-video",
  "input": {
    "duration": "5",
    "aspect_ratio": "16:9",
    "prompt": "scene description",
    "sound": false
  }
}
```

---

### Seedance 1.5 Pro（电影级+音频）
- 用途：电影级质量，支持原生音频
- 默认：480p / 4s / 无音频
- 价格：480p-4s $0.035，1080p-8s-带音频 $0.60

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "bytedance/seedance-1.5-pro",
  "input": {
    "duration": "4",
    "aspect_ratio": "16:9",
    "prompt": "scene description",
    "resolution": "720p"
  }
}
```

---

### Seedance V1 Pro
- 用途：稳定生产
- 价格：5s-720p $0.15，10s-1080p $0.70

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "bytedance/v1-pro-text-to-video",
  "input": {
    "duration": "5",
    "aspect_ratio": "16:9",
    "prompt": "scene description",
    "resolution": "720p"
  }
}
```

---

### Wan 2.6（长视频）
- 用途：长视频生成，最长15s
- 价格：5s-720p $0.35，10s-1080p $1.05，15s-1080p $1.575

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "wan/2-6-text-to-video",
  "input": {
    "duration": "5",
    "aspect_ratio": "16:9",
    "prompt": "scene description",
    "resolution": "720p"
  }
}
```

---

### Wan 2.6 Flash（快速版）
- 用途：快速出片，性价比高 ⭐
- 价格：5s-720p $0.10，10s-1080p $0.60

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "wan/2-6-flash-text-to-video",
  "input": {
    "duration": "5",
    "aspect_ratio": "16:9",
    "prompt": "scene description",
    "resolution": "720p"
  }
}
```

---

### Sora 2 Stable（高质量稳定）
- 用途：高质量稳定生成
- 价格：10s $0.10，15s $0.15

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "sora-2/stable-video",
  "input": {
    "duration": "10",
    "aspect_ratio": "16:9",
    "prompt": "scene description"
  }
}
```

---

### Runway Gen4 Turbo（快速）
- 用途：快速生成
- 价格：5s-720p $0.075，10s-720p $0.15

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "runway/gen4-turbo",
  "input": {
    "duration": "5",
    "aspect_ratio": "16:9",
    "prompt": "scene description"
  }
}
```

---

### Hailuo 02（MiniMax）
- 用途：标准质量
- 价格：6s $0.15，10s $0.25

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "hailuo/02-text-to-video-standard",
  "input": {
    "duration": "6",
    "aspect_ratio": "16:9",
    "prompt": "scene description"
  }
}
```

---

### Veo Fast（Google）
- 用途：快速生成
- 价格：$0.10

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "veo/video-fast-generate",
  "input": {
    "aspect_ratio": "16:9",
    "prompt": "scene description"
  }
}
```

---

### Grok Video（xAI）
- 用途：低成本快速
- 价格：6s-720p $0.10，10s-720p $0.15

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "grok-imagine/text-to-video",
  "input": {
    "duration": "6",
    "aspect_ratio": "16:9",
    "prompt": "scene description"
  }
}
```

---

## 🎬 视频转视频

### Wan 2.6 Video-to-Video
- 用途：视频风格转换
- 价格：5s $0.525，10s $1.05

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "wan/2-6-video-to-video",
  "input": {
    "prompt": "anime style",
    "video_url": "https://example.com/video.mp4",
    "duration": "5",
    "resolution": "1080p"
  }
}
```

---

## 🎬 视频延伸

### Runway Extend
- 用途：视频延伸 +5s
- 价格：720p $0.06，1080p $0.15

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "runway/extend",
  "input": {
    "video_url": "https://example.com/video.mp4",
    "prompt": "continue the scene"
  }
}
```

---

## 🎬 视频放大

### Topaz Video Upscale
- 用途：视频超分放大
- 价格：2x $0.04，4x $0.07

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "topaz/video-upscale",
  "input": {
    "video_url": "https://example.com/video.mp4",
    "scale": "4x"
  }
}
```

---

## 🎬 数字人 / 唇形同步

### InfiniTalk（文字/音频驱动数字人）
- 用途：数字人唇形同步
- 价格：文字-480p $0.00075/s，音频-720p $0.06/s

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "infinitalk/from-text",
  "input": {
    "text": "你好，欢迎使用数字人服务",
    "image_url": "https://example.com/avatar.jpg",
    "resolution": "720p"
  }
}
```

---

## 🖥️ 本地模型
- GPU：RTX 3080 Ti 12GB，CUDA 13.1
> 目前无本地视频模型。添加时告知：模型名、端口、任务类型，Leon 同步更新。

---

## 🔌 通用 API 规范

### 创建任务
```
POST https://api.kie.ai/api/v1/jobs/createTask
Authorization: Bearer {KIEAI_API_KEY}
Content-Type: application/json
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
    "resultJson": "{\"result_urls\":[\"https://...video.mp4\"]}"
  }
}
```

---

## 💰 费用速查
| 用途 | 推荐模型 | 单价 |
|------|---------|------|
| 日常 5s 720p | Kling 3.0 无音频 | $0.10 |
| 带音频 5s | Kling 3.0 带音频 | $0.15 |
| 快速出片 | Wan 2.6 Flash | $0.10 |
| 高清 1080p | Seedance 1.5 Pro | $0.15+ |
| 顶级质量 | Kling v2.1 Master | $0.80+ |
| 数字人 | InfiniTalk | $0.00075/s |

## ⚠️ 注意
- 视频生成耗时 1-3 分钟，异步轮询（每5秒，最多3分钟）
- Kling 3.0 音频字段是 `sound`（bool），不是 `with_audio`
- Kling v2.1 首尾帧用 `image_url` + `tail_image_url`（非数组）
- Kling 3.0 首尾帧用 `image_urls`（数组）
- Seedance/Wan 分辨率用 `resolution` 字段（"480p"/"720p"/"1080p"）
- KIEAI_API_KEY = `943650a08f4c9d76eb6991a8a5d23cfd`
- 1 credit = $0.01 USD
