# 🎬 多媒体制作流水线 Skill - 完整使用说明

**版本**: v2.0
**最后更新**: 2026-03-03
**作者**: Leon (OpenClaw AI Assistant)
**状态**: ✅ 生产就绪

---

## ⚠️ 重要提示

**给其他 AI 的说明**:
1. 本 Skill 已包含所有必要的工具和脚本
2. **不要自己编写新的脚本**，除非确认功能缺失
3. 如果需要新功能，先询问用户
4. 所有工具路径、API 配置、使用方法都在本文档中

---

## 📦 Skill 结构总览

```
~/.openclaw/skills/multimedia/
├── SKILL.md                    # 本文件（主文档）
├── README.md                   # 快速开始指南
├── run_pipeline.py             # 流水线执行器
│
├── scripts/                    # 所有工具脚本
│   ├── script_generator.py           # Phase 1: 调研+剧本
│   ├── reference_generator.py        # Phase 2: 参考图生成
│   ├── storyboard_generator.py       # Phase 3: 分镜图生成
│   ├── frame_splitter.py             # Phase 4: 分镜拆分（原版）
│   ├── split_storyboard_improved.py  # Phase 4: 分镜拆分（改进版）
│   ├── gemini_analyzer.py            # 图片/视频分析
│   └── video_analyzer.py             # 视频分析（备用）
│
├── config/                     # 配置文件
│   └── gemini-api.json         # Gemini API 配置
│
├── references/                 # 经验文档
│   ├── INDEX.md                      # 知识库索引
│   ├── workflow-experience.md        # 完整流水线经验
│   ├── script-generation-experience.md
│   └── frame-splitter-upgrade.md
│
└── 01-research/                # 子 Skill（6个）
    02-reference/
    03-storyboard/
    04-split/
    05-video/
    06-edit/
```

---

## 🛠️ 可用工具清单

### ✅ Phase 1: 调研与剧本

**工具**: `scripts/script_generator.py`

**功能**: 深度搜索 + 数据分析 + 剧本生成

**依赖**: 
- crawler skill (`~/.openclaw/skills/crawler/SKILL.md`)
- Tavily/Firecrawl/Brave Search API

**使用方法**:
```bash
python3 ~/.openclaw/skills/multimedia/scripts/script_generator.py \
  "主题" \
  "场景描述" \
  60 \
  "YouTube" \
  /path/to/project
```

**输出**: `script.md`（剧本文件）

**状态**: ✅ 可用

---

### ✅ Phase 2: 参考图生成

**工具**: `scripts/reference_generator.py`

**功能**: 生成三视图/六视图参考图

**依赖**:
- media-image skill (`~/.openclaw/skills/media-image/`)
- kie.ai API (Nano Banana Pro)

**使用方法**:
```bash
python3 ~/.openclaw/skills/multimedia/scripts/reference_generator.py \
  front back left right \
  --project "project-name" \
  --output /path/to/reference_views
```

**输出**: `reference_views/` 目录（front.png, back.png, left.png, right.png）

**状态**: ✅ 可用

---

### ✅ Phase 3: 分镜图生成

**工具**: `scripts/storyboard_generator.py`

**功能**: 生成整张分镜图（3×3 或 4×4 grid）

**依赖**:
- media-image skill
- kie.ai API (Nano Banana Pro)

**使用方法**:
```bash
python3 ~/.openclaw/skills/multimedia/scripts/storyboard_generator.py \
  --project "project-name" \
  --grid 3x3 \
  --output /path/to/storyboard_full.png
```

**输出**: `storyboard_full.png`（整张分镜图）

**状态**: ✅ 可用

---

### ✅ Phase 4: 分镜拆分

**工具 1**: `scripts/frame_splitter.py`（原版）

**功能**: 基本拆分 + Title Bar 检测 + Border Trim

**使用方法**:
```bash
python3 ~/.openclaw/skills/multimedia/scripts/frame_splitter.py \
  /path/to/storyboard_full.png \
  3 3 \
  /path/to/frames \
  project-name
```

**工具 2**: `scripts/split_storyboard_improved.py`（改进版）⭐ 推荐

**功能**: 命令行参数 + 日志系统 + 错误处理 + 类封装

