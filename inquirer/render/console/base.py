# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
from blessings import Terminal
import readchar
from inquirer import errors

class ConsoleRender(object):
    title_inline = False

    def __init__(self, question, key_generator=None, terminal=None, *args, **kwargs):
        super(ConsoleRender, self).__init__(*args, **kwargs)
        self._key_gen = key_generator or readchar.readkey
        self.question = question
        self.terminal = terminal or Terminal()
        self.answers = {}

    def render(self):
        height = self.get_height()
        pos_y = self.terminal.height - 3 - height

        self.reserve_height(height)

        try:
            result = None
            while result is None:
                with self.terminal.location(0, pos_y):
                    self.print_header()
                    self.print_options()

                    self.process_input(self._key_gen())
        except errors.EndOfInput as e:
            return e.selection
        except KeyboardInterrupt:
            self.print_line('Cancelled by user')
            raise

    def get_height(self):
        return 1

    def get_header(self):
        return self.question.message

    def get_options(self):
        raise NotImplemented('Abstract')

    def read_input(self):
        raise NotImplemented('Abstract')

    def render_error(self, message):
        if message:
            self.render_in_bottombar(
                '{t.red}>> {t.normal}{t.bold}{msg}{t.normal} '
                .format(msg=message, t=self.terminal)
                )

    def print_header(self):
        base = self.get_header()

        header = (base[:self.terminal.width - 9] + '...'
                   if len(base) > self.terminal.width - 6
                   else base)
        self.print_str('[{t.yellow}?{t.normal}] {msg}: ', msg=header, lf=not self.title_inline)

    def print_options(self):
        for message, symbol, color in self.get_options():
            self.print_line(' {color}{s} {m}{t.normal}',
                            m=message, color=color, s=symbol)

    def reserve_height(self, size):
        if self.title_inline:
            return
        for i in range(size):
            print('')
        print(self.terminal.clear_eos())

    def render_in_bottombar(self, message):
        with self.terminal.location(0, self.terminal.height - 1):
            self.terminal.clear_eos()
            self.print_str(message)

    def print_line(self, base, lf=True, **kwargs):
        self.print_str(base + self.terminal.clear_eol(), lf=lf, **kwargs)

    def print_str(self, base, lf=False, **kwargs):
        print(base.format(t=self.terminal, **kwargs), end='\n' if lf else '')
        sys.stdout.flush()

    def clear_eos(self, lf=True):
        print(self.terminal.clear_eos(), end='\n' if lf else '')
