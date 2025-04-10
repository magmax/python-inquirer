from typing import Any, Dict, Iterable, Optional, TYPE_CHECKING

from inquirer.themes import Theme

if TYPE_CHECKING:
    from inquirer.questions import Question
from inquirer.render import Render
from inquirer.render.console import ConsoleRender


def prompt(
    questions: Iterable["Question"],
    render: Optional[Render] = None,
    answers: Optional[Dict[str, Any]] = None,
    theme: Theme = Theme(),
    raise_keyboard_interrupt: bool = False,
):
    next: Render | ConsoleRender = render or ConsoleRender(theme=theme)
    answers = answers or {}

    try:
        for question in questions:
            answers[question.name] = next.render(question, answers)
        return answers
    except KeyboardInterrupt:
        if raise_keyboard_interrupt:
            raise
        return print("\nCancelled by user\n")
