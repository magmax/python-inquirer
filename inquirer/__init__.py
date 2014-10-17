from __future__ import print_function

__version__ = '1.0.3'

try:
    from .prompt import prompt
    from .questions import Text, Password, Confirm, List, Checkbox

    __all__ = ['prompt', 'Text', 'Password', 'Confirm', 'List', 'Checkbox']
except ImportError as e:
    print("An error was found, but returning just with the version: %s" % e)
