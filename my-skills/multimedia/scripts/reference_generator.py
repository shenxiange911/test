#!/usr/bin/env python3
"""
参考图生成工具 (Phase 2)
灵活生成任意数量和角度的参考图
"""

import sys
import json
import subprocess
import os
import time
from output_validator import OutputValidator, with_retry

# 预定义的常用视图
COMMON_VIEWS = {
    # 基础视图
    "front": ("正面", "front view, facing camera directly"),
    "back": ("背面", "back view, rear angle"),
    "left": ("左侧", "left side view, 90 degree profile"),
    "right": ("右侧", "right side view, 90 degree profile"),
    "top": ("俯视", "top-down view, bird's eye angle"),
    "bottom": ("仰视", "bottom-up view, worm's eye angle"),
    
    # 细节视图
    "detail-face": ("面部特写", "extreme close-up of face, facial details"),
    "detail-hands": ("手部特写", "close-up of hands, hand details"),
    "detail-feet": ("脚部特写", "close-up of feet, shoe details"),
    "detail-texture": ("材质特写", "extreme close-up of material texture"),
    "detail-logo": ("标志特写", "close-up of logo or branding"),
    
    # 产品视图
    "product-hero": ("主视图", "hero shot, main product angle"),
    "product-45": ("45度角", "45 degree angle view"),
    "product-flat": ("平铺", "flat lay, top-down product shot"),
    "product-lifestyle": ("场景图", "lifestyle shot, product in use"),
    
    # 动作视图
    "action-walk": ("行走", "walking pose, dynamic movement"),
    "action-run": ("奔跑", "running pose, action shot"),
    "action-jump": ("跳跃", "jumping pose, mid-air"),
    "action-sit": ("坐姿", "sitting pose, relaxed position"),
}

def generate_reference_views(subject_desc, output_dir, views=None, model="nano-banana-pro"):
    """
    Phase 2: Subject Reference Views (灵活版本)
    views: 视图列表，如 ["front", "back", "detail-face"] 或自定义
    """
    print(f"🖼️ Phase 2: 参考图生成")
    print(f"主体描述: {subject_desc}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 如果没有指定视图，使用默认的正反面
    if not views:
        views = ["front", "back"]
        print(f"⚠️ 未指定视图，使用默认: {views}")
    
    print(f"📊 将生成 {len(views)} 张参考图")
    
    # 解析视图列表
    view_configs = []
    for view in views:
        if view in COMMON_VIEWS:
            # 使用预定义视图
            label, angle_desc = COMMON_VIEWS[view]
            view_configs.append((view, label, angle_desc))
        elif ":" in view:
            # 自定义视图格式: "view_id:标签:角度描述"
            parts = view.split(":", 2)
            view_id = parts[0]
            label = parts[1] if len(parts) > 1 else view_id
            angle_desc = parts[2] if len(parts) > 2 else f"{label} view"
            view_configs.append((view_id, label, angle_desc))
        else:
            # 简单视图，直接使用
            view_configs.append((view, view, f"{view} view"))
    
    results = []
    kie_api = os.path.expanduser("~/.openclaw/skills/media-image/scripts/kie_api.py")
    
    for view_id, label, angle_desc in view_configs:
        print(f"\n📸 生成 {label} 视图...")
        
        # 构建 prompt
        prompt = f"""Character reference sheet, {angle_desc},
{subject_desc},
neutral pose, plain white background, no shadows,
orthographic camera, consistent scale, professional concept art,
label text "{label}" at top, ultra detailed, 8K"""
        
        # 调用 kie_api.py
        params = {
            "prompt": prompt,
            "aspect_ratio": "21:9",  # 超宽屏适合参考图
            "image_size": "2k"
        }
        
        try:
            # 创建任务
            result = subprocess.run(
                ["python3", kie_api, "create", model, json.dumps(params)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            task_data = json.loads(result.stdout)
            task_id = task_data.get("data", {}).get("taskId")
            
            if not task_id:
                print(f"❌ 创建任务失败: {label}")
                continue
            
            print(f"⏳ 任务ID: {task_id}，等待完成...")
            
            # 等待完成
            result = subprocess.run(
                ["python3", kie_api, "wait", task_id],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            complete_data = json.loads(result.stdout)
            image_url = complete_data.get("data", {}).get("output", {}).get("image_url")
            
            if not image_url:
                print(f"❌ 生成失败: {label}")
                continue
            
            # 下载图片
            output_path = os.path.join(output_dir, f"{view_id}.png")
            subprocess.run(
                ["python3", kie_api, "download", image_url, output_path],
                timeout=60
            )
            
            # 验证图片
            validator = OutputValidator(verbose=True)
            if not validator.validate_image(output_path, min_resolution=(512, 512)):
                print(f"⚠️ 图片验证失败: {', '.join(validator.errors)}")
                print(f"🔄 跳过此视图，继续下一个...")
                continue
            
            print(f"✅ {label} 完成: {output_path}")
            results.append({
                "view": view_id,
                "label": label,
                "path": output_path,
                "url": image_url
            })
            
            # 间隔 12 秒避免限流
            if view_id != view_configs[-1][0]:
                print("⏸️ 等待 12 秒...")
                time.sleep(12)
        
        except Exception as e:
            print(f"❌ {label} 生成失败: {e}")
            continue
    
    # 保存结果
    result_json = os.path.join(output_dir, "reference_views.json")
    with open(result_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 参考图生成完成: {len(results)}/{len(view_configs)}")
    print(f"📄 结果保存: {result_json}")
    
    return results

def main():
    if len(sys.argv) < 3:
        print("用法: python3 reference_generator.py <subject_desc> <output_dir> [views...] [--model=MODEL]")
        print("\n预定义视图:")
        print("  基础: front, back, left, right, top, bottom")
        print("  细节: detail-face, detail-hands, detail-feet, detail-texture, detail-logo")
        print("  产品: product-hero, product-45, product-flat, product-lifestyle")
        print("  动作: action-walk, action-run, action-jump, action-sit")
        print("\n自定义视图格式: view_id:标签:角度描述")
        print("\n示例:")
        print("  # 默认（正反面）")
        print("  python3 reference_generator.py '黑金铠甲' ./ref")
        print("\n  # 基础四视图")
        print("  python3 reference_generator.py '运动鞋' ./ref front back left right")
        print("\n  # 产品特写")
        print("  python3 reference_generator.py '手表' ./ref product-hero detail-texture detail-logo")
        print("\n  # 人物细节")
        print("  python3 reference_generator.py '模特' ./ref front back detail-face detail-hands")
        print("\n  # 自定义视图")
        print("  python3 reference_generator.py '汽车' ./ref 'front-left:左前45度:front-left 45 degree angle'")
        sys.exit(1)
    
    subject_desc = sys.argv[1]
    output_dir = sys.argv[2]
    
    # 解析参数
    views = []
    model = "nano-banana-pro"
    
    for arg in sys.argv[3:]:
        if arg.startswith("--model="):
            model = arg.split("=", 1)[1]
        else:
            views.append(arg)
    
    results = generate_reference_views(subject_desc, output_dir, views if views else None, model)
    
    # 输出 JSON
    print(json.dumps({"status": "success", "views": results}, ensure_ascii=False))

if __name__ == "__main__":
    main()
