#!/usr/bin/env python3
"""
kie.ai API 调用工具
用法: python3 kie_api.py <action> [options]
"""

import sys
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, Optional

API_BASE = "https://api.kie.ai/api/v1"
API_KEY = None  # 从环境变量或参数读取

def load_api_key():
    """从环境变量或配置文件加载 API Key"""
    import os
    global API_KEY
    API_KEY = os.getenv("KIE_API_KEY")
    if not API_KEY:
        # 尝试从 openclaw.json 读取
        try:
            with open(os.path.expanduser("~/.openclaw/openclaw.json")) as f:
                config = json.load(f)
                API_KEY = config.get("plugins", {}).get("kie", {}).get("apiKey")
        except:
            pass
    return API_KEY

def create_task(model: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """创建任务"""
    url = f"{API_BASE}/jobs/createTask"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "input": params
    }
    
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

def query_task(task_id: str) -> Dict[str, Any]:
    """查询任务状态 (使用 recordInfo)"""
    url = f"{API_BASE}/jobs/recordInfo?taskId={task_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
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

def wait_for_completion(task_id: str, max_wait: int = 300, interval: int = 12) -> Dict[str, Any]:
    """等待任务完成 (间隔 12 秒，避免限流)"""
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
        
        # 间隔 12 秒，避免限流
        time.sleep(interval)
    
    return {"error": "Timeout", "detail": f"Task not completed after {max_wait}s"}

def download_image(url: str, output_path: str) -> bool:
    """下载图片"""
    try:
        urllib.request.urlretrieve(url, output_path)
        return True
    except Exception as e:
        print(f"下载失败: {e}", file=sys.stderr)
        return False

def main():
    if len(sys.argv) < 2:
        print("用法: python3 kie_api.py <action> [options]")
        print("Actions:")
        print("  create <model> <params_json>  - 创建任务")
        print("  query <task_id>                - 查询任务")
        print("  wait <task_id>                 - 等待任务完成")
        print("  download <url> <output_path>   - 下载图片")
        sys.exit(1)
    
    load_api_key()
    if not API_KEY:
        print("错误: 未找到 KIE_API_KEY", file=sys.stderr)
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "create":
        if len(sys.argv) < 4:
            print("用法: create <model> <params_json>", file=sys.stderr)
            sys.exit(1)
        model = sys.argv[2]
        params = json.loads(sys.argv[3])
        result = create_task(model, params)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif action == "query":
        if len(sys.argv) < 3:
            print("用法: query <task_id>", file=sys.stderr)
            sys.exit(1)
        task_id = sys.argv[2]
        result = query_task(task_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif action == "wait":
        if len(sys.argv) < 3:
            print("用法: wait <task_id>", file=sys.stderr)
            sys.exit(1)
        task_id = sys.argv[2]
        result = wait_for_completion(task_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif action == "download":
        if len(sys.argv) < 4:
            print("用法: download <url> <output_path>", file=sys.stderr)
            sys.exit(1)
        url = sys.argv[2]
        output_path = sys.argv[3]
        success = download_image(url, output_path)
        sys.exit(0 if success else 1)
    
    else:
        print(f"未知操作: {action}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
