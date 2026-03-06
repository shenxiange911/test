#!/usr/bin/env python3
"""
产品分镜图生成器 - Nano Banana Prompt Protocol v2.3
用法: python3 generate_product_storyboard.py --config <config.json>
"""

import sys
import json
import os
import argparse
from typing import Dict, Any, List, Optional

# 导入 kie_api 工具
sys.path.insert(0, os.path.dirname(__file__))
import kie_api

# 模板 01: Nano Banana Prompt Protocol v2.3
TEMPLATE_01 = """/// NANO BANANA PROMPT PROTOCOL v2.3 ///

[SECTION 1: 资产扫描与坐标系定义]

SET ASSET_POOL = [All Uploaded Images];

IMAGE_ROLE_ASSIGNMENT:
{image_roles}

DEEP_SCAN({scan_targets}):
{scan_instructions}

COORDINATE_LOCK:
{coordinate_system}

[SECTION 2: 3D 实体合成]

{synthesis_instructions}

[SECTION 3: 渲染配置]

GLOBAL_SETTINGS:
画布：{aspect_ratio}，{panel_layout} 分镜网格
风格：{style}
精度：{resolution}
全局锁定：{global_lock}

[SECTION 4: 分镜输出]

OUTPUT_FORMAT — {panel_layout} 叙事分镜，单张 {aspect_ratio} 画布：

{panels}

RULES:
{rules}

最终目标：生成一张完整的产品{panel_count}格叙事分镜图"""


