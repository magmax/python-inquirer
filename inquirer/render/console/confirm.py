# -*- coding: utf-8 -*-

from readchar import key
from inquirer import errors
from .base import ConsoleRender


class Confirm(ConsoleRender):

    def render(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            confirm = '(Y/n)' if question.default else '(y/N)'
            message = ('[{t.yellow}?{t.normal}] {msg} {c}: '
                       .format(msg=question.message,
                               t=self.terminal,
                               c=confirm))

            self.print_str(message)
            answer = self._key_gen()
            if answer.lower() == key.ENTER:
                return question.default
            self.print_str(answer)
            if answer in 'yY':
                return True
            if answer in 'nN':
                return False
            raise errors.ValidationError()
