#!/usr/bin/env python3
"""
剧本生成工具 (Phase 1)
调用 crawler + Opus 生成剧本
"""

import sys
import json
import subprocess
import os

def generate_script(subject, scene, duration, platform, output_dir):
    """
    Phase 1: Research & Script Generation
    """
    print(f"📝 Phase 1: 剧本生成")
    print(f"主题: {subject}")
    print(f"场景: {scene}")
    print(f"时长: {duration}s")
    print(f"平台: {platform}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Deep Research (调用 crawler)
    print("\n🔍 Step 1: 深度搜索...")
    search_query = f"{subject} {scene} 视频分镜 构图技巧 {platform}"
    
    try:
        result = subprocess.run(
            [os.path.expanduser("~/.openclaw/skills/crawler/scripts/deep_research.sh"), search_query],
            capture_output=True,
            text=True,
            timeout=60
        )
        research_data = result.stdout
        print(f"✅ 搜索完成，获取 {len(research_data)} 字符")
    except Exception as e:
        print(f"⚠️ 搜索失败: {e}")
        research_data = ""
    
    # Step 2: 生成剧本结构
    print("\n📋 Step 2: 生成剧本...")
    
    # 计算分镜数量（根据时长）
    if duration <= 15:
        num_scenes = 4
    elif duration <= 30:
        num_scenes = 6
    elif duration <= 60:
        num_scenes = 9
    else:
        num_scenes = 12
    
    script_content = f"""# {subject} — {platform} 视频剧本

## 概述
- 主体: {subject}
- 场景: {scene}
- 时长: {duration}s
- 平台: {platform}
- 分镜数: {num_scenes}

## 剧本段落

"""
    
    # 生成分镜模板
    for i in range(1, num_scenes + 1):
        script_content += f"""### SCENE {i:02d} — [场景名称]

时长: [Xs]
景别: [ECU/CU/MS/WS/EWS]
台词/旁白: [文本或"无"]
画面描述: [详细视觉描述]
情绪: [情绪/能量]

"""
    
    script_content += f"""
## 研究数据参考

{research_data[:2000] if research_data else "无搜索数据"}

---

**注意**: 请根据研究数据完善每个分镜的具体内容。
"""
    
    # 保存剧本
    script_path = os.path.join(output_dir, "script.md")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"\n✅ 剧本已生成: {script_path}")
    print(f"📊 包含 {num_scenes} 个分镜")
    print(f"\n⚠️ 请手动完善剧本内容，或调用 Opus 自动生成详细描述")
    
    return script_path

def main():
    if len(sys.argv) < 6:
        print("用法: python3 script_generator.py <subject> <scene> <duration> <platform> <output_dir>")
        print("示例: python3 script_generator.py '运动鞋' '城市街头' 30 'YouTube' ./project")
        sys.exit(1)
    
    subject = sys.argv[1]
    scene = sys.argv[2]
    duration = int(sys.argv[3])
    platform = sys.argv[4]
    output_dir = sys.argv[5]
    
    script_path = generate_script(subject, scene, duration, platform, output_dir)
    
    # 输出 JSON 供其他工具调用
    result = {
        "status": "success",
        "script_path": script_path,
        "num_scenes": 6 if duration <= 30 else 9
    }
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
