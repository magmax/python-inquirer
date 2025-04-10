from typing import Any, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from inquirer.questions import Question

from inquirer.render.console import ConsoleRender


class Render:
    def __init__(self, impl: Type[ConsoleRender] = ConsoleRender):
        self._impl = impl

    def render(self, question: "Question", answers: dict) -> Any:
        return self._impl.render(question, answers)
