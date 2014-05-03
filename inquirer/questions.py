# -*- coding: utf-8 -*-

from . import errors


class Question(object):
    kind = 'base question'

    def __init__(self,
                 name,
                 message='',
                 choices=None,
                 default=None,
                 ignore=False,
                 validate=True):
        self.name = name
        self.message = message
        self._choices = choices or []
        self._default = default
        self._ignore = ignore
        self._validate = validate

    def ignore(self, values):
        return self._solve(self._ignore, values)

    def validate(self, values, current):
        if not self._solve(self._validate, values, current):
            raise errors.ValidationError()

    def default(self, values):
        return self._solve(self._default, values)

    def choices(self, values):
        return self._solve(self._choices, values)

    def _solve(self, value, *args, **kwargs):
        return (value(*args, **kwargs)
                if callable(value)
                else value)


class Text(Question):
    kind = 'text'


class Password(Question):
    kind = 'password'


class Confirm(Question):
    kind = 'confirm'

    def __init__(self, name, default=False, **kwargs):
        super(Confirm, self).__init__(name, default=default, **kwargs)


class List(Question):
    kind = 'list'
