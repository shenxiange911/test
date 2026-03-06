---
name: audio
description: "AI音频处理skill。用于：TTS语音合成、STT语音转文字、音效生成、音频降噪、人声分离、音轨分离。按模型名调用，供应商无关。本地优先：ChatTTS(port 8001)、Whisper STT(port 8002)。"
metadata:
  {"openclaw": {"emoji": "🎙️"}}
---

# Audio Skill

## ⚙️ 选择策略
- **中文TTS / 日常语音** → 优先本地 ChatTTS（免费，seed 132 奶音）
- **多语言TTS / 高质量 / 多角色** → ElevenLabs（kie.ai）
- **语音转文字** → 优先本地 Whisper STT（免费，CUDA 加速）
- **音效生成** → ElevenLabs Sound Effect V2（kie.ai）
- **人声分离 / 降噪** → kie.ai

---

## 📌 换供应商说明
每个模型块内有 provider 字段。换供应商时只改该模型的 provider 块。

---

## 🎙️ TTS 语音合成

### ChatTTS seed 132（本地，免费，优先）
- 用途：中文TTS，奶音，日常使用
- 价格：免费
- 延迟：低（本地 GPU）

**Provider: local**
```bash
# 健康检查
curl http://127.0.0.1:8001/health
# 返回：{"status":"ok","model":"ChatTTS","seed":132}

# 语音合成
curl -X POST http://127.0.0.1:8001/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，我是Leon", "seed": 132}' \
  --output output.wav
```

**启动服务：**
```bash
systemctl --user start chattts-tts.service
systemctl --user status chattts-tts.service
```

---

### ElevenLabs TTS Turbo 2.5（快速多语言）
- 用途：快速多语言TTS
- 价格：$0.03/千字符

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "elevenlabs/tts-turbo-2.5",
  "input": {
    "text": "Hello, welcome to our service",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "language_code": "en"
  }
}
```

---

### ElevenLabs TTS 多语言 v2（高质量）
- 用途：高质量多语言TTS
- 价格：$0.06/千字符

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "elevenlabs/tts-multilingual-v2",
  "input": {
    "text": "你好，欢迎使用AI语音合成服务",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "language_code": "zh"
  }
}
```

---

### ElevenLabs V3 多角色对话（最高质量）
- 用途：多角色对话TTS，支持情感标签
- 价格：$0.07/千字符

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "elevenlabs/text-to-dialogue-v3",
  "input": {
    "text": "<speaker1>你好！</speaker1><speaker2>你好，很高兴认识你！</speaker2>",
    "voice_id_1": "21m00Tcm4TlvDq8ikWAM",
    "voice_id_2": "AZnzlk1XvdvUeBnXmlld"
  }
}
```

---

## 🎙️ STT 语音转文字

### Whisper STT（本地，免费，优先）
- 用途：语音转文字，CUDA 加速
- 价格：免费
- 模型：faster-whisper-small

**Provider: local**
```bash
# 健康检查
curl http://127.0.0.1:8002/health
# 返回：{"status":"ok","device":"cuda"}

# 语音转文字
curl -X POST http://127.0.0.1:8002/transcribe \
  -F "file=@audio.mp3"
```

**启动服务：**
```bash
systemctl --user start whisper-stt.service
systemctl --user status whisper-stt.service
```

---

### ElevenLabs STT（高精度）
- 用途：高精度语音转文字
- 价格：$0.0175/分钟

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "elevenlabs/speech-to-text",
  "input": {
    "audio_url": "https://example.com/audio.mp3",
    "language_code": "zh"
  }
}
```

---

## 🎙️ 音效生成

### ElevenLabs Sound Effect V2
- 用途：AI生成音效，最长22秒
- 价格：$0.0012/秒

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "elevenlabs/sound-effect-v2",
  "input": {
    "text": "thunder storm with heavy rain and wind",
    "duration_seconds": 10
  }
}
```

---

## 🎙️ 音频降噪

### ElevenLabs Audio Isolation
- 用途：消除背景噪音，保留人声
- 价格：$0.001/秒

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "elevenlabs/audio-isolation",
  "input": {
    "audio_url": "https://example.com/noisy_audio.mp3"
  }
}
```

