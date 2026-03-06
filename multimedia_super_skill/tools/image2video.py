from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess

@dataclass
class Image2Video:
    mode: str = "mock"         # mock | command | api
    command: str = "img2video"
    baseUrl: str = ""          # if mode=api
    timeout: int = 300

    def available(self) -> bool:
        return shutil.which(self.command) is not None

    def generate(self, img: Path, out: Path, seconds: int = 3, fps: int = 24) -> Path:
        out.parent.mkdir(parents=True, exist_ok=True)

        if self.mode == "mock":
            out.write_text(f"MOCK_IMAGE2VIDEO\nimg={img}\nseconds={seconds}\nfps={fps}", encoding="utf-8")
            return out

        if self.mode == "command":
            if not self.available():
                raise RuntimeError(f"img2video command not found: {self.command}")
            subprocess.run([self.command, "--in", str(img), "--out", str(out),
                            "--seconds", str(seconds), "--fps", str(fps)],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=self.timeout)
            return out

        if self.mode == "api":
            raise NotImplementedError("image2video api mode not implemented yet")

        raise ValueError(f"Unknown image2video mode: {self.mode}")
