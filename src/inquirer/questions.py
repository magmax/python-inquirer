"""Module that implements the questions types."""

from __future__ import annotations

import json
import pathlib
from typing import Any, Callable, Dict, Generic, Tuple, TypeVar, Union, cast

from inquirer import errors
from inquirer.render.console._other import GLOBAL_OTHER_CHOICE, OtherChoice


T = TypeVar("T")
ValidatorType = Union[bool, Callable[[Dict[str, Any], Any], bool]]
MessageType = Union[str, Callable[[Dict[str, Any]], str]]
ChoiceType = Union[str, Tuple[str, T], OtherChoice]
IgnoreType = Union[bool, Callable[[Dict[str, Any]], bool]]


class TaggedValue(Generic[T]):
    def __init__(self, tag: str, value: T):
        self.tag = tag
        self.value = value
        self.tuple = (tag, value)

    def __str__(self) -> str:
        return self.tag

    def __repr__(self) -> str:
        return repr(self.value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, TaggedValue):
            return other.value == self.value  # type: ignore[operator]
        if isinstance(other, tuple):
            return other == self.tuple
        return other == self.value

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.tuple)


class Question:
    kind = "base question"
    carousel: bool = False

    def __init__(
        self,
        name: str,
        message: MessageType = "",
        choices: list[ChoiceType[Any]] | None = None,
        default: Any = None,
        ignore: IgnoreType = False,
        validate: ValidatorType = True,
        show_default: bool = False,
        hints: dict[str, str] | None = None,
        other: bool = False,
    ):
        self.name = name
        self._message = message
        self._choices: list[ChoiceType[Any]] = choices or []
        self._default = default
        self._ignore = ignore
        self._validate = validate
        self.answers: dict[str, Any] = {}
        self.show_default = show_default
        self.hints = hints
        self._other = other

        if self._other:
            self._choices.append(GLOBAL_OTHER_CHOICE)

    def add_choice(self, choice: str | tuple[str, Any]) -> int:
        try:
            index = self._choices.index(choice)
            return index
        except ValueError:
            if self._other:
                self._choices.insert(-1, choice)
                return len(self._choices) - 2

            self._choices.append(choice)
            return len(self._choices) - 1

    @property
    def ignore(self) -> bool:
        return bool(self._solve(self._ignore))

    @property
    def message(self) -> str:
        return cast(str, self._solve(self._message))

    @property
    def default(self) -> Any:
        return self.answers.get(self.name) or self._solve(self._default)

    @property
    def choices_generator(self):
        for choice in self._solve(self._choices):
            yield (TaggedValue(*choice) if isinstance(choice, tuple) and len(choice) == 2 else choice)

    @property
    def choices(self):
        return list(self.choices_generator)

    def validate(self, current: Any):
        try:
            if self._solve(self._validate, current):
                return
        except errors.ValidationError as e:
            raise e
        raise errors.ValidationError(current)

    def _solve(self, prop: Any, *args: Any, **kwargs: Any) -> Any:
        if callable(prop):
            return prop(self.answers, *args, **kwargs)
        if isinstance(prop, str):
            return prop.format(**self.answers)
        return prop


class Text(Question):
    kind: str = "text"

    def __init__(
        self,
        name: str,
        message: MessageType = "",
        default: Any = None,
        autocomplete: Callable[[str, int], str | None] | None = None,
        **kwargs: Any,
    ):
        super().__init__(
            name, message=message, default=str(default) if default and not callable(default) else default, **kwargs
        )
        self.autocomplete = autocomplete


class Password(Text):
    kind = "password"

    def __init__(self, name: str, echo: str = "*", **kwargs: Any):
        super().__init__(name, **kwargs)
        self.echo = echo


class Editor(Text):
    kind = "editor"


class Confirm(Question):
    kind = "confirm"

    def __init__(self, name: str, default: bool = False, **kwargs: Any):
        super().__init__(name, default=default, **kwargs)


