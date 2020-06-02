# encoding: utf-8

import os
import shutil
import tempfile
import unittest

from inquirer import questions
from inquirer import errors


class BaseQuestionTests(unittest.TestCase):
    def test_base_question_type(self):
        name = 'foo'
        q = questions.Question(name)

        self.assertEqual('base question', q.kind)
        self.assertEqual(name, q.name)

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
        q = questions.Question(name, ignore=lambda x: isinstance(x, dict))

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
        expected = [object(), ]
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

    def test_validate_function_raising_validation_error(self):
        err = errors.ValidationError('', reason='foo')

        def raise_exc(x, y):
            raise err

        name = 'foo'
        q = questions.Question(name, validate=raise_exc)

        try:
            q.validate(None)
        except errors.ValidationError as e:
            self.assertIs(e, err)

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

    def test_factory_text_type(self):
        name = 'foo'
        q = questions.question_factory('text', name)

        self.assertEqual('text', q.kind)
        self.assertIsInstance(q, questions.Text)
        self.assertEqual(name, q.name)

    def test_factory_confirm_type(self):
        name = 'foo'
        q = questions.question_factory('confirm', name)

        self.assertEqual('confirm', q.kind)
        self.assertIsInstance(q, questions.Confirm)
        self.assertEqual(name, q.name)

    def test_factory_password_type(self):
        name = 'foo'
        q = questions.question_factory('password', name)

        self.assertEqual('password', q.kind)
        self.assertIsInstance(q, questions.Password)
        self.assertEqual(name, q.name)

    def test_factory_list_type(self):
        name = 'foo'
        q = questions.question_factory('list', name)

        self.assertEqual('list', q.kind)
        self.assertIsInstance(q, questions.List)
        self.assertEqual(name, q.name)

    def test_factory_located_list_type(self):
        name = 'ñçÑÇ'
        q = questions.question_factory('list', name)

        self.assertEqual('list', q.kind)
        self.assertIsInstance(q, questions.List)
        self.assertEqual(name, q.name)

    def test_factory_checkbox_type(self):
        name = 'foo'
        q = questions.question_factory('checkbox', name)

        self.assertEqual('checkbox', q.kind)
        self.assertIsInstance(q, questions.Checkbox)
        self.assertEqual(name, q.name)

    def test_load_from_dict_text_type(self):
        name = 'foo'
        q = questions.load_from_dict({'kind': 'text', 'name': name})

        self.assertEqual('text', q.kind)
        self.assertIsInstance(q, questions.Text)
        self.assertEqual(name, q.name)

    def test_load_from_json_text_type(self):
        name = 'foo'
        q = questions.load_from_json(
            '{"kind": "text", "name": "%s"}' % name)

        self.assertEqual('text', q.kind)
        self.assertIsInstance(q, questions.Text)
        self.assertEqual(name, q.name)

    def test_factory_bad_type(self):
        name = 'foo'
        with self.assertRaises(errors.UnknownQuestionTypeError):
            questions.question_factory('bad', name)

    def test_load_from_json_list(self):
        name = 'foo'
        result = questions.load_from_json(
            '[{"kind": "text", "name": "%s"}]' % name)

        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertEqual('text', result[0].kind)
        self.assertIsInstance(result[0], questions.Text)
        self.assertEqual(name, result[0].name)


class TestConfirmQuestion(unittest.TestCase):
    def test_default_default_value_is_false_instead_of_none(self):
        name = 'foo'
        q = questions.Confirm(name)

        self.assertEqual(False, q.default)


