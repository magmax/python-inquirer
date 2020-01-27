# -*- coding: utf-8 -*-
import json

from collections import namedtuple
from blessings import Terminal

from .errors import ThemeError

term = Terminal()


def load_theme_from_json(json_theme):
    """
    Load a theme from a json.
    Expected format:
    {
        "Question": {
            "mark_color": "yellow",
            "brackets_color": "normal",
            ...
        },
        "List": {
            "selection_color": "bold_blue",
            "selection_cursor": "->"
        }
    }

    Color values should be string representing valid blessings.Terminal colors.
    """
    return load_theme_from_dict(json.loads(json_theme))


def load_theme_from_dict(dict_theme):
    """
    Load a theme from a dict.
    Expected format:
    {
        "Question": {
            "mark_color": "yellow",
            "brackets_color": "normal",
            ...
        },
        "List": {
            "selection_color": "bold_blue",
            "selection_cursor": "->"
        }
    }

    Color values should be string representing valid blessings.Terminal colors.
    """
    t = Default()
    for question_type, settings in dict_theme.items():
        if question_type not in vars(t):
            raise ThemeError('Error while parsing theme. Question type '
                             '`{}` not found or not customizable.'
                             .format(question_type))

        # calculating fields of namedtuple, hence the filtering
        question_fields = list(filter(lambda x: not x.startswith('_'),
                                      vars(getattr(t, question_type))))

        for field, value in settings.items():
            if field not in question_fields:
                raise ThemeError('Error while parsing theme. Field '
                                 '`{}` invalid for question type `{}`'
                                 .format(field, question_type))
            actual_value = getattr(term, value) or value
            setattr(getattr(t, question_type), field, actual_value)
    return t


class Theme(object):
    def __init__(self):
        self.Question = namedtuple('question', 'mark_color brackets_color '
                                               'default_color')
        self.Editor = namedtuple('editor', 'opening_prompt')
        self.Checkbox = namedtuple('common',
                                   'selection_color selection_icon '
                                   'selected_color unselected_color '
                                   'selected_icon unselected_icon '
                                   'selected_icon_color '
                                   'unselected_icon_color '
                                   'selector_color_selected '
                                   'selector_color_unselected '
                                   'selection_icon_color')
        self.List = namedtuple('List', 'selection_color selection_cursor '
                                       'unselected_color '
                                       'selector_color_selected '
                                       'selector_color_unselected')


class Default(Theme):
    def __init__(self):
        super(Default, self).__init__()
        self.Question.mark_color = term.yellow
        self.Question.brackets_color = term.normal
        self.Question.default_color = term.normal

        self.Editor.opening_prompt_color = term.bright_black
        self.Checkbox.selection_color = term.blue
        self.Checkbox.selected_icon_color = term.yellow + term.bold
        self.Checkbox.selection_icon_color = term.blue
        self.Checkbox.unselected_icon_color = term.normal
        self.Checkbox.selector_color_unselected = term.normal
        self.Checkbox.selector_color_selected = term.blue
        self.Checkbox.selection_icon = '>'
        self.Checkbox.selected_icon = 'X'
        self.Checkbox.selected_color = term.yellow + term.bold
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = 'o'

        self.List.selection_color = term.blue
        self.List.selection_cursor = '>'
        self.List.unselected_color = term.normal
        self.List.selector_color_unselected = term.normal
        self.List.selector_color_selected = term.blue


class GreenPassion(Theme):

    def __init__(self):
        super(GreenPassion, self).__init__()
        self.Question.mark_color = term.yellow
        self.Question.brackets_color = term.bright_green
        self.Question.default_color = term.yellow

        self.Checkbox.selection_color = term.bold_black_on_bright_green
        self.Checkbox.selection_icon_color = term.bold_black_on_bright_green
        self.Checkbox.unselected_icon_color = term.normal
        self.Checkbox.selected_icon_color = term.green
        self.Checkbox.selector_color_unselected = term.normal
        self.Checkbox.selector_color_selected = term.bold_black_on_bright_green
        self.Checkbox.selection_icon = '❯'
        self.Checkbox.selected_icon = '◉'
        self.Checkbox.selected_color = term.green
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = '◯'

        self.List.selection_color = term.bold_black_on_bright_green
        self.List.selection_cursor = '❯'
        self.List.unselected_color = term.normal
        self.List.selector_color_unselected = term.normal
        self.List.selector_color_selected = term.bold_black_on_bright_green


class Node(Theme):
    def __init__(self):
        super(Node, self).__init__()
        self.Question.mark_color = term.yellow
        self.Question.brackets_color = term.bright_green
        self.Question.default_color = term.yellow

        self.Checkbox.selection_icon_color = term.green + term.bold
        self.Checkbox.unselected_icon_color = term.green + term.bold
        self.Checkbox.selected_icon_color = term.green + term.bold
        self.Checkbox.selector_color_unselected = term.normal
        self.Checkbox.selector_color_selected = term.bright_blue + term.bold
        self.Checkbox.selection_color = term.normal + term.bold
        self.Checkbox.selection_icon = '❯'
        self.Checkbox.selected_icon = '⬢'
        self.Checkbox.selected_color = term.normal
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = '⬡'

        self.List.selection_color = term.bright_blue
        self.List.selection_cursor = '❯'
        self.List.unselected_color = term.normal
        self.List.selector_color_unselected = term.normal
        self.List.selector_color_selected = term.bright_blue + term.bold
