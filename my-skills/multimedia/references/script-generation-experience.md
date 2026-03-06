# 剧本生成经验

## 基本流程

### 输入
- 主题/概念（如 "蒙面超人 VS 超人"）
- 风格要求（动作片/科幻/悬疑等）
- 时长要求（30秒/1分钟/3分钟）

### 输出
- script.md 文件
- 包含：标题、概述、分镜列表（6-9个）

## 分镜结构

### 标准 6 分镜 (2×3)
1. 开场 - 建立场景
2. 角色A登场
3. 角色B登场
4. 冲突/对峙
5. 高潮动作
6. 结尾/悬念

### 电影级 9 分镜 (3×3)
1. ELS (Extreme Long Shot) - 超远景，建立环境
2. LS (Long Shot) - 远景，角色全身
3. MS (Medium Shot) - 中景，半身
4. CU (Close Up) - 特写，面部
5. ECU (Extreme Close Up) - 大特写，眼睛/细节
6. Low Angle - 低角度，仰拍
7. High Angle - 高角度，俯拍
8. POV Shot - 主观视角
9. Final Shot - 结尾镜头

## 实战经验 (2026-03-02)

### 成功案例：蒙面超人 VS 超人

**主题**: 两个英雄的对决
**风格**: 电影级动作片
**分镜数**: 6个

**剧本要点**:
1. 废墟场景建立氛围
2. 蒙面超人先登场（黑金铠甲）
3. 超人后登场（红蓝战衣）
4. 眼神对峙（张力）
5. 动作爆发（拳头碰撞）
6. 悬念结尾（谁会赢？）

### 关键技巧

1. **视觉化描述**
   - ❌ "两人打斗"
   - ✅ "蒙面超人挥出右拳，超人用左手格挡，火花四溅"

2. **镜头语言**
   - 明确镜头类型（特写/全景/中景）
   - 明确角度（平视/仰拍/俯拍）
   - 明确运动（静止/推进/旋转）

3. **情绪节奏**
   - 开场：平静 → 紧张
   - 中段：对峙 → 爆发
   - 结尾：高潮 → 悬念

4. **角色一致性**
   - 提前确定角色外观
   - 每个分镜都要提到角色特征
   - 保持 Subject Lock

## 提示词模板

### 生成剧本
```
Create a 6-panel storyboard script for: [主题]

Style: [风格]
Duration: [时长]

For each panel, provide:
1. Panel number
2. Shot type (ELS/LS/MS/CU/ECU)
3. Camera angle (low/high/eye-level)
4. Scene description (visual details)
5. Action/emotion
6. Lighting/atmosphere

Focus on visual storytelling, cinematic composition, and emotional impact.
```

### 扩展到 9 分镜
```
Expand this 6-panel script to a 9-panel cinematic storyboard:

[原剧本]

Add these shot types:
- ECU (Extreme Close Up) for emotional detail
- POV shot for immersion
- Additional angle variation (low/high)

Maintain story flow and pacing.
```

## 常见问题

### 问题1: 分镜太平淡
**原因**: 缺少镜头变化
**解决**: 混合使用 ELS/MS/CU，避免全是中景

### 问题2: 角色描述不一致
**原因**: 没有 Subject Lock
**解决**: 先生成参考图，提取外观描述

### 问题3: 节奏拖沓
**原因**: 每个分镜信息量不均
**解决**: 开场简洁，高潮密集，结尾留白

## 工具集成

### 自动化流程
1. 用户输入主题
2. Opus 生成剧本 (script.md)
3. 提取角色列表
4. 生成参考图（四视图）
5. 提取 Subject Lock
6. 基于剧本 + Subject Lock 生成分镜图

### 人工确认点
- 剧本生成后：确认分镜数量和节奏
- 参考图生成后：确认角色外观
- 分镜图生成后：确认构图和风格
