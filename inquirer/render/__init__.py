# -*- coding: utf-8 -*-
from .console import ConsoleRender

try:
    from .ncourses import CoursesRender  # noqa
except ImportError:
    # ncourses will not be available
    pass


class Render(object):
    def __init__(self, impl=ConsoleRender):
        self._impl = impl

    def render(self, question, answers):
        return self._impl.render(question, answers)
