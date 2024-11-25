import re

_ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def remove_color_and_style_special_chars(text):
    return _ANSI_ESCAPE.sub('', text)