class ProductStoryboardGenerator:
    """产品分镜图生成器"""
    
    def __init__(self, config_path: str):
        """初始化生成器"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 加载 API Key
        kie_api.load_api_key()
        if not kie_api.API_KEY:
            raise ValueError("未找到 KIE_API_KEY")
    
    def build_prompt(self) -> str:
        """构建完整 prompt"""
        cfg = self.config
        
        # [SECTION 1: 资产扫描与坐标系定义]
        image_roles = self._build_image_roles(cfg.get("images", {}))
        scan_targets = " / ".join([f"IMG_{chr(65+i)}" for i in range(len(cfg.get("images", {})))])
        scan_instructions = cfg.get("scan_instructions", "系统性解析参考图，完整理解产品几何结构、各面空间关系、连接方式与使用场景。")
        coordinate_system = cfg.get("coordinate_system", "基于 IMG_A 视图自动推算坐标系")
        
        # [SECTION 2: 3D 实体合成]
        synthesis_instructions = cfg.get("synthesis_instructions", "以 VAR_FRONT 为基准，强制对齐所有接口与边缘细节。")
        
        # [SECTION 3: 渲染配置]
        aspect_ratio = cfg.get("aspect_ratio", "16:9")
        panel_layout = cfg.get("panel_layout", "2×2")
        style = cfg.get("style", "写实场景摄影风格，自然光，电影感构图")
        resolution = cfg.get("resolution", "8K")
        global_lock = cfg.get("global_lock", "所有分镜中产品的外观/丝印/坐标轴方向严格统一")
        
        # [SECTION 4: 分镜输出]
        panels = self._build_panels(cfg.get("panels", []))
        panel_count = len(cfg.get("panels", []))
        rules = self._build_rules(cfg.get("rules", []))
        
        # 填充模板
        prompt = TEMPLATE_01.format(
            image_roles=image_roles,
            scan_targets=scan_targets,
            scan_instructions=scan_instructions,
            coordinate_system=coordinate_system,
            synthesis_instructions=synthesis_instructions,
            aspect_ratio=aspect_ratio,
            panel_layout=panel_layout,
            style=style,
            resolution=resolution,
            global_lock=global_lock,
            panels=panels,
            panel_count=panel_count,
            rules=rules
        )
        
        return prompt
    
    def _build_image_roles(self, images: Dict[str, str]) -> str:
        """构建图片角色分配"""
        roles = []
        for i, (key, desc) in enumerate(images.items()):
            label = f"IMG_{chr(65+i)}"
            roles.append(f"{label}（{key}）：{desc}")
        return "\n".join(roles)
    
    def _build_panels(self, panels: List[Dict[str, str]]) -> str:
        """构建分镜描述"""
        panel_texts = []
        for i, panel in enumerate(panels):
            position = panel.get("position", f"Panel {chr(65+i)}")
            description = panel.get("description", "")
            panel_texts.append(f"[{position}]：{description}")
        return "\n\n".join(panel_texts)
    
    def _build_rules(self, rules: List[str]) -> str:
        """构建规则列表"""
        if not rules:
            rules = [
                "所有面板禁止添加任何注解/箭头/标签，产品本身丝印除外",
                "连接方式须基于参考图理解后创作，禁止照抄或自行发明"
            ]
        return "\n".join(rules)
    
    def calculate_dimensions(self) -> tuple:
        """计算最终图片尺寸（Nano Banana Pro 支持 1K/2K/4K）"""
        resolution = self.config.get("resolution", "2K")
        aspect_ratio = self.config.get("aspect_ratio", "16:9")
        
        # 解析分辨率
        if resolution == "1K":
            base_width = 1024
        elif resolution == "2K":
            base_width = 2048
        elif resolution == "4K":
            base_width = 4096
        else:
            base_width = 2048  # 默认 2K
        
        # 解析宽高比
        if aspect_ratio == "16:9":
            width = base_width
            height = int(base_width * 9 / 16)
        elif aspect_ratio == "21:9":
            width = base_width
            height = int(base_width * 9 / 21)
        elif aspect_ratio == "1:1":
            width = height = base_width
        else:
            # 自定义比例 (e.g., "3:2")
            parts = aspect_ratio.split(":")
            w_ratio, h_ratio = int(parts[0]), int(parts[1])
            width = base_width
            height = int(base_width * h_ratio / w_ratio)
        
        return width, height
    
    def generate(self, output_path: str) -> Dict[str, Any]:
        """生成分镜图"""
        prompt = self.build_prompt()
        width, height = self.calculate_dimensions()
        
        print(f"📝 生成的 Prompt:\n{prompt}\n")
        print(f"📐 图片尺寸: {width}×{height}")
        
        # 调用 Nano Banana Pro API
        params = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_outputs": 1
        }
        
        # 添加可选参数
        if "negative_prompt" in self.config:
            params["negative_prompt"] = self.config["negative_prompt"]
        if "guidance_scale" in self.config:
            params["guidance_scale"] = self.config["guidance_scale"]
        if "num_inference_steps" in self.config:
            params["num_inference_steps"] = self.config["num_inference_steps"]
        
        print(f"🚀 创建任务...")
        result = kie_api.create_task("nano-banana-pro", params)
        
        if "error" in result:
            return result
        
        task_id = result.get("data", {}).get("taskId")
        if not task_id:
            return {"error": "未获取到 taskId", "detail": result}
        
        print(f"⏳ 等待任务完成 (taskId: {task_id})...")
        result = kie_api.wait_for_completion(task_id, max_wait=600, interval=12)
        
        if "error" in result:
            return result
        
        # 提取图片 URL
        output_url = result.get("data", {}).get("output", [None])[0]
        if not output_url:
            return {"error": "未获取到输出图片", "detail": result}
        
        print(f"📥 下载图片: {output_url}")
        success = kie_api.download_image(output_url, output_path)
        
        if success:
            return {
                "success": True,
                "output_path": output_path,
                "task_id": task_id,
                "url": output_url
            }
        else:
            return {"error": "下载失败"}


def main():
    parser = argparse.ArgumentParser(description="产品分镜图生成器")
    parser.add_argument("--config", required=True, help="配置文件路径 (JSON)")
    parser.add_argument("--output", help="输出图片路径 (默认: output.png)")
    parser.add_argument("--show-prompt", action="store_true", help="仅显示 prompt，不生成图片")
    
    args = parser.parse_args()
    
    try:
        generator = ProductStoryboardGenerator(args.config)
        
        if args.show_prompt:
            prompt = generator.build_prompt()
            print(prompt)
            return
        
        output_path = args.output or "output.png"
        result = generator.generate(output_path)
        
        if "error" in result:
            print(f"❌ 错误: {result['error']}", file=sys.stderr)
            if "detail" in result:
                print(f"详情: {result['detail']}", file=sys.stderr)
            sys.exit(1)
        
        print(f"✅ 生成完成: {result['output_path']}")
        print(f"🔗 URL: {result['url']}")
    
    except Exception as e:
        print(f"❌ 异常: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
