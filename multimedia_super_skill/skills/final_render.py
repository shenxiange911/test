from __future__ import annotations
import argparse
from pathlib import Path
from core.contracts import SkillResult, Artifact
from core.registry import register
from tools.ffmpeg import FFmpeg

@register("final.render")
def run(ctx, params):
    video = Path(params["video"])
    music = Path(params["music"])
    voice = Path(params["voice"])
    srt = Path(params["srt"])

    cfg = ctx["config"].get("tools", {}).get("ffmpeg", {})
    ff = FFmpeg(mode=cfg.get("mode","auto"))
    out_dir = Path(ctx["dirs"].artifacts) / "final"
    out_dir.mkdir(parents=True, exist_ok=True)

    with_audio = out_dir / "with_voice.mp4"
    ff.add_audio(video, voice, with_audio)

    final = out_dir / "final.mp4"
    ff.burn_subtitles(with_audio, srt, final)
    return SkillResult(ok=True, artifacts=[Artifact(type="file", value=str(final), mime="video/mp4")],
                       data={"final": str(final)})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--music", required=True)
    ap.add_argument("--voice", required=True)
    ap.add_argument("--srt", required=True)
    args = ap.parse_args()

    from core.io import make_workdirs
    from core.config import load_config
    project_root = Path(__file__).resolve().parents[1]
    ctx = {"dirs": make_workdirs("outputs"), "config": load_config(project_root)}
    res = run(ctx, {"video": args.video, "music": args.music, "voice": args.voice, "srt": args.srt})
    print(res.data["final"])

if __name__ == "__main__":
    main()
