---
name: 03-storyboard
description: "多媒体流水线第3层：整张分镜图生成（Nano Banana Pro 2K/4K）"
metadata:
  {"openclaw": {"emoji": "🎨"}}
---

# Step 3: 分镜图生成

## 概述
基于剧本和锁定的外观参考图，生成一整张分镜图（多格漫画式排列）。

## 输入
- `script.md`（分镜表 + 图片提示词）
- `reference_views/`（锁定的外观）

## 输出
- `storyboard_full.png` (2K或4K)

---

## 执行流程

### Phase 1: 构建分镜 Prompt
将所有分镜的提示词合并为一个整图 prompt：

```
A storyboard sheet with [N] panels arranged in a grid layout.
Panel 1: [Shot 01 prompt]
Panel 2: [Shot 02 prompt]
...
Each panel is clearly separated with thin black borders.
Consistent character design throughout all panels.
[主体外观描述 from reference views]
Professional storyboard style, clean composition.
```

### Phase 2: API 调用
读取 media-image skill: `~/.openclaw/skills/media-image/SKILL.md`

```json
{
  "model": "nano-banana-pro",
  "input": {
    "prompt": "[构建的分镜prompt]",
    "aspect_ratio": "16:9",
    "resolution": "4K"
  }
}
```

分辨率选择：
- 4-6个分镜 → 2K 即可
- 7个以上分镜 → 建议4K（保证拆分后清晰度）

### Phase 3: 保存
下载生成的图片，保存为 `storyboard_full.png`

---

## 确认点
展示整张分镜图给用户：
- "OK" → 进入 Step 4 拆分
- "修改" → 调整 prompt 重新生成
- "重做" → 完全重新生成

## 费用
- 2K: ~$0.04
- 4K: ~$0.07
