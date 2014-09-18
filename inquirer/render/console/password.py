# -*- coding: utf-8 -*-

from readchar import key
from inquirer import errors
from .base import ConsoleRender


class Password(ConsoleRender):
    title_inline = True

    def __init__(self, *args, **kwargs):
        super(Password, self).__init__(*args, **kwargs)
        self.current = ''

    def process_input(self, pressed):
        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()
        if pressed == key.ENTER:
            raise errors.EndOfInput(self.current)
        if len(pressed) != 1:
            return
        if pressed == key.BACKSPACE:
            if len(self.current):
                self.current = self.current[:-1]
                self.print_str(self.terminal.move_left
                               + self.terminal.clear_eol)
        else:
            self.current += pressed
            self.print_str('*')
