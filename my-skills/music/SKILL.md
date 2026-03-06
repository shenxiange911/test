---
name: music
description: "AI音乐生成/续写/混音。用于：文生音乐、歌词生成、音乐续写、混音、人声合成、导出MP4/WAV。支持：Suno。按模型名调用，供应商无关。"
metadata:
  {"openclaw": {"emoji": "🎵"}}
---

# Music Skill

## ⚙️ 默认参数
| 参数 | 默认值 | 说明 |
|------|--------|------|
| 时长 | ~2分钟 | 由模型决定 |
| 人声 | 有 | make_instrumental: false |
| 版本 | v4.5 | 最新稳定版 |

**生成前告知用户：** 默认生成带人声的完整歌曲，如需纯伴奏请说明。

---

## 📌 换供应商说明
每个模型块内有 provider 字段。换供应商时只改该模型的 provider 块。

---

## 🎵 音乐生成

### Suno v4.5（推荐，最新稳定）
- 用途：标准音乐生成 ⭐
- 价格：$0.06/首

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_generate_v45",
  "input": {
    "prompt": "A relaxing lo-fi hip hop track with soft piano and rain sounds",
    "style": "lo-fi, chill, instrumental",
    "title": "Rainy Day",
    "make_instrumental": true
  }
}
```

**带歌词生成：**
```json
{
  "model": "suno_generate_v45",
  "input": {
    "prompt": "upbeat pop song about summer",
    "lyrics": "[Verse]\nSunshine on my face\n[Chorus]\nSummer days forever",
    "style": "pop, upbeat, female vocal",
    "title": "Summer Vibes",
    "make_instrumental": false
  }
}
```

---

### Suno v4.5 Plus（增强版）
- 用途：增强质量生成
- 价格：$0.06/首

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_generate_v45_plus",
  "input": {
    "prompt": "epic orchestral battle theme",
    "style": "orchestral, epic, cinematic",
    "title": "Battle Theme",
    "make_instrumental": true
  }
}
```

---

### Suno v5（最新版）
- 用途：最新版生成
- 价格：$0.06/首

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_generate_v5",
  "input": {
    "prompt": "jazz fusion with electric guitar",
    "style": "jazz, fusion, electric guitar",
    "title": "Jazz Night",
    "make_instrumental": false
  }
}
```

---

### Suno v4（稳定版）
- 用途：稳定生成
- 价格：$0.06/首

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_generate_v4",
  "input": {
    "prompt": "acoustic folk song",
    "style": "folk, acoustic, guitar",
    "title": "Folk Song",
    "make_instrumental": false
  }
}
```

---

### Suno v3.5（低成本）
- 用途：低成本快速生成
- 价格：$0.035/首

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_generate_v35",
  "input": {
    "prompt": "simple background music",
    "style": "ambient, background",
    "make_instrumental": true
  }
}
```

---

## 🎵 音乐续写

### Suno v4.5 续写
- 用途：在已有音乐基础上续写
- 价格：$0.06/次

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_extend_v45",
  "input": {
    "audio_id": "suno_task_id_here",
    "prompt": "continue with a guitar solo",
    "continue_at": 60
  }
}
```

---

### Suno 上传续写（本地音频续写）
- 用途：上传本地音频文件续写
- 价格：$0.06/次

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_upload_extend_v4",
  "input": {
    "audio_url": "https://example.com/my_song.mp3",
    "prompt": "add a bridge section"
  }
}
```

---

## 🎵 音乐混音 / 编辑

### Suno 混音
- 用途：多曲混音
- 价格：$0.06/次

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_mashup",
  "input": {
    "audio_ids": ["id1", "id2"],
    "prompt": "blend these two songs"
  }
}
```

---

### Suno 替换片段
- 用途：替换歌曲某一段
- 价格：$0.025/次

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_replace_section",
  "input": {
    "audio_id": "suno_task_id",
    "start_time": 30,
    "end_time": 60,
    "prompt": "replace with piano solo"
  }
}
```

---

### Suno 添加人声
- 用途：给伴奏添加人声
- 价格：$0.06/次

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_add_vocals_v45_plus",
  "input": {
    "audio_id": "suno_task_id",
    "lyrics": "[Verse]\nYour lyrics here"
  }
}
```

---

## 🎵 歌词生成

### Suno 生成歌词
- 用途：AI 写歌词
- 价格：$0.0025/次

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_get_lyrics",
  "input": {
    "prompt": "a love song about missing someone"
  }
}
```

---

### Suno 创作歌词
- 用途：创作歌词
- 价格：$0.002/次

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno_create_lyric",
  "input": {
    "prompt": "write lyrics about summer vacation"
  }
}
```

---

## 🎵 导出

### Suno 导出 MP4（音乐视频）
- 用途：将音乐导出为 MP4 视频
- 价格：$0.01/次

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno-mp4-generate",
  "input": {
    "audio_id": "suno_task_id"
  }
}
```

---

### Suno 导出 WAV（无损）
- 用途：导出无损 WAV 格式
- 价格：$0.002/次

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "suno-wav-generate",
  "input": {
    "audio_id": "suno_task_id"
  }
}
```

---

## 🖥️ 本地模型
> 目前无本地音乐生成模型。添加时告知：模型名、端口、任务类型，Leon 同步更新。

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

---

## 💰 费用速查
| 用途 | 推荐模型 | 单价 |
|------|---------|------|
| 生成一首歌 | Suno v4.5 | $0.06 |
| 低成本生歌 | Suno v3.5 | $0.035 |
| 续写 | Suno v4.5 续写 | $0.06 |
| 写歌词 | Suno 生成歌词 | $0.0025 |
| 导出 MP4 | Suno MP4 | $0.01 |

## ⚠️ 注意
- Suno 生成的音乐版权归用户所有
- audio_id 是上一次生成任务的 taskId
- KIEAI_API_KEY = `943650a08f4c9d76eb6991a8a5d23cfd`
- 1 credit = $0.01 USD
