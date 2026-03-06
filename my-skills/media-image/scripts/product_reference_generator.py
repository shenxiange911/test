#!/usr/bin/env python3
"""
产品多视角参考图生成器
基于多个正交视图重建 3D 模型，生成统一风格的参考图

用法:
  python3 product_reference_generator.py --front front.png --back back.png --left left.png --right right.png --top top.png --bottom bottom.png --output reference.png
"""

import sys
import json
import os
import argparse
import time
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# API 配置
API_BASE = "https://api.kie.ai/api/v1"
API_KEY = os.getenv("KIE_API_KEY", "YOUR_KIE_API_KEY_HERE")

def create_reference_grid(views: dict, output_path: str) -> str:
    """
    创建参考图网格 (2x3)
    
    Args:
        views: {"front": path, "back": path, "left": path, "right": path, "top": path, "bottom": path}
        output_path: 输出路径
    
    Returns:
        生成的网格图路径
    """
    # 网格布局
    layout = [
        ("front", "Front View"),
        ("back", "Back View"),
        ("left", "Left Side View"),
        ("right", "Right Side View"),
        ("top", "Top View"),
        ("bottom", "Bottom View"),
    ]
    
    cols = 2
    rows = 3
    cell_width = 1000
    cell_height = 1000
    padding = 20
    label_height = 60
    
    # 创建画布
    canvas_width = cols * cell_width + (cols + 1) * padding
    canvas_height = rows * (cell_height + label_height) + (rows + 1) * padding
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(canvas)
    
    # 字体
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    # 拼接图片
    for idx, (view_key, label) in enumerate(layout):
        if view_key not in views or not os.path.exists(views[view_key]):
            print(f"⚠️  缺少视图: {view_key}")
            continue
        
        row = idx // cols
        col = idx % cols
        
        # 加载图片
        img = Image.open(views[view_key])
        img.thumbnail((cell_width, cell_height), Image.Resampling.LANCZOS)
        
        # 计算位置
        x = padding + col * (cell_width + padding) + (cell_width - img.width) // 2
        y = padding + row * (cell_height + label_height + padding) + label_height
        
        # 粘贴图片
        canvas.paste(img, (x, y))
        
        # 绘制标签
        label_x = padding + col * (cell_width + padding)
        label_y = padding + row * (cell_height + label_height + padding)
        
        draw.rectangle(
            [label_x, label_y, label_x + cell_width, label_y + label_height],
            fill='#2c3e50'
        )
        
        bbox = draw.textbbox((0, 0), label, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = label_x + (cell_width - text_width) // 2
        text_y = label_y + (label_height - (bbox[3] - bbox[1])) // 2
        
        draw.text((text_x, text_y), label, fill='white', font=font)
        
        print(f"✅ 已添加: {label}")
    
    # 保存
    canvas.save(output_path, quality=95)
    print(f"\n✅ 参考图网格已生成: {output_path}")
    return output_path

def generate_prompt(product_name: str = "wireless screen mirroring device") -> str:
    """生成 Nano Banana 2 的 Prompt"""
    return f"""Based on the reference images showing 6 orthographic views (Front/Back/Left/Right/Top/Bottom), reconstruct the complete 3D model of this {product_name}.

Generate a clean, professional 2x3 grid layout with the same 6 views:
ROW 1: Front View | Back View
ROW 2: Left Side View | Right Side View
ROW 3: Top View | Bottom View

Requirements:
- Pure white studio background
- Professional product photography lighting
- 4K resolution, hyper-realistic
- All 6 views must show the SAME device with IDENTICAL appearance
- Maintain exact proportions and design details from reference images"""

def create_task_with_url(prompt: str, image_url: str) -> dict:
    """创建 Nano Banana 2 任务（使用图片 URL）"""
    url = f"{API_BASE}/jobs/createTask"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": "nano-banana-2",
        "input": {
            "prompt": prompt,
            "aspect_ratio": "2:3",
            "resolution": "4K",
            "output_format": "png",
            "google_search": False,
            "image_input": [image_url]
        }
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
    except Exception as e:
        return {"error": str(e)}

def query_task(task_id: str) -> dict:
    """查询任务状态"""
    url = f"{API_BASE}/jobs/recordInfo?taskId={task_id}"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except Exception as e:
        return {"error": str(e)}

def wait_for_completion(task_id: str, max_wait: int = 300) -> dict:
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
        time.sleep(12)
    
    return {"error": "Timeout"}

def main():
    parser = argparse.ArgumentParser(description="产品多视角参考图生成器")
    parser.add_argument("--front", required=True, help="正面视图")
    parser.add_argument("--back", required=True, help="背面视图")
    parser.add_argument("--left", required=True, help="左侧视图")
    parser.add_argument("--right", required=True, help="右侧视图")
    parser.add_argument("--top", required=True, help="顶部视图")
    parser.add_argument("--bottom", required=True, help="底部视图")
    parser.add_argument("--product", default="wireless screen mirroring device", help="产品名称")
    parser.add_argument("--image-url", help="参考图 URL（如果已上传）")
    parser.add_argument("--output", default="product-reference.png", help="输出路径")
    
    args = parser.parse_args()
    
    # 1. 创建参考图网格
    views = {
        "front": args.front,
        "back": args.back,
        "left": args.left,
        "right": args.right,
        "top": args.top,
        "bottom": args.bottom,
    }
    
    grid_path = args.output.replace(".png", "-grid.png")
    create_reference_grid(views, grid_path)
    
    # 2. 检查是否提供了图片 URL
    if not args.image_url:
        print("\n⚠️  需要手动上传参考图网格到 kie.ai")
        print(f"📁 文件路径: {grid_path}")
        print("📋 上传后，使用 --image-url 参数重新运行")
        return
    
    # 3. 生成 Prompt
    prompt = generate_prompt(args.product)
    
    # 4. 创建任务
    print("\n🎨 创建生成任务...")
    result = create_task_with_url(prompt, args.image_url)
    
    if "error" in result:
        print(f"❌ 创建失败: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    task_id = result['data']['taskId']
    print(f"✅ 任务已创建: {task_id}")
    
    # 5. 等待完成
    print("\n⏳ 等待生成完成...")
    result = wait_for_completion(task_id)
    
    if "error" in result:
        print(f"❌ 生成失败: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    # 6. 保存结果
    output_urls = result['data'].get('output', [])
    print(f"\n✅ 生成完成！")
    print(f"📸 结果 URL: {output_urls}")
    
    # 保存到 JSON
    result_file = args.output.replace(".png", "-result.json")
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"💾 结果已保存: {result_file}")

if __name__ == "__main__":
    main()
