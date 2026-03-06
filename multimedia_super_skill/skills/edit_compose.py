from __future__ import annotations
import argparse
from pathlib import Path
from core.contracts import SkillResult, Artifact
from core.registry import register
from tools.ffmpeg import FFmpeg

@register("video.compose")
def run(ctx, params):
    videos = [Path(v) for v in params["videos"]]
    out = Path(ctx["dirs"].artifacts) / "composed.mp4"
    cfg = ctx["config"].get("tools", {}).get("ffmpeg", {})
    ff = FFmpeg(mode=cfg.get("mode","auto"))
    composed = ff.concat_videos(videos, out)
    return SkillResult(ok=True, artifacts=[Artifact(type="file", value=str(composed), mime="video/mp4")],
                       data={"composed": str(composed)})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--videos", nargs="+", required=True)
    args = ap.parse_args()
    from core.io import make_workdirs
    from core.config import load_config
    project_root = Path(__file__).resolve().parents[1]
    ctx = {"dirs": make_workdirs("outputs"), "config": load_config(project_root)}
    res = run(ctx, {"videos": args.videos})
    print(res.data["composed"])

if __name__ == "__main__":
    main()
