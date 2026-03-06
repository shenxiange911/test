#!/usr/bin/env python3
"""
分镜图生成工具 (Phase 3)
基于剧本生成整张分镜图
"""

import sys
import json
import subprocess
import os
import time
from output_validator import OutputValidator

def generate_storyboard(script_path, reference_dir, output_path, rows=2, cols=3, model="nano-banana-pro"):
    """
    Phase 3: Storyboard Sheet Generation
    """
    print(f"🎬 Phase 3: 分镜图生成 ({rows}×{cols})")
    print(f"剧本: {script_path}")
    print(f"参考图: {reference_dir}")
    
    # 读取剧本
    with open(script_path, 'r', encoding='utf-8') as f:
        script_content = f.read()
    
    # 提取分镜描述（简化版，实际应该解析 markdown）
    scenes = []
    for line in script_content.split('\n'):
        if line.startswith('### SCENE'):
            scenes.append(line)
    
    num_scenes = rows * cols
    print(f"📊 需要生成 {num_scenes} 个分镜")
    
    # 读取 Subject Lock（从参考图 JSON）
    subject_lock = ""
    ref_json = os.path.join(reference_dir, "reference_views.json")
    if os.path.exists(ref_json):
        print("🔒 加载 Subject Lock...")
        # 这里应该从参考图提取外观描述，暂时用占位符
        subject_lock = "[Subject Lock: 从参考图提取的外观描述]"
    
    # 构建分镜 prompt
    prompt = f"""Storyboard contact sheet, {rows} rows × {cols} columns grid layout,
{num_scenes} panels total, each panel labeled with number (01, 02, 03...),

Panel descriptions:
"""
    
    for i in range(1, num_scenes + 1):
        prompt += f"Panel {i:02d}: [Scene {i} visual description], {subject_lock}\n"
    
    prompt += f"""
Each panel: cinematic composition, movie quality, consistent style,
panel numbers visible at top-left corner,
professional storyboard layout, clean grid separation"""
    
    print(f"\n📝 Prompt 长度: {len(prompt)} 字符")
    
    # 调用 kie_api.py
    kie_api = os.path.expanduser("~/.openclaw/skills/media-image/scripts/kie_api.py")
    
    params = {
        "prompt": prompt,
        "aspect_ratio": "2:3" if rows == 2 else "1:1",  # 2×3 用 2:3，3×3 用 1:1
        "image_size": "4k"
    }
    
    try:
        print("\n🚀 创建任务...")
        result = subprocess.run(
            ["python3", kie_api, "create", model, json.dumps(params)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        task_data = json.loads(result.stdout)
        task_id = task_data.get("data", {}).get("taskId")
        
        if not task_id:
            print(f"❌ 创建任务失败")
            return None
        
        print(f"⏳ 任务ID: {task_id}，等待完成...")
        
        # 等待完成
        result = subprocess.run(
            ["python3", kie_api, "wait", task_id],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        complete_data = json.loads(result.stdout)
        image_url = complete_data.get("data", {}).get("output", {}).get("image_url")
        
        if not image_url:
            print(f"❌ 生成失败")
            return None
        
        # 下载图片
        subprocess.run(
            ["python3", kie_api, "download", image_url, output_path],
            timeout=120
        )
        
        # 验证分镜图
        validator = OutputValidator(verbose=True)
        min_resolution = (1024 * cols, 576 * rows)  # 根据网格计算最小分辨率
        
        if not validator.validate_image(output_path, min_resolution=min_resolution):
            print(f"⚠️ 分镜图验证失败: {', '.join(validator.errors)}")
            return None
        
        print(f"\n✅ 分镜图已生成: {output_path}")
        
        return {
            "status": "success",
            "path": output_path,
            "url": image_url,
            "rows": rows,
            "cols": cols
        }
    
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return None

def main():
    if len(sys.argv) < 4:
        print("用法: python3 storyboard_generator.py <script_path> <reference_dir> <output_path> [rows] [cols] [model]")
        print("示例: python3 storyboard_generator.py ./script.md ./reference_views ./storyboard_full.png 2 3 nano-banana-pro")
        sys.exit(1)
    
    script_path = sys.argv[1]
    reference_dir = sys.argv[2]
    output_path = sys.argv[3]
    rows = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    cols = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    model = sys.argv[6] if len(sys.argv) > 6 else "nano-banana-pro"
    
    result = generate_storyboard(script_path, reference_dir, output_path, rows, cols, model)
    
    if result:
        print(json.dumps(result, ensure_ascii=False))
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
