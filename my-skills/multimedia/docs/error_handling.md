# 错误处理和日志系统使用文档

## 概述

为 multimedia 流水线提供统一的错误处理和日志系统，确保所有脚本输出标准化的 JSON 格式响应。

## 核心组件

### 1. error_handler.py

统一错误处理模块，提供：
- 自定义异常类（APIError, ValidationError, FileError, TimeoutError）
- 日志配置函数
- 标准响应格式生成器
- 异常处理装饰器

### 2. logging_config.json

日志配置文件，定义：
- 日志格式（标准/详细）
- 日志级别（DEBUG/INFO/WARNING/ERROR）
- 日志输出（控制台/文件）
- 日志轮转（10MB，保留 5 个备份）

### 3. integration_examples.py

集成示例，演示 5 种使用场景。

---

## 快速开始

### 最简单的集成（3 行代码）

```python
from error_handler import setup_logger, success_response, error_response

# 1. 设置日志
logger = setup_logger("my_script")

# 2. 记录日志
logger.info("开始执行")

# 3. 返回标准响应
print(success_response("操作成功", data={"result": "ok"}))
```

---

## 标准响应格式

### 成功响应

```json
{
  "status": "success",
  "message": "图片生成成功",
  "data": {
    "taskId": "abc123",
    "url": "https://example.com/image.png"
  },
  "timestamp": "2026-03-04T22:10:00"
}
```

### 错误响应

```json
{
  "status": "error",
  "message": "图片生成失败",
  "data": {
    "taskId": "abc123"
  },
  "errors": [
    "API 超时",
    "重试 3 次失败"
  ],
  "timestamp": "2026-03-04T22:10:00"
}
```

---

## 使用方法

### 方法 1：基础集成（最小改动）

适合快速改造现有脚本。

```python
from error_handler import setup_logger, success_response, error_response

logger = setup_logger("storyboard_generator")

try:
    logger.info("开始生成分镜图")
    result = generate_storyboard(prompt)
    
    response = success_response(
        message="分镜图生成成功",
        data={"output": result}
    )
    logger.info(f"成功: {result}")
    print(response)
    
except Exception as e:
    response = error_response(
        message="分镜图生成失败",
        errors=[str(e)]
    )
    logger.error(f"失败: {e}")
    print(response)
    sys.exit(1)
```

### 方法 2：使用自定义异常（推荐）

提供更精确的错误分类。

```python
from error_handler import (
    setup_logger,
    APIError,
    ValidationError,
    TimeoutError
)

logger = setup_logger("api_caller")

try:
    # 验证输入
    if not prompt:
        raise ValidationError(
            message="prompt 不能为空",
            errors=["输入验证失败"]
        )
    
    # 调用 API
    response = call_kie_api(prompt)
    if response.status_code != 200:
        raise APIError(
            message="API 调用失败",
            data={"status_code": response.status_code},
            errors=[response.text]
        )
    
    # 超时检测
    if elapsed_time > 300:
        raise TimeoutError(
            message="任务超时",
            data={"elapsed": elapsed_time},
            errors=["超过 5 分钟未完成"]
        )
    
except (APIError, ValidationError, TimeoutError) as e:
    logger.error(e.to_json())
    print(e.to_json())
    sys.exit(1)
```

### 方法 3：使用装饰器（最优雅）

自动处理所有异常。

```python
from error_handler import setup_logger, handle_exception, ValidationError

logger = setup_logger("my_script")

@handle_exception(logger)
def main():
    logger.info("开始处理")
    
    if not validate_input():
        raise ValidationError(
            message="输入无效",
            errors=["缺少必需参数"]
        )
    
    result = process_data()
    
    print(success_response("处理完成", data={"result": result}))

if __name__ == "__main__":
    main()
```

---

## 日志级别使用指南

### DEBUG
详细的调试信息，仅在开发时使用。

```python
logger.debug(f"API 请求参数: {params}")
logger.debug(f"中间结果: {intermediate_data}")
```

### INFO
正常的业务流程信息。

```python
logger.info("开始生成分镜图")
logger.info(f"任务已提交: {task_id}")
logger.info(f"分镜图已保存: {output_path}")
```

### WARNING
潜在问题，但不影响执行。

```python
logger.warning("API 响应较慢，已等待 30 秒")
logger.warning("输出文件已存在，将覆盖")
```

