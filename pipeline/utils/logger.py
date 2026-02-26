"""
Logging utilities for the AutoSEO pipeline
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler


console = Console()


class PipelineLogger:
    """Logger with file and console output"""
    
    _instance: Optional['PipelineLogger'] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(
        self,
        name: str = "autoseo",
        level: str = "INFO",
        log_dir: str = "logs",
        file_prefix: str = "pipeline"
    ):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self._initialized = True
        self.name = name
        self.level = getattr(logging, level.upper(), logging.INFO)
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        
        self.logger.handlers.clear()
        
        console_handler = RichHandler(
            console=console,
            show_time=True,
            show_path=False,
            markup=True
        )
        console_handler.setLevel(self.level)
        console_formatter = logging.Formatter("%(message)s")
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_path / f"{file_prefix}_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(self.level)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        self.log_file = str(log_file)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def success(self, message: str):
        self.logger.info(f"[green]{message}[/green]")
    
    def stage(self, stage_name: str, message: str):
        self.logger.info(f"[bold blue][{stage_name}][/bold blue] {message}")


_logger: Optional[PipelineLogger] = None


def get_logger(
    level: str = "INFO",
    log_dir: str = "logs",
    file_prefix: str = "pipeline"
) -> PipelineLogger:
    """Get or create the singleton logger instance"""
    global _logger
    if _logger is None:
        _logger = PipelineLogger(level=level, log_dir=log_dir, file_prefix=file_prefix)
    return _logger
