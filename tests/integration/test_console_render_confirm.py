import sys
import unittest
import inquirer.questions as questions
import inquirer.errors as errors

from . import helper
from readchar import key

from inquirer.render import ConsoleRender


class ConfirmRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_no_as_default(self):
        input_str = key.ENTER
        message = 'Foo message'
        variable = 'Bar variable'
        expected = False

        self.set_input(input_str)
        question = questions.Confirm(variable,
                                     message=message)

        sut = ConsoleRender(key_generator=helper.fake_key_generator)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(y/N)')

    def test_yes_as_default(self):
        input_str = key.ENTER
        message = 'Foo message'
        variable = 'Bar variable'
        expected = True

        self.set_input(input_str)
        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(key_generator=helper.fake_key_generator)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(Y/n)')

    def test_answring_y(self):
        input_str = 'y'
        message = 'Foo message'
        variable = 'Bar variable'
        expected = True

        self.set_input(input_str)
        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(key_generator=helper.fake_key_generator)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(Y/n)')

    def test_answring_Y(self):
        input_str = 'Y'
        message = 'Foo message'
        variable = 'Bar variable'
        expected = True

        self.set_input(input_str)
        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(key_generator=helper.fake_key_generator)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(Y/n)')

    def test_answring_n(self):
        input_str = 'n'
        message = 'Foo message'
        variable = 'Bar variable'
        expected = False

        self.set_input(input_str)
        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(key_generator=helper.fake_key_generator)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(Y/n)')

    def test_answring_N(self):
        input_str = 'N'
        message = 'Foo message'
        variable = 'Bar variable'
        expected = False

        self.set_input(input_str)
        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(key_generator=helper.fake_key_generator)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(Y/n)')

    def test_invalid_answer(self):
        input_str = 'aN'
        message = 'Foo message'
        variable = 'Bar variable'

        self.set_input(input_str)
        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(key_generator=helper.fake_key_generator)
        sut.render(question)

        self.assertInStdout('Invalid value')
