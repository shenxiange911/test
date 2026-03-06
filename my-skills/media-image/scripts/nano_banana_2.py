#!/usr/bin/env python3
"""
Nano Banana 2 API 工具
完全按照 kie.ai 官方文档实现

用法:
  python3 nano_banana_2.py --prompt "your prompt" --aspect_ratio "16:9" --resolution "4K"
  python3 nano_banana_2.py --prompt "your prompt" --image_input "https://example.com/image.jpg"
"""

import sys
import json
import os
import argparse
import time
import urllib.request

# API 配置
API_BASE = "https://api.kie.ai/api/v1"
API_KEY = os.getenv("KIE_API_KEY", "YOUR_KIE_API_KEY_HERE")

def create_task(
    prompt: str,
    aspect_ratio: str = "auto",
    resolution: str = "2K",
    output_format: str = "jpg",
    google_search: bool = False,
    image_input: list = None,
    callback_url: str = None
) -> dict:
    """
    创建 Nano Banana 2 任务
    
    参数完全按照官方文档:
    https://docs.kie.ai/market/google/nano-banana-2
    """
    url = f"{API_BASE}/jobs/createTask"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": "nano-banana-2",
        "input": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "output_format": output_format,
            "google_search": google_search,
            "image_input": image_input or []
        }
    }
    
    if callback_url:
        data["callBackUrl"] = callback_url
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {"error": f"HTTP {e.code}", "detail": error_body}
    except Exception as e:
        return {"error": str(e)}

def query_task(task_id: str) -> dict:
    """查询任务状态 (使用 recordInfo)"""
    url = f"{API_BASE}/jobs/recordInfo?taskId={task_id}"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {"error": f"HTTP {e.code}", "detail": error_body}
    except Exception as e:
        return {"error": str(e)}

def wait_for_completion(task_id: str, max_wait: int = 300, interval: int = 12) -> dict:
    """等待任务完成"""
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        result = query_task(task_id)
        
        if "error" in result:
            return result
        
        status = result.get("data", {}).get("status")
        
        if status == "completed":
            return result
        elif status == "failed":
            return {"error": "Task failed", "detail": result}
        
        print(f"⏳ 状态: {status}")
        time.sleep(interval)
    
    return {"error": "Timeout", "detail": f"Task not completed after {max_wait}s"}

def save_result(result: dict, output_file: str):
    """保存结果到 JSON"""
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"💾 结果已保存: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Nano Banana 2 API 工具")
    parser.add_argument("--prompt", required=True, help="生成提示词")
    parser.add_argument("--aspect_ratio", default="auto", help="宽高比 (auto/1:1/16:9/9:16/4:3/3:4/21:9/9:21/2:3/3:2)")
    parser.add_argument("--resolution", default="2K", help="分辨率 (2K/4K)")
    parser.add_argument("--output_format", default="jpg", help="输出格式 (jpg/png)")
    parser.add_argument("--google_search", action="store_true", help="启用 Google 搜索")
    parser.add_argument("--image_input", nargs="+", help="参考图片 URL (可多个)")
    parser.add_argument("--callback_url", help="回调 URL")
    parser.add_argument("--output", default="nano_banana_2_result.json", help="结果保存路径")
    parser.add_argument("--wait", action="store_true", help="等待任务完成")
    
    args = parser.parse_args()
    
    # 创建任务
    print("🎨 创建 Nano Banana 2 任务...")
    result = create_task(
        prompt=args.prompt,
        aspect_ratio=args.aspect_ratio,
        resolution=args.resolution,
        output_format=args.output_format,
        google_search=args.google_search,
        image_input=args.image_input,
        callback_url=args.callback_url
    )
    
    if "error" in result:
        print(f"❌ 创建失败: {result['error']}", file=sys.stderr)
        if "detail" in result:
            print(f"详情: {result['detail']}", file=sys.stderr)
        sys.exit(1)
    
    task_id = result.get("data", {}).get("taskId")
    print(f"✅ 任务已创建: {task_id}")
    
    # 等待完成
    if args.wait:
        print("\n⏳ 等待生成完成...")
        result = wait_for_completion(task_id)
        
        if "error" in result:
            print(f"❌ 生成失败: {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        output_urls = result.get("data", {}).get("output", [])
        print(f"\n✅ 生成完成！")
        print(f"📸 结果 URL:")
        for url in output_urls:
            print(f"  - {url}")
        
        # 保存结果
        save_result(result, args.output)
    else:
        print(f"\n💡 使用以下命令查询任务状态:")
        print(f"  python3 nano_banana_2.py --query {task_id}")

if __name__ == "__main__":
    main()
