# -*- coding: utf-8 -*-

import exceptions

class Question(object):
    def __init__(self, kind, name, default=None, unless=False, validation=True):
        self.kind = kind
        self.name = name
        self.default = default
        self.unless = unless
        self.validation = validation

    @property
    def ignore(self):
        return self.unless() if callable(self.unless) else self.unless

    def validate(self, value):
        v = self.validation(value) if callable(self.validation) else self.validation

        if not v:
            raise exceptions.ValidationError()

class Text(Question):
    def __init__(self, name, message, default=None, unless=False, validation=True):
        super(Text, self).__init__('text', name, default, unless, validation)
        self.message = message
