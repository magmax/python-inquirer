# -*- coding: utf-8 -*-

import questions
from blessings import Terminal

class Render(object):
    def render(self, question):
        raise NotImplemented("Abstract method")


class ConsoleRender(Render):
    def __init__(self, *args, **kwargs):
        super(ConsoleRender, self).__init__(*args, **kwargs)
        self.terminal = Terminal()

    def render(self, question):
        if question.kind == 'text':
            return self.render_as_text(question)

    def render_as_text(self, question):
        self.terminal.clear_eos()
        with self.terminal.location(0, self.terminal.height - 2):
            self.terminal.clear_eos()
            message = ('[{t.yellow}?{t.normal}] {msg}: '
                       .format(msg=question.message, t=self.terminal))
            result = question.default if question.ignore else raw_input(message)
            print
        return question.name, result

    def print_in_bar(self, message):
        with self.terminal.location(0, self.terminal.height - 1):
            print message,
