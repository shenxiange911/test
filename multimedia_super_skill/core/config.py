from __future__ import annotations
from pathlib import Path
import json
import os
from typing import Any, Dict

def load_config(project_root: Path) -> Dict[str, Any]:
    # Priority: env JSON -> config/api.json -> config/api.example.json
    env_json = os.environ.get("MSS_CONFIG_JSON")
    if env_json:
        return json.loads(env_json)

    cfg = project_root / "config" / "api.json"
    if cfg.exists():
        return json.loads(cfg.read_text(encoding="utf-8"))

    example = project_root / "config" / "api.example.json"
    if example.exists():
        return json.loads(example.read_text(encoding="utf-8"))

    return {}
