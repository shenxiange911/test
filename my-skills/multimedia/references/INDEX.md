# Multimedia Skill 知识库索引

## 📚 文档结构

### 核心文档
- **SKILL.md** - Skill 使用说明和快速开始
- **INDEX.md** (本文件) - 知识库总索引
- **workflow-experience.md** - 完整流水线实战经验

### 专题文档
- **script-generation-experience.md** - 剧本生成经验
- **frame-splitter-upgrade.md** - 分镜拆分工具升级计划

## 🛠️ 工具清单

### Phase 1: 调研与剧本
- `scripts/script_generator.py` - 调用 crawler 深度搜索 + 生成剧本模板

### Phase 2: 参考图生成
- `scripts/reference_generator.py` - 三视图/六视图参考图生成
- 依赖: `~/.openclaw/skills/media-image/scripts/kie_api.py`

### Phase 3: 分镜图生成
- `scripts/storyboard_generator.py` - 整张分镜图生成（3×3 grid）

### Phase 4: 分镜拆分与增强
- `scripts/frame_splitter.py` - GPT 优化版，Title Bar 检测 + Border Trim
- 特性：自动检测网格、去黑边白边、序号命名

### Phase 5: 视频生成
- 工具：使用 `~/.openclaw/skills/media-video/` 中的 Kling API
- 参考：`~/.openclaw/workspace/storyboard_prompts_final.md`

### Phase 6: 剪辑配音（待开发）
- 音频：`~/.openclaw/skills/audio/`
- 视频编辑：待集成

## 📖 经验文档索引

### 完整流水线
**文件**: `workflow-experience.md`
**内容**:
- 2026-03-02: 蒙面超人 VS 超人项目完整流程
- 2026-03-03: Phase 5 视频生成实战
- 关键教训：先分析图片再写 prompt、Subject Lock 机制、URL 保存规则

### 剧本生成
**文件**: `script-generation-experience.md`
**内容**:
- 分镜结构设计（9格/12格）
- 镜头语言（ECU/CU/MS/WS/EWS）
- 运镜方式（Push in/Pull out/Pan/Static/Tracking）

### 分镜拆分
**文件**: `frame-splitter-upgrade.md`
**内容**:
- GPT 优化版特性
- Title Bar 检测算法
- Border Trim 阈值调优

## 🔗 相关 Skill 链接

### media-image Skill
**路径**: `~/.openclaw/skills/media-image/`
**用途**: AI 图片生成/编辑/放大
**索引**: `references/INDEX.md`
**核心工具**:
- `scripts/kie_api.py` - kie.ai API 调用（12秒间隔避免限流）
- `references/prompt-templates.md` - 提示词模板库
- `references/kie-ai-api-experience.md` - API 实战经验

### media-video Skill
**路径**: `~/.openclaw/skills/media-video/`
**用途**: AI 视频生成/编辑
**索引**: `SKILL.md`
**核心经验**:
- `references/kling-2.5-turbo-experience.md` - Kling 实战经验

### audio Skill
**路径**: `~/.openclaw/skills/audio/`
**用途**: TTS 语音合成、STT 语音转文字、音效生成

## 🎯 快速查找

### 我想生成参考图
→ 查看 `media-image/references/prompt-templates.md`
→ 使用 `multimedia/scripts/reference_generator.py`

### 我想生成分镜图
→ 查看 `workflow-experience.md` 中的 3×3 grid 经验
→ 使用 `multimedia/scripts/storyboard_generator.py`

### 我想拆分分镜
→ 使用 `multimedia/scripts/frame_splitter.py`
→ 查看 `frame-splitter-upgrade.md` 了解参数

### 我想生成视频
→ 查看 `media-video/references/kling-2.5-turbo-experience.md`
→ 参考 `~/.openclaw/workspace/storyboard_prompts_final.md`

### 我想了解完整流程
→ 查看 `workflow-experience.md`

## 📝 更新日志

- 2026-03-02: 建立 multimedia skill 知识库
- 2026-03-03: 完成 Phase 5 视频生成实战，更新索引
- 2026-03-03: 添加工具清单和快速查找指南
