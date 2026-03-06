# 多媒体流水线实战经验

## 完整流程 (2026-03-02 实测)

### 项目: 蒙面超人 VS 超人
- 目录: ~/multimedia-projects/masked-rider-vs-superman/
- 总耗时: ~2小时
- 迭代次数: 参考图4次，分镜图2次

## Step 1: 剧本生成 ✅
- 输入: 主题 "蒙面超人 VS 超人"
- 输出: script.md (6个分镜)
- 耗时: ~5分钟
- 经验: 无问题

## Step 2: 参考图生成 ⚠️

### 迭代历史
1. **第一版** ❌ - 分开生成6张
   - 问题: 应该合一张，不是分开
   
2. **第二版** ❌ - 三视图合一张 21:9
   - 问题: 不够真人，风格偏卡通
   
3. **第三版** ⚠️ - 四视图 21:9
   - 问题: 凭想象写 prompt，没分析参考图
   
4. **第四版** ✅ - 基于用户参考图
   - 用户提供花瓣网参考图
   - 先分析外观特征
   - 提取 Subject Lock
   - 生成四视图

### 关键教训
- ❌ **不要凭想象写 prompt**
- ✅ **先分析用户提供的参考图**
- ✅ **提取 Subject Lock 描述**
- ✅ **使用标准模板 (四视图/三视图)**

### 用户参考图特征
**蒙面超人:**
- 黑金配色昆虫铠甲
- 红色复眼
- 金色纹路
- 电影级CG质感

**超人:**
- Henry Cavill 风格
- 暗色调废墟背景
- 深蓝战衣 + 红披风
- 肌肉线条清晰

## Step 3: 分镜图生成 ✅

### 第一版 (2×3)
- 分辨率: 4K
- 文件大小: 8.4M
- 网格: 2行×3列

### 第二版 (3×3) - 用户模板
- 用户提供电影分镜模板
- 9个镜头: ELS→LS→MS→CU→ECU→低角→高角→POV→Final
- 更专业的电影级构图

### 经验
- 用户提供的模板很重要
- 3×3 比 2×3 更丰富
- Subject Lock 确保角色一致性

## Step 4: 拆分增强 ✅
- 输入: storyboard_full.jpg
- 输出: 6张 raw + 6张 clean
- 拆分脚本: frame_splitter.py
- 经验: 无问题

## Step 5: 图片增强 ✅
- 输入: 6张 clean (原始分辨率)
- 输出: 6张 2K (~3M each)
- 耗时: ~10分钟
- 经验: 无问题

## Step 6: 视频生成 (未完成)
- 超人四视图还在 waiting
- taskId: 6136fa10b422f752fa5edfc68d980a74

## 总结

### 成功经验
1. 先分析参考图，再写 prompt
2. 使用 Subject Lock 保持一致性
3. 采用标准模板 (四视图/三视图/3×3分镜)
4. Python urllib 比 curl 稳定

### 待改进
1. 参考图上传功能 (被 Cloudflare 拦截)
2. frame_splitter.py 升级 (title bar 检测)
3. SSML 情绪预设模板
4. 视频生成流程优化

## Gemini 视频分析

### 可用模型
- gemini-3-pro-preview（最新旗舰）
- gemini-3.1-pro-preview
- gemini-2.5-pro（推荐，平衡性能）
- gemini-2.5-flash（快速）
- gemini-2.5-flash-lite（轻量）
- gemini-3-flash-preview

### 支持的视频源
1. **YouTube 链接** - 直接传 URL，Gemini 原生支持
2. **在线视频 URL** - 公开可访问的视频链接
3. **本地视频文件** - 需要先上传或转换为 URL

### 使用示例
```bash
# 分析 YouTube 视频
python3 video_analyzer.py \
  "https://youtube.com/watch?v=xxx" \
  "分析这个广告的分镜构图和运镜技巧" \
  gemini-2.5-pro

# 分析在线视频
python3 video_analyzer.py \
  "https://example.com/ad.mp4" \
  "提取关键场景和色调" \
  gemini-2.5-flash
```

### 集成到流水线
在 Phase 1（剧本生成）前，可以先分析参考视频：
1. 用户提供参考视频 URL
2. 调用 video_analyzer.py 生成分析任务
3. 通过 sessions_spawn 调用 Gemini 分析
4. 提取关键特征用于剧本生成

## 参考图生成灵活化（2026-03-03 更新）

### 不再固定三视图/六视图
根据项目需求灵活生成任意数量和角度的参考图。

### 预定义视图类型

**基础视图**（适合大部分项目）:
- front（正面）
- back（背面）
- left（左侧）
- right（右侧）
- top（俯视）
- bottom（仰视）

**细节视图**（产品/人物特写）:
- detail-face（面部特写）
- detail-hands（手部特写）
- detail-feet（脚部/鞋子特写）
- detail-texture（材质特写）
- detail-logo（标志特写）

