"""
多媒体流水线执行器

提供统一的执行入口，负责项目创建、阶段执行、流水线运行和错误处理。
支持断点续传、输入验证和完整的日志系统。
"""

import logging
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from .models import (
    ProjectConfig, PhaseConfig, PhaseResult, PhaseStatus,
    ProjectState, MediaType
)
from .state import StateManager


class MultimediaExecutor:
    """
    多媒体流水线执行器
    
    负责整个流水线的执行控制，包括：
    - 项目创建和初始化
    - 单个阶段的执行
    - 完整流水线的运行
    - 输入验证和错误处理
    - 日志记录和状态管理
    
    Attributes:
        project_dir: 项目目录路径
        state_manager: 状态管理器
        logger: 日志记录器
        skill_root: Skill 根目录
    """
    
    def __init__(self, project_dir: str, log_level: int = logging.INFO):
        """
        初始化执行器
        
        Args:
            project_dir: 项目目录路径
            log_level: 日志级别 (默认 INFO)
        """
        self.project_dir = Path(project_dir).expanduser()
        self.state_manager = StateManager(str(self.project_dir))
        self.skill_root = Path(__file__).parent.parent
        
        # 配置日志
        self.logger = self._setup_logger(log_level)
    
    def _setup_logger(self, log_level: int) -> logging.Logger:
        """
        配置日志系统
        
        Args:
            log_level: 日志级别
            
        Returns:
            logging.Logger: 配置好的日志记录器
        """
        logger = logging.getLogger(f"MultimediaExecutor.{self.project_dir.name}")
        logger.setLevel(log_level)
        
        # 避免重复添加 handler
        if logger.handlers:
            return logger
        
        # 控制台输出
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # 文件输出
        log_dir = self.project_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"executor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(funcName)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def create_project(
        self,
        project_name: str,
        theme: str,
        style: str = "cinematic",
        duration: int = 60,
        aspect_ratio: str = "16:9",
        language: str = "zh-CN",
        phases: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ProjectState:
        """
        创建新项目
        
        Args:
            project_name: 项目名称
            theme: 项目主题/题材
            style: 视觉风格 (默认 "cinematic")
            duration: 目标时长（秒，默认 60）
            aspect_ratio: 画面比例 (默认 "16:9")
            language: 语言代码 (默认 "zh-CN")
            phases: 要执行的阶段列表 (默认全部 6 个阶段)
            metadata: 额外元数据
            
        Returns:
            ProjectState: 初始化的项目状态
            
        Raises:
            ValueError: 参数验证失败
            FileExistsError: 项目已存在
        """
        self.logger.info(f"创建项目: {project_name}")
        
        # 检查项目是否已存在
        if self.state_manager.state_file.exists():
            raise FileExistsError(f"项目已存在: {self.project_dir}")
        
        # 创建项目配置
        project_config = ProjectConfig(
            project_name=project_name,
            output_dir=str(self.project_dir),
            theme=theme,
            style=style,
            duration=duration,
            aspect_ratio=aspect_ratio,
            language=language,
            metadata=metadata or {}
        )
        
        # 默认阶段列表
        if phases is None:
            phases = ["01-research", "02-reference", "03-storyboard", 
                     "04-split", "05-video", "06-edit"]
        
        # 创建阶段配置
        phase_configs = []
        for phase_id in phases:
            phase_config = PhaseConfig(
                phase_id=phase_id,
                phase_name=self._get_phase_name(phase_id),
                enabled=True,
                auto_execute=False,
                dependencies=self._get_phase_dependencies(phase_id),
                params={},
                timeout=3600
            )
            phase_configs.append(phase_config)
        
        # 创建项目状态
        state = ProjectState(
            project_config=project_config,
            phase_configs=phase_configs
        )
        
        # 保存状态
        self.state_manager.state = state
        self.state_manager.save()
        
        self.logger.info(f"项目创建成功: {self.project_dir}")
        return state
    
    def _get_phase_name(self, phase_id: str) -> str:
        """获取阶段名称"""
        phase_names = {
            "01-research": "深度搜索+剧本生成",
            "02-reference": "角色/产品参考图",
            "03-storyboard": "整张分镜图生成",
            "04-split": "分镜拆分+放大",
            "05-video": "视频生成",
            "06-edit": "剪辑+配音+字幕"
        }
        return phase_names.get(phase_id, phase_id)
    
    def _get_phase_dependencies(self, phase_id: str) -> List[str]:
        """获取阶段依赖"""
        dependencies = {
            "01-research": [],
            "02-reference": ["01-research"],
            "03-storyboard": ["01-research", "02-reference"],
            "04-split": ["03-storyboard"],
            "05-video": ["04-split"],
            "06-edit": ["05-video"]
        }
        return dependencies.get(phase_id, [])
    
    def validate_phase_input(self, phase_id: str) -> bool:
        """
        验证阶段输入是否满足要求
        
        检查依赖的阶段是否已完成，以及必需的输入文件是否存在。
        
        Args:
            phase_id: 阶段 ID
            
        Returns:
            bool: 输入是否有效
        """
        self.logger.debug(f"验证阶段输入: {phase_id}")
        
        # 加载状态
        try:
            state = self.state_manager.load()
        except FileNotFoundError:
            self.logger.error("项目状态文件不存在")
            return False
        
        # 获取阶段配置
        phase_config = state.get_phase_config(phase_id)
        if phase_config is None:
            self.logger.error(f"阶段配置不存在: {phase_id}")
            return False
        
        # 检查依赖阶段
        for dep_id in phase_config.dependencies:
            dep_result = state.get_phase_result(dep_id)
            if dep_result is None or dep_result.status != PhaseStatus.COMPLETED:
                self.logger.error(f"依赖阶段未完成: {dep_id}")
                return False
        
        # 特定阶段的输入验证
        if phase_id == "02-reference":
            # 需要 01-research 的剧本文件
            research_result = state.get_phase_result("01-research")
            if not research_result or not research_result.output_files:
                self.logger.error("缺少 01-research 的输出文件")
                return False
        
        elif phase_id == "03-storyboard":
            # 需要剧本和参考图
            research_result = state.get_phase_result("01-research")
            reference_result = state.get_phase_result("02-reference")
            if not research_result or not reference_result:
                self.logger.error("缺少 01-research 或 02-reference 的输出")
                return False
        
        elif phase_id == "04-split":
            # 需要整张分镜图
            storyboard_result = state.get_phase_result("03-storyboard")
            if not storyboard_result or not storyboard_result.output_files:
                self.logger.error("缺少 03-storyboard 的输出文件")
                return False
        
        elif phase_id == "05-video":
            # 需要拆分后的分镜图
            split_result = state.get_phase_result("04-split")
            if not split_result or not state.frames:
                self.logger.error("缺少 04-split 的分镜帧数据")
                return False
        
        elif phase_id == "06-edit":
            # 需要视频片段
            video_result = state.get_phase_result("05-video")
            if not video_result or not state.clips:
                self.logger.error("缺少 05-video 的视频片段数据")
                return False
        
        self.logger.debug(f"阶段输入验证通过: {phase_id}")
        return True
    
    def call_phase_script(
        self,
        phase_id: str,
        extra_args: Optional[List[str]] = None
    ) -> subprocess.CompletedProcess:
        """
        调用阶段脚本
        
        Args:
            phase_id: 阶段 ID
            extra_args: 额外的命令行参数
            
        Returns:
            subprocess.CompletedProcess: 执行结果
            
        Raises:
            FileNotFoundError: 脚本文件不存在
        """
        state = self.state_manager.load()
        phase_config = state.get_phase_config(phase_id)
        
        if phase_config is None:
            raise ValueError(f"阶段配置不存在: {phase_id}")
        
        script_path = Path(phase_config.script_path)
        if not script_path.exists():
            raise FileNotFoundError(f"脚本文件不存在: {script_path}")
        
        # 构建命令
        cmd = [sys.executable, str(script_path), str(self.project_dir)]
        if extra_args:
            cmd.extend(extra_args)
        
        self.logger.info(f"执行脚本: {' '.join(cmd)}")
        
        # 执行脚本
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=script_path.parent
        )
        
        # 记录输出
        if result.stdout:
            self.logger.debug(f"标准输出:\n{result.stdout}")
        if result.stderr:
            self.logger.warning(f"标准错误:\n{result.stderr}")
        
        return result
    
    def handle_phase_error(
        self,
        phase_id: str,
        error: Exception,
        result: Optional[subprocess.CompletedProcess] = None
    ) -> None:
        """
        处理阶段执行错误
        
        记录错误信息，更新状态，并尝试提供恢复建议。
        
        Args:
            phase_id: 阶段 ID
            error: 异常对象
            result: 子进程执行结果（如果有）
        """
        self.logger.error(f"阶段执行失败: {phase_id}")
        self.logger.error(f"错误类型: {type(error).__name__}")
        self.logger.error(f"错误信息: {str(error)}")
        
        # 记录子进程输出
        if result:
            self.logger.error(f"返回码: {result.returncode}")
            if result.stdout:
                self.logger.error(f"标准输出:\n{result.stdout}")
            if result.stderr:
                self.logger.error(f"标准错误:\n{result.stderr}")
        
        # 更新状态
        try:
            state = self.state_manager.load()
            phase_result = state.get_phase_result(phase_id)
            
            if phase_result:
                phase_result.status = PhaseStatus.FAILED
                phase_result.error_message = str(error)
                phase_result.end_time = datetime.now()
            else:
                # 创建失败记录
                phase_result = PhaseResult(
                    phase_id=phase_id,
                    status=PhaseStatus.FAILED,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    error_message=str(error)
                )
                state.phase_results.append(phase_result)
            
            self.state_manager.save()
        except Exception as e:
            self.logger.error(f"更新状态失败: {e}")
        
        # 提供恢复建议
        self._suggest_recovery(phase_id, error)
    
    def _suggest_recovery(self, phase_id: str, error: Exception) -> None:
        """提供错误恢复建议"""
        suggestions = []
        
        if isinstance(error, FileNotFoundError):
            suggestions.append("检查依赖阶段的输出文件是否存在")
            suggestions.append("尝试重新运行依赖阶段")
        
        elif isinstance(error, subprocess.CalledProcessError):
            suggestions.append("检查脚本的命令行参数是否正确")
            suggestions.append("查看脚本的日志文件获取详细错误信息")
        
        elif isinstance(error, ValueError):
            suggestions.append("检查输入参数的格式和取值范围")
            suggestions.append("查看项目配置文件是否正确")
        
        else:
            suggestions.append("查看日志文件获取详细错误信息")
            suggestions.append("尝试使用 --debug 参数重新运行")
        
        if suggestions:
            self.logger.info("恢复建议:")
            for i, suggestion in enumerate(suggestions, 1):
                self.logger.info(f"  {i}. {suggestion}")
    
    def run_phase(
        self,
        phase_id: str,
        skip_validation: bool = False,
        extra_args: Optional[List[str]] = None
    ) -> PhaseResult:
        """
        运行单个阶段
        
        Args:
            phase_id: 阶段 ID
            skip_validation: 是否跳过输入验证
            extra_args: 额外的命令行参数
            
        Returns:
            PhaseResult: 阶段执行结果
            
        Raises:
            ValueError: 输入验证失败或阶段配置不存在
            RuntimeError: 脚本执行失败
        """
        self.logger.info(f"开始执行阶段: {phase_id}")
        
        # 加载状态
        state = self.state_manager.load()
        phase_config = state.get_phase_config(phase_id)
        
        if phase_config is None:
            raise ValueError(f"阶段配置不存在: {phase_id}")
        
        if not phase_config.enabled:
            self.logger.info(f"阶段已禁用，跳过: {phase_id}")
            phase_result = PhaseResult(
                phase_id=phase_id,
                status=PhaseStatus.SKIPPED,
                start_time=datetime.now(),
                end_time=datetime.now()
            )
            state.phase_results.append(phase_result)
            self.state_manager.save()
            return phase_result
        
        # 验证输入
        if not skip_validation and not self.validate_phase_input(phase_id):
            raise ValueError(f"阶段输入验证失败: {phase_id}")
        
        # 创建或更新阶段结果
        phase_result = state.get_phase_result(phase_id)
        if phase_result is None:
            phase_result = PhaseResult(
                phase_id=phase_id,
                status=PhaseStatus.RUNNING,
                start_time=datetime.now()
            )
            state.phase_results.append(phase_result)
        else:
            phase_result.status = PhaseStatus.RUNNING
            phase_result.start_time = datetime.now()
            phase_result.error_message = None
        
        state.current_phase = phase_id
        self.state_manager.save()
        
        # 执行脚本
        try:
            result = self.call_phase_script(phase_id, extra_args)
            
            if result.returncode != 0:
                error = RuntimeError(f"脚本返回非零退出码: {result.returncode}")
                self.handle_phase_error(phase_id, error, result)
                raise error
            
            # 更新成功状态
            phase_result.status = PhaseStatus.COMPLETED
            phase_result.end_time = datetime.now()
            
            # 重新加载状态以获取脚本写入的输出文件
            state = self.state_manager.load()
            phase_result = state.get_phase_result(phase_id)
            
            self.state_manager.save()
            self.logger.info(f"阶段执行成功: {phase_id}")
            
            return phase_result
        
        except Exception as e:
            self.handle_phase_error(phase_id, e)
            raise
    
    def run_pipeline(
        self,
        start_phase: Optional[str] = None,
        end_phase: Optional[str] = None,
        skip_validation: bool = False
    ) -> List[PhaseResult]:
        """
        运行完整流水线
        
        按顺序执行所有启用的阶段，支持断点续传。
        
        Args:
            start_phase: 起始阶段 ID（默认从第一个阶段开始）
            end_phase: 结束阶段 ID（默认执行到最后一个阶段）
            skip_validation: 是否跳过输入验证
            
        Returns:
            List[PhaseResult]: 所有阶段的执行结果
            
        Raises:
            ValueError: 阶段 ID 不存在
            RuntimeError: 阶段执行失败
        """
        self.logger.info("开始执行流水线")
        
        # 加载状态
        state = self.state_manager.load()
        
        # 确定执行范围
        phase_ids = [pc.phase_id for pc in state.phase_configs if pc.enabled]
        
        if start_phase:
            if start_phase not in phase_ids:
                raise ValueError(f"起始阶段不存在: {start_phase}")
            start_idx = phase_ids.index(start_phase)
            phase_ids = phase_ids[start_idx:]
        
        if end_phase:
            if end_phase not in phase_ids:
                raise ValueError(f"结束阶段不存在: {end_phase}")
            end_idx = phase_ids.index(end_phase)
            phase_ids = phase_ids[:end_idx + 1]
        
        self.logger.info(f"执行阶段: {' -> '.join(phase_ids)}")
        
        # 执行阶段
        results = []
        for phase_id in phase_ids:
            try:
                result = self.run_phase(phase_id, skip_validation)
                results.append(result)
                
                if result.status == PhaseStatus.FAILED:
                    self.logger.error(f"流水线中断: {phase_id} 执行失败")
                    break
            
            except Exception as e:
                self.logger.error(f"流水线执行失败: {e}")
                raise
        
        self.logger.info("流水线执行完成")
        return results
