# -*- coding: utf-8 -*-

from render import ConsoleRender

def prompt(questions, render=None):
    print
    render = render or ConsoleRender()

    result = {}
    for question in questions:
        result[question.name] = render.render(question)
    return result
