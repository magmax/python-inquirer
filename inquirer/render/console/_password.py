# -*- coding: utf-8 -*-

from ._text import Text


class Password(Text):
    def get_current_value(self):
        return self.question.echo * len(self.current)

    def handle_validation_error(self, error):
        return 'Entered value is not a valid {q}.'.format(q=self.question.name)
