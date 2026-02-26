"""
Configuration management for the AutoSEO pipeline
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class Config:
    """Configuration manager with YAML support"""
    
    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self._initialized = True
        self._config = {}
        self._config_path = None
    
    def load(self, config_path: Optional[str] = None) -> 'Config':
        """Load configuration from YAML file"""
        if config_path is None:
            config_path = self._find_config_file()
        
        if config_path is None:
            raise FileNotFoundError("No config.yaml found")
        
        self._config_path = config_path
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f) or {}
        
        self._resolve_paths()
        return self
    
    def _find_config_file(self) -> Optional[str]:
        """Find config.yaml in current or parent directories"""
        candidates = [
            'config.yaml',
            'config.yml',
            '../config.yaml',
            '../../config.yaml',
        ]
        
        for candidate in candidates:
            if os.path.exists(candidate):
                return os.path.abspath(candidate)
        
        return None
    
    def _resolve_paths(self):
        """Resolve relative paths to absolute paths"""
        base_dir = Path(self._config_path).parent if self._config_path else Path.cwd()
        
        path_fields = [
            ('input', 'directory'),
            ('input', 'processed_directory'),
            ('input', 'cache_directory'),
            ('output', 'seo_json_path'),
            ('output', 'backup_directory'),
            ('logging', 'directory'),
        ]
        
        for field_path in path_fields:
            try:
                current = self._config
                for key in field_path[:-1]:
                    current = current[key]
                
                last_key = field_path[-1]
                if last_key in current:
                    path_value = current[last_key]
                    if not os.path.isabs(path_value):
                        current[last_key] = str(base_dir / path_value)
            except (KeyError, TypeError):
                pass
    
    def get(self, *keys, default: Any = None) -> Any:
        """Get configuration value by dotted path"""
        current = self._config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    def __getitem__(self, key: str) -> Any:
        return self._config.get(key)
    
    @property
    def input_dir(self) -> str:
        return self.get('input', 'directory', default='data/input')
    
    @property
    def processed_dir(self) -> str:
        return self.get('input', 'processed_directory', default='data/processed')
    
    @property
    def cache_dir(self) -> str:
        return self.get('input', 'cache_directory', default='data/cache')
    
    @property
    def seo_json_path(self) -> str:
        return self.get('output', 'seo_json_path', default='sites/salamtalk/src/data/seo.json')
    
    @property
    def llm_endpoint(self) -> str:
        return self.get('llm', 'endpoint', default='')
    
    @property
    def site_name(self) -> str:
        return self.get('output', 'site', default='salamtalk')
    
    @property
    def required_columns(self) -> list:
        return self.get('input', 'required_columns', default=[])
    
    @property
    def batch_size(self) -> int:
        return self.get('llm', 'batch_size', default=30)
    
    @property
    def max_retries(self) -> int:
        return self.get('llm', 'max_retries', default=3)
    
    @property
    def timeout(self) -> int:
        return self.get('llm', 'timeout', default=120)
    
    @property
    def auto_commit(self) -> bool:
        return self.get('git', 'auto_commit', default=True)
    
    @property
    def auto_push(self) -> bool:
        return self.get('git', 'auto_push', default=True)
    
    @property
    def git_branch(self) -> str:
        return self.get('git', 'branch', default='main')
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary"""
        return self._config.copy()


_config: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get or create the singleton config instance"""
    global _config
    if _config is None:
        _config = Config()
        if config_path or _config._find_config_file():
            _config.load(config_path)
    return _config


def reload_config(config_path: Optional[str] = None) -> Config:
    """Force reload configuration"""
    global _config
    _config = Config()
    _config.load(config_path)
    return _config
