# -*- coding: utf-8 -*-
from __future__ import division
from readchar import key
from .base import BaseConsoleRender
from inquirer import errors


class Checkbox(BaseConsoleRender):
    def __init__(self, *args, **kwargs):
        super(Checkbox, self).__init__(*args, **kwargs)
        self.selection = [k for (k, v) in enumerate(self.question.choices)
                          if v in (self.question.default or [])]
        self.current = 0

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
            if (is_in_middle and
                self.current - self.half_options + index in self.selection) \
                or (is_in_beginning and index in self.selection) \
                or (is_in_end and index + max(len(choices) - self.MAX_OPTIONS_DISPLAYED_AT_ONCE, 0) in self.selection):  # noqa

                symbol = self.theme.Checkbox.selected_icon
                color = self.theme.Checkbox.selected_color
            else:
                symbol = self.theme.Checkbox.unselected_icon
                color = self.theme.Checkbox.unselected_color

            selector = ' '
            end_index = ending_milestone + index - self.half_options - 1
            if (is_in_middle and index == self.half_options) \
                    or (is_in_beginning and index == self.current) \
                    or (is_in_end and end_index == self.current):

                selector = self.theme.Checkbox.selection_icon
                color = self.theme.Checkbox.selection_color
            yield choice, selector + ' ' + symbol, color

    def process_input(self, pressed):
        if pressed == key.UP:
            self.current = max(0, self.current - 1)
            return
        elif pressed == key.DOWN:
            self.current = min(len(self.question.choices) - 1,
                               self.current + 1)
            return
        elif pressed == key.SPACE:
            if self.current in self.selection:
                self.selection.remove(self.current)
            else:
                self.selection.append(self.current)
        elif pressed == key.LEFT:
            if self.current in self.selection:
                self.selection.remove(self.current)
        elif pressed == key.RIGHT:
            if self.current not in self.selection:
                self.selection.append(self.current)
        elif pressed == key.ENTER:
            result = []
            for x in self.selection:
                value = self.question.choices[x]
                result.append(getattr(value, 'value', value))
            raise errors.EndOfInput(result)
        elif pressed == key.CTRL_C:
            raise KeyboardInterrupt()
