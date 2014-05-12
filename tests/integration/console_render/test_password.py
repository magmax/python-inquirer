import sys
import unittest
import inquirer.questions as questions
import inquirer.errors as errors

from . import helper
from readchar import key

from inquirer.render import ConsoleRender


class PasswordRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_do_not_show_values(self):
        stdin = helper.key_factory(
            'm', 'y', ' ', 'p', 'a', 's', 's', 'w', 'o', 'r', 'd',
            key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.Password(variable, message)

        sut = ConsoleRender(key_generator=stdin)
        result = sut.render(question)

        self.assertInStdout(message)
        self.assertNotInStdout('my password')
