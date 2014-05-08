# -*- coding: utf-8 -*-

from __future__ import print_function

from blessings import Terminal
import readchar
# from inquirer import errors


# Fixes for python 3 compatibility
try:
    safe_input = raw_input
except NameError:
    safe_input = input


class ConsoleRender(object):
    def __init__(self, key_generator=None, *args, **kwargs):
        super(ConsoleRender, self).__init__(*args, **kwargs)
        self._key_gen = key_generator or readchar.readkey
        self.terminal = Terminal()
        self.answers = {}
