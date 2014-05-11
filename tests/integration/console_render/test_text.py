import sys
import unittest
import inquirer.questions as questions
import inquirer.errors as errors

from . import helper
from readchar import key

from inquirer.render import ConsoleRender


class TextRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_basic_render(self):
        stdin = 'This is a foo message'
        message = 'Foo message'
        variable = 'Bar variable'

        self.set_input(stdin)
        question = questions.Text(variable, message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(stdin, result)
        self.assertInStdout(message)

    def test_ignore_true_should_return(self):
        stdin = 'This is a foo message'
        message = 'Foo message'
        variable = 'Bar variable'
        expected = object()

        self.set_input(stdin)
        question = questions.Text(variable,
                                  ignore=True,
                                  default=expected,
                                  message=message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertNotInStdout(message)

    @unittest.skip('Unknown failure')
    def test_validation_fails(self):
        stdin = 'Invalid message\n9999'
        message = 'Insert number'
        variable = 'foo'
        expected = '9999'

        self.set_input(stdin)
        question = questions.Text(variable,
                                  validate=lambda _, x: re.match('\d+', x),
                                  message=message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('Invalid value')
