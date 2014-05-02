# -*- coding: utf-8 -*-

from . import errors


class Question(object):
    kind = 'base question'

    def __init__(self, name, message='', default=None, unless=False,
                 validation=True):
        self.name = name
        self.message = message
        self.default = default
        self.unless = unless
        self.validation = validation

    @property
    def ignore(self):
        return (self.unless()
                if callable(self.unless)
                else self.unless)

    def validate(self, value):
        v = (self.validation(value)
             if callable(self.validation)
             else self.validation)

        if not v:
            raise errors.ValidationError()


class Text(Question):
    kind = 'text'


class Password(Question):
    kind = 'password'


class Confirm(Question):
    kind = 'confirm'

    def __init__(self, name, default=False, **kwargs):
        super(Confirm, self).__init__(name, default=default, **kwargs)
