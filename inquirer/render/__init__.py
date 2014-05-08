# -*- coding: utf-8 -*-
from console import ConsoleRender


class Render(object):
    def __init__(self, impl=ConsoleRender):
        self._impl = impl

    def render(self, question):
        return self._impl.render(question)
