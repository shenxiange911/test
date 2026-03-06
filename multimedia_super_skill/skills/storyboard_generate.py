from __future__ import annotations
import argparse
from pathlib import Path
from core.contracts import SkillResult, Artifact
from core.registry import register
from tools.storyboard_gen import StoryboardGen

@register("storyboard.generate")
def run(ctx, params):
    script = params["script"]
    refs = [Path(p) for p in params.get("refs", [])]
    cols = int(params.get("cols", 3))
    rows = int(params.get("rows", 2))
    subject_lock = params.get("subject_lock")
    style_lock = params.get("style_lock")

    cfg = ctx["config"].get("tools", {}).get("storyboard_gen", {})
    gen = StoryboardGen(mode=cfg.get("mode", "mock"), baseUrl=cfg.get("baseUrl", ""))
    out = Path(ctx["dirs"].artifacts) / "storyboard_sheet.png"
    sheet = gen.generate_sheet(script, refs, out, cols=cols, rows=rows, subject_lock=subject_lock, style_lock=style_lock)
    return SkillResult(ok=True, artifacts=[Artifact(type="file", value=str(sheet), mime="image/png")],
                       data={"sheet": str(sheet)})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script-file", required=True)
    ap.add_argument("--refs", nargs="*", default=[])
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--rows", type=int, default=2)
    args = ap.parse_args()

    from core.io import make_workdirs
    from core.config import load_config
    project_root = Path(__file__).resolve().parents[1]
    ctx = {"dirs": make_workdirs("outputs"), "config": load_config(project_root)}
    script = Path(args.script_file).read_text(encoding="utf-8")
    res = run(ctx, {"script": script, "refs": args.refs, "cols": args.cols, "rows": args.rows})
    print(res.data["sheet"])

if __name__ == "__main__":
    main()
