from __future__ import annotations
import argparse
from pathlib import Path
from core.contracts import SkillResult, Artifact
from core.registry import register
from tools.image2video import Image2Video

@register("scene.image2video")
def run(ctx, params):
    img = Path(params["image"])
    seconds = int(params.get("seconds", 3))
    fps = int(params.get("fps", 24))
    out_dir = Path(ctx["dirs"].artifacts) / "scene_videos"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / img.name.replace(".png", ".mp4")

    cfg = ctx["config"].get("tools", {}).get("image2video", {})
    tool = Image2Video(mode=cfg.get("mode","mock"), command=cfg.get("command","img2video"), baseUrl=cfg.get("baseUrl",""))
    vid = tool.generate(img, out, seconds=seconds, fps=fps)

    return SkillResult(ok=True, artifacts=[Artifact(type="file", value=str(vid), mime="video/mp4")],
                       data={"video": str(vid)})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--seconds", type=int, default=3)
    ap.add_argument("--fps", type=int, default=24)
    args = ap.parse_args()
    from core.io import make_workdirs
    from core.config import load_config
    project_root = Path(__file__).resolve().parents[1]
    ctx = {"dirs": make_workdirs("outputs"), "config": load_config(project_root)}
    res = run(ctx, {"image": args.image, "seconds": args.seconds, "fps": args.fps})
    print(res.data["video"])

if __name__ == "__main__":
    main()
