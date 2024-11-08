import os
import logging
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from wcwidth import wcswidth
from .text_styles import COLOR_CODES, STYLE_CODES
from .defaults import DefaultsManager, LogConfig

class LogLineFormatter:
    """Formats a single log line according to configuration."""
    
    def __init__(self, config: LogConfig):
        self.config = config
    
    def _apply_style(self, text: str, color: str = None, style: str = None) -> str:
        """Apply color and style to text."""
        if color:
            color_code = COLOR_CODES.get(color.strip(), '')
            text = f"{color_code}{text}{COLOR_CODES['reset']}"
        
        if style:
            style_list = style.split(',')
            style_codes = ''.join(
                [STYLE_CODES.get(s.strip(), '') for s in style_list if s.strip()]
            )
            text = f"{style_codes}{text}{COLOR_CODES['reset']}"
        
        return text

    def _wrap_text(self, text: str, max_width: int, word_wrap: bool = True) -> list[str]:
        """
        Wrap text to fit within max_width.
        
        Args:
            text: Text to wrap
            max_width: Maximum width for each line
            word_wrap: If True, try to wrap at word boundaries
            
        Returns:
            List of wrapped lines
        """
        if not text or max_width <= 0:
            return []
            
        if not word_wrap:
            # Simple character wrapping
            return [text[i:i+max_width] for i in range(0, len(text), max_width)]
            
        # Word wrapping
        lines = []
        words = text.split()
        current_line = []
        current_width = 0
        
        for word in words:
            word_width = wcswidth(word)
            
            if current_width + (1 if current_line else 0) + word_width <= max_width:
                # Word fits on current line
                if current_line:
                    current_width += 1  # Space before word
                    current_line.append(' ')
                current_line.append(word)
                current_width += word_width
            else:
                if current_line:
                    # Complete current line
                    lines.append(''.join(current_line))
                    current_line = []
                    current_width = 0
                
                if word_width > max_width:
                    # Word is too long, needs character wrapping
                    wrapped_word = [word[i:i+max_width] for i in range(0, len(word), max_width)]
                    lines.extend(wrapped_word[:-1])
                    # Start new line with remainder
                    current_line = [wrapped_word[-1]]
                    current_width = wcswidth(wrapped_word[-1])
                else:
                    # Start new line with word
                    current_line = [word]
                    current_width = word_width
        
        if current_line:
            lines.append(''.join(current_line))
            
        return lines

    def format_line(self, message: str, reason: str = None, status: str = None) -> str:
        """Format the complete log line with support for wrapped fields."""
        widths = self._calculate_widths(message, reason, status)
        
        # Get formatted lines for each field
        message_lines = self._format_field(message, 'message', widths['message'])
        padding = self._format_field('', 'padding', widths['padding'])[0]
        reason_lines = self._format_field(reason, 'reason', widths['reason']) if reason and widths['reason'] > 0 else []
        status_lines = self._format_field(status, 'status', widths['status']) if status and widths['status'] > 0 else []
        
        # Combine lines
        max_lines = max(
            len(message_lines),
            len(reason_lines) if reason_lines else 0,
            len(status_lines) if status_lines else 0,
            1  # Ensure at least one line
        )
        
        formatted_lines = []
        for i in range(max_lines):
            line_parts = []
            
            # Add message
            msg = message_lines[i] if i < len(message_lines) else ' ' * widths['message']
            line_parts.append(self._apply_style(msg, self.config.fields['message'].color, self.config.fields['message'].style))
            
            # Add padding
            line_parts.append(self._apply_style(padding, self.config.fields['padding'].color, self.config.fields['padding'].style))
            
            # Add reason if it exists
            if reason_lines:
                rsn = reason_lines[i] if i < len(reason_lines) else ' ' * widths['reason']
                line_parts.append(self._apply_style(rsn, self.config.fields['reason'].color, self.config.fields['reason'].style))
            
            # Add status if it exists (only on first line)
            if status_lines and i == 0:
                line_parts.append(self._apply_style(status_lines[0], self.config.fields['status'].color, self.config.fields['status'].style))
            elif status and i > 0:
                line_parts.append(' ' * widths['status'])
            
            formatted_lines.append(''.join(line_parts))
        
        return '\n'.join(formatted_lines)

    def _format_field(self, content: str, field_name: str, width: int) -> list[str]:
        """Format a single field with its configuration."""
        field_config = self.config.fields[field_name]
        
        if field_name == 'padding':
            # Padding is always single line
            inner_width = width - len(field_config.leading_char) - len(field_config.closing_char)
            formatted = f"{field_config.leading_char}{field_config.padding_char * inner_width}{field_config.closing_char}"
            return [formatted]
            
        # Handle wrapping for other fields
        max_content_width = width - len(field_config.leading_char) - len(field_config.closing_char)
        
        if not field_config.wrap:
            # If wrapping is disabled, truncate
            truncated = content[:max_content_width] if wcswidth(content) > max_content_width else content
            raw = f"{field_config.leading_char}{truncated}{field_config.closing_char}"
            
            # Handle alignment based on field type
            if field_name == 'message':
                formatted = raw.ljust(width)
            elif field_name == 'status':
                formatted = raw  # Status field gets no additional alignment
            else:
                formatted = raw.rjust(width)
                
            return [formatted]
        
        # Wrap content
        wrapped_lines = self._wrap_text(content, max_content_width, field_config.word_wrap)
        formatted_lines = []
        
        for i, line in enumerate(wrapped_lines):
            if field_name == 'message':
                # Left align all message lines
                raw = f"{field_config.leading_char if i == 0 else ''}{line}{field_config.closing_char if i == len(wrapped_lines)-1 else ''}"
                formatted = raw.ljust(width)
            elif field_name == 'status':
                # Status doesn't get alignment padding
                raw = f"{field_config.leading_char if i == 0 else ''}{line}{field_config.closing_char if i == len(wrapped_lines)-1 else ''}"
                formatted = raw
            else:
                # Right align all other fields
                raw = f"{field_config.leading_char if i == 0 else ''}{line}{field_config.closing_char if i == len(wrapped_lines)-1 else ''}"
                formatted = raw.rjust(width)
                
            formatted_lines.append(formatted)
            
        return formatted_lines or ['']  # Ensure at least one line

    def _calculate_widths(self, message: str, reason: str = None, status: str = None) -> dict:
        """Calculate exact widths including leading/closing chars for all fields."""
        fields = self.config.fields
        
        # Calculate base widths with leading/closing chars
        widths = {
            'message': wcswidth(message) + len(fields['message'].leading_char) + len(fields['message'].closing_char),
            'reason': (wcswidth(reason) + len(fields['reason'].leading_char) + len(fields['reason'].closing_char)) if reason else 0,
            'status': (wcswidth(status) + len(fields['status'].leading_char) + len(fields['status'].closing_char)) if status else 0
        }
        
        # Apply max width constraints
        for field, width in widths.items():
            if width > 0:  # Only apply constraints to non-empty fields
                max_width = fields[field].max_width
                if max_width:
                    widths[field] = min(width, max_width)
        
        # Calculate padding width with leading/closing chars
        used_width = sum(w for f, w in widths.items() if f != 'padding')
        padding_field = fields['padding']
        min_padding = (padding_field.min_width + len(padding_field.leading_char) + len(padding_field.closing_char))
        total_padding = self.config.total_width - used_width
        widths['padding'] = max(min_padding, total_padding)
        
        return widths

