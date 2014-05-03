# -*- coding: utf-8 -*-

import getpass
from blessings import Terminal
from . import errors
import getch


try:
    input = raw_input
except NameError:
    pass


class Render(object):
    def render(self, question):
        raise NotImplemented("Abstract method")


class ConsoleRender(Render):
    def __init__(self, *args, **kwargs):
        super(ConsoleRender, self).__init__(*args, **kwargs)
        self.terminal = Terminal()
        self.answers = {}

    def render(self, question, answers=None):
        self.answers = answers or {}
        message = ''
        print self.terminal.clear_eos(),

        while True:
            if question.ignore(self.answers):
                return question.default(self.answers)
            self.render_error(message)
            render = getattr(self, 'render_as_' + question.kind, None)
            if not render:
                raise errors.UnknownQuestionTypeError()
            result = render(question)
            try:
                question.validate(self.answers, result)
                return result
            except errors.ValidationError:
                message = 'Invalid value.'

    def render_as_text(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            print self.terminal.clear_eos(),
            message = ('[{t.yellow}?{t.normal}] {msg}: '
                       .format(msg=question.message, t=self.terminal))
            return input(message)

    def render_as_password(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            print self.terminal.clear_eos(),
            message = ('[{t.yellow}?{t.normal}] {msg}: '
                       .format(msg=question.message, t=self.terminal))
            return getpass.getpass(message)

    def render_as_confirm(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            print self.terminal.clear_eos(),
            confirm = '(Y/n)' if question.default(self.answers) else '(y/N)'
            message = ('[{t.yellow}?{t.normal}] {msg} {c}: '
                       .format(msg=question.message,
                               t=self.terminal,
                               c=confirm))

            answer = input(message)
            if answer == '':
                return question.default(self.answers)
            return answer in ('y', 'Y')

    def render_as_list(self, question):
        choices = question.choices(self.answers)
        try:
            selection = choices.index(question.default(self.answers))
        except ValueError:
            selection = 0

        message = ('[{t.yellow}?{t.normal}] {msg}: '
                   .format(msg=question.message, t=self.terminal))
        print message
        for choice in choices:
            print
        print self.terminal.clear_eos()

        while True:
            with self.terminal.location(0, self.terminal.height - 2 - len(choices)):
                for choice in choices:
                    if choice == choices[selection]:
                        print (' {t.blue}> {c}{t.normal}'
                               .format(c=choice, t=self.terminal))
                    else:
                        print ('   {c}'.format(c=choice))
                key = getch.get_key()
                if key == getch.UP:
                    selection = max(0, selection - 1)
                    continue
                if key == getch.DOWN:
                    selection = min(len(choices) - 1, selection + 1)
                    continue
                if key == getch.ENTER:
                    return choices[selection]
                if key == getch.CTRL_c:
                    raise errors.Aborted()

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
