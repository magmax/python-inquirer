# -*- coding: utf-8 -*-

from .base import safe_input, ConsoleRender


class Text(ConsoleRender):

    def render(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            message = ('[{t.yellow}?{t.normal}] {msg}: '
                       .format(msg=question.message,
                               t=self.terminal))
            return safe_input(message)
