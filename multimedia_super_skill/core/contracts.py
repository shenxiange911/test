from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class Artifact:
    type: str            # file | text | json
    value: str           # filepath or text or json path
    mime: Optional[str] = None
    name: Optional[str] = None

@dataclass
class SkillResult:
    ok: bool
    artifacts: List[Artifact] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
