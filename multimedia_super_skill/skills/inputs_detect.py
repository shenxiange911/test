from __future__ import annotations
import argparse
from core.contracts import SkillResult, Artifact
from core.registry import register
from core.input_resolver import resolve_inputs

@register("inputs.detect")
def run(ctx, params):
    text = params.get("text", "")
    also = params.get("also_inputs", [])
    download = bool(params.get("download_remote", True))
    dirs = ctx["dirs"]

    resolved = resolve_inputs(text, dirs.inputs, also_inputs=also, download_remote=download)
    data = {"inputs": [r.__dict__ for r in resolved]}
    return SkillResult(ok=True, artifacts=[Artifact(type="json", value=str(dirs.artifacts / "resolved_inputs.json"))], data=data)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default="")
    ap.add_argument("--input", action="append", default=[])
    ap.add_argument("--no-download", action="store_true")
    args = ap.parse_args()

    from core.io import make_workdirs, write_json
    dirs = make_workdirs("outputs")
    ctx = {"dirs": dirs}
    res = run(ctx, {"text": args.text, "also_inputs": args.input, "download_remote": (not args.no_download)})
    write_json(dirs.artifacts / "resolved_inputs.json", res.data)
    print(dirs.artifacts / "resolved_inputs.json")

if __name__ == "__main__":
    main()
