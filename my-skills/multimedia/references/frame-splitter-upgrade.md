# frame_splitter.py 升级计划

## 当前版本问题
- 简单的网格切割
- 没有 title bar 检测
- 没有 border trim 安全阈值

## GPT 版精华功能

### 1. Title Bar 检测
```python
def detect_title_bar(image):
    """检测顶部标题栏区域"""
    # 扫描顶部 10% 区域
    # 检测文字密度
    # 返回标题栏高度
    pass
```

### 2. Border Trim 安全阈值
```python
def safe_trim_borders(image, threshold=10):
    """安全裁剪边框，避免过度裁剪"""
    # 检测边缘像素
    # 设置最小保留边距
    # 避免裁掉重要内容
    pass
```

### 3. 智能网格检测
```python
def detect_grid_layout(image):
    """自动检测网格布局 (2×3 或 3×3)"""
    # 分析图片比例
    # 检测分隔线
    # 返回行列数
    pass
```

## 升级优先级
1. **高**: Border Trim 安全阈值 (避免裁掉内容)
2. **中**: Title Bar 检测 (提高准确性)
3. **低**: 智能网格检测 (当前手动指定也可以)

## 实施计划
- [ ] 备份当前版本
- [ ] 实现 safe_trim_borders()
- [ ] 测试多个分镜图
- [ ] 实现 detect_title_bar()
- [ ] 更新 04-split/SKILL.md 文档

## GPT 版本特性 (已实现)

### ✅ 已有功能
1. **Title Bar 检测** - 自动跳过顶部 8% 标题区域
2. **Border Trim** - 自动去除黑边/白边 (threshold=20)
3. **自动网格切割** - 按 rows × cols 均匀切割
4. **序号命名** - project_name_01.png, 02.png...

### 核心算法
```python
# 1. 跳过标题栏
title_h = int(H * 0.08)
usable = img.crop((0, title_h, W, H))

# 2. 均匀切割
cell_w = uW // cols
cell_h = uH // rows

# 3. 去边检测
def is_border_row(row):
    return (row.mean() < 20) or (row.mean() > 235)
```

### 使用示例
```bash
# 2×3 分镜
python3 frame_splitter.py storyboard.png 2 3 ./frames masked_rider

# 3×3 分镜
python3 frame_splitter.py storyboard_3x3.jpg 3 3 ./frames_v2 superman
```

### 输出
- masked_rider_01.png
- masked_rider_02.png
- ...
- masked_rider_06.png