**产品视图**（电商/广告）:
- product-hero（主视图）
- product-45（45度角）
- product-flat（平铺）
- product-lifestyle（场景图）

**动作视图**（人物动态）:
- action-walk（行走）
- action-run（奔跑）
- action-jump（跳跃）
- action-sit（坐姿）

### 使用示例

```bash
# 默认（只生成正反面）
python3 reference_generator.py "黑金铠甲超人" ./ref

# 基础四视图
python3 reference_generator.py "运动鞋" ./ref front back left right

# 产品特写（电商）
python3 reference_generator.py "智能手表" ./ref product-hero product-45 detail-texture detail-logo

# 人物动作（广告）
python3 reference_generator.py "运动员" ./ref front action-run action-jump detail-face

# 自定义视图
python3 reference_generator.py "汽车" ./ref "front:正面:front view" "custom:引擎盖:hood close-up"
```

### 实战建议
- **简单产品**: 2-4 张（正反面 + 1-2 个细节）
- **复杂产品**: 4-6 张（四视图 + 2 个细节）
- **人物模特**: 2-3 张（正面 + 1-2 个动作/细节）
- **场景道具**: 1-2 张（主视图 + 细节）

## API 结果 URL 管理（2026-03-03 重要更新）

### 核心原则
**所有在线 API 生成的图片/视频，必须保存返回的 URL！**

### 原因
1. 文件太大（图片 3-8MB，视频几百 MB）
2. 上传下载麻烦
3. URL 可以直接复用（分析、生成视频、分享）
4. 避免重复生成浪费 API 调用

### 实施方案
每个生成工具都要保存 task.json：
- Phase 2: `reference_views/{view}_task.json`
- Phase 3: `storyboard_task.json`
- Phase 5: `videos/{frame_id}_task.json`

### 查找历史 URL
如果忘记保存，可以：
1. 浏览器访问 https://kie.ai/logs
2. 找到对应的 taskId
3. 点击 "Result" 或 "Copy All URLs"
4. 手动保存到 JSON 文件

## 2026-03-03 Phase 5 视频生成实战

### 完整流程
1. 分镜图拆分（frame_splitter.py）
2. 分析每张图片内容（需要 Gemini vision）
3. 生成运镜逻辑和 Prompt
4. 调用 Kling 2.5 Turbo 生成视频
5. 保存 URL 到 JSON（14天有效期）
6. 下载视频到本地

### 关键教训
1. **必须先分析图片再写 Prompt** - 不能凭想象，要基于实际图片内容
2. **运镜描述放最前面** - "Slow push in camera movement. [场景]..."
3. **URL 立即保存** - 14天后会删除，必须保存到 JSON
4. **Gemini 配置很重要** - 图片/视频分析依赖 Gemini API

### 待解决问题
1. Gemini vision API 配置（node-hk 端点 404）
2. 视频下载 403 问题
3. 脚步动作不自然的优化

### 下一步
1. 完成 multimedia-analyzer skill（Gemini vision）
2. 生成剩余 5 个视频（P4, P5, P6, P8, P9）
3. 剪辑合成完整视频

## 2026-03-03 完整工具链总结

### 已完成的工具
1. **script_generator.py** - 调研 + 剧本生成
2. **reference_generator.py** - 参考图生成（三视图/六视图）
3. **storyboard_generator.py** - 整张分镜图生成
4. **frame_splitter.py** - 分镜拆分（GPT 优化版）
5. **视频生成脚本** - Kling 2.5 Turbo 调用

### 工具使用流程
```bash
# Phase 1: 调研与剧本
python3 ~/.openclaw/skills/multimedia/scripts/script_generator.py "蒙面超人 VS 超人"

# Phase 2: 参考图（可选）
python3 ~/.openclaw/skills/multimedia/scripts/reference_generator.py front back

# Phase 3: 分镜图
python3 ~/.openclaw/skills/multimedia/scripts/storyboard_generator.py

# Phase 4: 拆分
python3 ~/.openclaw/skills/multimedia/scripts/frame_splitter.py masked-rider-vs-superman

# Phase 5: 视频生成
# 使用 ~/.openclaw/workspace/generate_kling_videos.py
# 或手动调用 kie.ai API
```

### 关键配置
- **kie.ai API Keys**: 9 个可轮换使用（避免限流）
- **限流间隔**: 12-15 秒
- **视频参数**: 720p, 5秒, cfg_scale=0.5
- **URL 保存**: 14天有效期，必须立即保存到 JSON

### 待解决问题
1. Gemini vision API 配置（图片/视频分析）
2. 视频下载 403 问题（需要特殊 headers）
3. 脚步动作不自然的优化（需要更精确的 prompt）

### 下一步计划
1. 完成剩余 5 个视频生成（P4, P5, P6, P8, P9）
2. 配置 Gemini vision 分析工具
3. 开发 Phase 6 剪辑配音工具