class TestPathQuestion(unittest.TestCase):
    def test_path_validation(self):
        def do_test(path, result=True):
            q = questions.Path('validation_test')
            if result:
                self.assertIsNone(q.validate(path))
            else:
                with self.assertRaises(errors.ValidationError):
                    q.validate(path)

        do_test(None, False)

        if os.environ.get('TRAVIS_PYTHON_VERSION') != 'pypy3':
            # Path component must not be longer then 255 bytes
            do_test('a' * 256, False)
            do_test(os.path.abspath('/asdf/' + 'a' * 256), False)
            do_test('{}/{}'.format('a' * 255, 'b' * 255), True)

            # Path component must not contains null bytes
            do_test('some/path/with/{}byte'.format(b'\x00'.decode('utf-8')),
                    False)

    def test_path_type_validation_no_existence_check(self):
        def do_test(path_type, path, result=True):
            q = questions.Path('path_type_test', path_type=path_type)
            if result:
                self.assertIsNone(q.validate(path))
            else:
                with self.assertRaises(errors.ValidationError):
                    q.validate(path)

        do_test(questions.Path.ANY, './aa/bb')
        do_test(questions.Path.ANY, './aa/')
        do_test(questions.Path.ANY, 'aa/bb')
        do_test(questions.Path.ANY, 'aa/')
        do_test(questions.Path.ANY, '/aa/')
        do_test(questions.Path.ANY, '/aa/bb')
        do_test(questions.Path.ANY, '~/aa/bb')

        do_test(questions.Path.FILE, './aa/bb')
        do_test(questions.Path.FILE, './aa/', False)
        do_test(questions.Path.FILE, 'aa/bb')
        do_test(questions.Path.FILE, 'aa/', False)
        do_test(questions.Path.FILE, '/aa/', False)
        do_test(questions.Path.FILE, '~/aa/', False)
        do_test(questions.Path.FILE, '/aa/bb')
        do_test(questions.Path.FILE, '~/aa/.bb')

        do_test(questions.Path.DIRECTORY, './aa/bb', False)
        do_test(questions.Path.DIRECTORY, './aa/')
        do_test(questions.Path.DIRECTORY, 'aa/bb', False)
        do_test(questions.Path.DIRECTORY, 'aa/')
        do_test(questions.Path.DIRECTORY, '/aa/')
        do_test(questions.Path.DIRECTORY, '~/aa/')
        do_test(questions.Path.DIRECTORY, '/aa/bb', False)
        do_test(questions.Path.DIRECTORY, '~/aa/bb', False)

    def test_path_type_validation_existing(self):
        root = tempfile.mkdtemp()
        some_existing_dir = os.path.join(root, 'some_dir')
        some_non_existing_dir = os.path.join(root, 'some_non_existing_dir')
        some_existing_file = os.path.join(root, 'some_file')
        some_non_existing_file = os.path.join(root, 'some_non_existing_file')

        os.mkdir(some_existing_dir)
        open(some_existing_file, 'a').close()

        def do_test(path_type, path, exists, result=True):
            q = questions.Path('path_type_test', exists=exists,
                               path_type=path_type)
            if result:
                self.assertIsNone(q.validate(path))
            else:
                with self.assertRaises(errors.ValidationError):
                    q.validate(path)

        try:
            do_test(questions.Path.ANY, some_existing_file, True, True)
            do_test(questions.Path.ANY, some_non_existing_file, True, False)
            do_test(questions.Path.ANY, some_existing_file, False, False)
            do_test(questions.Path.ANY, some_non_existing_file, False, True)
            do_test(questions.Path.ANY, some_existing_dir, True, True)
            do_test(questions.Path.ANY, some_non_existing_dir, True, False)
            do_test(questions.Path.ANY, some_existing_dir, False, False)
            do_test(questions.Path.ANY, some_non_existing_dir, False, True)

            do_test(questions.Path.FILE, some_existing_file, True, True)
            do_test(questions.Path.FILE, some_non_existing_file, True, False)
            do_test(questions.Path.FILE, some_non_existing_file, False, True)
            do_test(questions.Path.FILE, some_existing_file, False, False)

            do_test(questions.Path.DIRECTORY,
                    some_existing_dir, True, True)
            do_test(questions.Path.DIRECTORY,
                    some_non_existing_dir, True, False)
            do_test(questions.Path.DIRECTORY,
                    some_existing_dir, False, False)
            do_test(questions.Path.DIRECTORY,
                    some_non_existing_dir, False, True)

        finally:
            shutil.rmtree(root)

    def test_normalizing_value(self):
        # Expanding Home
        home = os.path.expanduser('~')
        q = questions.Path('home')

        path = '~/some_path/some_file'
        self.assertNotIn(home, path)
        self.assertIn(home, q.normalize_value(path))

        # Normalizing to absolute path
        root = os.path.abspath(__file__).split(os.path.sep)[0]
        q = questions.Path('abs_path', normalize_to_absolute_path=True)
        self.assertEqual(root, q.normalize_value('some/relative/path').split(
            os.path.sep
        )[0])

    def test_default_value_validation(self):

        with self.assertRaises(ValueError):
            questions.Path('path', default='~/.toggl_log',
                           path_type=questions.Path.DIRECTORY)

        questions.Path('path', default='~/.toggl_log')
