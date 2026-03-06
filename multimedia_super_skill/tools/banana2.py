from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess

@dataclass
class Banana2:
    mode: str = "mock"         # mock | command | api
    command: str = "banana2"
    baseUrl: str = ""          # if mode=api
    timeout: int = 120

    def available(self) -> bool:
        return shutil.which(self.command) is not None

    def repair_upscale(self, img: Path, out: Path, scale: int = 2) -> Path:
        out.parent.mkdir(parents=True, exist_ok=True)

        if self.mode == "mock":
            out.write_bytes(img.read_bytes())
            return out

        if self.mode == "command":
            if not self.available():
                raise RuntimeError(f"banana2 command not found: {self.command}")
            subprocess.run([self.command, "--in", str(img), "--out", str(out), "--scale", str(scale)],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=self.timeout)
            return out

        if self.mode == "api":
            # Placeholder: implement your own API here using tools.http.HttpClient
            raise NotImplementedError("banana2 api mode not implemented yet")

        raise ValueError(f"Unknown banana2 mode: {self.mode}")
