# 产品分镜图生成器使用文档

## 概述

`generate_product_storyboard.py` 是基于 **Nano Banana Prompt Protocol v2.3** 的产品分镜图生成工具。

核心特性：
- **模板化 Prompt 构建** — 自动填充标准化提示词模板
- **灵活配置** — 支持自定义产品、分镜数量、画布尺寸
- **坐标系锁定** — 确保所有分镜中产品外观严格一致
- **多分辨率支持** — 2K/4K/8K 可选

---

## 快速开始

### 1. 基础用法

```bash
cd ~/.openclaw/skills/media-image/scripts
python3 generate_product_storyboard.py --config ../examples/product-storyboard-config.json --output /path/to/output.png
```

### 2. 配置文件结构

```json
{
  "images": {
    "多视角参考图": "产品外观数据来源",
    "使用场景参考图": "连接方式与场景参考"
  },
  "aspect_ratio": "16:9",
  "panel_layout": "2×2",
  "resolution": "4K",
  "panels": [
    {
      "position": "Panel A 左上",
      "description": "产品英雄视角特写"
    }
  ]
}
```

---

## 配置参数详解

### 核心参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `images` | Object | 必填 | 参考图角色定义 |
| `aspect_ratio` | String | `"16:9"` | 画布宽高比 (16:9/21:9/1:1/自定义) |
| `panel_layout` | String | `"2×2"` | 分镜网格布局 (2×2/2×3/3×3) |
| `resolution` | String | `"2K"` | 输出分辨率 (1K/2K/4K) |
| `panels` | Array | 必填 | 分镜描述列表 |

### 高级参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `scan_instructions` | String | 自动生成 | 参考图扫描指令 |
| `coordinate_system` | String | 自动生成 | 坐标系定义 |
| `synthesis_instructions` | String | 自动生成 | 3D 合成指令 |
| `style` | String | 写实摄影风格 | 渲染风格 |
| `global_lock` | String | 自动生成 | 全局一致性锁定规则 |
| `rules` | Array | 自动生成 | 输出规则列表 |
| `negative_prompt` | String | 可选 | 负面提示词 |
| `guidance_scale` | Float | 7.5 | 引导强度 |
| `num_inference_steps` | Integer | 50 | 推理步数 |

---

## 分辨率与尺寸对照表

| 分辨率 | 16:9 尺寸 | 21:9 尺寸 | 1:1 尺寸 |
|--------|-----------|-----------|----------|
| 1K | 1024×576 | 1024×439 | 1024×1024 |
| 2K | 2048×1152 | 2048×878 | 2048×2048 |
| 4K | 4096×2304 | 4096×1755 | 4096×4096 |

---

## 使用示例

### 示例 1: 标准 2×2 产品分镜 (默认模板)

```bash
python3 generate_product_storyboard.py \
  --config ../examples/product-storyboard-config.json \
  --output ~/output/product-2x2.png
```

**配置文件**: `product-storyboard-config.json`
- 2K 分辨率 (2048×1152)
- 2×2 网格布局
- 4 个分镜：英雄视角 / 正面平铺 / 连接场景 / 使用环境

### 示例 2: 自定义 2×3 六格分镜

```bash
python3 generate_product_storyboard.py \
  --config ../examples/custom-6-panel-config.json \
  --output ~/output/product-2x3.png
```

**配置文件**: `custom-6-panel-config.json`
- 2K 分辨率 (2048×1152)
- 2×3 网格布局
- 6 个分镜：正面/侧面/背面 + 3 个使用场景

### 示例 3: 高分辨率 3×3 九格分镜

创建配置文件 `9-panel-config.json`:

```json
{
  "images": {
    "产品参考图": "产品外观数据源"
  },
  "aspect_ratio": "16:9",
  "panel_layout": "3×3",
  "resolution": "4K",
  "panels": [
    {"position": "Panel 1", "description": "产品正面特写"},
    {"position": "Panel 2", "description": "产品侧面视角"},
    {"position": "Panel 3", "description": "产品背面视角"},
    {"position": "Panel 4", "description": "产品顶部视角"},
    {"position": "Panel 5", "description": "产品底部视角"},
    {"position": "Panel 6", "description": "产品细节特写 - 接口"},
    {"position": "Panel 7", "description": "使用场景 1 - 桌面"},
    {"position": "Panel 8", "description": "使用场景 2 - 手持"},
    {"position": "Panel 9", "description": "使用场景 3 - 环境氛围"}
  ]
}
```

