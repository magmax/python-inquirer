# -*- coding: utf-8 -*-

from .base import safe_input, ConsoleRender


class Confirm(ConsoleRender):

    def render(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            self.clear_eos(lf=False)
            confirm = '(Y/n)' if question.default else '(y/N)'
            message = ('[{t.yellow}?{t.normal}] {msg} {c}: '
                       .format(msg=question.message,
                               t=self.terminal,
                               c=confirm))

            answer = safe_input(message)
            if answer == '':
                return question.default
            return answer in ('y', 'Y')
