# -*- coding: utf-8 -*-

from readchar import key
from inquirer import errors
from .base import BaseConsoleRender


class Confirm(BaseConsoleRender):
    title_inline = True

    def get_header(self):
        confirm = '(Y/n)' if self.question.default else '(y/N)'
        return ('{msg} {c}'
                .format(msg=self.question.message,
                        c=confirm))

    def process_input(self, pressed):
        if pressed.lower() == key.ENTER:
            raise errors.EndOfInput(self.question.default)

        print(pressed)

        if pressed in 'yY':
            raise errors.EndOfInput(True)
        if pressed in 'nN':
            raise errors.EndOfInput(False)
        raise errors.ValidationError(pressed)
