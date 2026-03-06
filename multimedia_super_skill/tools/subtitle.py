from __future__ import annotations
from typing import List, Dict

def srt_from_lines(lines: List[str], seconds_per_line: int = 2) -> str:
    out = []
    t = 0
    for i, line in enumerate(lines, start=1):
        start = f"00:00:{t:02d},000"
        end = f"00:00:{t+seconds_per_line:02d},000"
        out += [str(i), f"{start} --> {end}", line, ""]
        t += seconds_per_line
    return "\n".join(out)

def safe_lines_from_script(script: str, max_lines: int = 8) -> List[str]:
    return [x.strip() for x in script.splitlines() if x.strip()][:max_lines]
