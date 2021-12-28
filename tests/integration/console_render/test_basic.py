import unittest

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
