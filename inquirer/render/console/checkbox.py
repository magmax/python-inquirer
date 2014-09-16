# -*- coding: utf-8 -*-

from readchar import key
from .base import ConsoleRender
from inquirer import errors


class Checkbox(ConsoleRender):

    def get_message(self, question):
        return question.message

    def get_height(self, question):
        return len(question.choices)

    def run(self, question):
        choices = question.choices
        selection = []
        current = 0

        pos_y = self.terminal.height - 2 - len(choices)

        while True:
            with self.terminal.location(0, pos_y):
                for n in range(len(choices)):
                    choice = choices[n]
                    if n in selection:
                        symbol = 'X'
                        color = self.terminal.yellow + self.terminal.bold
                    else:
                        symbol = 'o'
                        color = ''
                    selector = ' '
                    if n == current:
                        selector = '>'
                        color = self.terminal.blue
                    self.print_option(choice, selector + ' ' + symbol, color)
                pressed = self._key_gen()
                if pressed == key.UP:
                    current = max(0, current - 1)
                    continue
                elif pressed == key.DOWN:
                    current = min(len(choices) - 1, current + 1)
                    continue
                elif pressed == key.SPACE:
                    if current in selection:
                        selection.remove(current)
                    else:
                        selection.append(current)
                elif pressed == key.LEFT:
                    if current in selection:
                        selection.remove(current)
                elif pressed == key.RIGHT:
                    if current not in selection:
                        selection.append(current)
                elif pressed == key.ENTER:
                    raise errors.EndOfInput([choices[x] for x in selection])
                elif pressed == key.CTRL_C:
                    raise KeyboardInterrupt()
