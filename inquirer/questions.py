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
        self._message = message
        self._choices = choices or []
        self._default = default
        self._ignore = ignore
        self._validate = validate
        self.answers = {}

    @property
    def ignore(self):
        return bool(self._solve(self._ignore))

    @property
    def message(self):
        return self._solve(self._message)

    @property
    def default(self):
        return self._solve(self._default)

    @property
    def choices(self):
        return self._solve(self._choices)

    def validate(self, current):
        try:
            if self._solve(self._validate, current):
                return
        except Exception:
            pass
        raise errors.ValidationError()

    def _solve(self, prop, *args, **kwargs):
        if callable(prop):
            return prop(self.answers, *args, **kwargs)
        if isinstance(prop, str):
            return prop.format(**self.answers)
        return prop


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


class Checkbox(Question):
    kind = 'checkbox'
