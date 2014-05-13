# -*- coding: utf-8 -*-

from readchar import key
from .base import ConsoleRender


class Text(ConsoleRender):

    def render(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            text = question.default or ''
            message = ('[{t.yellow}?{t.normal}] {msg}: {default}'
                       .format(msg=question.message,
                               t=self.terminal,
                               default=text))
            self.print_str(message)
            while True:
                pressed = self._key_gen()
                if pressed == key.CTRL_C:
                    raise KeyboardInterrupt()
                if pressed in (key.CR, key.LF, key.ENTER):
                    break
                if len(pressed) != 1:
                    continue
                if pressed == key.BACKSPACE:
                    if len(text):
                        text = text[:-1]
                        self.print_str(self.terminal.move_left
                                       + self.terminal.clear_eol)
                else:
                    text += pressed
                    self.print_str(pressed)

            return text
