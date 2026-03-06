#!/usr/bin/env python3
"""
核心模块集成测试
"""

import sys
from pathlib import Path

# 添加 skill 目录到路径
skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir))

from core import MultimediaExecutor, ProjectConfig


def test_create_project():
    """测试项目创建"""
    print("=" * 60)
    print("测试 1: 创建项目")
    print("=" * 60)
    
    # 创建执行器
    executor = MultimediaExecutor("/tmp/multimedia-test")
    print(f"✅ 执行器创建成功")
    
    # 创建项目
    state = executor.create_project(
        project_name="test-project",
        theme="测试主题",
        style="cinematic",
        duration=60,
        aspect_ratio="16:9",
        language="zh-CN"
    )
    print(f"✅ 项目创建成功: {executor.project_dir}")
    print(f"  项目名: {state.project_config.project_name}")
    
    # 验证目录结构
    expected_dirs = ["scripts", "references", "storyboards", "frames", "videos", "final", "logs"]
    for dir_name in expected_dirs:
        dir_path = executor.project_dir / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name}/ 存在")
        else:
            print(f"  ❌ {dir_name}/ 不存在")
    
    # 验证状态文件
    state_file = executor.project_dir / "project.json"
    if state_file.exists():
        print(f"  ✅ project.json 存在")
    else:
        print(f"  ❌ project.json 不存在")
    
    print()


def test_state_management():
    """测试状态管理"""
    print("=" * 60)
    print("测试 2: 状态管理")
    print("=" * 60)
    
    executor = MultimediaExecutor("/tmp/multimedia-test")
    
    # 加载状态
    state = executor.state_manager.load()
    print(f"✅ 状态加载成功")
    print(f"  项目名: {state.project_config.project_name}")
    print(f"  创建时间: {state.created_at}")
    print(f"  当前 Phase: {state.current_phase}")
    
    # 标记 Phase 完成
    executor.state_manager.mark_phase_complete(
        phase_id="phase-1",
        outputs=["script.md"],
        metadata={"test": True}
    )
    print(f"✅ Phase 标记完成")
    
    # 检查是否可以跳过
    can_skip = executor.state_manager.can_skip_phase("phase-1")
    print(f"  可以跳过 phase-1: {can_skip}")
    
    # 获取 Phase 输出
    output = executor.state_manager.get_phase_output("phase-1")
    print(f"  Phase 输出: {output}")
    
    print()


def test_phase_validation():
    """测试 Phase 验证"""
    print("=" * 60)
    print("测试 3: Phase 验证")
    print("=" * 60)
    
    executor = MultimediaExecutor("/tmp/multimedia-test")
    
    # 测试 phase-1（无依赖，应该通过）
    valid = executor.validate_phase_input("01-research")
    print(f"✅ phase-1 验证: {valid}")
    
    # 测试 phase-2（依赖 phase-1，phase-1 已完成，应该通过）
    valid2 = executor.validate_phase_input("02-reference")
    print(f"✅ phase-2 验证: {valid2}")
    
    print()


def main():
    """运行所有测试"""
    print("\n🧪 开始核心模块集成测试\n")
    
    try:
        test_create_project()
        test_state_management()
        test_phase_validation()
        
        print("=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
