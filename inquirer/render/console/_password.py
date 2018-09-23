# -*- coding: utf-8 -*-

from ._text import Text


class Password(Text):
    def get_current_value(self):
        return self.question.echo * len(self.current)
