from unittest.mock import Mock

import pytest

import inquirer.shortcuts as shortcuts


@pytest.fixture()
def render_mock():
    render = Mock()
    render.render = lambda x: x
    yield render


@pytest.mark.parametrize(
    "func,kind,message",
    [
        (shortcuts.text, "text", "text message"),
        (shortcuts.editor, "editor", "editor message"),
        (shortcuts.password, "password", "password message"),
        (shortcuts.confirm, "confirm", "confirm message"),
        (shortcuts.list_input, "list", "list_input message"),
        (shortcuts.checkbox, "checkbox", "checkbox message"),
        (shortcuts.path, "path", "path message"),
    ],
)
def test_shortcuts(func, kind, message, render_mock):
    q = func(message, render=render_mock)

    assert q.kind == kind
    assert q.message == message
