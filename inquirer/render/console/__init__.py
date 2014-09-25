# -*- coding: utf-8 -*-
from __future__ import print_function

from blessings import Terminal

from inquirer import errors
from inquirer import events

from .text import Text
from .password import Password
from .confirm import Confirm
from .list import List
from .checkbox import Checkbox


class ConsoleRender(object):
    def __init__(self, event_generator=None, *args, **kwargs):
        super(ConsoleRender, self).__init__(*args, **kwargs)
        self._event_gen = event_generator or events.KeyEventGenerator()
        self.terminal = Terminal()
        self._previous_error = None

    def reset(self):
        print(self.terminal.move(0, 0) + self.terminal.clear_eos())

    def render(self, question, answers=None):
        question.answers = answers or {}

        if question.ignore:
            return question.default

        clazz = self.render_factory(question.kind)
        render = clazz(question, self.terminal)

        render.clear_eos()

        try:
            return self._event_loop(render)
        finally:
            print('')

    def _event_loop(self, render):
        try:
            while True:
                self._print_status_bar(render)

                with render.terminal.location():
                    render.print_header()
                    render.print_options()

                    self._process_input(render)
        except errors.EndOfInput as e:
            return e.selection

    def _print_status_bar(self, render):
        if self._previous_error is None:
            render.clear_bottombar()
            return

        render.render_error(self._previous_error)
        self._previous_error = None

    def _process_input(self, render):
        try:
            ev = self._event_gen.next()
            if isinstance(ev, events.KeyPressed):
                render.process_input(ev.value)
        except errors.EndOfInput as e:
            try:
                render.question.validate(e.selection)
                raise
            except errors.ValidationError as e:
                self._previous_error = ('"{e}" is not a valid {q}.'
                                        .format(e=e.value,
                                                q=render.question.name))

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
