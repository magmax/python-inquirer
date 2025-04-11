from unittest.mock import MagicMock
from unittest.mock import Mock
from inquirer.render import Render
import pytest

import inquirer


@pytest.fixture()
def render_mock_raise_keyboard():
    render = Mock()
    render.render = Mock(side_effect=KeyboardInterrupt)
    yield render


def test_prompt_returns_a_hash():
    answers = inquirer.prompt([])
    assert answers == {}


def test_prompt_renders_a_questions():
    question1 = MagicMock()
    question1.name = "foo"
    result1 = object()
    render = Mock()
    render.render.return_value = result1


def test_print(capsys, render_mock_raise_keyboard: "Render"):
    inquirer.prompt([MagicMock()], render=render_mock_raise_keyboard)
    out, _ = capsys.readouterr()

    assert "Cancelled by user" in out.rstrip().lstrip()


def test_raise_keyboard(render_mock_raise_keyboard: Render):
    with pytest.raises(KeyboardInterrupt):
        inquirer.prompt([MagicMock()], render=render_mock_raise_keyboard, raise_keyboard_interrupt=True)
