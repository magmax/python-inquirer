# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
from blessings import Terminal
from . import errors
from . import getch


# Fixes for python 3 compatibility
try:
    input = raw_input
except NameError:
    pass


class Render(object):
    def render(self, question):
        raise NotImplemented("Abstract method")


class ConsoleRender(Render):
    def __init__(self, *args, **kwargs):
        super(ConsoleRender, self).__init__(*args, **kwargs)
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
            render = getattr(self, 'render_as_' + question.kind, None)
            if not render:
                raise errors.UnknownQuestionTypeError()
            result = render(question)
            try:
                question.validate(result)
                return result
            except errors.ValidationError:
                message = 'Invalid value for {q}.'.format(q=question.name)

    def render_as_text(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            message = ('[{t.yellow}?{t.normal}] {msg}: '
                       .format(msg=question.message,
                               t=self.terminal))
            return input(message)

    def render_as_password(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            self.terminal.clear_eos(False)
            self._print_str('[{t.yellow}?{t.normal}] {msg}: ',
                            msg=question.message)
            password = ''
            while True:
                key = getch.get_key()
                if key == getch.CTRL_C:
                    raise errors.Aborted()
                if key == getch.ENTER:
                    break
                if len(key) != 1:
                    continue
                if key == getch.BACKSPACE:
                    if len(password):
                        password = password[:-1]
                        print(self.terminal.move_left, end='')
                        print(self.terminal.clear_eol, end='')
                else:
                    password += key
                    print('*', end='')
            return password

    def render_as_confirm(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            print(self.terminal.clear_eos(), end='')
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
                        self._print_line(' {t.blue}> {c}{t.normal}',
                                         c=choice)
                    else:
                        self._print_line('   {c}', c=choice)
                key = getch.get_key()
                if key == getch.UP:
                    current = max(0, current - 1)
                    continue
                if key == getch.DOWN:
                    current = min(len(choices) - 1, current + 1)
                    continue
                if key == getch.ENTER:
                    return choices[current]
                if key == getch.CTRL_C:
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
                key = getch.get_key()
                if key == getch.UP:
                    current = max(0, current - 1)
                    continue
                elif key == getch.DOWN:
                    current = min(len(choices) - 1, current + 1)
                    continue
                elif key == getch.SPACE:
                    if current in selection:
                        selection.remove(current)
                    else:
                        selection.append(current)
                elif key == getch.LEFT:
                    if current in selection:
                        selection.remove(current)
                elif key == getch.RIGHT:
                    if current not in selection:
                        selection.append(current)
                elif key == getch.ENTER:
                    return [choices[x] for x in selection]
                elif key == getch.CTRL_C:
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
