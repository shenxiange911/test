---
name: media-music
description: "AI音乐/音频生成skill。用于：文生音乐、音乐续写、人声分离、音效生成、TTS语音、语音转文字、音频降噪。支持：Suno、ElevenLabs、Vocal Removal。调用 kie.ai API。"
metadata:
  {"openclaw": {"emoji": "🎵"}}
---

# Media Music Skill — kie.ai 音乐/音频生成

## ⚙️ 默认参数（用户未指定时使用）

| 参数 | 默认值 | 可选范围 |
|------|--------|---------|
| 音乐时长 | ~2分钟 | 由模型决定 |
| 音乐风格 | 由 prompt 决定 | 任意风格 |
| TTS 语言 | 中文/英文自动识别 | 多语言 |
| 音频格式 | mp3 | mp3 / wav |

---

## 📋 完整模型表

### 🏢 Suno — AI 音乐生成

| 模型 | API model 字段 | Credits | USD | 推荐场景 |
|------|---------------|---------|-----|---------|
| Suno v4 生成 | `suno_generate_v4` | 12 | $0.06 | 标准音乐生成 ⭐ |
| Suno v4.5 生成 | `suno_generate_v45` | 12 | $0.06 | 最新版生成 |
| Suno v4.5 Plus | `suno_generate_v45_plus` | 12 | $0.06 | 增强版生成 |
| Suno v5 生成 | `suno_generate_v5` | 12 | $0.06 | v5版生成 |
| Suno v3.5 生成 | `suno_generate_v35` | 7 | $0.035 | 低成本生成 |
| Suno v4 续写 | `suno_extend_v4` | 12 | $0.06 | 音乐续写 |
| Suno v4.5 续写 | `suno_extend_v45` | 12 | $0.06 | 最新续写 |
| Suno v4.5 Plus 续写 | `suno_extend_v45_plus` | 12 | $0.06 | 增强续写 |
| Suno v5 续写 | `suno_extend_v5` | 12 | $0.06 | v5续写 |
| Suno v3.5 续写 | `suno_extend_v35` | 7 | $0.035 | 低成本续写 |
| Suno 上传续写 | `suno_upload_extend_v4` | 12 | $0.06 | 上传音频续写 |
| Suno 混音 | `suno_mashup` | 12 | $0.06 | 多曲混音 |
| Suno 人声合成 | `suno_add_vocals_v45_plus` | 12 | $0.06 | 添加人声 |
| Suno 伴奏合成 | `suno_add_instrumental_v45_plus` | 12 | $0.06 | 添加伴奏 |
| Suno 替换片段 | `suno_replace_section` | 5 | $0.025 | 替换某段 |
| Suno 生成歌词 | `suno_get_lyrics` | 0.5 | $0.0025 | AI写歌词 |
| Suno 创作歌词 | `suno_create_lyric` | 0.4 | $0.002 | 创作歌词 |
| Suno 风格AI生成 | `suno_style_ai_generate` | 0.4 | $0.002 | 风格分析 |
| Suno 上传封面 | `suno_upload_cover_v4` | 12 | $0.06 | 上传封面 |
| Suno 导出 MP4 | `suno-mp4-generate` | 2 | $0.01 | 导出视频 |
| Suno 导出 WAV | `suno-wav-generate` | 0.4 | $0.002 | 导出无损 |
| Suno 全量生成 | `suno_generate_v45_all` | 7 | $0.035 | 批量生成 |

### 🏢 ElevenLabs — TTS / 音频处理

| 模型 | API model 字段 | 计费单位 | Credits | USD | 推荐场景 |
|------|---------------|---------|---------|-----|---------|
| ElevenLabs V3 对话 | `elevenlabs/text-to-dialogue-v3` | 每1000字符 | 14 | $0.07 | 多角色对话TTS ⭐ |
| ElevenLabs TTS Turbo 2.5 | `elevenlabs/tts-turbo-2.5` | 每1000字符 | 6 | $0.03 | 快速TTS |
| ElevenLabs TTS 多语言 v2 | `elevenlabs/tts-multilingual-v2` | 每1000字符 | 12 | $0.06 | 高质量多语言TTS |
| ElevenLabs STT | `elevenlabs/speech-to-text` | 每分钟 | 3.5 | $0.0175 | 语音转文字 |
| ElevenLabs 音频降噪 | `elevenlabs/audio-isolation` | 每秒 | 0.2 | $0.001 | 背景噪音消除 |
| ElevenLabs 音效 V2 | `elevenlabs/sound-effect-v2` | 每秒 | 0.24 | $0.0012 | AI音效生成 |

### 🏢 Vocal Removal — 人声分离

| 模型 | API model 字段 | Credits | USD | 推荐场景 |
|------|---------------|---------|-----|---------|
| 人声分离（提取人声） | `vocal-removal/separate-vocal` | 10 | $0.05 | 提取纯人声 |
| 人声分离（分离所有轨道） | `vocal-removal/split-stem` | 50 | $0.25 | 分离人声+乐器各轨 |

### 🏢 Midjourney — 音乐视频

| 模型 | API model 字段 | Credits | USD | 推荐场景 |
|------|---------------|---------|-----|---------|
| MJ 音乐视频 SD | `mj_video_sd_1` | 15 | $0.075 | 标清音乐视频 |
| MJ 音乐视频 SD x2 | `mj_video_sd_2` | 30 | $0.15 | 标清x2 |
| MJ 音乐视频 HD | `mj_video_hd_1` | 45 | $0.225 | 高清音乐视频 |
| MJ 音乐视频 HD x2 | `mj_video_hd_2` | 90 | $0.45 | 高清x2 |
| MJ 音乐视频 HD x4 | `mj_video_hd_4` | 180 | $0.90 | 高清x4 |
| MJ 视频延伸 | `mj_video_extend_auto` | 60 | $0.30 | 自动延伸 |
| MJ 视频延伸手动 | `mj_video_extend_manual` | 60 | $0.30 | 手动延伸 |

