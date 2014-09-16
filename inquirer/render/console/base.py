# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
from blessings import Terminal
import readchar


class ConsoleRender(object):
    def __init__(self, key_generator=None, terminal=None, *args, **kwargs):
        super(ConsoleRender, self).__init__(*args, **kwargs)
        self._key_gen = key_generator or readchar.readkey
        self.terminal = terminal or Terminal()
        self.answers = {}

    def render(self, question):
        self.print_header(self.get_message(question))

        self.reserve_height(self.get_height(question))

        return self.run(question)

    def render_error(self, message):
        if message:
            self.render_in_bottombar(
                '{t.red}>> {t.normal}{t.bold}{msg}{t.normal} '
                .format(msg=message, t=self.terminal)
                )

    def print_header(self, message):
        message = (message[:self.terminal.width - 9] + '...'
                   if len(message) > self.terminal.width - 6
                   else message)
        self.print_line('[{t.yellow}?{t.normal}] {msg}: ', msg=message)

    def reserve_height(self, size):
        for i in range(size):
            print('')
        print(self.terminal.clear_eos())

    def render_in_bottombar(self, message):
        with self.terminal.location(0, self.terminal.height - 1):
            self.terminal.clear_eos()
            self.print_str(message)

    def print_option(self, message, symbol, color):
        self.print_line(' {color}{s} {m}{t.normal}',
                        m=message, color=color, s=symbol)

    def print_line(self, base, **kwargs):
        self.print_str(base + self.terminal.clear_eol(), lf=True, **kwargs)

    def print_str(self, base, lf=False, **kwargs):
        print(base.format(t=self.terminal, **kwargs), end='\n' if lf else '')
        sys.stdout.flush()

    def clear_eos(self, lf=True):
        print(self.terminal.clear_eos(), end='\n' if lf else '')
