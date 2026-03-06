#!/usr/bin/env python3
"""
图片分析工具（升级版）
调用 OpenClaw image 工具或 Gemini 分析图片
"""

import sys
import json
import os

def analyze_image(image_source, prompt, method="openclaw"):
    """
    分析图片
    image_source: 本地路径或 URL
    prompt: 分析提示词
    method: "openclaw" (使用 image 工具) 或 "gemini" (使用 Gemini)
    """
    print(f"🖼️ 图片分析工具")
    print(f"图片源: {image_source}")
    print(f"提示词: {prompt}")
    print(f"方法: {method}")
    
    # 构建分析任务
    analysis_task = f"""分析这张图片：{image_source}

{prompt}

请提供详细的分析。
"""
    
    if method == "openclaw":
        print(f"\n📋 使用 OpenClaw image 工具")
        print(f"⚠️ 需要在 OpenClaw 对话中调用:")
        print(f"image(image='{image_source}', prompt='''{prompt}''')")
    else:
        print(f"\n📋 使用 Gemini")
        print(f"⚠️ 需要通过 sessions_spawn 调用:")
        print(f"sessions_spawn(")
        print(f"    runtime='subagent',")
        print(f"    agentId='gemini-2.5-pro-preview',")
        print(f"    task='''{analysis_task}'''")
        print(f")")
    
    return {
        "status": "pending",
        "source": image_source,
        "method": method,
        "task": analysis_task
    }

def main():
    if len(sys.argv) < 3:
        print("用法: python3 image_analyzer.py <image_source> <prompt> [method]")
        print("\n示例:")
        print("  python3 image_analyzer.py ./ref.jpg '分析角色外观特征' openclaw")
        print("  python3 image_analyzer.py https://example.com/img.jpg '分析构图' gemini")
        sys.exit(1)
    
    image_source = sys.argv[1]
    prompt = sys.argv[2]
    method = sys.argv[3] if len(sys.argv) > 3 else "openclaw"
    
    result = analyze_image(image_source, prompt, method)
    print(f"\n{json.dumps(result, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    main()
