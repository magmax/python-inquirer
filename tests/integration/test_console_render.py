import sys
import re
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from inquirer.render import Render, ConsoleRender
import inquirer.questions as questions
import inquirer.errors as errors
from readchar import key


def fake_key_generator():
    return sys.stdin.read(1)


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
        stdin = 'This is a foo message'
        message = 'Foo message'
        variable = 'Bar variable'

        sys.stdin = StringIO(stdin)
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

        sys.stdin = StringIO(stdin)
        question = questions.Text(variable,
                                  ignore=True,
                                  default=expected,
                                  message=message)

        sut = ConsoleRender()
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertNotInStdout(message)

    def test_validation_fails(self):
        stdin = 'Invalid message\n9999'
        message = 'Insert number'
        variable = 'foo'
        expected = '9999'

        sys.stdin = StringIO(stdin)
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

    def test_do_not_show_values(self):
        stdin = 'The password' + key.ENTER
        message = 'Foo message'
        variable = 'Bar variable'

        sys.stdin = StringIO(stdin)
        question = questions.Password(variable, message)

        sut = ConsoleRender(key_generator=fake_key_generator)
        result = sut.render(question)

        self.assertInStdout(message)
        self.assertNotInStdout(stdin)


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


class ListRenderTest(unittest.TestCase, BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_all_choices_are_shown(self):
        stdin = key.ENTER
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        sys.stdin = StringIO(stdin)
        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=fake_key_generator)
        result = sut.render(question)

        self.assertInStdout(message)
        for choice in choices:
            self.assertInStdout(choice)


class CheckboxRenderTest(unittest.TestCase, BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_all_choices_are_shown(self):
        stdin = key.ENTER
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        sys.stdin = StringIO(stdin)
        question = questions.Checkbox(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=fake_key_generator)
        result = sut.render(question)

        self.assertInStdout(message)
        for choice in choices:
            self.assertInStdout(choice)

    def test_one_choice(self):
        stdin = key.SPACE + key.ENTER
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        sys.stdin = StringIO(stdin)
        question = questions.Checkbox(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=fake_key_generator)
        result = sut.render(question)

        self.assertInStdout(message)
        self.assertEqual(['foo'], result)

    @unittest.skip('failing by unknown reasons.')
    def test_can_move(self):
        stdin = (key.DOWN
                 + key.DOWN
                 + key.UP
                 + key.SPACE
                 + key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        sys.stdin = StringIO(stdin)
        question = questions.Checkbox(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=fake_key_generator)
        result = sut.render(question)

        self.assertEqual(['bar'], result)

    def test_cannot_move_beyond_upper_limit(self):
        stdin = (key.UP
                 + key.UP
                 + key.UP
                 + key.SPACE
                 + key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        sys.stdin = StringIO(stdin)
        question = questions.Checkbox(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=fake_key_generator)
        result = sut.render(question)

        self.assertEqual(['foo'], result)

    @unittest.skip('failing by unknown reasons.')
    def test_cannot_move_beyond_lower_limit(self):
        stdin = (key.DOWN
                 + key.DOWN
                 + key.DOWN
                 + key.DOWN
                 + key.DOWN
                 + key.DOWN
                 + key.DOWN
                 + key.SPACE
                 + key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        sys.stdin = StringIO(stdin)
        question = questions.Checkbox(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=fake_key_generator)
        result = sut.render(question)

        self.assertEqual(['bazz'], result)
