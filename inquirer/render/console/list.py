# -*- coding: utf-8 -*-

from readchar import key
from .base import ConsoleRender
from inquirer import errors


class List(ConsoleRender):

    def get_message(self, question):
        return question.message

    def get_height(self, question):
        return len(question.choices)

    def run(self, question):
        choices = question.choices
        current = self._current_index(question)
        pos_y = self.terminal.height - 2 - len(choices)

        while True:
            with self.terminal.location(0, pos_y):
                for choice in choices:
                    self._print_choice(choice, choice == choices[current])
                pressed = self._key_gen()
                if pressed == key.UP:
                    current = max(0, current - 1)
                    continue
                if pressed == key.DOWN:
                    current = min(len(choices) - 1, current + 1)
                    continue
                if pressed == key.ENTER:
                    raise errors.EndOfInput(choices[current])
                if pressed == key.CTRL_C:
                    raise KeyboardInterrupt()

    def _current_index(self, question):
        try:
            return question.choices.index(question.default)
        except ValueError:
            return 0

    def _print_choice(self, choice, selected):
        if selected:
            color = self.terminal.blue
            symbol = '>'
        else:
            color = self.terminal.normal
            symbol = ' '
        self.print_option(choice, symbol, color)
