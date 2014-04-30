# -*- coding: utf-8 -*-

import questions
import exceptions
from blessings import Terminal

class Render(object):
    def render(self, question):
        raise NotImplemented("Abstract method")


class ConsoleRender(Render):
    def __init__(self, *args, **kwargs):
        super(ConsoleRender, self).__init__(*args, **kwargs)
        self.terminal = Terminal()

    def render(self, question):
        message = ''
        while True:
            try:
                if question.kind == 'text':
                    result = self.render_as_text(question, message)
                question.validate(result)
                return result
            except exceptions.ValidationError:
                message = 'Invalid value.'

    def render_as_text(self, question, bar_message):
        self.terminal.clear_eos()
        with self.terminal.location(0, self.terminal.height - 2):
            self.terminal.clear_eos()
            self.print_in_bar(bar_message)
            message = ('[{t.yellow}?{t.normal}] {msg}: '
                       .format(msg=question.message, t=self.terminal))
            result = question.default if question.ignore else raw_input(message)
            print
        return result

    def print_in_bar(self, message):
        with self.terminal.location(0, self.terminal.height - 1):
            print message,
