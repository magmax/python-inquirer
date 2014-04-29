# -*- coding: utf-8 -*-

import questions


class Render(object):
    def render(self, question):
        raise NotImplemented("Abstract method")


class ConsoleRender(Render):
    def render(self, question):
        message = '[?] %s: ' % question.message
        result =  question.default if question.ignore else raw_input(message)
        return question.name, result
