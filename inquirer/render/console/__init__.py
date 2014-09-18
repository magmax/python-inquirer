# -*- coding: utf-8 -*-
from __future__ import print_function

from blessings import Terminal
import readchar

from inquirer import errors
from .text import Text
from .password import Password
from .confirm import Confirm
from .list import List
from .checkbox import Checkbox


class ConsoleRender(object):
    def __init__(self, key_generator=None, *args, **kwargs):
        super(ConsoleRender, self).__init__(*args, **kwargs)
        self._key_gen = key_generator or readchar.readkey
        self.terminal = Terminal()

    def reset(self):
        print(self.terminal.move(0, 0) + self.terminal.clear_eos())

    def render(self, question, answers=None):
        question.answers = answers or {}

        if question.ignore:
            return question.default

        clazz = self.render_factory(question.kind)
        render = clazz(question, self._key_gen, self.terminal)

        render.clear_eos()

        return render.render()

    def render_factory(self, question_type):
        matrix = {
            'text': Text,
            'password': Password,
            'confirm': Confirm,
            'list': List,
            'checkbox': Checkbox,
            }

        if question_type not in matrix:
            raise errors.UnknownQuestionTypeError()
        return matrix.get(question_type)

    def move_to_end(self):
        print(self.terminal.move(0, 7))
