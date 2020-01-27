# -*- coding: utf-8 -*-

from readchar import key
from .base import BaseConsoleRender
from inquirer import errors


class List(BaseConsoleRender):
    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.current = self._current_index()

    @property
    def is_long(self):
        choices = self.question.choices or []
        return len(choices) >= self.MAX_OPTIONS_DISPLAYED_AT_ONCE

    def get_options(self):
        choices = self.question.choices or []
        if self.is_long:
            cmin = 0
            cmax = self.MAX_OPTIONS_DISPLAYED_AT_ONCE

            if self.half_options < self.current < len(choices) - self.half_options:
                cmin += self.current - self.half_options
                cmax += self.current - self.half_options
            elif self.current >= len(choices) - self.half_options:
                cmin += len(choices) - self.MAX_OPTIONS_DISPLAYED_AT_ONCE
                cmax += len(choices)

            cchoices = choices[cmin:cmax]
        else:
            cchoices = choices

        ending_milestone = max(len(choices) - self.half_options, self.half_options + 1)
        is_in_beginning = self.current <= self.half_options
        is_in_middle = self.half_options < self.current < ending_milestone
        is_in_end = self.current >= ending_milestone

        for index, choice in enumerate(cchoices):
            end_index = ending_milestone + index - self.half_options - 1
            if (is_in_middle and index == self.half_options) \
                    or (is_in_beginning and index == self.current) \
                    or (is_in_end and end_index == self.current):

                color = self.theme.List.selection_color
                symbol = self.theme.List.selection_cursor
            else:
                color = self.theme.List.unselected_color
                symbol = ' '
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
                self.current = min(
                    len(self.question.choices) - 1,
                    self.current + 1
                )
            return
        if pressed == key.ENTER:
            value = self.question.choices[self.current]
            raise errors.EndOfInput(getattr(value, 'value', value))

        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()

    def _current_index(self):
        try:
            return self.question.choices.index(self.question.default)
        except ValueError:
            return 0

    def get_current_value(self):
        try:
            return self.question.choices[self.current]
        except IndexError:
            return ''
