# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
from blessings import Terminal
import readchar

from inquirer import errors
from .text import Text
from .password import Password
from .confirm import Confirm
from .list import List
from .checkbox import Checkbox


# Fixes for python 3 compatibility
try:
    input = raw_input
except NameError:
    pass


class ConsoleRender(object):
    def __init__(self, key_generator=None, *args, **kwargs):
        super(ConsoleRender, self).__init__(*args, **kwargs)
        self._key_gen = key_generator or readchar.readkey
        self.terminal = Terminal()
        self.answers = {}

    def render(self, question, answers=None):
        self.answers = answers or {}
        question.answers = self.answers
        message = ''

        matrix = {
            'text': Text,
            'password': Password,
            'confirm': Confirm,
            'list': List,
            'checkbox': Checkbox,
            }

        while True:
            if question.ignore:
                return question.default
            if not message:
                self.clear_eos()
            self.render_error(message)
            message = ''
            if question.kind not in matrix:
                raise errors.UnknownQuestionTypeError()
            clazz = matrix.get(question.kind)
            render = clazz(self._key_gen, self.terminal)
            result = render.render(question)
            try:
                question.validate(result)
                return result
            except errors.ValidationError:
                message = 'Invalid value for {q}.'.format(q=question.name)

    def render_error(self, message):
        if message:
            self.render_in_bottombar(
                '{t.red}>> {t.normal}{t.bold}{msg}{t.normal} '
                .format(msg=message, t=self.terminal)
                )
        else:
            self.render_in_bottombar('')

    def render_in_bottombar(self, message):
        with self.terminal.location(0, self.terminal.height - 1):
            self.terminal.clear_eos()
            self._print_str(message)

    def _print_str(self, base, lf=False, **kwargs):
        print(base.format(t=self.terminal, **kwargs), end='\n' if lf else '')
        sys.stdout.flush()

    def clear_eos(self, lf=True):
        print(self.terminal.clear_eos(), end='\n' if lf else '')
