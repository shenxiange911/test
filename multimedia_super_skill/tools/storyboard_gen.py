from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List
from PIL import Image, ImageDraw

@dataclass
class StoryboardGen:
    mode: str = "mock"   # mock | api
    baseUrl: str = ""

    def generate_sheet(self, script: str, refs: List[Path], out: Path, cols: int = 3, rows: int = 2,
                       subject_lock: str | None = None, style_lock: str | None = None) -> Path:
        out.parent.mkdir(parents=True, exist_ok=True)
        if self.mode == "mock":
            W, H = 1600, 900
            img = Image.new("RGB", (W, H), "white")
            d = ImageDraw.Draw(img)
            cell_w, cell_h = W // cols, H // rows
            idx = 1
            for r in range(rows):
                for c in range(cols):
                    x0, y0 = c * cell_w, r * cell_h
                    x1, y1 = x0 + cell_w, y0 + cell_h
                    d.rectangle([x0, y0, x1, y1], outline="black", width=4)
                    d.text((x0 + 20, y0 + 20), f"SCENE {idx}", fill="black")
                    idx += 1
            footer = f"MOCK storyboard | script_len={len(script)} | refs={len(refs)}"
            if subject_lock:
                footer += " | subject_lock=yes"
            if style_lock:
                footer += " | style_lock=yes"
            d.text((20, H-40), footer, fill="black")
            img.save(out)
            return out
        if self.mode == "api":
            raise NotImplementedError("storyboard_gen api mode not implemented yet")
        raise ValueError(f"Unknown storyboard_gen mode: {self.mode}")
