# -*- coding: utf-8 -*-

from render import ConsoleRender

def prompt(questions, render=None):
    print
    render = render or ConsoleRender()

    result = {}
    for question in questions:
        q, v = render.render(question)
        result[q] = v
    return result
