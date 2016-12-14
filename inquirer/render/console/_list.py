# -*- coding: utf-8 -*-

from readchar import key
from .base import BaseConsoleRender
from inquirer import errors


class List(BaseConsoleRender):
    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.current = self._current_index()

    def get_options(self):
        choices = self.question.choices

        for choice in choices:
            selected = choice == choices[self.current]

            if selected:
                color = self.terminal.blue
                symbol = '>'
            else:
                color = self.terminal.normal
                symbol = ' '
            yield choice, symbol, color

    def process_input(self, pressed):
        question = self.question
        if pressed == key.UP:
            if not question.carousel or self.current != 0:
                self.current = max(0, self.current - 1)
            else:
                self.current = len(question.choices) - 1
            return
        if pressed == key.DOWN:
            if not question.carousel or self.current != len(question.choices) - 1:
                self.current = min(len(self.question.choices) - 1,
                               self.current + 1)
            else:
                self.current = 0
            return
        if pressed == key.ENTER:
            value = self.question.choices[self.current]
            raise errors.EndOfInput(getattr(value, 'value', value))

            raise errors.EndOfInput(self.question.choices[self.current])
        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()

    def _current_index(self):
        try:
            return self.question.choices.index(self.question.default)
        except ValueError:
            return 0
