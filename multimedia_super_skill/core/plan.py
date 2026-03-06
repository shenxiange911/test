from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class Step:
    name: str
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Plan:
    steps: List[Step] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"steps": [{"name": s.name, "params": s.params} for s in self.steps]}
