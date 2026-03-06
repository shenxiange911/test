from __future__ import annotations
import argparse
from pathlib import Path
from core.contracts import SkillResult, Artifact
from core.registry import register

@register("voice.generate")
def run(ctx, params):
    script = params["script"]
    out_dir = Path(ctx["dirs"].artifacts) / "audio"
    out_dir.mkdir(parents=True, exist_ok=True)
    voice = out_dir / "voice.aac"
    voice.write_text("MOCK_TTS\n" + script, encoding="utf-8")
    return SkillResult(ok=True, artifacts=[Artifact(type="file", value=str(voice), mime="audio/aac")],
                       data={"voice": str(voice)})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script-file", required=True)
    args = ap.parse_args()
    script = Path(args.script_file).read_text(encoding="utf-8")
    from core.io import make_workdirs
    ctx = {"dirs": make_workdirs("outputs")}
    res = run(ctx, {"script": script})
    print(res.data["voice"])

if __name__ == "__main__":
    main()
