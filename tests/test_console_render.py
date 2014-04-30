import sys
import re
import unittest
from StringIO import StringIO

from inquirer.render import ConsoleRender
from inquirer.questions import Text


class TextRenderTest(unittest.TestCase):
    def setUp(self):
        self._base_stdin = sys.stdin
        self._base_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        sys.stdin = self._base_stdin
        sys.stdout = self._base_stdout

    def assertInStdout(self, message):
        sys.stdout.seek(0)
        stdout = sys.stdout.read()
        self.assertIn(message, stdout)

    def assertNotInStdout(self, message):
        sys.stdout.seek(0)
        stdout = sys.stdout.read()
        self.assertNotIn(message, stdout)


    def test_basic_render(self):
        value = 'This is a foo message'
        message = 'Foo message'
        variable = 'Bar variable'

        sys.stdin = StringIO(value)
        question = Text(variable, message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(value, result)
        self.assertInStdout(message)


    def test_unless_true_should_return(self):
        value = 'This is a foo message'
        message = 'Foo message'
        variable = 'Bar variable'
        expected = object()

        sys.stdin = StringIO(value)
        question = Text(variable,
                        unless=True,
                        default=expected,
                        message=message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertNotInStdout(message)

    def test_validation_fails(self):
        value = 'Invalid message\n9999'
        message = 'Insert number'
        variable = 'foo'
        expected = '9999'

        sys.stdin = StringIO(value)
        question = Text(variable,
                        validation=lambda x: re.match('\d+', x),
                        message=message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('Invalid value')
