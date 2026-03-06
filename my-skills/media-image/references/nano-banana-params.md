# Nano Banana Pro 参数表

## 基础参数
| 参数 | 默认值 | 范围 | 说明 |
|------|--------|------|------|
| width | 1024 | 512-2048 | 图片宽度 |
| height | 1024 | 512-2048 | 图片高度 |
| guidance_scale | 7.5 | 1-20 | 提示词引导强度 |
| num_inference_steps | 50 | 20-100 | 推理步数 |
| seed | random | 0-2^32 | 随机种子 |

## 高级参数
| 参数 | 默认值 | 范围 | 说明 |
|------|--------|------|------|
| denoising_strength | 0.75 | 0-1 | 图生图去噪强度 |
| scheduler | DPM++ 2M Karras | - | 采样器类型 |
| clip_skip | 1 | 1-2 | CLIP 跳过层数 |

## 常用分辨率

### 标准比例
- 1:1 → 1024×1024 (正方形)
- 4:3 → 1024×768 (传统)
- 16:9 → 1920×1080 (横屏)
- 9:16 → 1080×1920 (竖屏)

### 特殊比例
- 21:9 → 2560×1080 (超宽屏，适合参考图)
- 2:3 → 1024×1536 (分镜网格)
- 3:2 → 1536×1024 (横向分镜)

## 推荐配置

### 参考图生成 (四视图/三视图)
```json
{
  "width": 2560,
  "height": 1080,
  "guidance_scale": 8.0,
  "num_inference_steps": 60,
  "negative_prompt": "blurry, low quality, distorted..."
}
```

### 分镜图生成 (2×3 或 3×3)
```json
{
  "width": 2048,
  "height": 1536,
  "guidance_scale": 7.5,
  "num_inference_steps": 50
}
```

### 单张精修
```json
{
  "width": 2048,
  "height": 2048,
  "guidance_scale": 9.0,
  "num_inference_steps": 80
}
```

## 实测数据 (2026-03-02)
- 4K 分镜图 (2×3): 8.4M
- 2K 增强图: ~3M each
- 生成时间: 30-60秒/张
