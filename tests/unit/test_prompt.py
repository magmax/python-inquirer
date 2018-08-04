import unittest
try:
    from unittest import MagicMock, Mock
except ImportError:
    from mock import MagicMock, Mock

from inquirer import prompt


class PromptTests(unittest.TestCase):
    def test_prompt_returns_a_hash(self):
        self.assertEquals({}, prompt([]))

    def test_prompt_renders_a_questions(self):
        question1 = MagicMock()
        question1.name = 'foo'
        result1 = object()
        render = Mock()
        render.render.return_value = result1

        result = prompt([question1], render=render)

        self.assertEquals({'foo': result1}, result)
        render.render.assert_called()
        render.render.call_args_list[0][0] == result1
