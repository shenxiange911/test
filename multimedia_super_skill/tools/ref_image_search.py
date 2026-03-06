from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class RefImageSearch:
    mode: str = "mock"   # mock | api
    baseUrl: str = ""

    def search(self, query: str, out_dir: Path, k: int = 4) -> List[Path]:
        out_dir.mkdir(parents=True, exist_ok=True)
        if self.mode == "mock":
            refs = []
            for i in range(1, k+1):
                p = out_dir / f"ref_{i}.txt"
                p.write_text(f"MOCK_REF for query={query} #{i}", encoding="utf-8")
                refs.append(p)
            return refs
        if self.mode == "api":
            raise NotImplementedError("ref_image_search api mode not implemented yet")
        raise ValueError(f"Unknown ref_image_search mode: {self.mode}")
