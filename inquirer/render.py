# -*- coding: utf-8 -*-

import questions


class Render(object):
    def render(self, obj):
        raise NotImplemented("Abstract method")


class ConsoleRender(object):
    def render(self, obj):
        print type(obj)
