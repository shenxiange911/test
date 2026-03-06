from __future__ import annotations
import argparse
from pathlib import Path
from core.contracts import SkillResult, Artifact
from core.registry import register
from tools.banana2 import Banana2

@register("image.repair_upscale")
def run(ctx, params):
    inp = Path(params["image"])
    scale = int(params.get("scale", 2))
    out_dir = Path(ctx["dirs"].artifacts) / "scenes_fixed"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / inp.name.replace(".png", f"_x{scale}.png")

    cfg = ctx["config"].get("tools", {}).get("banana2", {})
    tool = Banana2(mode=cfg.get("mode","mock"), command=cfg.get("command","banana2"), baseUrl=cfg.get("baseUrl",""))
    fixed = tool.repair_upscale(inp, out, scale=scale)

    return SkillResult(ok=True, artifacts=[Artifact(type="file", value=str(fixed), mime="image/png")],
                       data={"fixed": str(fixed)})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--scale", type=int, default=2)
    args = ap.parse_args()
    from core.io import make_workdirs
    from core.config import load_config
    project_root = Path(__file__).resolve().parents[1]
    ctx = {"dirs": make_workdirs("outputs"), "config": load_config(project_root)}
    res = run(ctx, {"image": args.image, "scale": args.scale})
    print(res.data["fixed"])

if __name__ == "__main__":
    main()
