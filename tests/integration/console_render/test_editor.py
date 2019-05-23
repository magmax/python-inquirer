import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from readchar import key

import inquirer.questions as questions
from inquirer.render import ConsoleRender
from inquirer import errors
from . import helper


class EditorRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    @patch('editor.edit')
    def test_basic_render(self, edit):
        edit.return_value = b'Some text'
        stdin = [key.ENTER]
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.Editor(variable, message)

        sut = ConsoleRender(event_generator=helper.event_factory(*stdin))
        result = sut.render(question)

        self.assertEqual('Some text', result)
        self.assertInStdout(message)
        self.assertTrue(edit.called)

    @patch('editor.edit')
    def test_ignore_true_should_return(self, edit):
        edit.return_value = b'Some text'
        stdin = [key.ENTER]
        message = 'Foo message'
        variable = 'Bar variable'
        expected = 'Something default'

        question = questions.Editor(variable,
                                    ignore=True,
                                    default=expected,
                                    message=message)

        sut = ConsoleRender(event_generator=helper.event_factory(*stdin))
        result = sut.render(question)

        self.assertEqual(expected, result)
        self.assertNotInStdout(message)
        self.assertFalse(edit.called)

    @patch('editor.edit')
    def test_validation_fails(self, edit):
        stdin = [key.ENTER, key.ENTER]
        edit.side_effect = [b'Only one line', b'Two\nLines\nCool']

        message = 'Insert number'
        variable = 'foo'
        expected = 'Two\nLines\nCool'

        def val(_, x):
            return x.count('\n') >= 2

        question = questions.Editor(variable,
                                    validate=val,
                                    message=message)

        sut = ConsoleRender(event_generator=helper.event_factory(*stdin))
        result = sut.render(question)
        self.assertEqual(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('Entered value is not a valid foo')
        self.assertTrue(edit.called)

    @patch('editor.edit')
    def test_validation_fails_with_custom_error(self, edit):
        stdin = [key.ENTER, key.ENTER]
        edit.side_effect = [b'Only one line', b'Two\nLines\nCool']

        message = 'Insert number'
        variable = 'foo'
        expected = 'Two\nLines\nCool'

        def val(_, x):
            if x.count('\n') < 2:
                raise errors.ValidationError('', reason='Some bad reason')

            return True

        question = questions.Editor(variable,
                                    validate=val,
                                    message=message)

        sut = ConsoleRender(event_generator=helper.event_factory(*stdin))
        result = sut.render(question)
        self.assertEqual(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('Some bad reason')
        self.assertTrue(edit.called)

    @patch('editor.edit')
    def test_ctrl_c_breaks_execution(self, edit):
        stdin = [key.CTRL_C]
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.Editor(variable, message)

        sut = ConsoleRender(event_generator=helper.event_factory(*stdin))
        with self.assertRaises(KeyboardInterrupt):
            sut.render(question)
        self.assertFalse(edit.called)
