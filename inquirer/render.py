# -*- coding: utf-8 -*-

import questions


class Render(object):
    def render(self, question):
        raise NotImplemented("Abstract method")


class ConsoleRender(Render):
    def render(self, question):
        return question.name, raw_input(question.message)
