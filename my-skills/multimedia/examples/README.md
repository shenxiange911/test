# Multimedia 流水线配置模板库

标准化配置模板，降低使用门槛，快速启动多媒体创作任务。

## 📁 模板列表

### 1. product-video-2x2.json
**用途：** 产品展示视频  
**布局：** 2×2 分镜（4 个镜头）  
**适用场景：**
- 电商产品展示
- 产品功能介绍
- 多角度产品摄影

**工作流程：**
```
配置产品信息 → 生成 2×2 分镜图 → 自动拆分为 4 张图 → 可选择性生成视频
```

**关键参数：**
- `product_name`: 产品名称
- `product_description`: 产品描述
- `storyboard.scenes`: 4 个镜头的详细描述
- `video_generation.selected_frames`: 选择哪些镜头生成视频

---

### 2. character-reference-4view.json
**用途：** 角色设计参考图  
**布局：** 2×2 四视图（前/后/左/右）  
**适用场景：**
- 游戏角色设计
- 动画角色设定
- 3D 建模参考

**工作流程：**
```
配置角色信息 → 生成四视图参考图 → 拆分为独立视图 → 锁定外观一致性
```

**关键参数：**
- `character_name`: 角色名称
- `character_details.appearance`: 外观细节
- `character_details.outfit`: 服装设计
- `consistency_lock.enabled`: 是否锁定外观一致性

---

### 3. storyboard-3x3.json
**用途：** 故事分镜设计  
**布局：** 3×3 网格（9 个镜头）  
**适用场景：**
- 短视频分镜
- 动画故事板
- 广告脚本可视化

**工作流程：**
```
编写故事大纲 → 设计 9 个镜头 → 生成 3×3 分镜图 → 拆分镜头 → 选择关键帧生成视频
```

**关键参数：**
- `story_title`: 故事标题
- `storyboard.scenes`: 9 个镜头的详细描述（含时间轴）
- `video_generation.selected_frames`: 选择哪些关键镜头生成视频

---

### 4. simple-image-gen.json
**用途：** 单张图片生成  
**布局：** 无（单图）  
**适用场景：**
- 海报设计
- 封面图制作
- 概念图快速生成
- 社交媒体配图

**工作流程：**
```
编写提示词 → 生成图片 → 可选后处理（放大/增强）
```

**关键参数：**
- `prompt.main`: 主要描述
- `prompt.style`: 风格定义
- `image_generation.resolution`: 分辨率
- `image_generation.aspect_ratio`: 画幅比例

---

## 🚀 快速开始

### 方法 1：直接修改模板
```bash
# 1. 复制模板到工作目录
cp ~/.openclaw/skills/multimedia/examples/product-video-2x2.json my-project.json

# 2. 编辑配置
nano my-project.json

# 3. 运行流水线（根据具体 skill 调用方式）
```

### 方法 2：使用模板作为参考
```bash
# 查看模板内容
cat ~/.openclaw/skills/multimedia/examples/storyboard-3x3.json

# 根据模板结构创建自己的配置
```

---

## 📝 配置文件结构说明

所有模板遵循统一结构：

```json
{
  "_comment": "模板说明",
  "_usage": "使用场景",
  "_expected_output": "预期输出",
  
  "task_type": "任务类型标识",
  
  "storyboard": {
    "layout": "布局方式（2x2 / 3x3）",
    "scenes": [
      {
        "frame": 1,
        "description": "镜头描述",
        "camera": "机位信息",
        "lighting": "光照设置"
      }
    ]
  },
  
  "image_generation": {
    "model": "使用的模型",
    "resolution": "分辨率",
    "style": "风格描述"
  },
  
  "video_generation": {
    "enabled": false,
    "selected_frames": [1, 3],
    "model": "视频模型"
  },
  
  "output": {
    "storyboard_path": "输出路径",
    "split_frames_dir": "拆分帧目录"
  }
}
```

---

## 🎨 自定义提示

### 图片生成提示词技巧
- **主体描述：** 清晰描述主要内容
- **风格定义：** 指定艺术风格（写实/卡通/赛博朋克等）
- **光照设置：** 描述光线效果（自然光/工作室灯光/霓虹灯等）
- **质量控制：** 添加质量关键词（high quality, detailed, 8k 等）

### 分镜设计建议
- **镜头多样性：** 混合使用远景/中景/特写
- **叙事连贯性：** 确保镜头之间有逻辑关联
- **视觉节奏：** 控制镜头切换的快慢节奏
- **关键帧选择：** 优先为动作/情感高潮生成视频

---

## 🔧 常见问题

**Q: 如何修改分镜布局？**  
A: 修改 `storyboard.layout` 参数（支持 2x2, 3x3 等）

**Q: 如何保持角色外观一致？**  
A: 启用 `consistency_lock.enabled: true`，首次生成后将第一张图设为 `base_image`

**Q: 如何只生成部分镜头的视频？**  
A: 设置 `video_generation.selected_frames` 数组，只包含需要的帧编号

**Q: 如何调整图片分辨率？**  
A: 修改 `image_generation.resolution`，推荐值：
- 2048x2048（标准）
- 4096x4096（高清，适合 3×3 分镜）
- 1152x2048（竖屏）

---

## 📚 相关文档

- **multimedia skill 总览：** `~/.openclaw/skills/multimedia/SKILL.md`
- **各层级详细文档：**
  - 01-research: 深度搜索与剧本生成
  - 02-reference: 角色/产品参考图
  - 03-storyboard: 分镜图生成
  - 04-split: 分镜拆分与处理
  - 05-video: 视频生成
  - 06-edit: 剪辑与后期

---

## 💡 最佳实践

1. **从简单开始：** 先用 `simple-image-gen.json` 测试提示词效果
2. **迭代优化：** 生成后根据结果调整配置参数
3. **保存成功配置：** 将好的配置保存为自己的模板
4. **模块化使用：** 不必完整走完流水线，可单独使用某一层级

---

**更新日期：** 2026-03-04  
**版本：** v1.0
