#!/usr/bin/env python3
"""
分镜拆分工具 (GPT 版本优化)
用法: python3 frame_splitter.py <input_path> <rows> <cols> <output_dir> [project_name]
"""

from PIL import Image
import os
import sys

def split_storyboard(input_path, rows, cols, output_dir, project_name="frame"):
    """
    Split a storyboard grid image into individual labeled frames.
    Automatically detects and removes black/white borders between cells.
    """
    img = Image.open(input_path)
    W, H = img.size
    
    # Detect title bar height (skip top ~8% for title area)
    title_h = int(H * 0.08)
    usable = img.crop((0, title_h, W, H))
    uW, uH = usable.size
    
    cell_w = uW // cols
    cell_h = uH // rows
    
    os.makedirs(output_dir, exist_ok=True)
    
    frame_num = 1
    saved = []
    for row in range(rows):
        for col in range(cols):
            x1 = col * cell_w
            y1 = row * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h
            
            cell = usable.crop((x1, y1, x2, y2))
            
            # Trim black/white borders
            cell = trim_borders(cell)
            
            out_path = os.path.join(output_dir, f"{project_name}_{frame_num:02d}.png")
            cell.save(out_path, "PNG")
            saved.append(out_path)
            print(f"Saved frame {frame_num:02d}: {out_path}")
            frame_num += 1
    
    return saved

def trim_borders(img, threshold=20):
    """Remove near-black or near-white uniform border pixels."""
    import numpy as np
    arr = np.array(img)
    
    # Detect border rows/cols that are near-black or near-white
    def is_border_row(row):
        return (row.mean() < threshold) or (row.mean() > 255 - threshold)
    
    def is_border_col(col):
        return (col.mean() < threshold) or (col.mean() > 255 - threshold)
    
    top, bottom, left, right = 0, arr.shape[0], 0, arr.shape[1]
    
    for i in range(arr.shape[0]):
        if not is_border_row(arr[i]):
            top = i
            break
    for i in range(arr.shape[0]-1, -1, -1):
        if not is_border_row(arr[i]):
            bottom = i + 1
            break
    for j in range(arr.shape[1]):
        if not is_border_col(arr[:, j]):
            left = j
            break
    for j in range(arr.shape[1]-1, -1, -1):
        if not is_border_col(arr[:, j]):
            right = j + 1
            break
    
    return Image.fromarray(arr[top:bottom, left:right])

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("用法: python3 frame_splitter.py <input_path> <rows> <cols> <output_dir> [project_name]")
        print("示例: python3 frame_splitter.py storyboard.png 2 3 ./frames project")
        sys.exit(1)
    
    input_path = sys.argv[1]
    rows = int(sys.argv[2])
    cols = int(sys.argv[3])
    output_dir = sys.argv[4]
    project_name = sys.argv[5] if len(sys.argv) > 5 else "frame"
    
    frames = split_storyboard(input_path, rows, cols, output_dir, project_name)
    print(f"\n✅ Split complete: {len(frames)} frames saved to {output_dir}")
