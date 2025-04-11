from typing import Any, Callable, Optional, TypeVar

from inquirer import questions
from inquirer.render import Render
from inquirer.render.console import ConsoleRender


T = TypeVar("T")


def text(
    message: str,
    autocomplete: Optional[Callable[[str, int], Optional[str]]] = None,
    render: Optional["Render | ConsoleRender"] = None,
    **kwargs: Any
) -> str:
    render = render or ConsoleRender()
    question = questions.Text(name="", message=message, autocomplete=autocomplete, **kwargs)
    return render.render(question)


def editor(message: str, render: Optional["Render | ConsoleRender"] = None, **kwargs: Any) -> str:
    render = render or ConsoleRender()
    question = questions.Editor(name="", message=message, **kwargs)
    return render.render(question)


def password(message: str, render: Optional["Render | ConsoleRender"] = None, **kwargs: Any) -> str:
    render = render or ConsoleRender()
    question = questions.Password(name="", message=message, **kwargs)
    return render.render(question)


def confirm(message: str, render: Optional["Render | ConsoleRender"] = None, **kwargs: Any) -> bool:
    render = render or ConsoleRender()
    question = questions.Confirm(name="", message=message, **kwargs)
    return render.render(question)


def list_input(message: str, render: Optional["Render | ConsoleRender"] = None, **kwargs: Any):
    render = render or ConsoleRender()
    question = questions.List(name="", message=message, **kwargs)
    return render.render(question)


def checkbox(message: str, render: Optional["Render | ConsoleRender"] = None, **kwargs: Any) -> list[str]:
    render = render or ConsoleRender()
    question = questions.Checkbox(name="", message=message, **kwargs)
    return render.render(question)


def path(message: str, render: Optional["Render | ConsoleRender"] = None, **kwargs: Any) -> str:
    render = render or ConsoleRender()
    question = questions.Path(name="", message=message, **kwargs)
    return render.render(question)
