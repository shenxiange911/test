---
name: 06-edit
description: "多媒体流水线第6层：剪辑+配音+音效+字幕"
metadata:
  {"openclaw": {"emoji": "🎞️"}}
---

# Step 6: 剪辑+配音+字幕

## 概述
用户选择镜头序号进行剪辑拼接，添加配音、音效、字幕，输出最终成片。

## 输入
- `videos/001.mp4 ~ NNN.mp4`
- `script.md`（台词/旁白、音效标注）

## 输出
- `final_output.mp4`
- `subtitles.srt`

---

## 执行流程

### Phase 1: 镜头选择+排序

展示所有已生成的视频片段：
```
[001] 3s - 远景推镜
[003] 5s - 中景固定
[005] 4s - 特写跟踪
```

用户选择剪辑顺序，如："按 1,3,5 顺序剪辑" 或 "按原序号"

### Phase 2: 视频拼接（ffmpeg）

```bash
# 生成文件列表
for f in selected_videos; do
  echo "file '$f'" >> filelist.txt
done

# 拼接
ffmpeg -f concat -safe 0 -i filelist.txt -c copy joined.mp4
```

### Phase 3: 配音

读取 audio skill: `~/.openclaw/skills/audio/SKILL.md`

从 script.md 提取配音文案，生成语音：
- 本地 ChatTTS (免费，端口8001) → 中文配音首选
- ElevenLabs → 英文/高质量配音

保存到 `audio/narration.mp3`

### Phase 4: 音效+BGM

读取 media-music skill: `~/.openclaw/skills/media-music/SKILL.md`

- BGM: 根据剧本风格用 Suno 生成，或用户提供
- 音效: 根据 script.md 中的音效标注添加

### Phase 5: 字幕生成

从 script.md 提取台词，按时间轴生成 SRT：

```srt
1
00:00:00,000 --> 00:00:03,000
[第一句台词]

2
00:00:03,500 --> 00:00:08,000
[第二句台词]
```

保存为 `subtitles.srt`

### Phase 6: 最终合成（ffmpeg）

```bash
# 添加配音
ffmpeg -i joined.mp4 -i audio/narration.mp3 \
  -c:v copy -c:a aac -shortest output_voiced.mp4

# 混入BGM（降低BGM音量）
ffmpeg -i output_voiced.mp4 -i audio/bgm.mp3 \
  -filter_complex "[1:a]volume=0.3[bgm];[0:a][bgm]amix=inputs=2" \
  -c:v copy output_mixed.mp4

# 烧录字幕
ffmpeg -i output_mixed.mp4 \
  -vf "subtitles=subtitles.srt" final_output.mp4
```

---

## 确认点
- 拼接后预览 → 用户确认顺序
- 配音后预览 → 用户确认语音效果
- 最终成片 → 用户确认

## 费用
- 配音: 免费(ChatTTS) 或 ~$0.1(ElevenLabs)
- BGM: ~$0.05(Suno)
- ffmpeg: 免费(本地)
