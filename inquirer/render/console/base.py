# -*- coding: utf-8 -*-

from __future__ import print_function

from blessings import Terminal

# Should be odd number as there is always one question selected
MAX_OPTIONS_DISPLAYED_AT_ONCE = 13
half_options = int((MAX_OPTIONS_DISPLAYED_AT_ONCE - 1) / 2)


class BaseConsoleRender(object):
    title_inline = False

    def __init__(self, question, theme=None, terminal=None, show_default=False,
                 *args, **kwargs):
        super(BaseConsoleRender, self).__init__(*args, **kwargs)
        self.question = question
        self.terminal = terminal or Terminal()
        self.answers = {}
        self.theme = theme
        self.show_default = show_default

    def get_header(self):
        return self.question.message

    def get_current_value(self):
        return ''

    def get_options(self):
        return []

    def process_input(self, pressed):
        raise NotImplementedError('Abstract')

    def handle_validation_error(self, error):
        if error.reason:
            return error.reason

        return '"{e}" is not a valid {q}.'.format(e=error.value,
                                                  q=self.question.name)