---

## 🔌 API 调用规范

### 认证
```
POST https://api.kie.ai/api/v1/jobs/createTask
Authorization: Bearer {KIEAI_API_KEY}
Content-Type: application/json
```

### 文生音乐（Suno v4.5，默认推荐）
```json
{
  "model": "suno_generate_v45",
  "input": {
    "prompt": "A relaxing lo-fi hip hop track with soft piano and rain sounds",
    "style": "lo-fi, chill, instrumental",
    "title": "Rainy Day",
    "make_instrumental": true
  }
}
```

### 带歌词音乐生成
```json
{
  "model": "suno_generate_v45",
  "input": {
    "prompt": "upbeat pop song about summer",
    "lyrics": "[Verse]\nSunshine on my face\nWarm breeze in the air\n[Chorus]\nSummer days forever",
    "style": "pop, upbeat, female vocal",
    "title": "Summer Vibes",
    "make_instrumental": false
  }
}
```

### 音乐续写
```json
{
  "model": "suno_extend_v45",
  "input": {
    "audio_id": "suno_task_id_here",
    "prompt": "continue with a guitar solo",
    "continue_at": 60
  }
}
```

### TTS 语音合成（ElevenLabs Turbo）
```json
{
  "model": "elevenlabs/tts-turbo-2.5",
  "input": {
    "text": "你好，欢迎使用AI语音合成服务",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "language_code": "zh"
  }
}
```

### 多角色对话 TTS（ElevenLabs V3）
```json
{
  "model": "elevenlabs/text-to-dialogue-v3",
  "input": {
    "text": "<speaker1>你好！</speaker1><speaker2>你好，很高兴认识你！</speaker2>",
    "voice_id_1": "21m00Tcm4TlvDq8ikWAM",
    "voice_id_2": "AZnzlk1XvdvUeBnXmlld"
  }
}
```

### 音效生成（ElevenLabs Sound Effect V2）
```json
{
  "model": "elevenlabs/sound-effect-v2",
  "input": {
    "text": "thunder storm with heavy rain and wind",
    "duration_seconds": 10
  }
}
```

### 人声分离
```json
{
  "model": "vocal-removal/separate-vocal",
  "input": {
    "audio_url": "https://example.com/song.mp3"
  }
}
```

### 分离所有轨道（人声+鼓+贝斯+其他）
```json
{
  "model": "vocal-removal/split-stem",
  "input": {
    "audio_url": "https://example.com/song.mp3"
  }
}
```

### 音频降噪
```json
{
  "model": "elevenlabs/audio-isolation",
  "input": {
    "audio_url": "https://example.com/noisy_audio.mp3"
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

| 需求 | 推荐模型 | 单价 | 月100次预算 |
|------|---------|------|-----------|
| 生成一首歌 | Suno v4.5 | $0.06 | ~$6 |
| 低成本生歌 | Suno v3.5 | $0.035 | ~$3.5 |
| 快速TTS | ElevenLabs Turbo | $0.03/千字 | 极低 |
| 高质量TTS | ElevenLabs 多语言v2 | $0.06/千字 | 极低 |
| 人声提取 | Vocal Removal | $0.05/首 | ~$5 |
| 全轨分离 | Split Stem | $0.25/首 | ~$25 |
| 音效生成 | Sound Effect V2 | $0.012/10s | 极低 |

---

## 🔄 使用流程

1. 判断任务类型：生成音乐 / 续写 / TTS / 音效 / 人声分离 / 降噪
2. 推荐模型 + 告知价格
3. 用户确认 → 调用 createTask
4. 轮询结果（每3秒，最多2分钟）
5. 返回音频URL

## ⚠️ 注意事项
- Suno 生成的音乐版权归用户所有（商用需确认账号等级）
- TTS 按字符计费，中文每个汉字算1字符
- 人声分离需要公开可访问的音频URL
- 音效生成最长支持 22 秒
- API Key 存在环境变量 `KIEAI_API_KEY`（值：`943650a08f4c9d76eb6991a8a5d23cfd`）
- 1 credit = $0.01 USD
- 当前余额：9218 credits（$92.18）

---

## 🖥️ 本地模型（优先使用，免费）

> 本地模型运行在 WSL2，无需 API Key，无费用，优先于 kie.ai 调用。

| 模型 | 服务地址 | 任务 | 特点 |
|------|---------|------|------|
| ChatTTS | `http://127.0.0.1:8001` | TTS 语音合成 | 奶音 seed 132，中文效果好 |
| Whisper STT | `http://127.0.0.1:8002` | 语音转文字 | faster-whisper small，CUDA 加速 |

### ChatTTS 调用
```bash
# 健康检查
curl http://127.0.0.1:8001/health

# 语音合成
curl -X POST http://127.0.0.1:8001/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，我是Leon", "seed": 132}' \
  --output output.wav
```

### Whisper STT 调用
```bash
# 健康检查
curl http://127.0.0.1:8002/health

# 语音转文字
curl -X POST http://127.0.0.1:8002/transcribe \
  -F "file=@audio.mp3"
```

### 本地 vs kie.ai 选择策略
- **优先本地**：中文TTS、日常语音转文字 → ChatTTS / Whisper
- **用 kie.ai**：多语言高质量TTS、多角色对话、音效生成、音乐生成 → ElevenLabs / Suno
- **本地服务挂了**：`systemctl --user start chattts-tts.service whisper-stt.service`

### 📌 新增本地模型说明
> 以后添加新的本地模型，告诉 Leon：模型名、端口、任务类型，Leon 会同步更新此文件。
