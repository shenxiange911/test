"""
多媒体流水线核心数据模型

包含项目配置、阶段配置、执行结果、帧数据、视频片段和项目状态等模型。
所有模型支持 to_dict() 和 from_dict() 序列化。
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class PhaseStatus(Enum):
    """阶段执行状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class MediaType(Enum):
    """媒体类型"""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


@dataclass
class ProjectConfig:
    """
    项目配置模型
    
    Attributes:
        project_name: 项目名称
        output_dir: 输出目录路径
        theme: 项目主题/题材
        style: 视觉风格描述
        duration: 目标时长（秒）
        aspect_ratio: 画面比例 (16:9, 21:9, 9:16 等)
        language: 语言代码 (zh-CN, en-US 等)
        metadata: 额外元数据
    """
    project_name: str
    output_dir: str
    theme: str
    style: str = "cinematic"
    duration: int = 60
    aspect_ratio: str = "16:9"
    language: str = "zh-CN"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """数据验证"""
        if not self.project_name:
            raise ValueError("project_name 不能为空")
        if not self.output_dir:
            raise ValueError("output_dir 不能为空")
        if self.duration <= 0:
            raise ValueError("duration 必须大于 0")
        
        valid_ratios = ["16:9", "21:9", "9:16", "4:3", "1:1"]
        if self.aspect_ratio not in valid_ratios:
            raise ValueError(f"aspect_ratio 必须是 {valid_ratios} 之一")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectConfig':
        """从字典创建实例"""
        return cls(**data)


@dataclass
class PhaseConfig:
    """
    阶段配置模型
    
    Attributes:
        phase_id: 阶段标识 (01-research, 02-reference 等)
        phase_name: 阶段名称
        enabled: 是否启用
        auto_execute: 是否自动执行
        dependencies: 依赖的阶段列表
        params: 阶段特定参数
        timeout: 超时时间（秒）
    """
    phase_id: str
    phase_name: str
    enabled: bool = True
    auto_execute: bool = False
    dependencies: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 3600
    
    def __post_init__(self):
        """数据验证"""
        if not self.phase_id:
            raise ValueError("phase_id 不能为空")
        if not self.phase_name:
            raise ValueError("phase_name 不能为空")
        if self.timeout <= 0:
            raise ValueError("timeout 必须大于 0")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PhaseConfig':
        """从字典创建实例"""
        return cls(**data)


