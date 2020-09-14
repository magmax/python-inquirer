from inquirer.shortcuts import path, text, editor, password, confirm, list_input, checkbox
import unittest
import pytest
try:
    from unittest.mock import MagicMock, Mock
except ImportError:
    from mock import MagicMock, Mock

from inquirer import prompt


class PromptTests(unittest.TestCase):
    def test_prompt_returns_a_hash(self):
        self.assertEqual({}, prompt([]))

    def test_prompt_renders_a_questions(self):
        question1 = MagicMock()
        question1.name = 'foo'
        result1 = object()
        render = Mock()
        render.render.return_value = result1

        result = prompt([question1], render=render)

        self.assertEqual({'foo': result1}, result)
        self.assertTrue(render.render.called)
        render.render.call_args_list[0][0] == result1


@pytest.fixture()
def render_mock_raise_keyboard():
    render = Mock()
    render.render = Mock(side_effect=KeyboardInterrupt)
    yield render


class TestCancelled():
    def test_print(self, capsys, render_mock_raise_keyboard):
        prompt([MagicMock()], render=render_mock_raise_keyboard)
        out, _ = capsys.readouterr()

        assert "Cancelled by user" in out.rstrip().lstrip()

    def test_raise_keyboard(self, render_mock_raise_keyboard):
        with pytest.raises(KeyboardInterrupt):
            prompt([MagicMock()], render=render_mock_raise_keyboard, raise_keyboard_interrupt=True)


@pytest.fixture()
def render_mock():
    render = Mock()
    render.render = lambda x: x
    yield render


@pytest.mark.parametrize("func,kind,message", [(text, "text", "text message"),
                                               (editor, "editor", "editor message"),
                                               (password, "password", "password message"),
                                               (confirm, "confirm", "confirm message"),
                                               (list_input, "list", "list_input message"),
                                               (checkbox, "checkbox", "checkbox message"),
                                               (path, "path", "path message")])
def test_shortcuts(func, kind, message, render_mock):
    q = func(message, render=render_mock)

    assert q.kind == kind
    assert q.message == message
