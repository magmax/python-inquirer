import sys
import unittest
import inquirer.questions as questions
import inquirer.errors as errors

from . import helper
from readchar import key

from inquirer.render import ConsoleRender


class ListRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_all_choices_are_shown(self):
        stdin = helper.key_factory(key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=stdin)
        result = sut.render(question)

        self.assertInStdout(message)
        for choice in choices:
            self.assertInStdout(choice)
