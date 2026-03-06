"""
多媒体流水线状态管理

提供项目状态的持久化、加载、更新和查询功能。
支持断点续传和线程安全操作。
"""

import json
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from .models import ProjectState, PhaseResult, PhaseStatus, ProjectConfig


class StateManager:
    """
    项目状态管理器
    
    负责项目状态的持久化存储、加载和更新。
    支持断点续传和线程安全操作。
    
    Attributes:
        project_dir: 项目目录路径
        state_file: 状态文件路径
        state: 当前项目状态
        lock: 线程锁
    """
    
    def __init__(self, project_dir: str):
        """
        初始化状态管理器
        
        Args:
            project_dir: 项目目录路径
        """
        self.project_dir = Path(project_dir).expanduser()
        self.state_file = self.project_dir / "project.json"
        self.state: Optional[ProjectState] = None
        self.lock = threading.Lock()
    
    def load(self) -> ProjectState:
        """
        加载项目状态
        
        Returns:
            ProjectState: 项目状态对象
            
        Raises:
            FileNotFoundError: 状态文件不存在
            json.JSONDecodeError: 状态文件格式错误
        """
        with self.lock:
            if not self.state_file.exists():
                raise FileNotFoundError(f"状态文件不存在: {self.state_file}")
            
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.state = ProjectState.from_dict(data)
            return self.state
    
    def save(self) -> None:
        """
        保存项目状态
        
        注意：此方法不加锁，调用者需要确保线程安全
        
        Raises:
            ValueError: 状态对象未初始化
        """
        if self.state is None:
            raise ValueError("状态对象未初始化，无法保存")
        
        # 更新时间戳
        self.state.updated_at = datetime.now()
        
        # 确保目录存在
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存到文件
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state.to_dict(), f, indent=2, ensure_ascii=False)
    
    def create(self, config: ProjectConfig) -> ProjectState:
        """
        创建新项目状态
        
        Args:
            config: 项目配置
            
        Returns:
            ProjectState: 新创建的项目状态
        """
        with self.lock:
            self.state = ProjectState(
                project_config=config,
                phase_configs=[],
                phase_results=[],
                frames=[],
                clips=[],
                current_phase=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={}
            )
            self.save()
            return self.state
    
    def get_current_phase(self) -> Optional[str]:
        """
        获取当前执行的 Phase
        
        Returns:
            Optional[str]: Phase ID，如果没有则返回 None
        """
        if self.state is None:
            return None
        return self.state.current_phase
    
    def set_current_phase(self, phase_id: str) -> None:
        """
        设置当前执行的 Phase
        
        Args:
            phase_id: Phase ID
        """
        with self.lock:
            if self.state is None:
                raise ValueError("状态对象未初始化")
            self.state.current_phase = phase_id
            self.save()
    
    def mark_phase_complete(
        self,
        phase_id: str,
        outputs: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        标记 Phase 完成
        
        Args:
            phase_id: Phase ID
            outputs: 输出文件列表
            metadata: 额外的元数据
        """
        with self.lock:
            if self.state is None:
                raise ValueError("状态对象未初始化")
            
            # 查找现有结果
            result = self.state.get_phase_result(phase_id)
            
            if result:
                # 更新现有结果
                result.status = PhaseStatus.COMPLETED
                result.end_time = datetime.now()
                result.outputs = outputs
                if metadata:
                    result.metadata.update(metadata)
            else:
                # 创建新结果
                result = PhaseResult(
                    phase_id=phase_id,
                    status=PhaseStatus.COMPLETED,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    outputs=outputs,
                    error=None,
                    metadata=metadata or {}
                )
                self.state.phase_results.append(result)
            
            self.save()
    
    def mark_phase_failed(
        self,
        phase_id: str,
        error: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        标记 Phase 失败
        
        Args:
            phase_id: Phase ID
            error: 错误信息
            metadata: 额外的元数据
        """
        with self.lock:
            if self.state is None:
                raise ValueError("状态对象未初始化")
            
            # 查找现有结果
            result = self.state.get_phase_result(phase_id)
            
            if result:
                # 更新现有结果
                result.status = PhaseStatus.FAILED
                result.end_time = datetime.now()
                result.error = error
                if metadata:
                    result.metadata.update(metadata)
            else:
                # 创建新结果
                result = PhaseResult(
                    phase_id=phase_id,
                    status=PhaseStatus.FAILED,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    outputs=[],
                    error=error,
                    metadata=metadata or {}
                )
                self.state.phase_results.append(result)
            
            self.save()
    
    def can_skip_phase(self, phase_id: str) -> bool:
        """
        判断是否可以跳过 Phase
        
        如果 Phase 已经成功完成，则可以跳过。
        
        Args:
            phase_id: Phase ID
            
        Returns:
            bool: 是否可以跳过
        """
        if self.state is None:
            return False
        
        result = self.state.get_phase_result(phase_id)
        if result is None:
            return False
        
        return result.status == PhaseStatus.COMPLETED
    
    def reset_phase(self, phase_id: str) -> None:
        """
        重置 Phase 状态
        
        将 Phase 状态重置为 PENDING，允许重新执行。
        
        Args:
            phase_id: Phase ID
        """
        with self.lock:
            if self.state is None:
                raise ValueError("状态对象未初始化")
            
            # 移除该 Phase 的结果
            self.state.phase_results = [
                r for r in self.state.phase_results
                if r.phase_id != phase_id
            ]
            
            self.save()
    
    def get_phase_output(self, phase_id: str) -> Optional[List[str]]:
        """
        获取 Phase 的输出文件列表
        
        Args:
            phase_id: Phase ID
            
        Returns:
            Optional[List[str]]: 输出文件列表，如果 Phase 未完成则返回 None
        """
        if self.state is None:
            return None
        
        result = self.state.get_phase_result(phase_id)
        if result is None or result.status != PhaseStatus.COMPLETED:
            return None
        
        return result.outputs
    
    def get_phase_status(self, phase_id: str) -> Optional[PhaseStatus]:
        """
        获取 Phase 的状态
        
        Args:
            phase_id: Phase ID
            
        Returns:
            Optional[PhaseStatus]: Phase 状态，如果不存在则返回 None
        """
        if self.state is None:
            return None
        
        result = self.state.get_phase_result(phase_id)
        if result is None:
            return None
        
        return result.status
    
    def get_all_phases(self) -> List[PhaseResult]:
        """
        获取所有 Phase 的结果
        
        Returns:
            List[PhaseResult]: Phase 结果列表
        """
        if self.state is None:
            return []
        
        return self.state.phase_results.copy()
