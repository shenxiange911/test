#!/usr/bin/env python3
"""
分镜拆分脚本 - Phase 4
将总分镜图按照网格拆分成独立的分镜帧

使用方法:
    python3 split_storyboard.py --input storyboard.jpg --output ./frames
    python3 split_storyboard.py --input storyboard.jpg --rows 3 --cols 3
    python3 split_storyboard.py --help
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from PIL import Image

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StoryboardSplitter:
    """分镜拆分工具"""
    
    def __init__(self, rows=3, cols=3, project_name="project"):
        self.rows = rows
        self.cols = cols
        self.project_name = project_name
        self.frames = []
    
    def validate_input(self, image_path):
        """验证输入文件"""
        if not os.path.exists(image_path):
            logger.error(f"文件不存在: {image_path}")
            return False
        
        if not image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            logger.error(f"不支持的文件格式: {image_path}")
            return False
        
        return True
    
    def split(self, image_path, output_dir):
        """拆分分镜图"""
        
        # 验证输入
        if not self.validate_input(image_path):
            return False
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"输出目录: {output_dir}")
        
        # 打开图片
        try:
            img = Image.open(image_path)
            logger.info(f"打开图片: {image_path}")
            logger.info(f"分辨率: {img.width}x{img.height}")
            logger.info(f"格式: {img.format}")
        except Exception as e:
            logger.error(f"打开图片失败: {e}")
            return False
        
        # 计算每个分镜的宽高
        frame_width = img.width // self.cols
        frame_height = img.height // self.rows
        
        logger.info(f"网格: {self.rows}x{self.cols} ({self.rows * self.cols}个分镜)")
        logger.info(f"每个分镜大小: {frame_width}x{frame_height}")
        
        # 拆分分镜
        frame_num = 1
        
        for row in range(self.rows):
            for col in range(self.cols):
                try:
                    # 计算裁剪坐标
                    left = col * frame_width
                    top = row * frame_height
                    right = left + frame_width
                    bottom = top + frame_height
                    
                    # 裁剪分镜
                    frame = img.crop((left, top, right, bottom))
                    
                    # 生成文件名
                    frame_filename = f"{frame_num:02d}_{self.project_name}_scene.png"
                    frame_path = os.path.join(output_dir, frame_filename)
                    
                    # 保存分镜
                    frame.save(frame_path, quality=95)
                    
                    self.frames.append({
                        "frame_num": frame_num,
                        "filename": frame_filename,
                        "path": frame_path,
                        "size": f"{frame_width}x{frame_height}",
                        "position": f"({row},{col})"
                    })
                    
                    logger.info(f"✅ 分镜 {frame_num:02d}: {frame_filename}")
                    frame_num += 1
                    
                except Exception as e:
                    logger.error(f"拆分分镜 {frame_num} 失败: {e}")
                    return False
        
        # 保存元数据
        try:
            metadata = {
                "project": self.project_name,
                "source_image": os.path.basename(image_path),
                "source_size": f"{img.width}x{img.height}",
                "grid": f"{self.rows}x{self.cols}",
                "total_frames": len(self.frames),
                "frame_size": f"{frame_width}x{frame_height}",
                "frames": self.frames
            }
            
            metadata_path = os.path.join(output_dir, "frames_metadata.json")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"元数据已保存: {metadata_path}")
        except Exception as e:
            logger.error(f"保存元数据失败: {e}")
            return False
        
        logger.info(f"✅ 拆分完成! 总分镜数: {len(self.frames)}")
        return True

def main():
    parser = argparse.ArgumentParser(
        description='分镜拆分工具 - 将总分镜图按网格拆分成独立帧',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 基本用法
  python3 split_storyboard.py --input storyboard.jpg --output ./frames
  
  # 自定义网格
  python3 split_storyboard.py --input storyboard.jpg --rows 4 --cols 4
  
  # 自定义项目名称
  python3 split_storyboard.py --input storyboard.jpg --project my-project
        '''
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入分镜图文件路径')
    parser.add_argument('--output', '-o', default='./frames', help='输出目录 (默认: ./frames)')
    parser.add_argument('--rows', type=int, default=3, help='网格行数 (默认: 3)')
    parser.add_argument('--cols', type=int, default=3, help='网格列数 (默认: 3)')
    parser.add_argument('--project', '-p', default='project', help='项目名称 (默认: project)')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细日志输出')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # 验证参数
    if args.rows < 1 or args.cols < 1:
        logger.error("网格行数和列数必须大于 0")
        return False
    
    # 执行拆分
    splitter = StoryboardSplitter(
        rows=args.rows,
        cols=args.cols,
        project_name=args.project
    )
    
    success = splitter.split(args.input, args.output)
    
    if success:
        logger.info(f"📁 输出目录: {os.path.abspath(args.output)}")
        return True
    else:
        logger.error("拆分失败")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"未预期的错误: {e}")
        sys.exit(1)
