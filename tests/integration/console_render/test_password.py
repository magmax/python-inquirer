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
        stdin = 'The password' + key.ENTER
        message = 'Foo message'
        variable = 'Bar variable'

        self.set_input(stdin)
        question = questions.Password(variable, message)

        sut = ConsoleRender(key_generator=helper.fake_key_generator)
        result = sut.render(question)

        self.assertInStdout(message)
        self.assertNotInStdout(stdin)