@dataclass
class PhaseResult:
    """
    阶段执行结果模型
    
    Attributes:
        phase_id: 阶段标识
        status: 执行状态
        start_time: 开始时间
        end_time: 结束时间
        duration: 执行时长（秒）
        outputs: 输出文件路径列表
        metadata: 结果元数据（API URLs, 模型信息等）
        error: 错误信息（如果失败）
    """
    phase_id: str
    status: PhaseStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: float = 0.0
    outputs: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    
    def __post_init__(self):
        """数据验证和计算"""
        if not self.phase_id:
            raise ValueError("phase_id 不能为空")
        
        # 计算时长
        if self.start_time and self.end_time:
            self.duration = (self.end_time - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        # 转换枚举和日期时间
        data['status'] = self.status.value
        if self.start_time:
            data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PhaseResult':
        """从字典创建实例"""
        # 转换枚举和日期时间
        if 'status' in data:
            data['status'] = PhaseStatus(data['status'])
        if 'start_time' in data and data['start_time']:
            data['start_time'] = datetime.fromisoformat(data['start_time'])
        if 'end_time' in data and data['end_time']:
            data['end_time'] = datetime.fromisoformat(data['end_time'])
        return cls(**data)


@dataclass
class Frame:
    """
    分镜帧数据模型
    
    Attributes:
        frame_id: 帧编号
        image_path: 图片路径
        prompt: 生成提示词
        duration: 持续时长（秒）
        camera_movement: 运镜描述
        narration: 旁白文本
        media_type: 媒体类型（图片/视频）
        video_path: 视频路径（如果已生成）
        metadata: 额外元数据
    """
    frame_id: int
    image_path: str
    prompt: str
    duration: float = 3.0
    camera_movement: str = "static"
    narration: str = ""
    media_type: MediaType = MediaType.IMAGE
    video_path: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """数据验证"""
        if self.frame_id < 0:
            raise ValueError("frame_id 必须 >= 0")
        if not self.image_path:
            raise ValueError("image_path 不能为空")
        if self.duration <= 0:
            raise ValueError("duration 必须大于 0")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['media_type'] = self.media_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Frame':
        """从字典创建实例"""
        if 'media_type' in data:
            data['media_type'] = MediaType(data['media_type'])
        return cls(**data)


@dataclass
class VideoClip:
    """
    视频片段模型
    
    Attributes:
        clip_id: 片段编号
        video_path: 视频文件路径
        start_time: 开始时间（秒）
        end_time: 结束时间（秒）
        duration: 持续时长（秒）
        frame_ids: 关联的帧编号列表
        audio_path: 音频路径
        subtitle_path: 字幕路径
        effects: 特效列表
        metadata: 额外元数据
    """
    clip_id: int
    video_path: str
    start_time: float
    end_time: float
    duration: float
    frame_ids: List[int] = field(default_factory=list)
    audio_path: Optional[str] = None
    subtitle_path: Optional[str] = None
    effects: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """数据验证"""
        if self.clip_id < 0:
            raise ValueError("clip_id 必须 >= 0")
        if not self.video_path:
            raise ValueError("video_path 不能为空")
        if self.start_time < 0:
            raise ValueError("start_time 必须 >= 0")
        if self.end_time <= self.start_time:
            raise ValueError("end_time 必须大于 start_time")
        if self.duration <= 0:
            raise ValueError("duration 必须大于 0")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VideoClip':
        """从字典创建实例"""
        return cls(**data)


@dataclass
class ProjectState:
    """
    项目状态模型
    
    Attributes:
        project_config: 项目配置
        phase_configs: 阶段配置列表
        phase_results: 阶段执行结果列表
        frames: 分镜帧列表
        clips: 视频片段列表
        current_phase: 当前执行阶段
        created_at: 创建时间
        updated_at: 更新时间
        metadata: 项目级元数据
    """
    project_config: ProjectConfig
    phase_configs: List[PhaseConfig] = field(default_factory=list)
    phase_results: List[PhaseResult] = field(default_factory=list)
    frames: List[Frame] = field(default_factory=list)
    clips: List[VideoClip] = field(default_factory=list)
    current_phase: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_phase_config(self, phase_id: str) -> Optional[PhaseConfig]:
        """获取指定阶段的配置"""
        for config in self.phase_configs:
            if config.phase_id == phase_id:
                return config
        return None
    
    def get_phase_result(self, phase_id: str) -> Optional[PhaseResult]:
        """获取指定阶段的执行结果"""
        for result in self.phase_results:
            if result.phase_id == phase_id:
                return result
        return None
    
    def get_frame(self, frame_id: int) -> Optional[Frame]:
        """获取指定编号的帧"""
        for frame in self.frames:
            if frame.frame_id == frame_id:
                return frame
        return None
    
    def get_clip(self, clip_id: int) -> Optional[VideoClip]:
        """获取指定编号的片段"""
        for clip in self.clips:
            if clip.clip_id == clip_id:
                return clip
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'project_config': self.project_config.to_dict(),
            'phase_configs': [pc.to_dict() for pc in self.phase_configs],
            'phase_results': [pr.to_dict() for pr in self.phase_results],
            'frames': [f.to_dict() for f in self.frames],
            'clips': [c.to_dict() for c in self.clips],
            'current_phase': self.current_phase,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectState':
        """从字典创建实例"""
        return cls(
            project_config=ProjectConfig.from_dict(data['project_config']),
            phase_configs=[PhaseConfig.from_dict(pc) for pc in data.get('phase_configs', [])],
            phase_results=[PhaseResult.from_dict(pr) for pr in data.get('phase_results', [])],
            frames=[Frame.from_dict(f) for f in data.get('frames', [])],
            clips=[VideoClip.from_dict(c) for c in data.get('clips', [])],
            current_phase=data.get('current_phase'),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            metadata=data.get('metadata', {})
        )
