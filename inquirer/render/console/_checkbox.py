# -*- coding: utf-8 -*-

from readchar import key
from .base import BaseConsoleRender
from inquirer import errors


class Checkbox(BaseConsoleRender):
    def __init__(self, *args, **kwargs):
        super(Checkbox, self).__init__(*args, **kwargs)
        self.selection = [k for (k, v) in enumerate(self.question.choices)
                          if v in (self.question.default or [])]
        self.current = 0

    def get_options(self):
        for n in range(len(self.question.choices)):
            choice = self.question.choices[n]
            if n in self.selection:
                symbol = 'X'
                color = self.terminal.yellow + self.terminal.bold
            else:
                symbol = 'o'
                color = ''
            selector = ' '
            if n == self.current:
                selector = '>'
                color = self.terminal.blue
            yield choice, selector + ' ' + symbol, color

    def process_input(self, pressed):
        if pressed == key.UP:
            self.current = max(0, self.current - 1)
            return
        elif pressed == key.DOWN:
            self.current = min(len(self.question.choices) - 1,
                               self.current + 1)
            return
        elif pressed == key.SPACE:
            if self.current in self.selection:
                self.selection.remove(self.current)
            else:
                self.selection.append(self.current)
        elif pressed == key.LEFT:
            if self.current in self.selection:
                self.selection.remove(self.current)
        elif pressed == key.RIGHT:
            if self.current not in self.selection:
                self.selection.append(self.current)
        elif pressed == key.ENTER:
            result = []
            for x in self.selection:
                value = self.question.choices[x]
                result.append(getattr(value, 'value', value))
            raise errors.EndOfInput(result)
        elif pressed == key.CTRL_C:
            raise KeyboardInterrupt()
