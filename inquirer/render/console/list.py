# -*- coding: utf-8 -*-

from readchar import key
from .base import ConsoleRender


class List(ConsoleRender):

    def render(self, question):
        choices = question.choices
        try:
            current = choices.index(question.default)
        except ValueError:
            current = 0

        self.print_line('[{t.yellow}?{t.normal}] {msg}: ',
                        msg=question.message)
        for choice in choices:
            print('')
        print(self.terminal.clear_eos())

        pos_y = self.terminal.height - 2 - len(choices)

        while True:
            with self.terminal.location(0, pos_y):
                for choice in choices:
                    if choice == choices[current]:
                        color = self.terminal.blue
                        symbol = '>'
                    else:
                        color = self.terminal.normal
                        symbol = ' '
                    self.print_line(' {color}{s} {c}{t.normal}',
                                    c=choice, color=color, s=symbol)
                pressed = self._key_gen()
                if pressed == key.UP:
                    current = max(0, current - 1)
                    continue
                if pressed == key.DOWN:
                    current = min(len(choices) - 1, current + 1)
                    continue
                if pressed == key.ENTER:
                    return choices[current]
                if pressed == key.CTRL_C:
                    raise KeyboardInterrupt()
