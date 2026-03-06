from __future__ import annotations
import argparse
from pathlib import Path
from core.contracts import SkillResult, Artifact
from core.registry import register
from tools.ref_image_search import RefImageSearch

@register("ref.collect")
def run(ctx, params):
    query = params["query"]
    k = int(params.get("k", 4))
    cfg = ctx["config"].get("tools", {}).get("ref_image_search", {})
    tool = RefImageSearch(mode=cfg.get("mode", "mock"), baseUrl=cfg.get("baseUrl", ""))
    out_dir = Path(ctx["dirs"].artifacts) / "refs"
    refs = tool.search(query, out_dir, k=k)
    return SkillResult(ok=True,
                       artifacts=[Artifact(type="file", value=str(p)) for p in refs],
                       data={"refs": [str(p) for p in refs]})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--k", type=int, default=4)
    args = ap.parse_args()
    from core.io import make_workdirs
    from core.config import load_config
    project_root = Path(__file__).resolve().parents[1]
    ctx = {"dirs": make_workdirs("outputs"), "config": load_config(project_root)}
    res = run(ctx, {"query": args.query, "k": args.k})
    print("\n".join(res.data["refs"]))

if __name__ == "__main__":
    main()
