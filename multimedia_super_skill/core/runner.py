from __future__ import annotations
from typing import Any, Dict
from core.contracts import SkillResult
from core.registry import SKILLS

def run_skill(name: str, ctx: Dict[str, Any], params: Dict[str, Any]) -> SkillResult:
    fn = SKILLS.get(name)
    if not fn:
        return SkillResult(ok=False, error=f"Skill not found: {name}")
    try:
        return fn(ctx, params)
    except Exception as e:
        return SkillResult(ok=False, error=f"{name} crashed: {e}")
