# -*- coding: utf-8 -*-

class Question(object):
    def __init__(self, kind, name, default=None, unless=False, validate=None):
        self.kind = kind
        self.name = name
        self.default = default
        self.unless = unless
        self.validate = validate

    @property
    def ignore(self):
        return self.unless() if callable(self.unless) else self.unless

class Text(Question):
    def __init__(self, name, message, default=None, unless=False, validate=None):
        super(Text, self).__init__('text', name, default, unless, validate)
        self.message = message
