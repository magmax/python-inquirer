from readchar import key

from inquirer import errors
from inquirer.render.console._other import GLOBAL_OTHER_CHOICE
from inquirer.render.console.base import MAX_OPTIONS_DISPLAYED_AT_ONCE
from inquirer.render.console.base import BaseConsoleRender
from inquirer.render.console.base import half_options


class FilterList(BaseConsoleRender):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current = self._current_index()
        self.current_text = ""
        self.cursor_offset = 0
        self._autocomplete_state = None

    def get_current_value(self):
        return self.current_text + (self.terminal.move_left * self.cursor_offset)

    @property
    def is_long(self):
        choices = self.question.choices or []
        return len(choices) >= MAX_OPTIONS_DISPLAYED_AT_ONCE

    def get_hint(self):
        try:
            choice = self.question.choices[self.current]
            hint = self.question.hints[choice]
            if hint:
                return f"{choice}: {hint}"
            else:
                return f"{choice}"
        except (KeyError, IndexError):
            return ""

    def get_options(self):
        choices = self.question.choices or []
        if self.is_long:
            cmin = 0
            cmax = MAX_OPTIONS_DISPLAYED_AT_ONCE

            if half_options < self.current < len(choices) - half_options:
                cmin += self.current - half_options
                cmax += self.current - half_options
            elif self.current >= len(choices) - half_options:
                cmin += len(choices) - MAX_OPTIONS_DISPLAYED_AT_ONCE
                cmax += len(choices)

            cchoices = choices[cmin:cmax]
        else:
            cchoices = choices

        ending_milestone = max(len(choices) - half_options, half_options + 1)
        is_in_beginning = self.current <= half_options
        is_in_middle = half_options < self.current < ending_milestone
        is_in_end = self.current >= ending_milestone

        for index, choice in enumerate(cchoices):
            end_index = ending_milestone + index - half_options - 1
            if (
                (is_in_middle and index == half_options)
                or (is_in_beginning and index == self.current)
                or (is_in_end and end_index == self.current)
            ):
                color = self.theme.List.selection_color
                symbol = "+" if choice == GLOBAL_OTHER_CHOICE else self.theme.List.selection_cursor
            else:
                color = self.theme.List.unselected_color
                symbol = " " if choice == GLOBAL_OTHER_CHOICE else " " * len(self.theme.List.selection_cursor)
            yield choice, symbol, color

    def process_input(self, pressed):
        question = self.question
        if pressed == key.UP:
            if question.carousel and self.current == 0:
                self.current = len(question.choices) - 1
            else:
                self.current = max(0, self.current - 1)
            return
        if pressed == key.DOWN:
            if question.carousel and self.current == len(question.choices) - 1:
                self.current = 0
            else:
                self.current = min(len(self.question.choices) - 1, self.current + 1)
            return
        if pressed == key.ENTER:
            value = self.question.choices[self.current]

            if value == GLOBAL_OTHER_CHOICE:
                value = self.other_input()
                if not value:
                    # Clear the print inquirer.text made, since the user didn't enter anything
                    print(self.terminal.move_up + self.terminal.clear_eol, end="")
                    return

            raise errors.EndOfInput(getattr(value, "value", value))

        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()

        # Add text processing
        self._process_text(pressed)

    def _process_text(self, pressed):
        prev_text = self.current_text

        if pressed == key.TAB and self.question.autocomplete:
            if self._autocomplete_state is None:
                self._autocomplete_state = [self.current_text, 0]

            [text, state] = self._autocomplete_state
            autocomplete = self.question.autocomplete(text, state)
            if isinstance(autocomplete, str):
                self.current_text = autocomplete
                self._autocomplete_state[1] += 1
            else:
                self._autocomplete_state = None
            return

        self._autocomplete_state = None

        if pressed == key.BACKSPACE:
            if self.current_text and self.cursor_offset != len(self.current_text):
                if self.cursor_offset > 0:
                    n = -self.cursor_offset
                    self.current_text = self.current_text[: n - 1] + self.current_text[n:]
                else:
                    self.current_text = self.current_text[:-1]
        elif pressed == key.SUPR:
            if self.current_text and self.cursor_offset:
                n = -self.cursor_offset
                self.cursor_offset -= 1
                if n < -1:
                    self.current_text = self.current_text[:n] + self.current_text[n + 1 :]  # noqa E203
                else:
                    self.current_text = self.current_text[:n]
        elif pressed == key.LEFT:
            if self.cursor_offset < len(self.current_text):
                self.cursor_offset += 1
        elif pressed == key.RIGHT:
            self.cursor_offset = max(self.cursor_offset - 1, 0)
        elif len(pressed) != 1:
            return
        else:
            if self.cursor_offset == 0:
                self.current_text += pressed
            else:
                n = -self.cursor_offset
                self.current_text = "".join((self.current_text[:n], pressed, self.current_text[n:]))
        if self.question.filter_func:
            if prev_text != self.current_text:
                self.current = 0
                f = lambda x: self.question.filter_func(self.current_text, x)
                self.question.apply_filter(f)
                if self.current_text == '':
                    self.question.remove_filter()

    def _current_index(self):
        try:
            return self.question.choices.index(self.question.default)
        except ValueError:
            return 0
