#!/usr/bin/env python3
"""
使用 Google Gemini API 分析图片
"""

import sys
import json
import urllib.request
import urllib.parse
import base64
import os

GEMINI_API_URL = "https://claude2.sssaicode.com/api/v1/chat/completions"
GEMINI_API_KEY = "YOUR_API_KEY_HERE"  # 从环境变量或配置文件读取

def encode_image_to_base64(image_path):
    """将图片编码为 base64"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def analyze_image(image_path, prompt, model="google/gemini-3-pro-preview"):
    """使用 Gemini 分析图片"""
    print(f"📸 分析图片: {image_path}")
    print(f"🤖 模型: {model}")
    
    # 编码图片
    image_base64 = encode_image_to_base64(image_path)
    
    # 构建请求
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2000
    }
    
    # 发送请求
    req = urllib.request.Request(
        GEMINI_API_URL,
        data=json.dumps(data).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GEMINI_API_KEY}'
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            return content
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def main():
    if len(sys.argv) < 3:
        print("用法: python3 gemini_image_analyzer.py <image_path> <prompt> [model]")
        print("\n示例:")
        print("  python3 gemini_image_analyzer.py ./P2.jpg '描述这张图片的内容'")
        sys.exit(1)
    
    image_path = sys.argv[1]
    prompt = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else "google/gemini-3-pro-preview"
    
    if not os.path.exists(image_path):
        print(f"❌ 图片不存在: {image_path}")
        sys.exit(1)
    
    result = analyze_image(image_path, prompt, model)
    
    if result:
        print(f"\n✅ 分析结果:\n{result}")
    else:
        print("❌ 分析失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
