from __future__ import annotations
import argparse
from pathlib import Path

from core.io import make_workdirs, write_json, read_json
from core.logger import make_logger
from core.plan import Plan, Step
from core.runner import run_skill
from core.config import load_config

# Import all skills to register them
from skills import (
    inputs_detect,
    media_understand_gemini,
    script_generate,
    ref_collect,
    storyboard_generate,
    storyboard_split,
    image_repair_upscale,
    scene_image2video,
    edit_compose,
    music_add,
    voice_generate,
    subtitle_generate,
    final_render,
)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user-need", required=True, help="用户需求")
    ap.add_argument("--input", action="append", default=[], help="本地路径或URL（可多次）")
    ap.add_argument("--no-download", action="store_true", help="不下载远程直链媒体（只识别）")
    ap.add_argument("--ref-query", default="产品/模特参考图", help="参考图检索 query")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--rows", type=int, default=2)
    ap.add_argument("--skip-understand", action="store_true", help="跳过 Gemini 理解阶段")
    args = ap.parse_args()

    project_root = Path(__file__).resolve().parent
    cfg = load_config(project_root)

    dirs = make_workdirs("outputs")
    logger = make_logger(dirs.logs)
    ctx = {"dirs": dirs, "logger": logger, "config": cfg}

    logger.log(f"RUN_ID={dirs.run_id}")
    logger.log(f"user_need={args.user_need}")

    # Build plan (for reproducibility)
    plan = Plan(steps=[
        Step("inputs.detect", {"text": args.user_need, "also_inputs": args.input, "download_remote": (not args.no_download)}),
        Step("media.understand_gemini", {"mode": "auto"}),
        Step("script.generate", {"user_need": args.user_need}),
        Step("ref.collect", {"query": args.ref_query, "k": 4}),
        Step("storyboard.generate", {"cols": args.cols, "rows": args.rows}),
        Step("storyboard.split", {"cols": args.cols, "rows": args.rows}),
        Step("image.repair_upscale", {"scale": 2}),
        Step("scene.image2video", {"seconds": 3, "fps": 24}),
        Step("video.compose", {}),
        Step("music.add", {}),
        Step("voice.generate", {}),
        Step("subtitle.generate", {}),
        Step("final.render", {}),
    ])
    write_json(dirs.run_dir / "plan.json", plan.to_dict())

    # 1) inputs.detect
    r_inputs = run_skill("inputs.detect", ctx, {"text": args.user_need, "also_inputs": args.input, "download_remote": (not args.no_download)})
    if not r_inputs.ok:
        raise SystemExit(r_inputs.error)
    write_json(dirs.artifacts / "resolved_inputs.json", r_inputs.data)
    resolved_inputs = r_inputs.data.get("inputs", [])

    # 2) media understanding (optional)
    subject_lock = None
    style_lock = None
    if not args.skip_understand and resolved_inputs:
        try:
            r_under = run_skill("media.understand_gemini", ctx, {"inputs": resolved_inputs, "mode": "auto"})
            if r_under.ok:
                subject_lock = r_under.data.get("subject_lock")
                style_lock = r_under.data.get("style_lock")
        except Exception as e:
            logger.log(f"understand skipped due to error: {e}")

    # 3) script
    r_script = run_skill("script.generate", ctx, {"user_need": args.user_need})
    if not r_script.ok:
        raise SystemExit(r_script.error)
    script = r_script.data["script"]
    (dirs.artifacts / "script.txt").write_text(script, encoding="utf-8")

    # 4) refs
    r_refs = run_skill("ref.collect", ctx, {"query": args.ref_query, "k": 4})
    refs = r_refs.data.get("refs", [])

    # 5) storyboard
    r_sheet = run_skill("storyboard.generate", ctx, {"script": script, "refs": refs, "cols": args.cols, "rows": args.rows,
                                                     "subject_lock": subject_lock, "style_lock": style_lock})
    sheet = r_sheet.data["sheet"]

    # 6) split
    r_split = run_skill("storyboard.split", ctx, {"sheet": sheet, "cols": args.cols, "rows": args.rows})
    scenes = r_split.data["scenes"]

    # 7) banana2 fix+upscale
    fixed = []
    for sc in scenes:
        r = run_skill("image.repair_upscale", ctx, {"image": sc, "scale": 2})
        if not r.ok:
            raise SystemExit(r.error)
        fixed.append(r.data["fixed"])

    # 8) image2video per scene
    clips = []
    for img in fixed:
        r = run_skill("scene.image2video", ctx, {"image": img, "seconds": 3, "fps": 24})
        if not r.ok:
            raise SystemExit(r.error)
        clips.append(r.data["video"])

    # 9) compose
    r_comp = run_skill("video.compose", ctx, {"videos": clips})
    composed = r_comp.data["composed"]

    # 10) music
    r_music = run_skill("music.add", ctx, {})
    music = r_music.data["music"]

    # 11) voice
    r_voice = run_skill("voice.generate", ctx, {"script": script})
    voice = r_voice.data["voice"]

    # 12) subs
    r_sub = run_skill("subtitle.generate", ctx, {"script": script})
    srt = r_sub.data["srt"]

    # 13) final
    r_final = run_skill("final.render", ctx, {"video": composed, "music": music, "voice": voice, "srt": srt})
    final = r_final.data["final"]

    summary = {
        "run_id": dirs.run_id,
        "workdir": str(dirs.run_dir),
        "resolved_inputs": resolved_inputs,
        "subject_lock": subject_lock,
        "style_lock": style_lock,
        "script_file": str(dirs.artifacts / "script.txt"),
        "refs": refs,
        "sheet": sheet,
        "scenes": scenes,
        "fixed_scenes": fixed,
        "clips": clips,
        "composed": composed,
        "music": music,
        "voice": voice,
        "srt": srt,
        "final": final
    }
    write_json(dirs.run_dir / "summary.json", summary)
    logger.log(f"DONE final={final}")
    print(f"✅ DONE. final={final}")
    print(f"📁 workdir={dirs.run_dir}")

if __name__ == "__main__":
    main()
