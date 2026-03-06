from __future__ import annotations
from typing import Callable, Dict

SKILLS: Dict[str, Callable] = {}

def register(name: str):
    def deco(fn: Callable):
        SKILLS[name] = fn
        return fn
    return deco
