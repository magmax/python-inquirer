# -*- coding: utf-8 -*-

from .render.console import ConsoleRender


def prompt(questions, render=None, answers=None):
    render = render or ConsoleRender()
    answers = answers or {}

    try:
        render.reset()
        for question in questions:
            answers[question.name] = render.render(question, answers)
        return answers
    except KeyboardInterrupt:
        pass
    finally:
        render.reset()
