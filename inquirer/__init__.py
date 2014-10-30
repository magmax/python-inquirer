from __future__ import print_function

__version__ = '2.0.1'

try:
    from .prompt import prompt
    from .questions import Text, Password, Confirm, List, Checkbox, Question

    __all__ = ['prompt', 'Text', 'Password', 'Confirm', 'List', 'Checkbox', 'Question']
except ImportError as e:
    print("An error was found, but returning just with the version: %s" % e)
