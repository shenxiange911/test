from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import shutil
import uuid
from typing import Any, Dict

@dataclass
class WorkDirs:
    root: Path
    run_id: str
    run_dir: Path
    inputs: Path
    cache: Path
    temp: Path
    artifacts: Path
    logs: Path

def make_workdirs(base: str = "outputs") -> WorkDirs:
    root = Path(base).resolve()
    root.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex[:12]
    run_dir = root / f"run_{run_id}"
    inputs = run_dir / "inputs"
    cache = run_dir / "cache"
    temp = run_dir / "temp"
    artifacts = run_dir / "artifacts"
    logs = run_dir / "logs"
    for p in [run_dir, inputs, cache, temp, artifacts, logs]:
        p.mkdir(parents=True, exist_ok=True)
    return WorkDirs(root, run_id, run_dir, inputs, cache, temp, artifacts, logs)

def write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def copy_into(src: str, dst_dir: Path) -> Path:
    srcp = Path(src).resolve()
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / srcp.name
    shutil.copy2(srcp, dst)
    return dst
