# 输出验证器集成示例

## 1. 在 reference_generator.py 中使用

```python
from output_validator import OutputValidator

# 在下载图片后验证
validator = OutputValidator(verbose=True)
if not validator.validate_image(output_path, min_resolution=(512, 512)):
    print(f"⚠️ 图片验证失败: {', '.join(validator.errors)}")
    print(f"🔄 跳过此视图，继续下一个...")
    continue
```

**已集成位置：** `~/.openclaw/skills/multimedia/scripts/reference_generator.py` (第 136-141 行)

---

## 2. 在 storyboard_generator.py 中使用

```python
from output_validator import OutputValidator

# 验证分镜图
validator = OutputValidator(verbose=True)
min_resolution = (1024 * cols, 576 * rows)  # 根据网格计算最小分辨率

if not validator.validate_image(output_path, min_resolution=min_resolution):
    print(f"⚠️ 分镜图验证失败: {', '.join(validator.errors)}")
    return None
```

**已集成位置：** `~/.openclaw/skills/multimedia/scripts/storyboard_generator.py` (第 108-115 行)

---

## 3. 带重试的验证

```python
from output_validator import OutputValidator, validate_with_retry

validator = OutputValidator(verbose=True)

# 自动重试 3 次，每次间隔 2 秒
success, error = validate_with_retry(
    validator,
    validator.validate_image,
    max_retries=3,
    retry_delay=2.0,
    file_path=output_path,
    min_resolution=(1024, 768)
)

if not success:
    print(f"❌ 验证失败（已重试 3 次）: {error}")
```

---

## 4. JSON 结果验证

```python
from output_validator import OutputValidator

validator = OutputValidator(verbose=True)

# 验证 API 返回结果
api_result = {
    "status": "success",
    "taskId": "task_123",
    "image_url": "https://example.com/image.png"
}

if not validator.validate_json_result(
    api_result,
    required_fields=["status", "taskId", "image_url"],
    check_urls=False  # 生产环境可设为 True
):
    print(f"❌ API 结果验证失败: {', '.join(validator.errors)}")
    return None
```

---

## 5. 视频验证（未来扩展）

```python
from output_validator import OutputValidator

validator = OutputValidator(verbose=True)

# 验证视频文件
if not validator.validate_video(
    video_path,
    min_duration=1.0,  # 最少 1 秒
    check_codec=True
):
    print(f"❌ 视频验证失败: {', '.join(validator.errors)}")
```

---

## 6. 批量验证

```python
from output_validator import OutputValidator

validator = OutputValidator(verbose=True)

# 批量验证多个文件
files = ["image1.png", "image2.png", "image3.png"]
results = []

for f in files:
    valid = validator.validate_image(f, min_resolution=(512, 512))
    results.append({
        'file': f,
        'valid': valid,
        'error': None if valid else validator.get_error_message()
    })

# 统计结果
passed = sum(1 for r in results if r['valid'])
print(f"✅ 批量验证完成: {passed}/{len(files)} 通过")
```

---

## 验证规则配置

可以在 `output_validator.py` 中调整验证规则：

```python
class OutputValidator:
    # 图片验证规则
    IMAGE_MIN_SIZE = 1 * 1024  # 1KB
    IMAGE_MAX_SIZE = 50 * 1024 * 1024  # 50MB
    IMAGE_MIN_RESOLUTION = (256, 256)
    
    # 视频验证规则
    VIDEO_MIN_SIZE = 100 * 1024  # 100KB
    VIDEO_MAX_SIZE = 500 * 1024 * 1024  # 500MB
    VIDEO_MIN_DURATION = 0.5  # 秒
```

---

## 测试

运行测试套件验证功能：

```bash
cd ~/.openclaw/skills/multimedia/scripts
python3 test_validator.py
```

测试覆盖：
- ✅ 图片验证（正常/低分辨率/文件过小/自定义分辨率）
- ✅ JSON 验证（正常/缺少字段/URL 格式）
- ✅ 重试机制（成功/失败）
- ✅ 批量验证
