# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
from blessings import Terminal
import readchar

from inquirer import errors
from inquirer.render.console.text import Text
from inquirer.render.console.password import Password


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

        while True:
            if question.ignore:
                return question.default
            if not message:
                self.clear_eos()
            self.render_error(message)
            message = ''
            if question.kind == 'text':
                render = Text(self._key_gen, self.terminal)
                result = render.render(question)
                try:
                    question.validate(result)
                    return result
                except errors.ValidationError:
                    message = 'Invalid value for {q}.'.format(q=question.name)
            elif question.kind == 'password':
                render = Password(self._key_gen, self.terminal)
                result = render.render(question)
                try:
                    question.validate(result)
                    return result
                except errors.ValidationError:
                    message = 'Invalid value for {q}.'.format(q=question.name)
            else:
                render = getattr(self, 'render_as_' + question.kind, None)
                if not render:
                    raise errors.UnknownQuestionTypeError()
                result = render(question)
                try:
                    question.validate(result)
                    return result
                except errors.ValidationError:
                    message = 'Invalid value for {q}.'.format(q=question.name)

    def render_as_confirm(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            self.clear_eos(lf=False)
            confirm = '(Y/n)' if question.default else '(y/N)'
            message = ('[{t.yellow}?{t.normal}] {msg} {c}: '
                       .format(msg=question.message,
                               t=self.terminal,
                               c=confirm))

            answer = input(message)
            if answer == '':
                return question.default
            return answer in ('y', 'Y')

    def render_as_list(self, question):
        choices = question.choices
        try:
            current = choices.index(question.default)
        except ValueError:
            current = 0

        self._print_line('[{t.yellow}?{t.normal}] {msg}: ',
                         msg=question.message)
        for choice in choices:
            print('')
        print(self.terminal.clear_eos())

        pos_y = self.terminal.height - 2 - len(choices)

        while True:
            with self.terminal.location(0, pos_y):
                for choice in choices:
                    if choice == choices[current]:
                        color = self.terminal.blue
                        symbol = '>'
                    else:
                        color = self.terminal.normal
                        symbol = ' '
                    self._print_line(' {color}{s} {c}{t.normal}',
                                     c=choice, color=color, s=symbol)
                key = self._key_gen()
                if key == readchar.key.UP:
                    current = max(0, current - 1)
                    continue
                if key == readchar.key.DOWN:
                    current = min(len(choices) - 1, current + 1)
                    continue
                if key == readchar.key.ENTER:
                    return choices[current]
                if key == readchar.key.CTRL_C:
                    raise errors.Aborted()

    def render_as_checkbox(self, question):
        choices = question.choices
        selection = []
        current = 0

        self._print_line('[{t.yellow}?{t.normal}] {msg}: ',
                         msg=question.message)
        for choice in choices:
            print('')
        print(self.terminal.clear_eos())

        pos_y = self.terminal.height - 2 - len(choices)

        while True:
            with self.terminal.location(0, pos_y):
                for n in range(len(choices)):
                    choice = choices[n]
                    if n in selection:
                        symbol = 'X'
                        color = self.terminal.yellow + self.terminal.bold
                    else:
                        symbol = 'o'
                        color = ''
                    selector = ' '
                    if n == current:
                        selector = '>'
                        color = self.terminal.blue
                    self._print_line(' {color}{sel} {s} {c}{t.normal}',
                                     c=choice, s=symbol, sel=selector,
                                     color=color)
                key = self._key_gen()
                if key == readchar.key.UP:
                    current = max(0, current - 1)
                    continue
                elif key == readchar.key.DOWN:
                    current = min(len(choices) - 1, current + 1)
                    continue
                elif key == readchar.key.SPACE:
                    if current in selection:
                        selection.remove(current)
                    else:
                        selection.append(current)
                elif key == readchar.key.LEFT:
                    if current in selection:
                        selection.remove(current)
                elif key == readchar.key.RIGHT:
                    if current not in selection:
                        selection.append(current)
                elif key == readchar.key.ENTER:
                    return [choices[x] for x in selection]
                elif key == readchar.key.CTRL_C:
                    raise errors.Aborted()

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

    def _print_line(self, base, **kwargs):
        self._print_str(base + self.terminal.clear_eol(), lf=True, **kwargs)

    def _print_str(self, base, lf=False, **kwargs):
        print(base.format(t=self.terminal, **kwargs), end='\n' if lf else '')
        sys.stdout.flush()

    def clear_eos(self, lf=True):
        print(self.terminal.clear_eos(), end='\n' if lf else '')
