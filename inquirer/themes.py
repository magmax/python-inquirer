# -*- coding: utf-8 -*-
import json

from blessed import Terminal

from .errors import ThemeError

term = Terminal()


def load_theme_from_json(json_theme):
    """
    Load a theme from a json.
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

    Color values should be string representing valid blessings.Terminal colors.
    """
    return load_theme_from_dict(json.loads(json_theme))


def load_theme_from_dict(dict_theme):
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

    Color values should be string representing valid blessings.Terminal colors.
    """
    t = Default()
    for question_type, settings in dict_theme.items():
        question_type = question_type.lower()
        if question_type not in vars(t):
            raise ThemeError(
                "Error while parsing theme. Question type " "`{}` not found or not customizable.".format(question_type)
            )

        # calculating fields of namedtuple, hence the filtering
        question_fields = list(filter(lambda x: not x.startswith("_"), vars(getattr(t, question_type))))

        for field, value in settings.items():
            if field not in question_fields:
                raise ThemeError(
                    "Error while parsing theme. Field "
                    "`{}` invalid for question type `{}`".format(field, question_type)
                )
            actual_value = getattr(term, value) or value
            setattr(getattr(t, question_type), field, actual_value)
    return t


class ThemeItem(object):
    def __init__(self):
        self.template_for_title = (
            "{theme.brackets_color}" "[{theme.mark_color}?{theme.brackets_color}]{t.normal}" " {msg}: {value}"
        )


class Text(ThemeItem):
    def __init__(self):
        super(Text, self).__init__()


class Path(ThemeItem):
    def __init__(self):
        super(Path, self).__init__()


class Confirm(ThemeItem):
    def __init__(self):
        super(Confirm, self).__init__()


class Password(ThemeItem):
    def __init__(self):
        super(Password, self).__init__()
        self.template_for_title = (
            "{theme.brackets_color}" "[{theme.mark_color}?{theme.brackets_color}]{t.normal}" " {msg}: {value}"
        )


class Question(ThemeItem):
    def __init__(self):
        super(Question, self).__init__()
        self.mark_color = term.yellow
        self.brackets_color = term.normal
        self.default_color = term.normal


class Editor(ThemeItem):
    def __init__(self):
        super(Editor, self).__init__()
        self.opening_prompt_color = term.bright_black


class Checkbox(ThemeItem):
    def __init__(self):
        super(Checkbox, self).__init__()
        self.selection_color = term.blue
        self.selection_icon = ">"
        self.selected_icon = "X"
        self.selected_color = term.yellow + term.bold
        self.unselected_color = term.normal
        self.unselected_icon = "o"


class List(ThemeItem):
    def __init__(self):
        super(List, self).__init__()
        self.selection_color = term.blue
        self.selection_cursor = ">"
        self.unselected_color = term.normal


class Theme(object):
    def __init__(self):
        super(Theme, self).__init__()
        self.question = Question()
        self.text = Text()
        self.path = Path()
        self.password = Password()
        self.confirm = Confirm()
        self.editor = Editor()
        self.checkbox = Checkbox()
        self.list = List()


class Default(Theme):
    def __init__(self):
        super(Default, self).__init__()


class GreenPassion(Theme):
    def __init__(self):
        super(GreenPassion, self).__init__()
        self.question.brackets_color = term.bright_green
        self.question.default_color = term.yellow
        self.checkbox.selection_color = term.bold_black_on_bright_green
        self.checkbox.selection_icon = "❯"
        self.checkbox.selected_icon = "◉"
        self.checkbox.selected_color = term.green
        self.checkbox.unselected_color = term.normal
        self.checkbox.unselected_icon = "◯"
        self.list.selection_color = term.bold_black_on_bright_green
        self.list.selection_cursor = "❯"

        # Backward compatibility. Deprecated.
        self.Question = self.question
        self.Editor = self.editor
        self.Checkbox = self.checkbox
        self.List = self.list
