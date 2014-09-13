import unittest

from inquirer import questions
from inquirer import errors


class BaseQuestionTests(unittest.TestCase):
    def test_base_question_type(self):
        name = 'foo'
        q = questions.Question(name)

        self.assertEquals('base question', q.kind)
        self.assertEquals(name, q.name)

    def test_ignore_works_for_true(self):
        name = 'foo'
        q = questions.Question(name, ignore=True)

        self.assertTrue(q.ignore)

    def test_ignore_works_for_false(self):
        name = 'foo'
        q = questions.Question(name, ignore=False)

        self.assertFalse(q.ignore)

    def test_ignore_works_for_function_returning_true(self):
        name = 'foo'
        q = questions.Question(name, ignore=lambda x: True)

        self.assertTrue(q.ignore)

    def test_ignore_works_for_function_returning_false(self):
        name = 'foo'
        q = questions.Question(name, ignore=lambda x: False)

        self.assertFalse(q.ignore)

    def test_ignore_works_for_function_returning_none(self):
        name = 'foo'
        q = questions.Question(name, ignore=lambda x: None)

        self.assertFalse(q.ignore)

    def test_ignore_function_receives_answers(self):
        name = 'foo'
        method = lambda x: isinstance(x, dict)
        q = questions.Question(name, ignore=method)

        self.assertTrue(q.ignore, "Method was not called with a dict instance")

    def test_default_message_is_empty(self):
        name = 'foo'
        q = questions.Question(name)

        self.assertEqual('', q.message)

    def test_message_set(self):
        name = 'foo'
        message = 'bar'
        q = questions.Question(name, message=message)

        self.assertEqual(message, q.message)

    def test_message_previous_answers_replacement(self):
        name = 'foo'
        message = 'replacement == {whatever}'
        expected = 'replacement == replacement'
        q = questions.Question(name, message=message)
        q.answers = {'whatever': 'replacement'}

        self.assertEqual(expected, q.message)

    def test_default_default_value(self):
        name = 'foo'
        q = questions.Question(name)

        self.assertIsNone(q.default)

    def test_setting_default_value(self):
        name = 'foo'
        expected = object()
        q = questions.Question(name, default=expected)

        self.assertEqual(expected, q.default)

    def test_default_choices_value(self):
        name = 'foo'
        expected = []
        q = questions.Question(name)

        self.assertEqual(expected, q.choices)

    def test_setting_choices_value(self):
        name = 'foo'
        expected = (object(), )
        q = questions.Question(name, choices=expected)

        self.assertEqual(expected, q.choices)

    def test_validate_false_raises_exception(self):
        name = 'foo'
        q = questions.Question(name, validate=False)

        with self.assertRaises(errors.ValidationError):
            q.validate(None)

    def test_validate_function_returning_false_raises_exception(self):
        name = 'foo'
        q = questions.Question(name, validate=lambda x, y: False)

        with self.assertRaises(errors.ValidationError):
            q.validate(None)

    def test_validate_function_returning_true_ends_ok(self):
        name = 'foo'
        q = questions.Question(name, validate=lambda x, y: True)

        q.validate(None)

    def test_validate_function_raising_exception(self):
        def raise_exc(x, y):
            raise Exception('foo')
        name = 'foo'
        q = questions.Question(name, validate=raise_exc)

        with self.assertRaises(errors.ValidationError):
            q.validate(None)

    def test_validate_function_receives_object(self):
        expected = object()

        def compare(x, y):
            return expected == y
        name = 'foo'
        q = questions.Question(name, validate=compare)

        try:
            q.validate(expected)
        except errors.ValidationError:
            self.fail('Validation function did not receive the current value')


class TestConfirmQuestion(unittest.TestCase):
    def test_default_default_value_is_false_instead_of_none(self):
        name = 'foo'
        q = questions.Confirm(name)

        self.assertEquals(False, q.default)
