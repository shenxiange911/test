"""
多媒体流水线核心模块

提供执行框架、状态管理和数据模型。
"""

from .models import (
    ProjectConfig,
    PhaseConfig,
    PhaseResult,
    Frame,
    VideoClip,
    ProjectState,
    PhaseStatus,
    MediaType
)

from .state import StateManager
from .executor import MultimediaExecutor

__all__ = [
    'ProjectConfig',
    'PhaseConfig',
    'PhaseResult',
    'Frame',
    'VideoClip',
    'ProjectState',
    'PhaseStatus',
    'MediaType',
    'StateManager',
    'MultimediaExecutor'
]