class CustomFormatter(logging.Formatter):
    """Custom formatter that handles template-based log formatting."""
    
    def __init__(self, template_dir: str, defaults_manager: DefaultsManager):
        super().__init__()
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.defaults_manager = defaults_manager
        self.template_dir = template_dir
        self._load_template_configs()
        
    def _get_template_name_from_path(self, template_path: str) -> str:
        """Extract template name from the template path."""
        dirname = os.path.dirname(template_path)
        if dirname:
            return os.path.basename(dirname)
        return 'default'
        
    def _load_template_configs(self):
        """Load all template configurations."""
        self.template_configs = {}
        
        for template_path in self.env.list_templates():
            if template_path.endswith('_config.j2'):
                template = self.env.get_template(template_path)
                template_name = self._get_template_name_from_path(template_path)
                
                template.render()
                
                if hasattr(template.module, 'config'):
                    self.template_configs[template_name] = template.module.config
                    
    def _load_template_config(self, template_name: str) -> dict:
        """Load configuration for a specific template."""
        config = self.template_configs.get(template_name)
        if config is None:
            config = self.template_configs.get('default', {})
        return config
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record using templates and configuration."""
        template_name = getattr(record, 'template', 'default')
        template_config = self._load_template_config(template_name)
        
        # Get effective configuration
        config = self.defaults_manager.get_effective_defaults(
            instance_id=str(id(record)),
            template_name=template_name,
            level=record.levelname,
            template_config=template_config
        )
        
        # Get default status from template config if not explicitly set
        status = getattr(record, 'status', None)
        if status is None and template_config.get('defaults'):
            status = template_config['defaults'].get(record.levelname, {}).get('status')
        
        # Format the log line
        formatter = LogLineFormatter(config)
        return formatter.format_line(
            message=record.msg,
            reason=getattr(record, 'reason', None),
            status=status
        )
