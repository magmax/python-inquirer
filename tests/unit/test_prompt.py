import unittest
from unittest import mock

from inquirer import prompt


class PromptTests(unittest.TestCase):
    def test_prompt_returns_a_hash(self):
        self.assertEquals({}, prompt([]))

    def test_prompt_renders_a_questions(self):
        question1 = mock.MagicMock()
        question1.name = 'foo'
        result1 = object()
        render = mock.Mock()
        render.render.return_value = result1

        result = prompt([question1], render=render)

        self.assertEquals({'foo': result1}, result)
        render.render.assert_called()
        render.render.call_args_list[0][0] == result1
