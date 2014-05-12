# -*- coding: utf-8 -*-

from readchar import key
from .base import ConsoleRender


class Checkbox(ConsoleRender):

    def render(self, question):
        choices = question.choices
        selection = []
        current = 0

        self.print_line('[{t.yellow}?{t.normal}] {msg}: ',
                        msg=question.message)
        for choice in choices:
            self.print_line('')
        self.clear_eos()

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
                    self.print_line(' {color}{sel} {s} {c}{t.normal}',
                                    c=choice, s=symbol, sel=selector,
                                    color=color)
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
                    return [choices[x] for x in selection]
                elif pressed == key.CTRL_C:
                    raise KeyboardInterrupt()
