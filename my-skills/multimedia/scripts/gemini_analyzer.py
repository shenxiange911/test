#!/usr/bin/env python3
"""
使用 Gemini 分析图片和视频
"""

import sys
import json
import urllib.request
import base64
import os

# Gemini CLI API 配置
API_KEY = "YOUR_API_KEY_HERE"  # 从环境变量或配置文件读取
API_BASE_URL = "https://gemini2.sssaicode.com/api"
DEFAULT_MODEL = "google/gemini-3.0-pro-preview"

def encode_file_to_base64(file_path):
    """将文件编码为 base64"""
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def analyze_media(file_path, prompt, model=DEFAULT_MODEL):
    """分析图片或视频"""
    print(f"📸 分析: {os.path.basename(file_path)}")
    print(f"🤖 模型: {model}")
    
    # 判断文件类型
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        mime_type = f"image/{ext[1:]}"
    elif ext in ['.mp4', '.mov', '.avi', '.webm']:
        mime_type = f"video/{ext[1:]}"
    else:
        print(f"❌ 不支持的文件类型: {ext}")
        return None
    
    # 编码文件
    file_b64 = encode_file_to_base64(file_path)
    
    # 构建请求
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{file_b64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2000
    }
    
    # 发送请求
    url = f"{API_BASE_URL}/chat/completions"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ HTTP Error {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("用法: python3 gemini_analyzer.py <file_path> [prompt] [model]")
        print("\n示例:")
        print("  python3 gemini_analyzer.py ./image.jpg '详细描述这张图片'")
        print("  python3 gemini_analyzer.py ./video.mp4 '分析这个视频的内容' google/gemini-2.5-flash")
        sys.exit(1)
    
    file_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "详细描述这个文件的内容"
    model = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_MODEL
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)
    
    result = analyze_media(file_path, prompt, model)
    
    if result:
        print(f"\n✅ 分析结果:\n{result}")
        return 0
    else:
        print("❌ 分析失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
