from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from copy import deepcopy

@dataclass
class FieldConfig:
    """Configuration for a single field in the log line."""
    min_width: int = 0
    max_width: Optional[int] = None
    leading_char: str = ''
    closing_char: str = ''
    padding_char: str = ' '
    color: Optional[str] = None
    style: Optional[str] = None
    wrap: bool = True
    word_wrap: bool = True

@dataclass
class LogConfig:
    """Complete logging configuration."""
    total_width: int = 80
    fields: Dict[str, FieldConfig] = field(default_factory=lambda: {
        'message': FieldConfig(min_width=20, max_width=55, wrap=True, word_wrap=True),
        'padding': FieldConfig(min_width=1, padding_char='.', leading_char=' ', closing_char=' '),
        'reason': FieldConfig(max_width=22, leading_char='(', closing_char=')', wrap=False, word_wrap=True),
        'status': FieldConfig(max_width=10, wrap=False)
    })
    level_styles: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        'DEBUG': {'status': {'color': 'blue', 'style': 'bold'}},
        'INFO': {'status': {'color': 'green', 'style': 'bold'}},
        'WARNING': {'status': {'color': 'yellow', 'style': 'bold'}},
        'ERROR': {'status': {'color': 'red', 'style': 'bold'}},
        'CRITICAL': {'status': {'color': 'red', 'style': 'bold,blink'}}
    })

class DefaultsManager:
    """Manages the cascading of defaults through different levels."""
    def __init__(self, system_defaults: LogConfig = None):
        self.system_defaults = system_defaults or LogConfig()
        self.template_defaults = {}
        self.instance_defaults = {}
    
    def get_effective_defaults(self, instance_id: str, template_name: str = None,
                             level: str = None, template_config: dict = None, **kwargs) -> LogConfig:
        """Get the effective defaults for a specific log message."""
        # Start with system defaults
        config = deepcopy(self.system_defaults)
        
        # Apply template config if provided
        if template_config:
            config = self._merge_defaults(config, template_config)
            
        # Apply level-specific styles
        if level and level in config.level_styles:
            level_styles = config.level_styles[level]
            for field, style in level_styles.items():
                if field in config.fields:
                    for key, value in style.items():
                        setattr(config.fields[field], key, value)
        
        # Apply any additional overrides
        if kwargs:
            config = self._merge_defaults(config, kwargs)
            
        return config
    
    @staticmethod
    def _merge_defaults(base: LogConfig, override: dict) -> LogConfig:
        """Deep merge override dict into base LogConfig."""
        result = deepcopy(base)
        
        if 'total_width' in override:
            result.total_width = override['total_width']
        
        if 'fields' in override:
            for field_name, field_config in override['fields'].items():
                if field_name in result.fields:
                    for key, value in field_config.items():
                        setattr(result.fields[field_name], key, value)
        
        return result