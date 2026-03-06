#!/usr/bin/env python3
"""
统一错误处理和日志系统
用于 multimedia 流水线的所有脚本
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from logging.handlers import RotatingFileHandler


class MultimediaError(Exception):
    """multimedia 流水线基础异常类"""
    def __init__(self, message: str, data: Optional[Dict] = None, errors: Optional[List[str]] = None):
        self.message = message
        self.data = data or {}
        self.errors = errors or []
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """转换为标准错误格式"""
        return {
            "status": "error",
            "message": self.message,
            "data": self.data,
            "errors": self.errors,
            "timestamp": datetime.now().isoformat()
        }

    def to_json(self) -> str:
        """输出 JSON 格式"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class APIError(MultimediaError):
    """API 调用错误"""
    pass


class ValidationError(MultimediaError):
    """数据验证错误"""
    pass


class FileError(MultimediaError):
    """文件操作错误"""
    pass


class TimeoutError(MultimediaError):
    """超时错误"""
    pass


def setup_logger(
    name: str,
    log_dir: Optional[Path] = None,
    level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    配置日志系统
    
    Args:
        name: 日志名称（通常是脚本名）
        log_dir: 日志目录（默认 ~/.openclaw/skills/multimedia/logs）
        level: 日志级别（DEBUG/INFO/WARNING/ERROR）
        max_bytes: 单个日志文件最大大小
        backup_count: 保留的日志文件数量
    
    Returns:
        配置好的 logger 实例
    """
    # 默认日志目录
    if log_dir is None:
        log_dir = Path.home() / ".openclaw/skills/multimedia/logs"
    
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建 logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # 避免重复添加 handler
    if logger.handlers:
        return logger
    
    # 统一日志格式
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件 handler（带轮转）
    log_file = log_dir / f"{name}.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 控制台 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def success_response(
    message: str,
    data: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    生成标准成功响应
    
    Args:
        message: 成功消息
        data: 附加数据
    
    Returns:
        标准格式的成功响应
    """
    return {
        "status": "success",
        "message": message,
        "data": data or {},
        "timestamp": datetime.now().isoformat()
    }


def error_response(
    message: str,
    data: Optional[Dict] = None,
    errors: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    生成标准错误响应
    
    Args:
        message: 错误消息
        data: 附加数据
        errors: 错误详情列表
    
    Returns:
        标准格式的错误响应
    """
    return {
        "status": "error",
        "message": message,
        "data": data or {},
        "errors": errors or [],
        "timestamp": datetime.now().isoformat()
    }


def log_and_exit(logger: logging.Logger, error: Exception, exit_code: int = 1):
    """
    记录错误并退出
    
    Args:
        logger: logger 实例
        error: 异常对象
        exit_code: 退出码
    """
    if isinstance(error, MultimediaError):
        logger.error(error.to_json())
        print(error.to_json(), file=sys.stderr)
    else:
        error_dict = error_response(
            message=str(error),
            errors=[type(error).__name__]
        )
        logger.error(json.dumps(error_dict, ensure_ascii=False))
        print(json.dumps(error_dict, ensure_ascii=False, indent=2), file=sys.stderr)
    
    sys.exit(exit_code)


def handle_exception(logger: logging.Logger, func):
    """
    装饰器：统一异常处理
    
    用法：
        @handle_exception(logger)
        def my_function():
            ...
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MultimediaError as e:
            log_and_exit(logger, e)
        except Exception as e:
            log_and_exit(logger, e)
    
    return wrapper


# 示例用法
if __name__ == "__main__":
    # 1. 设置日志
    logger = setup_logger("error_handler_test", level="DEBUG")
    
    # 2. 记录不同级别的日志
    logger.debug("这是调试信息")
    logger.info("这是普通信息")
    logger.warning("这是警告信息")
    logger.error("这是错误信息")
    
    # 3. 成功响应示例
    success = success_response(
        message="图片生成成功",
        data={"taskId": "abc123", "url": "https://example.com/image.png"}
    )
    print("\n成功响应示例：")
    print(json.dumps(success, ensure_ascii=False, indent=2))
    
    # 4. 错误响应示例
    error = error_response(
        message="图片生成失败",
        data={"taskId": "abc123"},
        errors=["API 超时", "重试 3 次失败"]
    )
    print("\n错误响应示例：")
    print(json.dumps(error, ensure_ascii=False, indent=2))
    
    # 5. 自定义异常示例
    try:
        raise APIError(
            message="kie.ai API 调用失败",
            data={"endpoint": "/generate", "status_code": 500},
            errors=["连接超时", "服务器内部错误"]
        )
    except MultimediaError as e:
        print("\n自定义异常示例：")
        print(e.to_json())
