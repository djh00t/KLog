# klog/text_styles.py

COLOR_CODES = {
    "light_red": "\u001b[91m",
    "red": "\u001b[31m",
    "dark_red": "\u001b[31;2m",
    "light_green": "\u001b[92m",
    "green": "\u001b[32m",
    "dark_green": "\u001b[32;2m",
    "light_yellow": "\u001b[93m",
    "yellow": "\u001b[33m",
    "dark_yellow": "\u001b[33;2m",
    "light_orange": "\u001b[38;5;215m",
    "orange": "\u001b[38;5;208m",
    "dark_orange": "\u001b[38;5;202m",
    "light_blue": "\u001b[94m",
    "blue": "\u001b[34m",
    "dark_blue": "\u001b[34;2m",
    "light_purple": "\u001b[95m",
    "purple": "\u001b[35m",
    "dark_purple": "\u001b[35;2m",
    "light_pink": "\u001b[95m",
    "pink": "\u001b[38;5;205m",
    "dark_pink": "\u001b[38;5;95m",
    "white": "\u001b[37m",
    "grey": "\u001b[90m",
    "black": "\u001b[30m",
    "reset": "\u001b[0m",
}

STYLE_CODES = {
    "bold": "\u001b[1m",
    "italic": "\u001b[3m",
    "underlined": "\u001b[4m",
    "blink": "\u001b[5m",
    "reverse": "\u001b[7m",
    "hidden": "\u001b[8m",
    "default": "",
}
