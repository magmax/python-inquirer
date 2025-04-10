from typing import Any, Optional, Tuple, TypeVar, TYPE_CHECKING

from blessed import Terminal

from inquirer.errors import ValidationError

if TYPE_CHECKING:
    from inquirer.questions import Question
    from inquirer.themes import Theme

MAX_OPTIONS_DISPLAYED_AT_ONCE = 15
half_options = int(MAX_OPTIONS_DISPLAYED_AT_ONCE / 2)

T = TypeVar("T")


class BaseConsoleRender:
    title_inline: bool = False

    def __init__(
        self,
        question: "Question",
        theme: Optional["Theme"] = None,
        terminal: Optional[Terminal] = None,
        show_default: bool = False,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.question = question
        self.terminal = terminal or Terminal()
        self.answers = {}
        self.theme = theme
        self.show_default = show_default

    def other_input(self):
        from inquirer.shortcuts import text  # Avoiding circular import

        other = text(self.question.message, autocomplete=getattr(self.question, "autocomplete", None))
        return other

    def get_header(self):
        return self.question.message

    def get_hint(self):
        return ""

    def get_current_value(self) -> str:
        return ""

    def get_options(self) -> list[Tuple[Any, str, str]]:
        return []

    def process_input(self, pressed: str) -> None:
        raise NotImplementedError("Abstract")

    def handle_validation_error(self, error: ValidationError) -> str:
        if error.reason:
            return error.reason

        ret = f'"{error.value}" is not a valid {self.question.name}.'
        try:
            ret.format()
            return ret
        except (ValueError, KeyError):
            return f"Entered value is not a valid {self.question.name}."
