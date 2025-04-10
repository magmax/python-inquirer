import json
from typing import Dict, TypeVar

from blessed import Terminal
from inquirer import errors

term = Terminal()

T = TypeVar("T", bound="Theme")


def load_theme_from_json(json_theme: str | bytes | bytearray) -> "Theme":
    """Load a theme from a json.

    Expected format:
        >>> {
        ...     "Question": {
        ...         "mark_color": "yellow",
        ...         "brackets_color": "normal",
        ...         ...
        ...     },
        ...     "List": {
        ...         "selection_color": "bold_blue",
        ...         "selection_cursor": "->"
        ...     }
        ... }

    Color values should be string representing valid blessings.Terminal colors.
    """
    return load_theme_from_dict(json.loads(json_theme))


def load_theme_from_dict(dict_theme: Dict[str, Dict[str, str]]) -> "Theme":
    """Load a theme from a dict.

    Expected format:
        >>> {
        ...     "Question": {
        ...         "mark_color": "yellow",
        ...         "brackets_color": "normal",
        ...         ...
        ...     },
        ...     "List": {
        ...         "selection_color": "bold_blue",
        ...         "selection_cursor": "->"
        ...     }
        ... }

    Color values should be string representing valid blessings.Terminal colors.
    """
    t = Theme()
    for question_type, settings in dict_theme.items():
        if question_type not in vars(t):
            raise errors.ThemeError(
                f"Error while parsing theme. Question type `{question_type}` not found or not customizable."
            )

        # calculating fields of namedtuple, hence the filtering
        question_fields = list(filter(lambda x: not x.startswith("_"), vars(getattr(t, question_type))))

        for field, value in settings.items():
            if field not in question_fields:
                raise errors.ThemeError(
                    f"Error while parsing theme. Field `{field}` invalid for question type `{question_type}`"
                )
            actual_value = getattr(term, value) or value
            setattr(getattr(t, question_type), field, actual_value)
    return t


class QuestionTheme:
    mark_color: str
    brackets_color: str
    default_color: str


class EditorTheme:
    opening_prompt_color: str


class CheckboxTheme:
    selection_color: str
    selection_icon: str
    selected_color: str
    unselected_color: str
    selected_icon: str
    unselected_icon: str
    locked_option_color: str


class ListTheme:
    selection_color: str
    selection_cursor: str
    unselected_color: str


class Theme:
    def __init__(self) -> None:
        self.Question = QuestionTheme()
        self.Editor = EditorTheme()
        self.Checkbox = CheckboxTheme()
        self.List = ListTheme()
        self.Question.mark_color = term.yellow
        self.Question.brackets_color = term.normal
        self.Question.default_color = term.normal
        self.Editor.opening_prompt_color = term.bright_black
        self.Checkbox.selection_color = term.cyan
        self.Checkbox.selection_icon = ">"
        self.Checkbox.selected_icon = "[X]"
        self.Checkbox.selected_color = term.yellow + term.bold
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = "[ ]"
        self.Checkbox.locked_option_color = term.gray50
        self.List.selection_color = term.cyan
        self.List.selection_cursor = ">"
        self.List.unselected_color = term.normal


class GreenPassion(Theme):
    def __init__(self) -> None:
        super().__init__()
        self.Question.brackets_color = term.bright_green
        self.Checkbox.selection_color = term.bold_black_on_bright_green
        self.Checkbox.selection_icon = "❯"
        self.Checkbox.selected_icon = "◉"
        self.Checkbox.selected_color = term.green
        self.Checkbox.unselected_icon = "◯"
        self.List.selection_color = term.bold_black_on_bright_green
        self.List.selection_cursor = "❯"


class BlueComposure(Theme):
    def __init__(self) -> None:
        super().__init__()
        self.Question.brackets_color = term.dodgerblue
        self.Question.default_color = term.deepskyblue2
        self.Checkbox.selection_icon = "➤"
        self.Checkbox.selection_color = term.bold_black_on_darkslategray3
        self.Checkbox.selected_icon = "☒"
        self.Checkbox.selected_color = term.cyan3
        self.Checkbox.unselected_icon = "☐"
        self.List.selection_color = term.bold_black_on_darkslategray3
        self.List.selection_cursor = "➤"
