# -*- coding: utf-8 -*-

from readchar import key
from .base import BaseConsoleRender
from inquirer import errors
import editor


class Editor(BaseConsoleRender):
    title_inline = True

    def __init__(self, *args, **kwargs):
        super(Editor, self).__init__(*args, **kwargs)
        self.current = ""

    def get_current_value(self):
        return "{}Press <enter> to launch your editor{}".format(
            self.theme.Editor.opening_prompt_color, self.terminal.normal
        )

    def handle_validation_error(self, error):
        if error.reason:
            return error.reason

        return "Entered value is not a valid {q}.".format(q=self.question.name)

    def process_input(self, pressed):
        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()

        if pressed in (key.CR, key.LF, key.ENTER):
            data = editor.edit(contents=self.question.default or "")
            raise errors.EndOfInput(data.decode("utf-8"))

        raise errors.ValidationError(
            "You have pressed unknown key! " "Press <enter> to open editor or " "CTRL+C to exit."
        )
