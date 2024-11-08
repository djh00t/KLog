# KLog: A Custom Logging Library for Python

## Detailed Design Document

### Overview

KLog is a Python logging library that extends the standard logging module,
providing advanced formatting capabilities, including per-level custom
templates, custom fields, dynamic padding, and support for extended colors and
styles, including emojis and Unicode characters. KLog is designed for ease of
use, allowing developers to initialize the logger with a single class
instantiation, with all defaults, templates, and log levels set up and ready to
use.

### Key Features

    1. **Easy Initialization:** Initialize KLog with a single class instantiation.
    2. **Per-Level Custom Templates:** Define distinct log formats for each log level using an intuitive template syntax.
    3. **Custom Fields in Single-Line Logging Calls:** Pass custom fields directly as keyword arguments in logging method calls without using the extra parameter.
    4. **Advanced Field Attributes:** Control width, alignment, text color, text style, padding character, and default values of fields.
    5. **Dynamic Padding Field:** Automatically fills space between fields to achieve alignment, treating emojis as single-character width.
    6. **Extended Color and Style Support:** Supports a wide range of colors (with underscores in names) and multiple text styles via comma-separated lists.
    7. **Elegant Template Syntax:** Intuitive and expressive template definitions stored in separate files for each template group.

### Library Components

#### 1. KLog Class**

*KLog()*

**Responsibilities:**

- Provides a simple interface to initialize and configure the logger.
- Sets up default templates, log levels, and other configurations during initialization.
- Exposes the logger instance for use in the application.

**Initialization Parameters:**

- name: (Optional) Name of the logger. Defaults to 'KLog'.
- level: (Optional) Logging level. Defaults to logging.INFO.
- template: (Optional) Template to use. Defaults to 'default'.

**Example:**

```python
from klog import KLog

log = KLog()
```

#### 2. CustomLogger Class

*CustomLogger(logging.Logger)*

**Responsibilities:**

- Overrides logging methods (info, warning, error, critical, debug) to accept custom fields directly as keyword arguments.
- Merges custom fields into the LogRecord using the extra parameter internally.

#### 3. CustomFormatter Class

*CustomFormatter(logging.Formatter)*

**Responsibilities:**

- Parses custom templates from template files.
- Handles field attributes and applies them to the log output.
- Manages dynamic padding and alignment.
- Evaluates conditional blocks (if statements).
- Treats emojis as single-character width during padding calculations.

#### 4. Template Parser

**Functionality:**

- Interprets the custom template syntax.
- Extracts fields and their attributes.
- Supports nested conditional blocks.
- Loads templates from the templates/ directory.

#### 5. Field Handlers

**Base Class:** *FieldHandler*

**Derived Classes:**

- MessageFieldHandler
- StatusFieldHandler
- ReasonFieldHandler
- PaddingFieldHandler

**Responsibilities:**

- Applies width, alignment, color, style, padding, and default values.
- Handles content wrapping and text styling.
- Supports multiple text styles via comma-separated lists.

#### 6. Conditional Logic Processor

**Functionality:**

- Evaluates if conditions within templates.
- Includes or excludes fields based on the presence of custom fields in the LogRecord.

#### 7. Color and Style Support

**Module:** *text_styles*

**Capabilities:**

- Maps extended color and style strings to ANSI escape codes.
- Supports a wide range of colors, including light, dark, and standard shades, using underscores in names.
- Allows multiple text styles via comma-separated lists.

#### Extended Color and Style Support

**Color Codes**

The color names use underscores instead of spaces.

```python
COLOR_CODES = {
    'light_red': '\u001b[91m',
    'red': '\u001b[31m',
    'dark_red': '\u001b[31;2m',
    'light_green': '\u001b[92m',
    'green': '\u001b[32m',
    'dark_green': '\u001b[32;2m',
    'light_yellow': '\u001b[93m',
    'yellow': '\u001b[33m',
    'dark_yellow': '\u001b[33;2m',
    'light_orange': '\u001b[38;5;215m',
    'orange': '\u001b[38;5;208m',
    'dark_orange': '\u001b[38;5;202m',
    'light_blue': '\u001b[94m',
    'blue': '\u001b[34m',
    'dark_blue': '\u001b[34;2m',
    'light_purple': '\u001b[95m',
    'purple': '\u001b[35m',
    'dark_purple': '\u001b[35;2m',
    'light_pink': '\u001b[95m',
    'pink': '\u001b[38;5;205m',
    'dark_pink': '\u001b[38;5;95m',
    'white': '\u001b[37m',
    'grey': '\u001b[90m',
    'black': '\u001b[30m',
    'reset': '\u001b[0m',
}
```

**Style Codes**

Style codes can be specified as a comma-separated list.

