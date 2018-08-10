from __future__ import print_function

__version__ = '2.3.0'

try:
    from .prompt import prompt
    from .questions import Text, Password, Confirm, List, Checkbox, \
        load_from_dict, load_from_json
    from .shortcuts import text, password, confirm, list_input, checkbox

    __all__ = ['prompt', 'Text', 'Password', 'Confirm', 'List', 'Checkbox',
               'load_from_list', 'load_from_dict', 'load_from_json',
               'text', 'password', 'confirm', 'list_input', 'checkbox']
except ImportError as e:
    print("An error was found, but returning just with the version: %s" % e)
