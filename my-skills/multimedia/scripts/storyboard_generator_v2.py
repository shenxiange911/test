#!/usr/bin/env python3
"""
实际集成示例：改造 storyboard_generator.py
演示如何将错误处理系统集成到现有脚本
"""

import sys
import json
import time
import requests
from pathlib import Path

# 导入错误处理模块
from error_handler import (
    setup_logger,
    success_response,
    error_response,
    APIError,
    ValidationError,
    TimeoutError,
    handle_exception
)

# 配置
KIE_API_BASE = "https://api.kie.ai"
KIE_API_KEY = "your_api_key_here"

# 设置日志
logger = setup_logger("storyboard_generator_v2", level="INFO")


def validate_prompt(prompt: str) -> None:
    """验证 prompt 参数"""
    if not prompt:
        raise ValidationError(
            message="prompt 不能为空",
            errors=["输入验证失败"]
        )
    
    if len(prompt) < 10:
        raise ValidationError(
            message="prompt 太短",
            data={"length": len(prompt)},
            errors=["prompt 至少需要 10 个字符"]
        )
    
    logger.debug(f"Prompt 验证通过: {len(prompt)} 字符")


def call_kie_api(prompt: str, model: str = "nano-banana-pro") -> str:
    """调用 kie.ai API 生成图片"""
    logger.info(f"调用 kie.ai API: {model}")
    logger.debug(f"Prompt: {prompt[:100]}...")
    
    try:
        response = requests.post(
            f"{KIE_API_BASE}/generate",
            headers={"Authorization": f"Bearer {KIE_API_KEY}"},
            json={
                "model": model,
                "prompt": prompt,
                "width": 2048,
                "height": 1152
            },
            timeout=30
        )
        
        if response.status_code != 200:
            raise APIError(
                message="API 调用失败",
                data={
                    "status_code": response.status_code,
                    "endpoint": "/generate"
                },
                errors=[response.text]
            )
        
        data = response.json()
        task_id = data.get("taskId")
        
        if not task_id:
            raise ValidationError(
                message="API 响应缺少 taskId",
                data=data,
                errors=["响应格式错误"]
            )
        
        logger.info(f"任务已提交: {task_id}")
        return task_id
        
    except requests.exceptions.Timeout:
        raise TimeoutError(
            message="API 请求超时",
            data={"timeout": 30},
            errors=["连接超时"]
        )
    except requests.exceptions.RequestException as e:
        raise APIError(
            message="API 请求失败",
            errors=[str(e)]
        )


def poll_task(task_id: str, max_retries: int = 30, interval: int = 12) -> dict:
    """轮询任务状态"""
    logger.info(f"开始轮询任务: {task_id}")
    
    for attempt in range(1, max_retries + 1):
        logger.debug(f"轮询尝试 {attempt}/{max_retries}")
        
        try:
            response = requests.get(
                f"{KIE_API_BASE}/task/{task_id}",
                headers={"Authorization": f"Bearer {KIE_API_KEY}"},
                timeout=10
            )
            
            if response.status_code != 200:
                logger.warning(f"轮询失败: {response.status_code}")
                time.sleep(interval)
                continue
            
            data = response.json()
            status = data.get("status")
            
            if status == "completed":
                logger.info(f"任务完成: {task_id}")
                return data
            elif status == "failed":
                raise APIError(
                    message="任务失败",
                    data={"taskId": task_id},
                    errors=[data.get("error", "未知错误")]
                )
            else:
                logger.debug(f"任务状态: {status}")
                time.sleep(interval)
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"轮询请求失败: {e}")
            time.sleep(interval)
    
    # 超时
    raise TimeoutError(
        message="任务超时",
        data={
            "taskId": task_id,
            "max_retries": max_retries,
            "elapsed": max_retries * interval
        },
        errors=[f"超过 {max_retries * interval} 秒未完成"]
    )


def download_image(url: str, output_dir: Path) -> Path:
    """下载生成的图片"""
    logger.info(f"下载图片: {url}")
    
    try:
        response = requests.get(url, timeout=60)
        
        if response.status_code != 200:
            raise APIError(
                message="图片下载失败",
                data={"url": url, "status_code": response.status_code},
                errors=["下载请求失败"]
            )
        
        # 保存文件
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = int(time.time())
        output_path = output_dir / f"storyboard_{timestamp}.png"
        
        output_path.write_bytes(response.content)
        logger.info(f"图片已保存: {output_path}")
        
        return output_path
        
    except requests.exceptions.RequestException as e:
        raise APIError(
            message="图片下载失败",
            data={"url": url},
            errors=[str(e)]
        )


@handle_exception(logger)
def main():
    """主函数"""
    # 解析参数
    if len(sys.argv) < 2:
        raise ValidationError(
            message="缺少必需参数",
            errors=["用法: python3 storyboard_generator_v2.py <prompt>"]
        )
    
    prompt = sys.argv[1]
    output_dir = Path.home() / ".openclaw/skills/multimedia/output"
    
    logger.info("=" * 60)
    logger.info("开始生成分镜图")
    logger.info("=" * 60)
    
    # 步骤 1: 验证输入
    logger.info("[1/4] 验证输入参数")
    validate_prompt(prompt)
    
    # 步骤 2: 调用 API
    logger.info("[2/4] 调用 kie.ai API")
    task_id = call_kie_api(prompt)
    
    # 步骤 3: 轮询结果
    logger.info("[3/4] 轮询任务状态")
    result = poll_task(task_id)
    
    # 步骤 4: 下载图片
    logger.info("[4/4] 下载生成的图片")
    output_path = download_image(result["url"], output_dir)
    
    # 返回成功响应
    response = success_response(
        message="分镜图生成成功",
        data={
            "taskId": task_id,
            "output": str(output_path),
            "url": result["url"],
            "size": output_path.stat().st_size
        }
    )
    
    logger.info("=" * 60)
    logger.info("分镜图生成完成")
    logger.info("=" * 60)
    
    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