class List(Question):
    kind = "list"

    def __init__(
        self,
        name: str,
        message: MessageType = "",
        choices: list[ChoiceType[Any]] | None = None,
        hints: dict[str, str] | None = None,
        default: Any = None,
        ignore: IgnoreType = False,
        validate: ValidatorType = True,
        carousel: bool = False,
        other: bool = False,
        autocomplete: Callable[[str, int], str | None] | None = None,
    ):
        super().__init__(name, message, choices, default, ignore, validate, hints=hints, other=other)
        self.carousel = carousel
        self.autocomplete = autocomplete


class Checkbox(Question):
    kind = "checkbox"

    def __init__(
        self,
        name: str,
        message: MessageType = "",
        choices: list[ChoiceType[Any]] | None = None,
        hints: dict[str, str] | None = None,
        locked: list[Any] | None = None,
        default: list[Any] | None = None,
        ignore: IgnoreType = False,
        validate: ValidatorType = True,
        carousel: bool = False,
        other: bool = False,
        autocomplete: Callable[[str, int], str | None] | None = None,
    ):
        super().__init__(name, message, choices, default, ignore, validate, hints=hints, other=other)
        self.locked = locked
        self.carousel = carousel
        self.autocomplete = autocomplete


class Path(Text):
    ANY = "any"
    FILE = "file"
    DIRECTORY = "directory"

    kind = "path"

    def __init__(
        self,
        name: str,
        default: str | None = None,
        path_type: str = "any",
        exists: bool | None = None,
        **kwargs: Any,
    ):
        super().__init__(name, default=default, **kwargs)

        if path_type in (Path.ANY, Path.FILE, Path.DIRECTORY):
            self._path_type = path_type
        else:
            raise ValueError("'path_type' must be one of [ANY, FILE, DIRECTORY]")

        self._exists = exists

        if default is not None:
            try:
                self.validate(default)
            except errors.ValidationError:
                raise ValueError(f"Default value '{default}' is not valid based on your Path's criteria")

    def validate(self, current: str | None) -> None:
        super().validate(current)

        if current is None:
            raise errors.ValidationError(current)

        path = pathlib.Path(current)

        # this block validates the path in correspondence with the OS
        # it will error if the path contains invalid characters
        try:
            path.lstat()
        except FileNotFoundError:
            pass
        except (ValueError, OSError) as e:
            raise errors.ValidationError(e)

        if (self._exists is True and not path.exists()) or (self._exists is False and path.exists()):
            raise errors.ValidationError(current)

        # os.path.isdir and isfile check also existence of the path,
        # which might not be desirable
        if self._path_type == Path.FILE:
            if current.endswith(("\\", "/")):
                raise errors.ValidationError(current)
            if path.exists() and not path.is_file():
                raise errors.ValidationError(current)

        if self._path_type == Path.DIRECTORY:
            if current == "":
                raise errors.ValidationError(current)
            if path.exists() and not path.is_dir():
                raise errors.ValidationError(current)


def question_factory(kind: str, *args: Any, **kwargs: Any) -> Question:
    for cl in (Text, Editor, Password, Confirm, List, Checkbox, Path):
        if cl.kind == kind:
            return cl(*args, **kwargs)
    raise errors.UnknownQuestionTypeError()


def load_from_dict(question_dict: dict[str, Any]) -> Question:
    """Load one question from a dict.

    It requires the keys 'name' and 'kind'.

    Returns:
        The Question object with associated data.
    """
    return question_factory(**question_dict)


def load_from_list(question_list: list[dict[str, Any]]) -> list[Question]:
    """Load a list of questions from a list of dicts.

    It requires the keys 'name' and 'kind' for each dict.

    Returns:
        A list of Question objects with associated data.
    """
    return [load_from_dict(q) for q in question_list]


def load_from_json(question_json: str | bytes | bytearray) -> list[Question] | Question:
    """Load Questions from a JSON string.

    Returns:
        A list of Question objects with associated data if the JSON
        contains a list or a Question if the JSON contains a dict.
    """
    data = json.loads(question_json)
    if isinstance(data, list):
        return load_from_list(data)
    if isinstance(data, dict):
        return load_from_dict(data)
    raise TypeError(f"Json contained a {type(data)} variable when a dict or list was expected")
