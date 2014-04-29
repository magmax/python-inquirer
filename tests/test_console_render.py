import sys
import unittest
from StringIO import StringIO

from inquirer.render import ConsoleRender
from inquirer.questions import Text


class TextRenderTest(unittest.TestCase):
    def setUp(self):
        self._base_stdin = sys.stdin
        self._base_stdout = sys.stdout

    def tearDown(self):
        sys.stdin = self._base_stdin
        sys.stdout = self._base_stdout


    def test_basic_render(self):
        value = 'This is a foo message'
        message = 'Foo message'
        variable = 'Bar variable'

        sys.stdin = StringIO(value)
        sys.stdout = StringIO()
        question = Text(variable, message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals((variable, value), result)

        sys.stdout.seek(0)
        stdout = sys.stdout.read()
        self.assertIn(message, stdout)


    def test_unless_true(self):
        value = 'This is a foo message'
        message = 'Foo message'
        variable = 'Bar variable'
        expected = object()

        sys.stdin = StringIO(value)
        sys.stdout = StringIO()
        question = Text(variable,
                        unless=True,
                        default=expected,
                        message=message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals((variable, expected), result)

        sys.stdout.seek(0)
        stdout = sys.stdout.read()
        self.assertNotIn(message, stdout)
