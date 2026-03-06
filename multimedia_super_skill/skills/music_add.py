from __future__ import annotations
import argparse
from pathlib import Path
from core.contracts import SkillResult, Artifact
from core.registry import register

@register("music.add")
def run(ctx, params):
    out_dir = Path(ctx["dirs"].artifacts) / "audio"
    out_dir.mkdir(parents=True, exist_ok=True)
    music = out_dir / "bgm.aac"
    music.write_text("MOCK_BGM", encoding="utf-8")
    return SkillResult(ok=True, artifacts=[Artifact(type="file", value=str(music), mime="audio/aac")],
                       data={"music": str(music)})

def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    from core.io import make_workdirs
    ctx = {"dirs": make_workdirs("outputs")}
    res = run(ctx, {})
    print(res.data["music"])

if __name__ == "__main__":
    main()
