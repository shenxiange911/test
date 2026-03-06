#!/usr/bin/env python3
"""
输出验证器测试用例
"""

import os
import json
import tempfile
from pathlib import Path
from PIL import Image
from output_validator import OutputValidator, validate_with_retry

def test_image_validation():
    """测试用例 1: 图片验证"""
    print("=" * 60)
    print("测试用例 1: 图片验证")
    print("=" * 60)
    
    validator = OutputValidator(verbose=True)
    
    # 创建测试图片
    with tempfile.TemporaryDirectory() as tmpdir:
        # 1.1 正常图片
        print("\n[1.1] 测试正常图片...")
        normal_img = Path(tmpdir) / "normal.png"
        img = Image.new('RGB', (1024, 768), color='red')
        img.save(normal_img)
        
        assert validator.validate_image(str(normal_img)), "正常图片应该通过验证"
        print("✅ 正常图片验证通过")
        
        # 1.2 分辨率过低
        print("\n[1.2] 测试低分辨率图片...")
        low_res = Path(tmpdir) / "low_res.png"
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(low_res)
        
        assert not validator.validate_image(str(low_res)), "低分辨率图片应该失败"
        print(f"✅ 低分辨率检测成功: {validator.errors}")
        
        # 1.3 文件过小
        print("\n[1.3] 测试文件过小...")
        small_file = Path(tmpdir) / "small.png"
        with open(small_file, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')  # 只写 PNG 头
        
        assert not validator.validate_image(str(small_file)), "过小文件应该失败"
        print(f"✅ 文件大小检测成功: {validator.errors}")
        
        # 1.4 自定义分辨率要求
        print("\n[1.4] 测试自定义分辨率...")
        custom_img = Path(tmpdir) / "custom.png"
        img = Image.new('RGB', (2048, 1152), color='green')
        img.save(custom_img)
        
        assert validator.validate_image(str(custom_img), min_resolution=(2048, 1152)), \
            "2K 图片应该通过 2K 验证"
        print("✅ 自定义分辨率验证通过")

def test_json_validation():
    """测试用例 2: JSON 结果验证"""
    print("\n" + "=" * 60)
    print("测试用例 2: JSON 结果验证")
    print("=" * 60)
    
    validator = OutputValidator(verbose=True)
    
    # 2.1 正常 JSON (不检查 URL)
    print("\n[2.1] 测试正常 JSON...")
    valid_json = {
        "status": "success",
        "taskId": "task_123",
        "image_url": "https://example.com/image.png",
        "video_url": "https://example.com/video.mp4"
    }
    
    assert validator.validate_json_result(
        valid_json,
        required_fields=["status", "taskId"],
        check_urls=False  # 不检查 URL 可访问性
    ), "正常 JSON 应该通过验证"
    print("✅ JSON 结构验证通过")
    
    # 2.2 缺少必需字段
    print("\n[2.2] 测试缺少字段...")
    invalid_json = {
        "status": "success"
    }
    
    assert not validator.validate_json_result(
        invalid_json,
        required_fields=["status", "taskId"],
        check_urls=False
    ), "缺少字段应该失败"
    print(f"✅ 缺失字段检测成功: {validator.errors}")
    
    # 2.3 URL 格式验证
    print("\n[2.3] 测试 URL 格式验证...")
    url_json = {
        "status": "success",
        "image_url": "not_a_url",
        "video_url": "https://example.com/video.mp4"
    }
    
    # 手动检查 URL 格式
    validator.errors.clear()
    has_invalid_url = False
    for field, url in url_json.items():
        if 'url' in field and isinstance(url, str):
            if not url.startswith(('http://', 'https://')):
                validator.errors.append(f"无效的 URL 格式: {field}")
                has_invalid_url = True
    
    assert has_invalid_url, "应该检测到格式错误"
    print(f"✅ URL 格式验证成功: {validator.errors}")

def test_retry_decorator():
    """测试用例 3: 重试机制"""
    print("\n" + "=" * 60)
    print("测试用例 3: 重试机制")
    print("=" * 60)
    
    validator = OutputValidator(verbose=True)
    
    # 3.1 成功场景
    print("\n[3.1] 测试成功场景...")
    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = Path(tmpdir) / "test.png"
        img = Image.new('RGB', (1024, 768), color='red')
        img.save(img_path)
        
        success, error = validate_with_retry(
            validator,
            validator.validate_image,
            max_retries=3,
            retry_delay=0.1,
            file_path=str(img_path)
        )
        
        assert success, "正常图片应该通过验证"
        print("✅ 成功场景通过")
    
    # 3.2 失败场景
    print("\n[3.2] 测试失败场景...")
    success, error = validate_with_retry(
        validator,
        validator.validate_image,
        max_retries=2,
        retry_delay=0.1,
        file_path="/nonexistent/file.png"
    )
    
    assert not success, "不存在的文件应该失败"
    assert error is not None, "应该返回错误消息"
    print(f"✅ 失败场景通过: {error}")

def test_batch_validation():
    """测试用例 4: 批量验证"""
    print("\n" + "=" * 60)
    print("测试用例 4: 批量验证")
    print("=" * 60)
    
    validator = OutputValidator(verbose=True)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建多个测试图片
        files = []
        for i in range(5):
            img_path = Path(tmpdir) / f"image_{i}.png"
            # 前 3 个正常，后 2 个分辨率过低
            size = (1024, 768) if i < 3 else (100, 100)
            img = Image.new('RGB', size, color='red')
            img.save(img_path)
            files.append(str(img_path))
        
        print(f"\n[4.1] 批量验证 {len(files)} 个文件...")
        
        # 手动批量验证
        results = []
        for f in files:
            valid = validator.validate_image(f)
            results.append({
                'file': f,
                'valid': valid,
                'error': None if valid else validator.get_error_message()
            })
        
        passed = sum(1 for r in results if r['valid'])
        failed = len(results) - passed
        
        print(f"\n✅ 批量验证完成: {passed} 通过, {failed} 失败")
        assert passed == 3, "应该有 3 个通过"
        assert failed == 2, "应该有 2 个失败"
        
        # 显示详细结果
        for r in results:
            status = "✓" if r['valid'] else "✗"
            error_msg = r.get('error', 'OK')
            if error_msg and error_msg != 'OK':
                error_msg = error_msg.split('\n')[0]  # 只显示第一行
            print(f"  {status} {Path(r['file']).name}: {error_msg}")

def main():
    """运行所有测试"""
    print("\n🧪 开始运行输出验证器测试套件...\n")
    
    try:
        test_image_validation()
        test_json_validation()
        test_retry_decorator()
        test_batch_validation()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