### ERROR
错误信息，导致任务失败。

```python
logger.error(f"API 调用失败: {e}")
logger.error(f"文件保存失败: {path}")
```

---

## 改造现有脚本示例

### 改造前（storyboard_generator.py）

```python
print("生成分镜图...")
result = generate_storyboard(prompt)
print(f"成功: {result}")
```

### 改造后

```python
from error_handler import setup_logger, success_response, APIError

logger = setup_logger("storyboard_generator")

try:
    logger.info("开始生成分镜图")
    logger.debug(f"Prompt: {prompt[:50]}...")
    
    task_id = call_kie_api(prompt)
    logger.info(f"任务已提交: {task_id}")
    
    result = poll_task(task_id)
    output_path = download_image(result["url"])
    
    response = success_response(
        message="分镜图生成成功",
        data={
            "taskId": task_id,
            "output": str(output_path),
            "url": result["url"]
        }
    )
    logger.info(f"分镜图已保存: {output_path}")
    print(response)
    
except APIError as e:
    logger.error(e.to_json())
    print(e.to_json())
    sys.exit(1)
```

---

## 日志文件位置

所有日志保存在：`~/.openclaw/skills/multimedia/logs/`

- `multimedia.log` - 所有日志（DEBUG 及以上）
- `errors.log` - 仅错误日志（ERROR 及以上）
- `<script_name>.log` - 单个脚本的日志

日志文件自动轮转：
- 单个文件最大 10MB
- 保留最近 5 个备份
- 自动压缩旧日志

---

## 自定义异常类型

### APIError
API 调用失败。

```python
raise APIError(
    message="kie.ai API 调用失败",
    data={"endpoint": "/generate", "status_code": 500},
    errors=["连接超时", "服务器内部错误"]
)
```

### ValidationError
数据验证失败。

```python
raise ValidationError(
    message="输入参数无效",
    data={"param": "prompt"},
    errors=["prompt 不能为空"]
)
```

### FileError
文件操作失败。

```python
raise FileError(
    message="文件保存失败",
    data={"path": "/tmp/output.png"},
    errors=["磁盘空间不足"]
)
```

### TimeoutError
任务超时。

```python
raise TimeoutError(
    message="任务超时",
    data={"taskId": "abc123", "elapsed": 300},
    errors=["超过 5 分钟未完成"]
)
```

---

## 多步骤任务日志示例

```python
logger = setup_logger("pipeline", level="DEBUG")

steps = [
    "验证输入参数",
    "调用搜索 API",
    "分析搜索结果",
    "生成剧本",
    "生成分镜图",
    "保存输出"
]

for i, step in enumerate(steps, 1):
    logger.info(f"[{i}/{len(steps)}] {step}")
    
    try:
        execute_step(step)
        logger.debug(f"✓ {step} 完成")
    except Exception as e:
        logger.error(f"✗ {step} 失败: {e}")
        raise APIError(
            message=f"流水线在步骤 {i} 失败",
            data={"step": step, "step_number": i},
            errors=[str(e)]
        )

logger.info("所有步骤完成")
```

---

## 测试

运行测试脚本：

```bash
# 测试错误处理模块
python3 ~/.openclaw/skills/multimedia/scripts/error_handler.py

# 查看集成示例
python3 ~/.openclaw/skills/multimedia/scripts/integration_examples.py
```

---

## 最佳实践

1. **所有脚本都应该使用 setup_logger()**
   - 统一日志格式
   - 自动文件轮转
   - 同时输出到控制台和文件

2. **使用自定义异常类型**
   - APIError：API 调用失败
   - ValidationError：输入验证失败
   - FileError：文件操作失败
   - TimeoutError：任务超时

3. **返回标准 JSON 格式**
   - 成功：success_response()
   - 失败：error_response() 或 exception.to_json()

4. **记录关键步骤**
   - INFO：业务流程（开始/完成/保存）
   - DEBUG：详细参数（仅开发时）
   - ERROR：错误信息（必须记录）

5. **优雅退出**
   - 捕获异常
   - 记录日志
   - 返回标准错误响应
   - sys.exit(1)

---

## 下一步

1. 逐个改造现有脚本（scripts/*.py）
2. 统一所有输出格式
3. 添加重试机制（结合错误处理）
4. 创建错误监控仪表板