---

## 🎙️ 人声分离 / 音轨分离

### Vocal Removal（提取人声）
- 用途：从歌曲中提取纯人声
- 价格：$0.05/首

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "vocal-removal/separate-vocal",
  "input": {
    "audio_url": "https://example.com/song.mp3"
  }
}
```

---

### Vocal Removal Split Stem（分离所有轨道）
- 用途：分离人声 + 鼓 + 贝斯 + 其他乐器
- 价格：$0.25/首

**Provider: kie-ai**
```json
{
  "base_url": "https://api.kie.ai/api/v1/jobs/createTask",
  "auth": "Authorization: Bearer {KIEAI_API_KEY}",
  "model_id": "vocal-removal/split-stem",
  "input": {
    "audio_url": "https://example.com/song.mp3"
  }
}
```

---

## 🖥️ 本地模型
| 模型 | 端口 | 任务 | 状态 |
|------|------|------|------|
| ChatTTS seed 132 | 8001 | TTS 中文语音合成 | ✅ 运行中 |
| Whisper STT small | 8002 | 语音转文字 | ✅ 运行中 |

**重启本地服务：**
```bash
systemctl --user restart chattts-tts.service whisper-stt.service
```

> 添加新本地模型时告知：模型名、端口、任务类型，Leon 同步更新。

---

## 🔌 通用 API 规范（kie.ai）

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
| 中文TTS | ChatTTS（本地） | 免费 |
| 快速多语言TTS | ElevenLabs Turbo | $0.03/千字 |
| 高质量TTS | ElevenLabs 多语言v2 | $0.06/千字 |
| 多角色对话 | ElevenLabs V3 | $0.07/千字 |
| 语音转文字 | Whisper（本地） | 免费 |
| 高精度STT | ElevenLabs STT | $0.0175/分钟 |
| 音效生成 | Sound Effect V2 | $0.012/10s |
| 人声提取 | Vocal Removal | $0.05/首 |
| 全轨分离 | Split Stem | $0.25/首 |
| 音频降噪 | Audio Isolation | $0.001/秒 |

## ⚠️ 注意
- 本地服务优先，kie.ai 作为备用
- 本地服务挂了先检查：`systemctl --user status chattts-tts.service whisper-stt.service`
- KIEAI_API_KEY = `943650a08f4c9d76eb6991a8a5d23cfd`
- 1 credit = $0.01 USD

## 🔴 已知 Bug 与修复（必读）

### ChatTTS 兼容版本（2026-02-27 验证）
- ChatTTS: 0.2.4
- transformers: **必须 4.44.2**（5.x 移除了 encode_plus，会报 AttributeError）
- 降级命令：`cd ~/voice-stack/chattts-service && .venv/bin/pip install "transformers==4.44.2"`

### sample_random_speaker API 变更
- 旧版：`chat.sample_random_speaker(seed=132)` ← 会报 TypeError
- 新版（0.2.4）：无参数，调用前设置随机种子：
```python
torch.manual_seed(seed)
np.random.seed(seed)
spk = chat.sample_random_speaker()
```

### 排查流程
```bash
# 1. 检查服务状态
systemctl --user status chattts-tts.service

# 2. 查错误日志
journalctl --user -u chattts-tts.service -n 20 --no-pager | grep -E "Error|error|Exception"

# 3. 常见错误对照
# TypeError: sample_random_speaker() got unexpected keyword argument 'seed'
#   → 修改 app.py，去掉 seed 参数，改用 torch.manual_seed + np.random.seed
# AttributeError: BertTokenizer has no attribute encode_plus
#   → 降级 transformers: pip install "transformers==4.44.2"
```

## 💬 语音对话规范

### 收到用户语音消息时
1. 先调用 Whisper 转录：`curl -X POST http://127.0.0.1:8002/transcribe -F "audio=@<path>" -F "language=zh"`
2. 回复格式：
   > 🎙️ 你说的是：「转录内容」
   > 
   > （正常回复内容）

### 发送语音给用户时
- 必须同时带文字说明，不能只发语音
- 格式：先发文字，再发语音文件