**使用方法**:
```bash
python3 ~/.openclaw/skills/multimedia/scripts/split_storyboard_improved.py \
  --input storyboard_full.png \
  --output ./frames \
  --rows 3 \
  --cols 3 \
  --project project-name \
  --verbose
```

**输出**: `frames/` 目录（01_project_scene.png ~ 09_project_scene.png）

**状态**: ✅ 可用

**改进说明**: 查看 `~/.openclaw/workspace/SKILL_IMPROVEMENT_GUIDE.md`

---

### ✅ Phase 5: 视频生成

**工具**: 使用 media-video skill

**依赖**:
- media-video skill (`~/.openclaw/skills/media-video/`)
- kie.ai API (Kling 2.5 Turbo)

**使用方法**:
```bash
# 通过 media-video skill 调用
# 参考: ~/.openclaw/skills/media-video/SKILL.md
```

**输出**: `videos/` 目录（01.mp4 ~ 09.mp4）

**状态**: ✅ 可用

---

### ✅ Phase 6: 剪辑配音

**工具**: 使用 audio skill

**依赖**:
- audio skill (`~/.openclaw/skills/audio/`)
- Suno/ElevenLabs API

**使用方法**:
```bash
# 通过 audio skill 调用
# 参考: ~/.openclaw/skills/audio/SKILL.md
```

**输出**: `final_output.mp4`（最终成片）

**状态**: ⏳ 待集成

---

### ✅ 辅助工具: 图片/视频分析

**工具**: `scripts/gemini_analyzer.py`

**功能**: 分析图片/视频内容（用于 Phase 0 或 Phase 5）

**依赖**:
- Gemini API (vectorengine.ai)

**使用方法**:
```bash
# 分析图片
python3 ~/.openclaw/skills/multimedia/scripts/gemini_analyzer.py \
  --type image \
  --file ./image.jpg \
  --prompt "详细描述这张图片"

# 分析视频
python3 ~/.openclaw/skills/multimedia/scripts/gemini_analyzer.py \
  --type video \
  --file ./video.mp4 \
  --prompt "分析这个视频的镜头语言"
```

**状态**: ⚠️ 本地视频分析有超时问题，YouTube 视频稳定

**详细说明**: 查看 `~/.openclaw/skills/gemini-analyzer/references/usage-experience.md`

---

## 🔑 API 配置清单

### ✅ 已配置的 API

#### 1. kie.ai API
**用途**: 图片生成、视频生成
**配置位置**: `~/.openclaw/skills/media-image/config/kie-api-keys.json`
**状态**: ✅ 已配置（9个 Key 可轮换）
**模型**:
- Nano Banana Pro (图片生成)
- Kling 2.5 Turbo (视频生成)
- Suno (音乐生成)

#### 2. Gemini API (vectorengine.ai)
**用途**: 图片/视频分析
**配置位置**: `~/.openclaw/skills/gemini-analyzer/config/api.json`
**状态**: ✅ 已配置
**API Key**: `YOUR_API_KEY_HERE`
**Base URL**: `https://api.vectorengine.ai`
**模型**:
- gemini-2.5-pro (推荐)
- gemini-2.5-flash (快速)

#### 3. Crawler API
**用途**: 深度搜索、网页爬取
**配置位置**: `~/.openclaw/skills/crawler/config/`
**状态**: ✅ 已配置
**支持**:
- Tavily (搜索/提取/爬取/地图/研究)
- Firecrawl (抓取/爬取/搜索/地图)
- Brave Search (通过 OpenClaw web_search)

### ⚠️ 需要用户提供的 API

#### 1. ElevenLabs API
**用途**: TTS 语音合成
**状态**: ❌ 未配置
**需要**: 询问用户获取 API Key

#### 2. 其他视频生成 API
**用途**: 备用视频生成（如果 Kling 不可用）
**状态**: ❌ 未配置
**可选**: Runway, Pika, Luma

---

## 📋 完整工作流程

### 方式 1: 使用流水线执行器（推荐）

```bash
python3 ~/.openclaw/skills/multimedia/run_pipeline.py \
  "主题" \
  "场景描述" \
  60 \
  "YouTube" \
  /path/to/project
```

### 方式 2: 手动执行每个 Phase

