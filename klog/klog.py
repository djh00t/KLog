import logging
import os
from .custom_formatter import CustomFormatter
from .custom_logger import CustomLogger
from .defaults import DefaultsManager, LogConfig

class KLog:
    """Main logger class that provides the public interface for the klog system."""
    
    def __init__(
        self,
        name: str = "KLog",
        level: int = logging.INFO,
        template: str = "default",
        **kwargs
    ):
        self.instance_id = id(self)
        self.defaults_manager = DefaultsManager()
        
        # Store template and any additional configuration
        self.template = template
        self.kwargs = kwargs
        
        # Set up the logger
        logging.setLoggerClass(CustomLogger)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Configure handler with defaults manager
        handler = logging.StreamHandler()
        formatter = CustomFormatter(
            template_dir=self._get_template_path(template),
            defaults_manager=self.defaults_manager
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def _get_template_path(self, template: str) -> str:
        """
        Get the template directory path.
        
        Args:
            template: Either a built-in template name or a custom template directory path
            
        Returns:
            str: Full path to the template directory
        """
        if os.path.isdir(template):
            return template
        return os.path.join(os.path.dirname(__file__), "templates", template)
    
    def _handle_template_override(self, level: int, message: str, args: tuple, **kwargs):
        """
        Handle template override for a specific log message.
        
        Args:
            level: Logging level
            message: Log message
            args: Additional positional arguments
            **kwargs: Additional keyword arguments including possible template override
        """
        template = kwargs.get('template')
        
        if template and template != self.template:
            # Create temporary handler with new template
            handler = logging.StreamHandler()
            formatter = CustomFormatter(
                template_dir=self._get_template_path(template),
                defaults_manager=self.defaults_manager
            )
            handler.setFormatter(formatter)
            
            # Store current handlers
            current_handlers = self.logger.handlers.copy()
            
            try:
                # Replace handlers temporarily
                self.logger.handlers.clear()
                self.logger.addHandler(handler)
                
                # Log with temporary handler
                self.logger._log(level, message, args, **kwargs)
            finally:
                # Restore original handlers
                self.logger.handlers.clear()
                for h in current_handlers:
                    self.logger.addHandler(h)
        else:
            # Log with default handler
            self.logger._log(level, message, args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs):
        """Log a debug message."""
        self._handle_template_override(logging.DEBUG, message, args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Log an info message."""
        self._handle_template_override(logging.INFO, message, args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log a warning message."""
        self._handle_template_override(logging.WARNING, message, args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log an error message."""
        self._handle_template_override(logging.ERROR, message, args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log a critical message."""
        self._handle_template_override(logging.CRITICAL, message, args, **kwargs)