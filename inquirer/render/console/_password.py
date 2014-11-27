# -*- coding: utf-8 -*-

from readchar import key
from inquirer import errors
from .base import BaseConsoleRender


class Password(BaseConsoleRender):
    title_inline = True

    def __init__(self, *args, **kwargs):
        super(Password, self).__init__(*args, **kwargs)
        self.current = ''

    def get_current_value(self):
        return '*' * len(self.current)

    def process_input(self, pressed):
        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()

        if pressed == key.ENTER:
            raise errors.EndOfInput(self.current)

        if pressed == key.BACKSPACE:
            if len(self.current):
                self.current = self.current[:-1]
            return

        if len(pressed) != 1:
            return

        self.current += pressed
