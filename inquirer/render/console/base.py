# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
from blessings import Terminal


class BaseConsoleRender(object):
    title_inline = False

    def __init__(self, question, terminal=None,
                 *args, **kwargs):
        super(BaseConsoleRender, self).__init__(*args, **kwargs)
        self.question = question
        self.terminal = terminal or Terminal()
        self.answers = {}

    def get_header(self):
        return self.question.message

    def get_current_value(self):
        return ''

    def get_options(self):
        return []

    def read_input(self):
        raise NotImplemented('Abstract')

    def render_error(self, message):
        if message:
            symbol = '>> '
            size = len(symbol) + 1
            length = len(message)
            message = message.rstrip()
            message = (message
                       if length + size < self.width
                       else message[:self.width - (size + 3)] + '...')

            self.render_in_bottombar(
                '{t.red}{s}{t.normal}{t.bold}{msg}{t.normal} '
                .format(msg=message, s=symbol, t=self.terminal)
                )

    def print_header(self):
        base = self.terminal.clear_eol() + self.get_header()

        header = (base[:self.width - 9] + '...'
                  if len(base) > self.width - 6
                  else base)
        header += ': {c}'.format(c=self.get_current_value())
        self.print_str('[{t.yellow}?{t.normal}] {msg}',
                       msg=header,
                       lf=not self.title_inline)

    def print_options(self):
        for message, symbol, color in self.get_options():
            self.print_line(' {color}{s} {m}{t.normal}',
                            m=message, color=color, s=symbol)

    def render_in_bottombar(self, message):
        with self.terminal.location(0, self.height - 2):
            self.clear_eos()
            self.print_str(message)

    def clear_bottombar(self):
        with self.terminal.location(0, self.height - 2):
            self.clear_eos()

    def print_line(self, base, lf=True, **kwargs):
        self.print_str(base + self.terminal.clear_eol(), lf=lf, **kwargs)

    def print_str(self, base, lf=False, **kwargs):
        print(base.format(t=self.terminal, **kwargs), end='\n' if lf else '')
        sys.stdout.flush()

    def clear_eos(self, lf=True):
        print(self.terminal.clear_eos(), end='\n' if lf else '')

    @property
    def width(self):
        return self.terminal.width or 80

    @property
    def height(self):
        return self.terminal.width or 24
