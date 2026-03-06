#!/usr/bin/env python3
"""
使用 Google Gemini Vision API 分析图片
基于 sssaicode 配置
"""

import sys
import json
import urllib.request
import base64
import os

# 从配置中提取的关键信息
API_BASE_URL = "https://claude2.sssaicode.com/api"
API_KEY = "YOUR_API_KEY_HERE"  # 从环境变量或配置文件读取
MODEL = "google/gemini-3-pro-preview"

def encode_image(image_path):
    """将图片编码为 base64"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def analyze_image(image_path, prompt):
    """分析图片"""
    print(f"📸 分析: {os.path.basename(image_path)}")
    
    # 编码图片
    image_b64 = encode_image(image_path)
    
    # 构建请求（OpenAI vision 格式）
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2000
    }
    
    # 发送请求
    url = f"{API_BASE_URL}/v1/chat/completions"
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
        print(f"❌ HTTP Error {e.code}: {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("用法: python3 gemini_vision.py <image_path> [prompt]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "详细描述这张图片的内容"
    
    if not os.path.exists(image_path):
        print(f"❌ 文件不存在: {image_path}")
        sys.exit(1)
    
    result = analyze_image(image_path, prompt)
    
    if result:
        print(f"\n✅ 分析结果:\n{result}")
        return result
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
