# -*- coding: utf-8 -*-

import getpass
import questions
import errors
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
        self.terminal.clear_eos()

        while True:
            self.render_error(message)
            if question.kind == 'text':
                result = self.render_as_text(question)
            elif question.kind == 'password':
                result = self.render_as_password(question)
            elif question.kind == 'confirm':
                result = self.render_as_confirm(question)
            else:
                raise errors.UnknownQuestionTypeError()
            try:
                question.validate(result)
                print()
                return result
            except errors.ValidationError:
                message = 'Invalid value.'

    def render_as_text(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            self.terminal.clear_eos()
            message = ('[{t.yellow}?{t.normal}] {msg}: '
                       .format(msg=question.message, t=self.terminal))
            return question.default if question.ignore else raw_input(message)

    def render_as_password(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            self.terminal.clear_eos()
            message = ('[{t.yellow}?{t.normal}] {msg}: '
                       .format(msg=question.message, t=self.terminal))
            return question.default if question.ignore else getpass.getpass(message)

    def render_as_confirm(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            self.terminal.clear_eos()
            confirm = '(Y/n)' if question.default else '(y/N)'
            message = ('[{t.yellow}?{t.normal}] {msg} {c}: '
                       .format(msg=question.message, t=self.terminal, c=confirm))

            if question.ignore:
                return question.default

            answer = raw_input(message)
            if answer == '':
                return question.default
            return answer in ('y', 'Y')

    def render_error(self, message):
        if message:
            self.render_in_bottombar(
                '{t.red}>> {t.normal}{t.bold}{msg}{t.normal} '
                .format(msg=message, t=self.terminal)
                )
        else:
            self.render_in_bottombar('')

    def render_in_bottombar(self, message):
        with self.terminal.location(0, self.terminal.height - 1):
            self.terminal.clear_eos()
            print(message),
