from __future__ import annotations
import argparse
from pathlib import Path
from core.contracts import SkillResult, Artifact
from core.registry import register
from tools.subtitle import srt_from_lines, safe_lines_from_script

@register("subtitle.generate")
def run(ctx, params):
    script = params["script"]
    lines = safe_lines_from_script(script, max_lines=int(params.get("max_lines", 8)))
    srt_text = srt_from_lines(lines, seconds_per_line=int(params.get("seconds_per_line", 2)))
    out_dir = Path(ctx["dirs"].artifacts) / "subs"
    out_dir.mkdir(parents=True, exist_ok=True)
    srt = out_dir / "subtitles.srt"
    srt.write_text(srt_text, encoding="utf-8")
    return SkillResult(ok=True, artifacts=[Artifact(type="file", value=str(srt), mime="text/srt")],
                       data={"srt": str(srt)})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script-file", required=True)
    args = ap.parse_args()
    script = Path(args.script_file).read_text(encoding="utf-8")
    from core.io import make_workdirs
    ctx = {"dirs": make_workdirs("outputs")}
    res = run(ctx, {"script": script})
    print(res.data["srt"])

if __name__ == "__main__":
    main()
