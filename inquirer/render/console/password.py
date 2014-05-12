# -*- coding: utf-8 -*-

from readchar import key

from .base import ConsoleRender


class Password(ConsoleRender):

    def render(self, question):
        with self.terminal.location(0, self.terminal.height - 2):
            self.terminal.clear_eos(False)
            self.print_str('[{t.yellow}?{t.normal}] {msg}: ',
                           msg=question.message)
            password = ''
            while True:
                pressed = self._key_gen()
                if pressed == key.CTRL_C:
                    raise KeyboardInterrupt()
                if pressed == key.ENTER:
                    break
                if len(pressed) != 1:
                    continue
                if pressed == key.BACKSPACE:
                    if len(password):
                        password = password[:-1]
                        self.print_str(self.terminal.move_left
                                       + self.terminal.clear_eol)
                else:
                    password += pressed
                    self.print_str('*')
            return password
