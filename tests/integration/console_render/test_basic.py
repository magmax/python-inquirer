import unittest

import inquirer.errors as errors
import inquirer.questions as questions
from inquirer.render import ConsoleRender

from . import helper


class BasicTest(unittest.TestCase, helper.BaseTestCase):
    def test_rendering_erroneous_type(self):
        question = questions.Question("foo", "bar")

        sut = ConsoleRender()
        with self.assertRaises(errors.UnknownQuestionTypeError):
            sut.render(question)
