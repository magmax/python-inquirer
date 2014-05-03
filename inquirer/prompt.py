# -*- coding: utf-8 -*-

from .render import ConsoleRender


def prompt(questions, render=None, answers=None):
    render = render or ConsoleRender()
    answers = answers or {}

    for question in questions:
        answers[question.name] = render.render(question, answers)
    return answers
