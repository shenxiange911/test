from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any, Dict, List

from core.contracts import SkillResult, Artifact
from core.registry import register
from tools.gemini_client import GeminiClient
from tools.gemini_youtube import analyze_youtube
from tools.gemini_local import analyze_local_media

SUBJECT_LOCK_PROMPT = """详细描述这张图片中的主体对象的外观特征，用于后续生成一致的图片。
请提取：主体类型、颜色、形状结构、材质纹理、细节特征、光线风格。
输出格式：
Subject Lock: "[简洁英文描述]"
"""

STYLE_LOCK_PROMPT = """分析这个视频的视觉风格和镜头语言，用于后续生成类似风格的视频。
请提取：镜头类型分布、运镜方式、色调风格、节奏、构图特点。
输出格式：
Style Lock: "[镜头语言] + [色调风格] + [节奏]"
"""

STORYBOARD_BREAKDOWN_PROMPT = """请把视频拆解为分镜列表，输出结构化信息：
- 总镜头数
- 每个镜头：时间段(如00:00-00:02)、景别(WS/MS/CU)、运镜、内容、关键台词(如有)
最后给一个3句以内总结。
"""

def _make_client(cfg: Dict[str, Any]) -> GeminiClient:
    g = cfg.get("gemini", {})
    apiKey = g.get("apiKey", "")
    baseUrl = g.get("baseUrl", "")
    model = g.get("model", "gemini-2.5-pro")
    if not apiKey or apiKey == "YOUR_API_KEY":
        raise RuntimeError("Gemini apiKey not configured. Put it in config/api.json (gitignored) or env MSS_CONFIG_JSON.")
    if not baseUrl or "YOUR_ENDPOINT" in baseUrl or "example.com" in baseUrl:
        raise RuntimeError("Gemini baseUrl not configured. Set config/api.json gemini.baseUrl.")
    return GeminiClient(apiKey=apiKey, baseUrl=baseUrl, model=model, timeout=int(g.get("timeout", 120)))

@register("media.understand_gemini")
def run(ctx, params):
    cfg = ctx["config"]
    dirs = ctx["dirs"]
    client = _make_client(cfg)

    inputs = params.get("inputs", [])  # list of dicts from inputs.detect
    mode = params.get("mode", "auto")  # auto | subject_lock | style_lock | storyboard
    prompt = params.get("prompt")

    subject_lock = None
    style_lock = None
    breakdown = None
    raw_outputs: List[Dict[str, Any]] = []

    for inp in inputs:
        kind = inp.get("kind")
        url = inp.get("url")
        local_path = inp.get("local_path")

        if kind == "youtube":
            p = prompt or (STORYBOARD_BREAKDOWN_PROMPT if mode in ("auto", "storyboard") else STYLE_LOCK_PROMPT)
            out = analyze_youtube(client, url, p)
            raw_outputs.append({"input": inp, "analysis": out})
            text = out.get("text", "")
            if "Style Lock:" in text and style_lock is None:
                style_lock = text.strip()
            if breakdown is None:
                breakdown = text.strip()
            continue

        if kind in ("image", "video") and local_path:
            if kind == "image":
                p = prompt or SUBJECT_LOCK_PROMPT
                out = analyze_local_media(client, local_path, p)
                raw_outputs.append({"input": inp, "analysis": out})
                if subject_lock is None:
                    subject_lock = out.get("text", "").strip()
            else:
                p = prompt or (STORYBOARD_BREAKDOWN_PROMPT if mode in ("auto", "storyboard") else STYLE_LOCK_PROMPT)
                out = analyze_local_media(client, local_path, p)
                raw_outputs.append({"input": inp, "analysis": out})
                text = out.get("text", "")
                if "Style Lock:" in text and style_lock is None:
                    style_lock = text.strip()
                if breakdown is None:
                    breakdown = text.strip()

    data = {
        "subject_lock": subject_lock,
        "style_lock": style_lock,
        "storyboard_breakdown": breakdown,
        "raw": raw_outputs
    }
    out_path = dirs.artifacts / "understanding.json"
    from core.io import write_json
    write_json(out_path, data)
    return SkillResult(ok=True, artifacts=[Artifact(type="json", value=str(out_path), name="understanding.json")], data=data)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resolved-inputs", required=True, help="Path to resolved_inputs.json (from inputs.detect)")
    ap.add_argument("--mode", default="auto", choices=["auto","subject_lock","style_lock","storyboard"])
    ap.add_argument("--prompt", default=None)
    args = ap.parse_args()

    from core.io import make_workdirs, read_json
    from core.config import load_config
    project_root = Path(__file__).resolve().parents[1]
    cfg = load_config(project_root)

    dirs = make_workdirs("outputs")
    ctx = {"dirs": dirs, "config": cfg}

    resolved = read_json(Path(args.resolved_inputs))
    res = run(ctx, {"inputs": resolved.get("inputs", []), "mode": args.mode, "prompt": args.prompt})
    print(res.artifacts[0].value)

if __name__ == "__main__":
    main()
