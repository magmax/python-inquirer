from typing import Any

from readchar import key

from inquirer import errors
from inquirer.render.console.base import BaseConsoleRender


class Confirm(BaseConsoleRender):
    title_inline: bool = True

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.current = self.question.default

    def get_current_value(self) -> str:
        return "(Y/n)" if self.current else "(y/N)"

    def process_input(self, pressed: str) -> None:
        if pressed == key.ENTER:
            raise errors.EndOfInput(self.current)
        if pressed in ("y", "Y", "n", "N"):
            self.current = pressed.lower() == "y"
            raise errors.EndOfInput(self.current)
        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()
