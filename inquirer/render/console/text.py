# -*- coding: utf-8 -*-

from readchar import key
from .base import ConsoleRender


class Text(ConsoleRender):
    title_inline = True

    def get_message(self, question):
        if question.default:
            template = '{msg} ({default})'
        else:
            template = '{msg}'
        return (template.format(msg=question.message,
                                default=question.default or ''))

    def run(self, question):
        text = question.default or ''
        with self.terminal.location(0, self.terminal.height):
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
