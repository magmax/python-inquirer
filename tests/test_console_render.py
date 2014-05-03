import sys
import re
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from inquirer.render import ConsoleRender
import inquirer.questions as questions
import inquirer.errors as errors


class BaseTestCase(object):
    def base_setup(self):
        self._base_stdin = sys.stdin
        self._base_stdout = sys.stdout
        sys.stdout = StringIO()

    def base_teardown(self):
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


class BasicTest(unittest.TestCase, BaseTestCase):
    def test_rendering_erroneous_type(self):
        question = questions.Question('foo', 'bar')

        sut = ConsoleRender()
        with self.assertRaises(errors.UnknownQuestionTypeError):
            sut.render(question)


class TextRenderTest(unittest.TestCase, BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_basic_render(self):
        value = 'This is a foo message'
        message = 'Foo message'
        variable = 'Bar variable'

        sys.stdin = StringIO(value)
        question = questions.Text(variable, message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(value, result)
        self.assertInStdout(message)


    def test_ignore_true_should_return(self):
        value = 'This is a foo message'
        message = 'Foo message'
        variable = 'Bar variable'
        expected = object()

        sys.stdin = StringIO(value)
        question = questions.Text(variable,
                                  ignore=True,
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
        question = questions.Text(variable,
                                  validate=lambda _, x: re.match('\d+', x),
                                  message=message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('Invalid value')


class PasswordRenderTest(unittest.TestCase, BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    @unittest.skip('Not working because getpass mocks stdin too')
    def test_do_not_show_values(self):
        value = 'This is a foo message'
        message = 'Foo message'
        variable = 'Bar variable'

        sys.stdin = StringIO(value)
        question = questions.Password(variable, message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(value, result)
        self.assertInStdout(message)
        self.assertNotInStdout(value)


class ConfirmRenderTest(unittest.TestCase, BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_no_as_default(self):
        input_str = '\n'
        message = 'Foo message'
        variable = 'Bar variable'
        expected = False

        sys.stdin = StringIO(input_str)
        question = questions.Confirm(variable,
                                     message=message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(y/N)')

    def test_yes_as_default(self):
        input_str = '\n'
        message = 'Foo message'
        variable = 'Bar variable'
        expected = True

        sys.stdin = StringIO(input_str)
        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(Y/n)')
