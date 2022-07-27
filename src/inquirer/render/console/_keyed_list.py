from readchar import key

from inquirer import errors
from inquirer.render.console.base import MAX_OPTIONS_DISPLAYED_AT_ONCE
from inquirer.render.console.base import BaseConsoleRender
from inquirer.render.console.base import half_options
from inquirer.render.console._list import List


class KeyedList(List):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current = self._current_index()

    def process_input(self, pressed):
        super().process_input(pressed)

        keys = [choice.key for choice in self.question.choices]

        if pressed in keys:
            self.current = self.get_next(keys, pressed)

            if self.question.auto_confirm:
                value = self.question.choices[self.current]

                raise errors.EndOfInput(getattr(value, "value", value))

    def get_next(self, keys, pressed):
        try:
            # Multiple entries with the same key?  Get the 'next' one.
            return keys.index(pressed, self.current + 1)
        except ValueError:
            # There isn't a next one, so get the first.
            return keys.index(pressed)
