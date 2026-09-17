import unittest
from unittest.mock import MagicMock

import inquirer.errors as errors
import inquirer.questions as questions
import tests.integration.console_render.helper as helper
from inquirer.render import ConsoleRender


class BasicTest(unittest.TestCase, helper.BaseTestCase):
    def test_rendering_erroneous_type(self):
        question = questions.Question("foo", "bar")

        sut = ConsoleRender()
        with self.assertRaises(errors.UnknownQuestionTypeError):
            sut.render(question)

    def test_height_uses_terminal_height_not_width(self):
        sut = ConsoleRender()
        sut.terminal = MagicMock(width=123, height=45)

        self.assertEqual(sut.height, 45)
        self.assertEqual(sut.width, 123)
