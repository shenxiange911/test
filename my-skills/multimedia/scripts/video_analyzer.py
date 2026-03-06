#!/usr/bin/env python3
"""
视频分析工具
调用 Gemini 分析视频内容
支持：本地视频、在线视频 URL、YouTube 链接
"""

import sys
import json
import os

# 可用的 Gemini 模型
GEMINI_MODELS = [
    "gemini-3-pro-preview",
    "gemini-3.1-pro-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3-flash-preview"
]

def analyze_video(video_source, prompt, model="gemini-2.5-pro", output_path=None):
    """
    使用 Gemini 分析视频
    video_source: 本地路径、URL 或 YouTube 链接
    prompt: 分析提示词
    model: Gemini 模型名称
    """
    print(f"🎥 视频分析工具")
    print(f"视频源: {video_source}")
    print(f"模型: {model}")
    print(f"提示词: {prompt}")
    
    # 验证模型
    if model not in GEMINI_MODELS:
        print(f"⚠️ 警告: {model} 不在推荐列表中")
        print(f"推荐模型: {', '.join(GEMINI_MODELS)}")
    
    # 判断视频类型
    if video_source.startswith("http"):
        if "youtube.com" in video_source or "youtu.be" in video_source:
            source_type = "youtube"
        else:
            source_type = "url"
    else:
        source_type = "local"
    
    print(f"类型: {source_type}")
    
    # 构建分析任务
    analysis_task = f"""分析这个视频：{video_source}

{prompt}

请提供详细的分析，包括：
1. 视觉风格和色调
2. 镜头运用和构图
3. 节奏和剪辑
4. 关键场景描述
5. 可借鉴的技巧
"""
    
    print(f"\n📋 分析任务已构建")
    print(f"⚠️ 需要通过 OpenClaw sessions_spawn 调用 Gemini")
    print(f"\n建议命令:")
    print(f"sessions_spawn(")
    print(f"    runtime='subagent',")
    print(f"    agentId='{model}',")
    print(f"    task='''{analysis_task}'''")
    print(f")")
    
    # 保存任务到文件
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# 视频分析任务\n\n")
            f.write(f"**模型**: {model}\n")
            f.write(f"**视频源**: {video_source}\n")
            f.write(f"**类型**: {source_type}\n\n")
            f.write(f"## 分析任务\n\n")
            f.write(analysis_task)
        print(f"\n✅ 任务已保存: {output_path}")
    
    return {
        "status": "pending",
        "source": video_source,
        "type": source_type,
        "model": model,
        "task": analysis_task,
        "note": "需要通过 OpenClaw sessions_spawn 调用 Gemini"
    }

def main():
    if len(sys.argv) < 3:
        print("用法: python3 video_analyzer.py <video_source> <prompt> [model] [output_path]")
        print(f"\n可用模型:")
        for m in GEMINI_MODELS:
            print(f"  - {m}")
        print(f"\n默认模型: gemini-2.5-pro")
        print("\n示例:")
        print("  本地视频: python3 video_analyzer.py ./video.mp4 '分析分镜构图' gemini-2.5-pro")
        print("  在线视频: python3 video_analyzer.py https://example.com/video.mp4 '分析运镜技巧' gemini-2.5-flash")
        print("  YouTube: python3 video_analyzer.py https://youtube.com/watch?v=xxx '分析剪辑节奏' gemini-3-pro-preview")
        sys.exit(1)
    
    video_source = sys.argv[1]
    prompt = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else "gemini-2.5-pro"
    output_path = sys.argv[4] if len(sys.argv) > 4 else None
    
    result = analyze_video(video_source, prompt, model, output_path)
    print(f"\n{json.dumps(result, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    main()
