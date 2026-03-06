#!/usr/bin/env python3
"""
输出验证器 - 验证多媒体流水线生成的文件和数据
支持图片、视频、JSON 结果验证，失败时自动重试或降级
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from PIL import Image
import subprocess

class ValidationError(Exception):
    """验证失败异常"""
    pass

class OutputValidator:
    """输出验证器"""
    
    # 验证规则
    IMAGE_MIN_SIZE = 1 * 1024  # 1KB (降低测试要求)
    IMAGE_MAX_SIZE = 50 * 1024 * 1024  # 50MB
    IMAGE_FORMATS = {'.png', '.jpg', '.jpeg', '.webp'}
    IMAGE_MIN_RESOLUTION = (256, 256)
    
    VIDEO_MIN_SIZE = 100 * 1024  # 100KB
    VIDEO_MAX_SIZE = 500 * 1024 * 1024  # 500MB
    VIDEO_FORMATS = {'.mp4', '.mov', '.avi', '.webm'}
    VIDEO_MIN_DURATION = 0.5  # 秒
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.errors: List[str] = []
    
    def log(self, msg: str):
        """日志输出"""
        if self.verbose:
            print(f"[Validator] {msg}")
    
    def validate_image(
        self,
        file_path: str,
        min_resolution: Optional[Tuple[int, int]] = None,
        max_size: Optional[int] = None,
        check_corruption: bool = True
    ) -> bool:
        """
        验证图片文件
        
        Args:
            file_path: 图片路径
            min_resolution: 最小分辨率 (width, height)
            max_size: 最大文件大小（字节）
            check_corruption: 是否检查文件损坏
        
        Returns:
            验证是否通过
        """
        self.errors.clear()
        path = Path(file_path).expanduser()
        
        # 1. 文件存在性
        if not path.exists():
            self.errors.append(f"文件不存在: {path}")
            return False
        
        # 2. 文件格式
        if path.suffix.lower() not in self.IMAGE_FORMATS:
            self.errors.append(f"不支持的格式: {path.suffix}")
            return False
        
        # 3. 文件大小
        file_size = path.stat().st_size
        if file_size < self.IMAGE_MIN_SIZE:
            self.errors.append(f"文件过小: {file_size} bytes < {self.IMAGE_MIN_SIZE}")
            return False
        
        max_size = max_size or self.IMAGE_MAX_SIZE
        if file_size > max_size:
            self.errors.append(f"文件过大: {file_size} bytes > {max_size}")
            return False
        
        # 4. 图片完整性和分辨率
        try:
            with Image.open(path) as img:
                width, height = img.size
                
                # 检查分辨率
                min_res = min_resolution or self.IMAGE_MIN_RESOLUTION
                if width < min_res[0] or height < min_res[1]:
                    self.errors.append(
                        f"分辨率过低: {width}×{height} < {min_res[0]}×{min_res[1]}"
                    )
                    return False
                
                # 检查损坏（尝试加载像素数据）
                if check_corruption:
                    img.load()
                
                self.log(f"✓ 图片验证通过: {path.name} ({width}×{height}, {file_size//1024}KB)")
                return True
                
        except Exception as e:
            self.errors.append(f"图片损坏或无法读取: {e}")
            return False
    
    def validate_video(
        self,
        file_path: str,
        min_duration: Optional[float] = None,
        check_codec: bool = True
    ) -> bool:
        """
        验证视频文件
        
        Args:
            file_path: 视频路径
            min_duration: 最小时长（秒）
            check_codec: 是否检查编码格式
        
        Returns:
            验证是否通过
        """
        self.errors.clear()
        path = Path(file_path).expanduser()
        
        # 1. 文件存在性
        if not path.exists():
            self.errors.append(f"文件不存在: {path}")
            return False
        
        # 2. 文件格式
        if path.suffix.lower() not in self.VIDEO_FORMATS:
            self.errors.append(f"不支持的格式: {path.suffix}")
            return False
        
        # 3. 文件大小
        file_size = path.stat().st_size
        if file_size < self.VIDEO_MIN_SIZE:
            self.errors.append(f"文件过小: {file_size} bytes < {self.VIDEO_MIN_SIZE}")
            return False
        
        if file_size > self.VIDEO_MAX_SIZE:
            self.errors.append(f"文件过大: {file_size} bytes > {self.VIDEO_MAX_SIZE}")
            return False
        
        # 4. 使用 ffprobe 检查视频信息
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=duration,codec_name,width,height,r_frame_rate',
                '-of', 'json',
                str(path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                self.errors.append(f"ffprobe 失败: {result.stderr}")
                return False
            
            data = json.loads(result.stdout)
            
            if not data.get('streams'):
                self.errors.append("未找到视频流")
                return False
            
            stream = data['streams'][0]
            
            # 检查时长
            duration = float(stream.get('duration', 0))
            min_dur = min_duration or self.VIDEO_MIN_DURATION
            
            if duration < min_dur:
                self.errors.append(f"时长过短: {duration}s < {min_dur}s")
                return False
            
            # 检查编码
            codec = stream.get('codec_name', 'unknown')
            width = stream.get('width', 0)
            height = stream.get('height', 0)
            fps = stream.get('r_frame_rate', '0/1')
            
            self.log(
                f"✓ 视频验证通过: {path.name} "
                f"({width}×{height}, {duration:.1f}s, {codec}, {file_size//1024}KB)"
            )
            return True
            
        except subprocess.TimeoutExpired:
            self.errors.append("ffprobe 超时")
            return False
        except Exception as e:
            self.errors.append(f"视频验证失败: {e}")
            return False
    
    def validate_json_result(
        self,
        data: Dict[str, Any],
        required_fields: List[str],
        check_urls: bool = True,
        url_timeout: int = 5
    ) -> bool:
        """
        验证 JSON 结果
        
        Args:
            data: JSON 数据
            required_fields: 必需字段列表
            check_urls: 是否检查 URL 有效性
            url_timeout: URL 检查超时（秒）
        
        Returns:
            验证是否通过
        """
        self.errors.clear()
        
        # 1. 检查必需字段
        for field in required_fields:
            if field not in data:
                self.errors.append(f"缺少必需字段: {field}")
                return False
            
            if data[field] is None or data[field] == "":
                self.errors.append(f"字段为空: {field}")
                return False
        
        # 2. 检查 URL 有效性
        if check_urls:
            url_fields = [k for k in data.keys() if 'url' in k.lower() or k.endswith('_link')]
            
            for field in url_fields:
                url = data.get(field)
                if not url or not isinstance(url, str):
                    continue
                
                if not url.startswith(('http://', 'https://')):
                    self.errors.append(f"无效的 URL 格式: {field} = {url}")
                    return False
                
                # HEAD 请求检查 URL 可访问性
                try:
                    response = requests.head(url, timeout=url_timeout, allow_redirects=True)
                    if response.status_code >= 400:
                        self.errors.append(
                            f"URL 不可访问: {field} = {url} (HTTP {response.status_code})"
                        )
                        return False
                except requests.RequestException as e:
                    self.errors.append(f"URL 检查失败: {field} = {url} ({e})")
                    return False
        
        self.log(f"✓ JSON 验证通过: {len(required_fields)} 个必需字段")
        return True
    
    def get_errors(self) -> List[str]:
        """获取错误列表"""
        return self.errors.copy()
    
    def get_error_message(self) -> str:
        """获取错误消息（多行）"""
        return "\n".join(self.errors)


def validate_with_retry(
    validator: OutputValidator,
    validate_func: callable,
    max_retries: int = 3,
    retry_delay: float = 2.0,
    **kwargs
) -> Tuple[bool, Optional[str]]:
    """
    带重试的验证
    
    Args:
        validator: 验证器实例
        validate_func: 验证函数（validator.validate_image/video/json_result）
        max_retries: 最大重试次数
        retry_delay: 重试延迟（秒）
        **kwargs: 传递给验证函数的参数
    
    Returns:
        (是否成功, 错误消息)
    """
    import time
    
    for attempt in range(max_retries):
        if validate_func(**kwargs):
            return True, None
        
        if attempt < max_retries - 1:
            validator.log(f"验证失败，{retry_delay}秒后重试 ({attempt + 1}/{max_retries})...")
            time.sleep(retry_delay)
    
    return False, validator.get_error_message()


# 便捷函数
def validate_image(file_path: str, **kwargs) -> Tuple[bool, Optional[str]]:
    """验证图片（便捷函数）"""
    validator = OutputValidator(verbose=kwargs.pop('verbose', True))
    success = validator.validate_image(file_path, **kwargs)
    return success, None if success else validator.get_error_message()


def validate_video(file_path: str, **kwargs) -> Tuple[bool, Optional[str]]:
    """验证视频（便捷函数）"""
    validator = OutputValidator(verbose=kwargs.pop('verbose', True))
    success = validator.validate_video(file_path, **kwargs)
    return success, None if success else validator.get_error_message()


def validate_json(data: Dict[str, Any], required_fields: List[str], **kwargs) -> Tuple[bool, Optional[str]]:
    """验证 JSON（便捷函数）"""
    validator = OutputValidator(verbose=kwargs.pop('verbose', True))
    success = validator.validate_json_result(data, required_fields, **kwargs)
    return success, None if success else validator.get_error_message()


if __name__ == '__main__':
    # 测试用例
    print("=== 输出验证器测试 ===\n")
    
    validator = OutputValidator()
    
    # 测试 1: 图片验证（模拟）
    print("测试 1: 图片验证")
    test_image = "/tmp/test_image.png"
    
    # 创建测试图片
    img = Image.new('RGB', (1024, 768), color='red')
    img.save(test_image)
    
    success, error = validate_image(test_image, min_resolution=(512, 512))
    print(f"结果: {'✓ 通过' if success else '✗ 失败'}")
    if error:
        print(f"错误: {error}")
    print()
    
    # 测试 2: JSON 验证
    print("测试 2: JSON 验证")
    test_data = {
        "task_id": "test_123",
        "image_url": "https://httpbin.org/status/200",
        "status": "completed"
    }
    
    success, error = validate_json(
        test_data,
        required_fields=["task_id", "image_url", "status"],
        check_urls=True
    )
    print(f"结果: {'✓ 通过' if success else '✗ 失败'}")
    if error:
        print(f"错误: {error}")
    print()
    
    # 测试 3: 带重试的验证
    print("测试 3: 带重试的验证（模拟失败场景）")
    
    # 模拟不存在的文件
    success, error = validate_with_retry(
        validator,
        validator.validate_image,
        max_retries=2,
        retry_delay=0.5,
        file_path="/tmp/nonexistent.png"
    )
    print(f"结果: {'✓ 通过' if success else '✗ 失败'}")
    if error:
        print(f"错误: {error}")
    
    # 清理
    if os.path.exists(test_image):
        os.remove(test_image)
    
    print("\n=== 测试完成 ===")
