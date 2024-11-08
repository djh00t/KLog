# KLog

[![PyPI version](https://badge.fury.io/py/klog.svg)](https://badge.fury.io/py/klog)
[![Build Status](https://github.com/djh00t/klog/workflows/CI/badge.svg)](https://github.com/djh00t/klog/actions)
[![Python Versions](https://img.shields.io/pypi/pyversions/klog.svg)](https://pypi.org/project/klog/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

KLog is a powerful Python logging library that transforms how you handle logging in your applications. Unlike standard logging solutions, KLog provides:

- 🎨 Rich formatting with colors, styles, and emoji support
- 📝 Jinja2 templating for complete log message customization
- 🔧 Per-level custom templates without complex configuration
- 📊 Dynamic field padding and alignment that properly handles Unicode
- 🚀 Simple setup with powerful defaults

*Requires Python 3.7+*

## Table of Contents

- [KLog](#klog)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Installation Options](#installation-options)
      - [Quick Install via pip](#quick-install-via-pip)
      - [Development Installation via git](#development-installation-via-git)
      - [Installation via Poetry (Recommended for Development)](#installation-via-poetry-recommended-for-development)
      - [Docker Installation](#docker-installation)
    - [Initialization](#initialization)
    - [Logging Messages](#logging-messages)
  - [Templates](#templates)
    - [Built-in Templates](#built-in-templates)
    - [Selecting a Template](#selecting-a-template)
    - [Customizing Templates](#customizing-templates)
    - [Template Structure](#template-structure)
      - [Directories](#directories)
      - [Files](#files)
      - [jinja2](#jinja2)
      - [Example template structure:](#example-template-structure)
      - [Base Template Example](#base-template-example)
      - [Log level Specific Template Example](#log-level-specific-template-example)
    - [Custom Fields](#custom-fields)
    - [Field Attributes and Filters](#field-attributes-and-filters)
      - [Custom Filters in Action](#custom-filters-in-action)
      - [Padding Examples](#padding-examples)
    - [Color and Style Options](#color-and-style-options)
      - [Color Examples](#color-examples)
      - [Style Combinations](#style-combinations)
    - [Handling Emojis and Unicode](#handling-emojis-and-unicode)
    - [Examples](#examples)
      - [Example 1: Web Application Logging](#example-1-web-application-logging)
      - [Example 2: System Monitoring](#example-2-system-monitoring)
      - [Example 3: Deployment Pipeline](#example-3-deployment-pipeline)
  - [Advanced Usage](#advanced-usage)
    - [Creating Custom Templates](#creating-custom-templates)
    - [Arguments and Parameters](#arguments-and-parameters)
      - [KLog Class](#klog-class)
      - [Logging Methods](#logging-methods)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)
  - [Contact](#contact)

## Features

- **Easy Initialization** - Set up the logger with a single class instantiation.
- **Per-Level Custom Templates** - Define custom log formats for each log level using Jinja2 templates.
- **Custom Fields** - Pass custom fields directly in logging calls without using the extra parameter.
- **Dynamic Padding** - Automatically adjusts spacing and alignment, treating emojis as single-character width.
- **Extended Color and Style Support** - Supports a wide range of colors and multiple text styles.
- **Templates** - Switch between different built-in templates or create your own.
- **Single-Line Log Messages** - Ensures that each log message is rendered on a single line.

## Getting Started

### Installation Options

KLog can be installed through several methods, choose the one that best fits your workflow:

#### Quick Install via pip

For most users, installing via pip is the simplest option:

```bash
# Install latest stable version
pip install klog

# Install with all optional dependencies
pip install klog[all]

# Install specific version
pip install klog==1.2.0
```

#### Development Installation via git

For the latest features and development version:

```bash
# Clone with depth 1 for faster download
git clone --depth 1 https://github.com/djh00t/klog.git

# Change to project directory
cd klog

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

#### Installation via Poetry (Recommended for Development)

Poetry provides better dependency management and virtual environment handling:

1. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone and Install:
   ```bash
   # Clone repository
   git clone https://github.com/djh00t/klog.git
   cd klog

   # Install dependencies and create virtual environment
   poetry install

   # Activate the virtual environment
   poetry shell
   ```

3. Development Setup:
   ```bash
   # Install development dependencies
   poetry install --with dev

   # Run tests
   poetry run pytest

   # Build documentation
   poetry run sphinx-build -b html docs/ docs/_build/html
   ```

#### Docker Installation

For containerized environments:

```bash
# Build image
docker build -t klog .

# Run tests in container
docker run klog pytest

# Run interactive shell
docker run -it klog bash
```


### Initialization

Import and initialize KLog:

```python
from klog import KLog

# Initialize KLog with default settings
log = KLog()

# Initialize KLog with a built-in template
log = KLog(template='basic')

# Initialize KLog with a custom templates directory
log = KLog(template='path/to/your/templates')
```

Parameters:
- `name` (str): Name of the logger. Defaults to 'KLog'.
- `level` (int): Logging level (e.g., logging.INFO). Defaults to logging.INFO.
- `template` (str): The template to use for log output formatting. The library
  comes with `default`, `basic`, `precommit` & `none` as builtin templates.
  Defaults to 'default'.

### Logging Messages

Log messages using standard logging methods, passing custom fields directly as keyword arguments:

```python
# INFO level log
log.info(
    message="System check completed.",
    reason="All systems operational.",
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

## Templates

The core of KLog is its template system, which allows you to define custom log
message formats for each log level. KLog comes with built-in templates that you
can use out of the box or customize to suit your needs.

### Built-in Templates

- **default**: The default template with standard formatting
- **basic**: A basic template with minimal formatting
- **none**: A template with no formatting and only a message field which is
  wrapped at 80 characters by default (plain text)
- **precommit**: A template optimized for pre-commit hooks & CI/CD pipelines

### Selecting a Template

Specify the template when initializing KLog:

```python
log = KLog(template='basic')
```

### Customizing Templates

You can copy & customize existing templates or create new ones by modifying the
templates in the `klog/templates/` directory of the KLog git repository.

KLog uses Jinja2 templates with inheritance to define log message formats. You
can find more information about Jinja2 templates in the [official
documentation](https://jinja.palletsprojects.com/en/3.0.x/) or by checking the
existing templates in the `klog/templates/` directory.

### Template Structure

When creating a new template it should be structured as follows:

#### Directories

- The template directory should be named after the template (e.g.,
  `my_template`).

#### Files

- Each template must have at least a `base_template.j2` file which defines the
  base log formatting and structure.
- Optional loglevel specific templates are used to extend & override the base
  template based on the loglevel in use. Loglevel specific templates should be
  named as follows: `<loglevel>_template.j2` (e.g., `info_template.j2`).

#### jinja2

- The `base_template.j2` file should define at least the following blocks:
  - `message`: The main log message.

- Additional blocks can be defined to add more detail to the log message:
  - `reason`: An optional field providing additional context.
  - `status`: An optional field for status indicators (supports emojis).
  - `padding`: An optional field for inserting padding characters between
    fields. This is useful for fixed width log messages with multiple fields.

#### Example template structure:

```shell
templates/
├── my_template_01
│   ├── base_template.j2
│   ├── critical_template.j2
│   ├── debug_template.j2
│   ├── error_template.j2
│   ├── info_template.j2
│   └── warning_template.j2
├── my_template_02
│   └── base_template.j2
└── my_template_03
    ├── base_template.j2
    ├── critical_template.j2
    ├── debug_template.j2
    ├── error_template.j2
    ├── info_template.j2
    └── warning_template.j2
```

#### Base Template Example

```jinja
{# templates/basic/base_template.j2 #}
{%- block message -%}
{{ message | align(width=72, direction='left') }}
{%- endblock -%}
{%- block padding -%}
{{ padding(' ') }}
{%- endblock -%}
{%- block reason -%}
{% if reason -%}
{{ reason | align(direction='right') }}
{{ padding(' ', width=3) }}
{%- endif -%}
{%- endblock -%}
{%- block status -%}
{{ status | default('') | color('white') | style('bold') | align(direction='right') }}
{%- endblock -%}
```

#### Log level Specific Template Example

```jinja
{# templates/basic/critical_template.j2 #}
{% extends 'base_template.j2' %}

{% block status %}
{{ status | default('CRITICAL') | color('red') | style('bold','blink') | align(direction='right') }}
{% endblock %}
```

### Custom Fields

KLog supports custom fields that can be used in your templates. Here are examples:

```python
# Basic usage
log.info(
    message="User logged in",
    status="✅"
)

# With all custom fields
log.error(
    message="Database connection failed",
    reason="Connection timeout",
    status="❌",
    user="admin",
    attempt=3,
    duration="5s"
)

# Custom fields in template
{# template.j2 #}
{{ message }} - User: {{ user | default('anonymous') }} 
{% if attempt %}(Attempt {{ attempt }}){% endif %}
```

### Field Attributes and Filters

KLog provides powerful filters for formatting your log messages:

#### Custom Filters in Action

```python
# Template usage examples
{# Alignment #}
{{ message | align(width=50, direction='left') }}     # Left-aligned, 50 chars
{{ status | align(width=10, direction='center') }}    # Centered, 10 chars

# Color combinations
{{ message | color('light_blue') | style('bold') }}   # Bold blue text
{{ status | color('red') | style('blink,italic') }}   # Blinking italic red

# Default values
{{ user | default('guest') | color('grey') }}         # Grey 'guest' if user is empty
```

#### Padding Examples

```python
# In templates
{{ padding('-', width=50) }}                         # Creates a 50-char divider
{{ message }} {{ padding() }} {{ status }}           # Default single space padding
```

### Color and Style Options

Make your logs visually distinctive with these formatting options:

#### Color Examples
```python
log.info(
    message="{{ 'Success' | color('green') }}",
    status="✅"
)

log.error(
    message="{{ 'Critical Error' | color('light_red') }}",
    reason="{{ 'Permission Denied' | color('yellow') }}",
    status="❌"
)
```

#### Style Combinations
```python
# Template examples
{{ 'URGENT' | style('bold,blink') | color('red') }}
{{ 'Note' | style('italic') | color('grey') }}
{{ 'Warning' | style('reverse') | color('yellow') }}

# Real-world usage
log.warning(
    message="{{ 'Security Alert' | style('bold,underlined') | color('orange') }}",
    reason="Unusual login pattern",
    status="⚠️"
)
```

Complete Color Palette:
```python
COLORS = {
    'light_red': '\033[91m',    'red': '\033[31m',    'dark_red': '\033[31;2m',
    'light_green': '\033[92m',  'green': '\033[32m',  'dark_green': '\033[32;2m',
    'light_yellow': '\033[93m', 'yellow': '\033[33m', 'dark_yellow': '\033[33;2m',
    'light_blue': '\033[94m',   'blue': '\033[34m',   'dark_blue': '\033[34;2m',
    'light_purple': '\033[95m', 'purple': '\033[35m', 'dark_purple': '\033[35;2m',
    'light_pink': '\033[95m',   'pink': '\033[38;5;206m', 'dark_pink': '\033[38;5;162m',
    'orange': '\033[38;5;208m', 'light_orange': '\033[38;5;214m', 'dark_orange': '\033[38;5;166m',
    'white': '\033[97m',        'grey': '\033[90m',   'black': '\033[30m',
    'reset': '\033[0m'
}
```

### Handling Emojis and Unicode

KLog treats emojis and Unicode characters as single-character width when calculating padding and alignment, ensuring proper alignment in log messages.

### Examples

#### Example 1: Web Application Logging

```python
from klog import KLog

log = KLog(template='default')

# API request logging
log.info(
    message="Received API request",
    reason="GET /api/v1/users",
    status="📥"
)

# Authentication events
log.warning(
    message="Failed login attempt",
    reason="Invalid credentials for user 'admin'",
    status="🔒",
    ip="192.168.1.100",
    attempts=3
)

# Error handling
log.error(
    message="Database connection failed",
    reason="Connection timeout after 30s",
    status="💥",
    db_host="db.example.com",
    retry_count=5
)
```

#### Example 2: System Monitoring

```python
from klog import KLog
import psutil

log = KLog(template='basic')

# Resource monitoring
memory = psutil.virtual_memory()
log.info(
    message=f"Memory usage: {memory.percent}%",
    reason="System check",
    status="📊" if memory.percent < 80 else "⚠️"
)

# Service status checks
services = {'nginx': 'running', 'postgresql': 'stopped'}
for service, status in services.items():
    log.warning(
        message=f"Service {service} is {status}",
        reason="Routine check",
        status="✅" if status == 'running' else "❌"
    )
```

#### Example 3: Deployment Pipeline

```python
from klog import KLog
import logging

log = KLog(level=logging.DEBUG, template='precommit')

# Deployment steps
log.info(
    message="Starting deployment process",
    reason="Version 2.1.0",
    status="🚀"
)

# Build process
log.debug(
    message="Running unit tests",
    reason="424 tests in test suite",
    status="🧪"
)

# Deployment validation
try:
    # Simulated deployment check
    raise Exception("Invalid configuration")
except Exception as e:
    log.error(
        message="Deployment validation failed",
        reason=str(e),
        status="❌",
        environment="production",
        rollback=True
    )
```

## Advanced Usage

### Creating Custom Templates

Custom templates allow you to define exactly how your log messages appear. Here's a comprehensive guide:

1. Create a New Template Directory
   ```bash
   mkdir -p klog/templates/my_template
   ```

2. Define the Base Template Structure
   Create `base_template.j2` with these components:

   ```jinja
   {# klog/templates/my_template/base_template.j2 #}
   
   {# Timestamp block #}
   {%- block timestamp -%}
   {{ now().strftime('%Y-%m-%d %H:%M:%S') | color('grey') }}
   {%- endblock -%}
   
   {# Level indicator block #}
   {%- block level -%}
   {{ level | upper | color('cyan') | style('bold') | align(width=8) }}
   {%- endblock -%}
   
   {# Main message block #}
   {%- block message -%}
   {{ message | align(width=50, direction='left') }}
   {%- endblock -%}
   
   {# Context/reason block #}
   {%- block reason -%}
   {%- if reason -%}
   {{ reason | truncate(30) | align(direction='right') }}
   {%- endif -%}
   {%- endblock -%}
   
   {# Status indicator block #}
   {%- block status -%}
   {{ status | default('●') | color('white') | align(direction='right') }}
   {%- endblock -%}
   
   {# Optional metadata block #}
   {%- block metadata -%}
   {%- if metadata is defined -%}
   {{ metadata | to_json | color('grey') }}
   {%- endif -%}
   {%- endblock -%}
   ```

3. Create Level-Specific Templates
   Example for error level (`error_template.j2`):

   ```jinja
   {% extends 'base_template.j2' %}
   
   {# Override level block for errors #}
   {% block level %}
   {{ level | upper | color('red') | style('bold,blink') | align(width=8) }}
   {% endblock %}
   
   {# Override status for errors #}
   {% block status %}
   {{ status | default('❌') | color('red') | style('bold') }}
   {% endblock %}
   
   {# Add stack trace for errors #}
   {% block metadata %}
   {% if exc_info %}
   {{ exc_info | format_exception | color('red') | style('dim') }}
   {% endif %}
   {% endblock %}
   ```

4. Advanced Template Features

   ```jinja
   {# Custom filters #}
   {{ value | padding(char='-', width=20) }}  {# Create separators #}
   {{ dict_value | to_json | pretty }}        {# Format JSON data #}
   {{ long_text | truncate(80) }}            {# Truncate long messages #}
   
   {# Conditional formatting #}
   {% if level == 'ERROR' %}
   {{ message | color('red') | style('bold') }}
   {% elif level == 'WARNING' %}
   {{ message | color('yellow') }}
   {% endif %}
   ```

5. Use Your Template
   ```python
   # Basic usage
   log = KLog(template='my_template')
   
   # With additional configuration
   log = KLog(
       template='my_template',
       level=logging.DEBUG,
       name='MyApp'
   )
   ```



### Arguments and Parameters

#### KLog Class

```python
KLog(name='KLog', level=logging.INFO, template='default')
```

- **name** (str): Name of the logger
- **level** (int): Logging level
- **template** (str): Name of the template to use

#### Logging Methods

KLog exposes standard logging methods:

- `log.debug(message, *args, **kwargs)`
- `log.info(message, *args, **kwargs)`
- `log.warning(message, *args, **kwargs)`
- `log.error(message, *args, **kwargs)`
- `log.critical(message, *args, **kwargs)`

Parameters:

- **message** (str): The main log message
- **Custom Fields**: Pass additional fields directly as keyword arguments (e.g., reason, status)
- ***args, **kwargs**: Additional arguments passed to the underlying logger

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the Repository
   ```bash
   git clone https://github.com/djh00t/klog.git
   ```

2. Create a Feature Branch
   ```bash
   git checkout -b feature/my-feature
   ```

3. Commit Your Changes
   ```bash
   git commit -am 'Add new feature'
   ```

4. Push to the Branch
   ```bash
   git push origin feature/my-feature
   ```

5. Create a Pull Request
   - Submit a pull request detailing your changes.

## License

KLog is released under the MIT License. See [LICENSE](LICENSE) file for details.

## Acknowledgements

- Inspired by Python's built-in logging module
- Uses Jinja2 for templating
- Thanks to all contributors and users who have provided feedback

## Contact

For questions or feedback:
- Open an issue on [GitHub](https://github.com/djh00t/klog/issues)
- Contact the maintainer: [David Hooton](mailto:klog+david@hooton.org)
