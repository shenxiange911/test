---
name: 04-split
description: "多媒体流水线第4层：分镜拆分+去边+放大+序号排列"
metadata:
  {"openclaw": {"emoji": "✂️"}}
---

# Step 4: 分镜拆分+增强

## 概述
将整张分镜图拆分为独立小图，去除黑边白边水印，放大到2K，按序号排列输出。

## 输入
- `storyboard_full.png`

## 输出
- `frames/001.png ~ NNN.png` (2K独立分镜)

---

## 执行流程

### Phase 1: 自动拆分（本地 Python PIL）

```python
from PIL import Image
import numpy as np

img = Image.open('storyboard_full.png')
arr = np.array(img)

# 检测网格分割线（颜色突变的行/列）
# 按行列切割为独立图片
# 从左到右、从上到下编号
```

拆分策略：
1. 转灰度 → 检测水平/垂直方向的暗色线条（分割线）
2. 按分割线位置切割
3. 过滤掉太小的碎片（宽或高 < 总尺寸10%）
4. 按从左到右、从上到下排序，编号 001, 002...
5. 保存到 `frames/001_raw.png ~ NNN_raw.png`

### Phase 2: 去边+增强（Nano Banana Pro 图生图）

读取 media-image skill: `~/.openclaw/skills/media-image/SKILL.md`

对每张 raw 小图调用 nano-banana-pro 图生图：

```json
{
  "model": "nano-banana-pro",
  "input": {
    "prompt": "Clean up this image, remove black borders, white borders, watermarks and text overlays. Enhance image quality and details. Keep the original composition and content exactly the same.",
    "image_input": ["[frame_url]"],
    "aspect_ratio": "16:9",
    "resolution": "2K"
  }
}
```

### Phase 3: 序号排列输出

1. 下载增强后的图片
2. 重命名为 `frames/001.png ~ NNN.png`
3. 删除 raw 临时文件

---

## 确认点
展示所有拆分后的独立分镜（缩略图列表）：
- "OK" → 进入 Step 5
- "删除 X" → 删除指定序号
- "重做 X" → 重新增强指定序号
- "手动调整" → 用户提供裁剪坐标

## 费用
- 每张增强: ~$0.04
- N张总计: ~$0.04 × N
