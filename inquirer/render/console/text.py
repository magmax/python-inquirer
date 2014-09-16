# -*- coding: utf-8 -*-

from readchar import key
from .base import ConsoleRender


class Text(ConsoleRender):
    title_inline = True

    def __init__(self, *args, **kwargs):
        super(Text, self).__init__(*args, **kwargs)
        self.current = self.question.default or ''

    def get_message(self, question):
        if question.default:
            template = '{msg} ({default})'
        else:
            template = '{msg}'
        return (template.format(msg=question.message,
                                default=question.default or ''))

    def get_options(self):
        return []

    def process_input(self, pressed):
        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()
        if pressed in (key.CR, key.LF, key.ENTER):
            return self.current
        if len(pressed) != 1:
            return
        if pressed == key.BACKSPACE:
            if len(self.current):
                self.current = self.current[:-1]
                self.print_str(self.terminal.move_left
                               + self.terminal.clear_eol)
            return

        self.current += pressed
        self.print_str(pressed)
