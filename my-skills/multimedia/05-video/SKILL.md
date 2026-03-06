---
name: 05-video
description: "多媒体流水线第5层：运镜提示词+选择性视频生成"
metadata:
  {"openclaw": {"emoji": "🎥"}}
---

# Step 5: 视频生成

## 概述
根据每个独立分镜和剧本，生成运镜提示词，用户选择生成哪几个分镜的视频。

## 输入
- `frames/001.png ~ NNN.png`
- `script.md`（分镜表中的运镜和视频提示词）

## 输出
- `videos/001.mp4 ~ NNN.mp4`

---

## 执行流程

### Phase 1: 生成运镜提示词

为每个分镜生成视频提示词，结合：
- script.md 中的画面描述和运镜指示
- 分镜图片作为参考（图生视频）

运镜类型映射：
| 中文 | 英文prompt关键词 |
|------|----------------|
| 推镜 | slow push in, dolly forward |
| 拉镜 | pull out, dolly back |
| 平移 | pan left/right, lateral tracking |
| 升降 | crane up/down, vertical movement |
| 旋转 | orbit around, 360 rotation |
| 固定 | static shot, locked camera |
| 手持 | handheld, slight shake |
| 跟踪 | tracking shot, follow subject |

### Phase 2: 用户选择

展示所有分镜缩略图 + 运镜提示词列表：
```
[001] 远景-推镜: A vast mountain landscape, slow dolly forward...
[002] 中景-固定: Character standing in doorway, static shot...
[003] 特写-跟踪: Close-up of product, tracking shot...
```

用户选择要生成的序号，如："生成 1,3,5" 或 "全部生成"

### Phase 3: 视频生成

读取 media-video skill: `~/.openclaw/skills/media-video/SKILL.md`

对用户选中的每个分镜，用图生视频：
- 输入图片: `frames/NNN.png`
- 提示词: Phase 1 生成的运镜提示词
- 模型: 用户选择（默认推荐 Kling 2.6 或 Seedance）

生成完成后保存到 `videos/NNN.mp4`

---

## 确认点
每个视频生成后展示给用户：
- "OK" → 继续下一个 / 进入 Step 6
- "重做 X" → 调整提示词重新生成
- "换模型" → 用其他视频模型重试

## 费用
- 每条视频: ~$0.2~0.5（取决于模型和时长）
