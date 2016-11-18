# -*- coding: utf-8 -*-

from .render.console import ConsoleRender


def prompt(questions, render=None, answers=None,
           raise_keyboard_interrupt=False):
    render = render or ConsoleRender()
    answers = answers or {}

    try:
        for question in questions:
            answers[question.name] = render.render(question, answers)
        return answers
    except KeyboardInterrupt:
        if raise_keyboard_interrupt:
            raise
        print('')
        print('Cancelled by user')
        print('')
