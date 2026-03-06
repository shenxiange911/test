# 提示词模板库

## Subject Lock 机制
在生成参考图后，提取外观描述作为 Subject Lock，附加到后续所有 prompt 中，确保角色一致性。

### 示例
```
Subject Lock (蒙面超人):
Black and gold insect-themed armor, red compound eyes, golden patterns, cinematic CG quality

Subject Lock (超人):
Henry Cavill style, dark blue suit with red cape, muscular build, heroic pose
```

## 参考图 Prompt 模板

### 四视图 (21:9)
```
Character turnaround sheet, 4 views (front, left side, back, right side), 
[角色描述], standing pose, neutral background, 
cinematic lighting, ultra detailed, 8K, professional concept art
```

### 三视图 (21:9)
```
Character design sheet, 3 views (front, side, back),
[角色描述], T-pose, white background,
high detail, concept art style
```

## 分镜图 Prompt 模板

### 电影级分镜 (3×3)
```
Cinematic contact sheet, 9 panels storyboard:
1. ELS (Extreme Long Shot) - [场景描述]
2. LS (Long Shot) - [场景描述]
3. MS (Medium Shot) - [场景描述]
4. CU (Close Up) - [场景描述]
5. ECU (Extreme Close Up) - [场景描述]
6. Low angle - [场景描述]
7. High angle - [场景描述]
8. POV shot - [场景描述]
9. Final shot - [场景描述]

Style: [Subject Lock], cinematic lighting, epic atmosphere
```

### 简化版 (2×3)
```
Storyboard layout, 6 panels in 2 rows:
[逐个分镜描述]

Style: [Subject Lock], movie quality
```

## Negative Prompt 模板
```
blurry, low quality, distorted, deformed, ugly, bad anatomy, 
extra limbs, missing limbs, floating objects, watermark, text, 
cartoon style, anime style, oversaturated colors
```

## 实战经验 (2026-03-02)

### 错误示范
- ❌ 凭想象写 prompt，不分析参考图
- ❌ 分开生成多张参考图（应该合一张）
- ❌ 忽略用户提供的参考图模板

### 正确流程
1. 用户提供参考图 → 先分析外观特征
2. 提取 Subject Lock 描述
3. 基于模板生成四视图/三视图
4. 用 Subject Lock 生成分镜图
5. 保持风格一致性
