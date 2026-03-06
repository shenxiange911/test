#!/usr/bin/env python3
"""
集成示例：如何在现有脚本中使用 error_handler
演示如何改造现有的 multimedia 脚本
"""

import sys
from pathlib import Path

# 导入错误处理模块
from error_handler import (
    setup_logger,
    success_response,
    error_response,
    APIError,
    ValidationError,
    FileError,
    TimeoutError,
    handle_exception
)


# ============================================
# 示例 1：基础集成（最小改动）
# ============================================

def example_basic_integration():
    """最简单的集成方式"""
    # 1. 设置日志
    logger = setup_logger("my_script")
    
    # 2. 记录日志
    logger.info("脚本开始执行")
    
    try:
        # 你的业务逻辑
        result = do_something()
        
        # 3. 返回成功响应
        response = success_response(
            message="操作成功",
            data={"result": result}
        )
        logger.info(f"操作成功: {result}")
        print(response)
        
    except Exception as e:
        # 4. 返回错误响应
        response = error_response(
            message="操作失败",
            errors=[str(e)]
        )
        logger.error(f"操作失败: {e}")
        print(response)
        sys.exit(1)


# ============================================
# 示例 2：使用自定义异常
# ============================================

def example_custom_exceptions():
    """使用自定义异常类型"""
    logger = setup_logger("api_caller")
    
    try:
        # API 调用
        response = call_api()
        
        if response.status_code != 200:
            raise APIError(
                message="API 调用失败",
                data={"status_code": response.status_code},
                errors=[response.text]
            )
        
        # 数据验证
        data = response.json()
        if "taskId" not in data:
            raise ValidationError(
                message="响应数据缺少 taskId",
                data=data,
                errors=["必需字段缺失"]
            )
        
        logger.info(f"API 调用成功: {data['taskId']}")
        
    except APIError as e:
        logger.error(e.to_json())
        sys.exit(1)
    except ValidationError as e:
        logger.error(e.to_json())
        sys.exit(1)


# ============================================
# 示例 3：使用装饰器（推荐）
# ============================================

logger = setup_logger("decorated_script")

@handle_exception(logger)
def main():
    """使用装饰器自动处理异常"""
    logger.info("开始处理")
    
    # 验证输入
    if not validate_input():
        raise ValidationError(
            message="输入参数无效",
            errors=["缺少必需参数"]
        )
    
    # 调用 API
    task_id = call_api_with_retry()
    
    # 轮询结果
    result = poll_result(task_id)
    
    # 保存文件
    output_path = save_result(result)
    
    # 返回成功
    response = success_response(
        message="处理完成",
        data={"output": str(output_path)}
    )
    print(response)


# ============================================
# 示例 4：改造现有脚本（storyboard_generator.py）
# ============================================

def example_refactor_existing_script():
    """
    改造示例：storyboard_generator.py
    
    原代码：
        print("生成分镜图...")
        result = generate_storyboard(prompt)
        print(f"成功: {result}")
    
    改造后：
    """
    logger = setup_logger("storyboard_generator")
    
    try:
        logger.info("开始生成分镜图")
        
        # 验证输入
        if not prompt:
            raise ValidationError(
                message="prompt 不能为空",
                errors=["输入验证失败"]
            )
        
        # 调用 API
        logger.debug(f"调用 kie.ai API: {prompt[:50]}...")
        task_id = call_kie_api(prompt)
        
        # 轮询结果
        logger.info(f"任务已提交: {task_id}")
        result = poll_task(task_id, max_retries=30)
        
        # 下载图片
        logger.info("下载生成的图片")
        output_path = download_image(result["url"])
        
        # 返回成功
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
        logger.error(f"API 错误: {e.message}")
        print(e.to_json())
        sys.exit(1)
    except TimeoutError as e:
        logger.error(f"超时: {e.message}")
        print(e.to_json())
        sys.exit(1)
    except Exception as e:
        logger.error(f"未知错误: {e}")
        response = error_response(
            message="分镜图生成失败",
            errors=[str(e)]
        )
        print(response)
        sys.exit(1)


# ============================================
# 示例 5：多步骤任务的日志记录
# ============================================

def example_multi_step_logging():
    """多步骤任务的详细日志"""
    logger = setup_logger("multi_step", level="DEBUG")
    
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
            # 执行步骤
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


# ============================================
# 辅助函数（模拟）
# ============================================

def do_something():
    return "result"

def call_api():
    class Response:
        status_code = 200
        text = "OK"
        def json(self):
            return {"taskId": "abc123"}
    return Response()

def validate_input():
    return True

def call_api_with_retry():
    return "task_123"

def poll_result(task_id):
    return {"url": "https://example.com/result.png"}

def save_result(result):
    return Path("/tmp/result.png")

def call_kie_api(prompt):
    return "task_456"

def poll_task(task_id, max_retries):
    return {"url": "https://example.com/storyboard.png"}

def download_image(url):
    return Path("/tmp/storyboard.png")

def execute_step(step):
    pass


if __name__ == "__main__":
    print("=== 示例 1: 基础集成 ===")
    example_basic_integration()
    
    print("\n=== 示例 3: 装饰器用法 ===")
    main()
    
    print("\n=== 示例 5: 多步骤日志 ===")
    example_multi_step_logging()
