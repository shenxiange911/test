from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image
from core.contracts import SkillResult, Artifact
from core.registry import register

@register("storyboard.split")
def run(ctx, params):
    sheet = Path(params["sheet"])
    cols = int(params.get("cols", 3))
    rows = int(params.get("rows", 2))
    out_dir = Path(ctx["dirs"].artifacts) / "scenes"
    out_dir.mkdir(parents=True, exist_ok=True)

    img = Image.open(sheet)
    W, H = img.size
    cw, ch = W // cols, H // rows

    scenes = []
    idx = 1
    for r in range(rows):
        for c in range(cols):
            crop = img.crop((c*cw, r*ch, (c+1)*cw, (r+1)*ch))
            out = out_dir / f"scene_{idx:02d}.png"
            crop.save(out)
            scenes.append(out)
            idx += 1

    return SkillResult(ok=True,
                       artifacts=[Artifact(type="file", value=str(p), mime="image/png") for p in scenes],
                       data={"scenes": [str(p) for p in scenes]})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--rows", type=int, default=2)
    args = ap.parse_args()
    from core.io import make_workdirs
    ctx = {"dirs": make_workdirs("outputs")}
    res = run(ctx, {"sheet": args.sheet, "cols": args.cols, "rows": args.rows})
    print("\n".join(res.data["scenes"]))

if __name__ == "__main__":
    main()
