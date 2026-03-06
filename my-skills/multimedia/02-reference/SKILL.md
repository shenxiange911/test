---
name: 02-reference
description: "多媒体流水线第2层：角色/产品参考图（多角度合一张）+外观锁定"
metadata:
  {"openclaw": {"emoji": "📐"}}
---

# Step 2: 参考图生成

## 概述
生成一张包含多角度的角色/产品参考图（character sheet），用于锁定外观。
默认一张图包含三视图，用户要求时可扩展到六视图。

## 输入
- `script.md` 中的"角色/产品设定"部分

## 输出
- `reference_views/character_sheet_[name].jpg` （每个角色/产品一张多角度图）

---

## 执行流程

### Phase 1: 提取外观描述
从 script.md 提取每个主体的详细外观描述。

### Phase 2: 生成多角度参考图

读取 media-image skill: `~/.openclaw/skills/media-image/SKILL.md`

**每个角色/产品生成一张多角度图**（不是分开生成）：

三视图 prompt 模板：
```
Character reference sheet of [subject description], multiple views on one image: front view, left side view, right side view. Full body, white background, clean lines, consistent design across all views, professional character design sheet, labeled angles, photorealistic CG
```

六视图 prompt 模板（用户指定时）：
```
Character reference sheet of [subject description], 6 views on one image: front, left side, right side, back, top-down, bottom. Full body, white background, clean lines, consistent design, professional character design sheet, labeled angles, photorealistic CG
```

### Phase 3: API 调用

```json
{
  "model": "nano-banana-pro",
  "input": {
    "prompt": "[多角度prompt]",
    "aspect_ratio": "21:9",
    "resolution": "2K"
  }
}
```

比例选择：
- 三视图: `21:9` 或 `16:9`（横向排列3个角度）
- 六视图: `16:9`（2行×3列排列）

**注意**: 默认生成一张合图，除非用户明确要求分开生成单独角度图。

---

## 确认点
展示参考图给用户：
- "OK" → 外观锁定，进入 Step 3
- "修改" → 调整 prompt 重新生成
- "分开生成" → 切换为单独生成每个角度

## 费用
- 每个角色/产品: ~$0.04（一张图）
