from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess

@dataclass
class FFmpeg:
    mode: str = "auto"  # auto | mock
    def available(self) -> bool:
        return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

    @property
    def mock(self) -> bool:
        return self.mode == "mock" or (self.mode == "auto" and not self.available())

    def _run(self, cmd: list[str]) -> None:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def concat_videos(self, videos: list[Path], out: Path) -> Path:
        out.parent.mkdir(parents=True, exist_ok=True)
        if self.mock:
            out.write_text("MOCK_CONCAT\n" + "\n".join([str(v) for v in videos]), encoding="utf-8")
            return out
        lst = out.parent / "concat_list.txt"
        lst.write_text("\n".join([f"file '{v.as_posix()}'" for v in videos]), encoding="utf-8")
        self._run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)])
        return out

    def add_audio(self, video: Path, audio: Path, out: Path) -> Path:
        out.parent.mkdir(parents=True, exist_ok=True)
        if self.mock:
            out.write_text(f"MOCK_ADD_AUDIO\nvideo={video}\naudio={audio}", encoding="utf-8")
            return out
        self._run(["ffmpeg", "-y", "-i", str(video), "-i", str(audio),
                   "-c:v", "copy", "-c:a", "aac", "-shortest", str(out)])
        return out

    def burn_subtitles(self, video: Path, srt: Path, out: Path) -> Path:
        out.parent.mkdir(parents=True, exist_ok=True)
        if self.mock:
            out.write_text(f"MOCK_BURN_SUBS\nvideo={video}\nsrt={srt}", encoding="utf-8")
            return out
        self._run(["ffmpeg", "-y", "-i", str(video), "-vf", f"subtitles={srt}", str(out)])
        return out
