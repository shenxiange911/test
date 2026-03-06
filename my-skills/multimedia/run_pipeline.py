#!/usr/bin/env python3
"""
多媒体制作流水线主执行脚本
"""

import sys
import json
import subprocess
import os

def run_script(script_name, *args):
    """执行一个脚本并返回结果"""
    script_path = os.path.expanduser(f"~/.openclaw/skills/multimedia/scripts/{script_name}")
    cmd = ["python3", script_path] + list(args)
    print(f"\n▶️ 执行: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        print(result.stdout)
        if result.stderr:
            print(f"⚠️ 错误: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False

def main():
    if len(sys.argv) < 6:
        print("用法: python3 run_pipeline.py <subject> <scene> <duration> <platform> <output_dir>")
        sys.exit(1)

    subject = sys.argv[1]
    scene = sys.argv[2]
    duration = int(sys.argv[3])
    platform = sys.argv[4]
    output_dir = sys.argv[5]

    print(f"""
╔════════════════════════════════════════════════════════════╗
║         🎬 多媒体制作流水线 - 完整执行                      ║
╚════════════════════════════════════════════════════════════╝

📌 项目信息:
  主题: {subject}
  场景: {scene}
  时长: {duration}s
  平台: {platform}
  输出目录: {output_dir}
""")

    os.makedirs(output_dir, exist_ok=True)

    # Phase 1: 剧本生成
    print("\n" + "="*60)
    print("📝 Phase 1: 剧本生成 (01-research)")
    print("="*60)
    if not run_script("script_generator.py", subject, scene, str(duration), platform, output_dir):
        print("❌ 剧本生成失败")
        return False

    # Phase 2: 参考图生成
    print("\n" + "="*60)
    print("🎨 Phase 2: 参考图生成 (02-reference)")
    print("="*60)
    if not run_script("reference_generator.py", subject, output_dir):
        print("⚠️ 参考图生成失败，继续...")

    # Phase 3: 分镜图生成
    print("\n" + "="*60)
    print("📋 Phase 3: 分镜图生成 (03-storyboard)")
    print("="*60)
    if not run_script("storyboard_generator.py", subject, scene, output_dir):
        print("⚠️ 分镜图生成失败，继续...")

    # Phase 4: 分镜拆分
    print("\n" + "="*60)
    print("✂️ Phase 4: 分镜拆分 (04-split)")
    print("="*60)
    if not run_script("frame_splitter.py", output_dir):
        print("⚠️ 分镜拆分失败，继续...")

    print(f"""
╔════════════════════════════════════════════════════════════╗
║                    ✅ 流水线执行完成                        ║
╚════════════════════════════════════════════════════════════╝

📁 输出目录: {output_dir}
📊 生成的文件:
  - script.md (剧本)
  - reference_views/ (参考图)
  - storyboard_full.png (分镜图)
  - frames/ (拆分后的分镜)
""")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
