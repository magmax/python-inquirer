# -*- coding: utf-8 -*-

class Question(object):
    def __init__(self, name, validate=None):
        self.name = name
        self.validate = validate


class Text(Question):
    def __init__(self, name, message, validate=None):
        super(Text, self).__init__(name, validate)
        self.message = message
