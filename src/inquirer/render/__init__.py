from typing import Any, Dict, Type, TYPE_CHECKING
from inquirer.render.console import ConsoleRender


if TYPE_CHECKING:
    from inquirer.questions import Question


class Render:
    def __init__(self, impl: Type[ConsoleRender] = ConsoleRender):
        self._impl = impl

    def render(self, question: "Question", answers: Dict[str, Any] | None = None) -> Any:
        return self._impl.render(question, answers)