```python
STYLE_CODES = {
    'bold': '\u001b[1m',
    'italic': '\u001b[3m',
    'underlined': '\u001b[4m',
    'blink': '\u001b[5m',
    'reverse': '\u001b[7m',
    'hidden': '\u001b[8m',
    'default': '',
}
```

**Example:** `text_style="bold,underlined"`

#### Handling Emojis and Padding

- KLog treats all emojis as single-character width when calculating padding and alignment.
- Uses the wcwidth library to accurately calculate the display width of Unicode characters and emojis.
- Ensures that log messages align correctly even when they contain emojis or Unicode characters.

#### Template Files Organization

- **Templates Directory:** A designated directory templates/ contains template files.
- **Template Files:** Each template is defined in a separate Python file.

#### Default Template

```python
# templates/default.py

import logging

default = {
    logging.INFO: '''
        {message: align="left", width=72}
        {padding: char=" "}
        {if: reason,
            {reason: align="right"}
            {padding: char=" ", width=3}
        }
        {status: align="right", text_color="green", text_style="bold", default="OK"}
    ''',
    logging.WARNING: '''
        {message: align="left", width=72}
        {padding: char=" "}
        {if: reason,
            {reason: align="right"}
            {padding: char=" ", width=3}
        }
        {status: align="right", text_color="yellow", text_style="bold", default="WARNING"}
    ''',
    logging.ERROR: '''
        {message: align="left", width=72}
        {padding: char=" "}
        {if: reason,
            {reason: align="right"}
            {padding: char=" ", width=3}
        }
        {status: align="right", text_color="red", text_style="bold", default="ERROR"}
    ''',
    logging.CRITICAL: '''
        {message: align="left", width=72}
        {padding: char=" "}
        {if: reason,
            {reason: align="right"}
            {padding: char=" ", width=3}
        }
        {status: align="right", text_color="red", text_style="bold", default="CRITICAL"}
    ''',
    logging.DEBUG: '''
        {message: align="left", width=72}
        {padding: char=" "}
        {if: reason,
            {reason: align="right"}
            {padding: char=" ", width=3}
        }
        {status: align="right", text_color="blue", text_style="bold", default="DEBUG"}
    '''
}
```

#### Pre-Commit Template

```python
# templates/pre_commit.py

import logging

pre_commit = {
    logging.INFO: '''
        {message: align="left", width=72}
        {padding: char="."}
        {if: reason,
            {reason: align="right"}
            {padding: char=".", width=3}
        }
        {status: align="right", text_color="green", text_style="bold", default="✅"}
    ''',
    logging.WARNING: '''
        {message: align="left", width=72}
        {padding: char="."}
        {if: reason,
            {reason: align="right"}
            {padding: char=".", width=3}
        }
        {status: align="right", text_color="yellow", text_style="bold", default="⚠️"}
    ''',
    logging.ERROR: '''
        {message: align="left", width=72}
        {padding: char="."}
        {if: reason,
            {reason: align="right"}
            {padding: char=".", width=3}
        }
        {status: align="right", text_color="red", text_style="bold", default="❌"}
    ''',
    logging.CRITICAL: '''
        {message: align="left", width=72}
        {padding: char="."}
        {if: reason,
            {reason: align="right"}
            {padding: char=".", width=3}
        }
        {status: align="right", text_color="red", text_style="bold", default="🛑"}
    ''',
    logging.DEBUG: '''
        {message: align="left", width=72}
        {padding: char="."}
        {if: reason,
            {reason: align="right"}
            {padding: char=".", width=3}
        }
        {status: align="right", text_color="blue", text_style="bold", default="🐛"}
    '''
}
```

### Usage Example

#### Initialization

```python
from klog import KLog

# Initialize KLog with default settings

log = KLog()

# Initialize KLog with custom settings

log = KLog(name='my_logger', level=logging.DEBUG, template='pre_commit')
```

#### Logging Messages

```python
# INFO level log

log.info(
    message="System check completed.",
    reason="All systems operational",
    status="✅"
)

# WARNING level log

log.warning(
    message="Disk space running low.",
    reason="Less than 10% space remaining.",
    status="⚠️"
)

# ERROR level log

log.error(
    message="Failed to save file.",
    reason="Permission denied.",
    status="❌"
)
```

#### Detailed Class and Method Definitions

**KLog Class**

```python

class KLog:
def **init**(self, name='KLog', level=logging.INFO, template='default'): # Set the custom logger class
logging.setLoggerClass(CustomLogger)

        # Create a logger instance
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Load the template
        if template == 'default':
            from templates.default import default as templates
        elif template == 'pre_commit':
            from templates.pre_commit import pre_commit as templates
        else:
            raise ValueError(f"Unknown template: {template}")

        # Configure the handler and formatter
        handler = logging.StreamHandler()
        formatter = CustomFormatter(templates=templates)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    # Expose logging methods
    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)
```