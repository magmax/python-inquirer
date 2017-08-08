# -*- coding: utf-8 -*-

from collections import namedtuple
from blessings import Terminal

term = Terminal()


def load_theme_from_dict(dict):
    """
    Load a theme from a dict.
    Expected format:
    {
        "question": {
            "mark_color": "yellow",
            "brackets_color": "normal",
            ...
        },
        "list": {
            "selection_color": "bold_blue",
            "selection_cursor": "->"
        }
    }
    Important: color values should be valid blessings.Terminal colors.
    """
    t = Default()
    for question_type, settings in dict.items():
        for field, value in settings.items():
            setattr(getattr(t, question_type), field, getattr(term, value))
    return t


class Theme(object):
    def __init__(self):
        self.Question = namedtuple('question', 'mark_color brackets_color default_color')
        self.Checkbox = namedtuple('common', 'selection_color selection_icon '
                                             'selected_color unselected_color '
                                             'selected_icon unselected_icon')
        self.List = namedtuple('List', 'selection_color selection_cursor '
                                       'unselected_color')


class Default(Theme):
    def __init__(self):
        super(Default, self).__init__()
        self.Question.mark_color = term.yellow
        self.Question.brackets_color = term.normal
        self.Question.default_color = term.normal
        self.Checkbox.selection_color = term.blue
        self.Checkbox.selection_icon = '>'
        self.Checkbox.selected_icon = 'X'
        self.Checkbox.selected_color = term.yellow + term.bold
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = 'o'
        self.List.selection_color = term.blue
        self.List.selection_cursor = '>'
        self.List.unselected_color = term.normal


class GreenPassion(Theme):

    def __init__(self):
        super(GreenPassion, self).__init__()
        self.Question.mark_color = term.yellow
        self.Question.brackets_color = term.bright_green
        self.Question.default_color = term.yellow
        self.Checkbox.selection_color = term.bold_black_on_bright_green
        self.Checkbox.selection_icon = '❯'
        self.Checkbox.selected_icon = '◉'
        self.Checkbox.selected_color = term.green
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = '◯'
        self.List.selection_color = term.bold_black_on_bright_green
        self.List.selection_cursor = '❯'
        self.List.unselected_color = term.normal