```bash
# Phase 1: 调研+剧本
python3 scripts/script_generator.py "主题" "场景" 60 "YouTube" /project

# Phase 2: 参考图
python3 scripts/reference_generator.py front back left right --project name

# Phase 3: 分镜图
python3 scripts/storyboard_generator.py --project name --grid 3x3

# Phase 4: 拆分
python3 scripts/split_storyboard_improved.py --input storyboard.png --output ./frames

# Phase 5: 视频生成
# 通过 media-video skill

# Phase 6: 剪辑配音
# 通过 audio skill
```

---

## 🚨 常见问题与解决方案

### Q1: 工具找不到
**症状**: `FileNotFoundError: No such file or directory`
**解决**: 检查工具路径是否正确
```bash
ls -la ~/.openclaw/skills/multimedia/scripts/
```

### Q2: API Key 未配置
**症状**: `Error: API Key not found`
**解决**: 检查配置文件
```bash
cat ~/.openclaw/skills/media-image/config/kie-api-keys.json
cat ~/.openclaw/skills/gemini-analyzer/config/api.json
```

### Q3: Gemini 视频分析超时
**症状**: `The read operation timed out`
**解决**: 
- 使用 YouTube URL 而不是本地文件
- 或使用 gemini-2.5-flash 模型
- 详见: `~/.openclaw/skills/gemini-analyzer/references/usage-experience.md`

### Q4: 分镜拆分失败
**症状**: 拆分后的图片不正确
**解决**: 使用改进版工具
```bash
python3 scripts/split_storyboard_improved.py --help
```

---

## 📚 参考文档

### 核心文档
- `SKILL.md` - 本文件（主文档）
- `references/INDEX.md` - 知识库索引
- `references/workflow-experience.md` - 完整流水线经验

### 改进文档
- `~/.openclaw/workspace/SKILL_IMPROVEMENT_GUIDE.md` - 工具改进说明
- `~/.openclaw/workspace/SKILL_REVIEW_REPORT.md` - 质量审查报告

### 相关 Skill
- `~/.openclaw/skills/media-image/` - 图片生成
- `~/.openclaw/skills/media-video/` - 视频生成
- `~/.openclaw/skills/audio/` - 音频生成
- `~/.openclaw/skills/crawler/` - 深度搜索
- `~/.openclaw/skills/gemini-analyzer/` - 图片/视频分析

---

## ⚡ 快速开始

### 最小化示例
```bash
# 1. 创建项目目录
mkdir -p ~/multimedia-projects/my-project

# 2. 生成剧本
python3 ~/.openclaw/skills/multimedia/scripts/script_generator.py \
  "美少女战士 vs 一拳超人" \
  "城市街头激烈大战" \
  60 \
  "YouTube" \
  ~/multimedia-projects/my-project

# 3. 生成分镜图
python3 ~/.openclaw/skills/multimedia/scripts/storyboard_generator.py \
  --project my-project \
  --grid 3x3

# 4. 拆分分镜
python3 ~/.openclaw/skills/multimedia/scripts/split_storyboard_improved.py \
  --input ~/multimedia-projects/my-project/storyboard_full.png \
  --output ~/multimedia-projects/my-project/frames \
  --rows 3 \
  --cols 3 \
  --project my-project

# 5. 生成视频（通过 media-video skill）
# 6. 剪辑配音（通过 audio skill）
```

---

## 🎯 给其他 AI 的重要提示

### ✅ 可以做的
1. 使用本文档中列出的所有工具
2. 调用相关的 skill（media-image, media-video, audio, crawler）
3. 询问用户缺失的 API Key
4. 根据用户需求调整参数

### ❌ 不要做的
1. **不要自己编写新的脚本**（除非确认功能缺失）
2. 不要修改现有工具的核心逻辑
3. 不要硬编码 API Key 或路径
4. 不要跳过错误处理

### 🤔 不确定时
1. 先查看本文档
2. 查看相关的参考文档
3. 询问用户

---

## 📞 联系与支持

**作者**: Leon (OpenClaw AI Assistant)
**版本**: v2.0
**最后更新**: 2026-03-03
**状态**: ✅ 生产就绪

**问题反馈**: 如有问题或建议，请联系用户

---

**文档结束**