```bash
python3 generate_product_storyboard.py \
  --config 9-panel-config.json \
  --output ~/output/product-3x3-4k.png
```

---

## 工作流程

```
1. 读取配置文件
   ↓
2. 构建 Nano Banana Prompt Protocol v2.3 提示词
   ↓
3. 计算最终图片尺寸 (基于 resolution + aspect_ratio)
   ↓
4. 调用 kie.ai API (nano-banana-pro 模型)
   ↓
5. 等待任务完成 (12 秒间隔轮询，避免限流)
   ↓
6. 下载生成的图片到指定路径
```

---

## 注意事项

### ⚠️ API 限流
- 任务查询间隔固定为 **12 秒**，避免触发 kie.ai 限流
- 默认最大等待时间 **300 秒** (5 分钟)

### ⚠️ 参考图要求
- **IMG_A (多视角参考图)**: 必须包含产品的正面/侧面/背面视图
- **IMG_B (使用场景参考图)**: 展示产品的连接方式和使用场景
- 参考图需要在调用 API 前上传到 kie.ai 或提供 URL

### ⚠️ 坐标系一致性
- 所有分镜中产品的外观、丝印、接口位置必须严格一致
- 坐标系锁定机制确保不因视角变化产生偏差

### ⚠️ 分镜数量
- 支持任意数量的分镜 (2/4/6/9/12...)
- `panel_layout` 参数决定网格布局 (如 2×2, 2×3, 3×3)
- 分镜数量应与 `panels` 数组长度一致

---

## 故障排查

### 问题 1: API Key 未找到
```
错误: 未找到 KIE_API_KEY
```

**解决方案**:
```bash
export KIE_API_KEY="your-api-key"
# 或在 ~/.openclaw/openclaw.json 中配置
```

### 问题 2: 任务超时
```
{"error": "Timeout", "detail": "Task not completed after 300s"}
```

**解决方案**:
- 检查 kie.ai API 状态
- 增加 `max_wait` 参数 (修改脚本中的默认值)
- 降低分辨率 (4K → 2K)

### 问题 3: 图片下载失败
```
下载失败: HTTP Error 403
```

**解决方案**:
- 检查任务状态是否为 `completed`
- 确认输出路径有写入权限
- 检查网络连接

---

## 进阶用法

### 自定义宽高比

```json
{
  "aspect_ratio": "3:2",
  "resolution": "2K"
}
```

计算逻辑: `width = 2048, height = 2048 * 2 / 3 = 1365`

### 自定义负面提示词

```json
{
  "negative_prompt": "blurry, low quality, distorted, watermark, text overlay, annotations, cartoon style, anime style"
}
```

### 调整生成参数

```json
{
  "guidance_scale": 8.0,
  "num_inference_steps": 60
}
```

- `guidance_scale`: 引导强度 (7.0-10.0，越高越严格遵循 prompt)
- `num_inference_steps`: 推理步数 (30-100，越高质量越好但速度越慢)

---

## 相关文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 主脚本 | `scripts/generate_product_storyboard.py` | 分镜图生成器 |
| API 工具 | `scripts/kie_api.py` | kie.ai API 调用工具 |
| 示例配置 1 | `examples/product-storyboard-config.json` | 标准 2×2 四格分镜 |
| 示例配置 2 | `examples/custom-6-panel-config.json` | 自定义 2×3 六格分镜 |
| 提示词模板库 | `references/prompt-templates.md` | 其他提示词模板参考 |

---

## 更新日志

### v1.0.2 (2026-03-04)
- ✅ 确认支持 1K/2K/4K 分辨率（根据官方脚本）

### v1.0.1 (2026-03-04)
- 🐛 修正分辨率限制：Nano Banana Pro 最大 2048×2048（不支持 4K/8K）
- ✅ 更新文档和示例配置

### v1.0.0 (2026-03-04)
- ✅ 实现 Nano Banana Prompt Protocol v2.3 模板
- ✅ 支持自定义分镜数量和布局
- ✅ 集成 kie.ai API 调用
- ✅ 12 秒间隔轮询，避免限流

---

## 许可证

MIT License
