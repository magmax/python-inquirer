import pathlib
import shutil
import tempfile
import unittest
import sys

from inquirer import errors
from inquirer import questions


class BaseQuestionTests(unittest.TestCase):
    def test_base_question_type(self):
        name = "foo"
        q = questions.Question(name)

        self.assertEqual("base question", q.kind)
        self.assertEqual(name, q.name)

    def test_ignore_works_for_true(self):
        name = "foo"
        q = questions.Question(name, ignore=True)

        self.assertTrue(q.ignore)

    def test_ignore_works_for_false(self):
        name = "foo"
        q = questions.Question(name, ignore=False)

        self.assertFalse(q.ignore)

    def test_ignore_works_for_function_returning_true(self):
        name = "foo"
        q = questions.Question(name, ignore=lambda x: True)

        self.assertTrue(q.ignore)

    def test_ignore_works_for_function_returning_false(self):
        name = "foo"
        q = questions.Question(name, ignore=lambda x: False)

        self.assertFalse(q.ignore)

    def test_ignore_works_for_function_returning_none(self):
        name = "foo"
        q = questions.Question(name, ignore=lambda x: None)

        self.assertFalse(q.ignore)

    def test_ignore_function_receives_answers(self):
        name = "foo"
        q = questions.Question(name, ignore=lambda x: isinstance(x, dict))

        self.assertTrue(q.ignore, "Method was not called with a dict instance")

    def test_default_message_is_empty(self):
        name = "foo"
        q = questions.Question(name)

        self.assertEqual("", q.message)

    def test_message_set(self):
        name = "foo"
        message = "bar"
        q = questions.Question(name, message=message)

        self.assertEqual(message, q.message)

    def test_message_previous_answers_replacement(self):
        name = "foo"
        message = "replacement == {whatever}"
        expected = "replacement == replacement"
        q = questions.Question(name, message=message)
        q.answers = {"whatever": "replacement"}

        self.assertEqual(expected, q.message)

    def test_default_default_value(self):
        name = "foo"
        q = questions.Question(name)

        self.assertIsNone(q.default)

    def test_setting_default_value(self):
        name = "foo"
        expected = object()
        q = questions.Question(name, default=expected)

        self.assertEqual(expected, q.default)

    def test_default_choices_value(self):
        name = "foo"
        expected = []
        q = questions.Question(name)

        self.assertEqual(expected, q.choices)

    def test_setting_choices_value(self):
        name = "foo"
        expected = [
            object(),
        ]
        q = questions.Question(name, choices=expected)

        self.assertEqual(expected, q.choices)

    def test_validate_false_raises_exception(self):
        name = "foo"
        q = questions.Question(name, validate=False)

        with self.assertRaises(errors.ValidationError):
            q.validate(None)

    def test_validate_function_returning_false_raises_exception(self):
        name = "foo"
        q = questions.Question(name, validate=lambda x, y: False)

        with self.assertRaises(errors.ValidationError):
            q.validate(None)

    def test_validate_function_returning_true_ends_ok(self):
        name = "foo"
        q = questions.Question(name, validate=lambda x, y: True)

        q.validate(None)

    def test_validate_function_raising_validation_error(self):
        err = errors.ValidationError("", reason="foo")

        def raise_exc(x, y):
            raise err

        name = "foo"
        q = questions.Question(name, validate=raise_exc)

        try:
            q.validate(None)
        except errors.ValidationError as e:
            self.assertIs(e, err)

    def test_validate_function_receives_object(self):
        expected = object()

        def compare(x, y):
            return expected == y

        name = "foo"
        q = questions.Question(name, validate=compare)

        q.validate(expected)

    def test_factory_text_type(self):
        name = "foo"
        q = questions.question_factory("text", name)

        self.assertEqual("text", q.kind)
        self.assertIsInstance(q, questions.Text)
        self.assertEqual(name, q.name)

    def test_factory_confirm_type(self):
        name = "foo"
        q = questions.question_factory("confirm", name)

        self.assertEqual("confirm", q.kind)
        self.assertIsInstance(q, questions.Confirm)
        self.assertEqual(name, q.name)

    def test_factory_password_type(self):
        name = "foo"
        q = questions.question_factory("password", name)

        self.assertEqual("password", q.kind)
        self.assertIsInstance(q, questions.Password)
        self.assertEqual(name, q.name)

    def test_factory_list_type(self):
        name = "foo"
        q = questions.question_factory("list", name)

        self.assertEqual("list", q.kind)
        self.assertIsInstance(q, questions.List)
        self.assertEqual(name, q.name)

    def test_factory_located_list_type(self):
        name = "ñçÑÇ"
        q = questions.question_factory("list", name)

        self.assertEqual("list", q.kind)
        self.assertIsInstance(q, questions.List)
        self.assertEqual(name, q.name)

    def test_factory_checkbox_type(self):
        name = "foo"
        q = questions.question_factory("checkbox", name)

        self.assertEqual("checkbox", q.kind)
        self.assertIsInstance(q, questions.Checkbox)
        self.assertEqual(name, q.name)

    def test_load_from_dict_text_type(self):
        name = "foo"
        q = questions.load_from_dict({"kind": "text", "name": name})

        self.assertEqual("text", q.kind)
        self.assertIsInstance(q, questions.Text)
        self.assertEqual(name, q.name)

    def test_load_from_json_text_type(self):
        name = "foo"
        q = questions.load_from_json('{"kind": "text", "name": "%s"}' % name)

        self.assertEqual("text", q.kind)
        self.assertIsInstance(q, questions.Text)
        self.assertEqual(name, q.name)

    def test_factory_bad_type(self):
        name = "foo"
        with self.assertRaises(errors.UnknownQuestionTypeError):
            questions.question_factory("bad", name)

    def test_load_from_json_list(self):
        name = "foo"
        result = questions.load_from_json('[{"kind": "text", "name": "%s"}]' % name)

        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertEqual("text", result[0].kind)
        self.assertIsInstance(result[0], questions.Text)
        self.assertEqual(name, result[0].name)


class TestConfirmQuestion(unittest.TestCase):
    def test_default_default_value_is_false_instead_of_none(self):
        name = "foo"
        q = questions.Confirm(name)

        self.assertEqual(False, q.default)


class TestPathQuestion(unittest.TestCase):
    def test_path_validation(self):
        def do_test(path, result=True):
            q = questions.Path("validation_test")
            if result:
                self.assertIsNone(q.validate(path))
            else:
                with self.assertRaises(errors.ValidationError):
                    q.validate(path)

        do_test(None, False)

        # Path component must not contains null bytes
        do_test("some/path/with/{}byte".format("\x00"), False)

    @unittest.skipUnless(sys.platform.startswith("lin"), "Linux only")
    def test_path_validation_linux(self):
        q = questions.Path("validation_test")
        for path in []:
            with self.assertRaises(errors.ValidationError):
                q.validate(path)

    @unittest.skipUnless(sys.platform.startswith("win"), "Windows only")
    def test_path_validation_windows(self):
        q = questions.Path("validation_test")
        for path in ["fo:/bar"]:
            with self.assertRaises(errors.ValidationError):
                q.validate(path)

    def test_path_type_validation_no_existence_check(self):
        def do_test(path_type, path, result=True):
            q = questions.Path("path_type_test", path_type=path_type)
            if result:
                self.assertIsNone(q.validate(path))
            else:
                with self.assertRaises(errors.ValidationError):
                    q.validate(path)

        do_test(questions.Path.ANY, "./aa/bb")
        do_test(questions.Path.ANY, "./aa/")
        do_test(questions.Path.ANY, "aa/bb")
        do_test(questions.Path.ANY, "aa/")
        do_test(questions.Path.ANY, "/aa/")
        do_test(questions.Path.ANY, "/aa/bb")
        do_test(questions.Path.ANY, "~/aa/bb")

        do_test(questions.Path.FILE, "./aa/bb")
        do_test(questions.Path.FILE, "./aa/", False)
        do_test(questions.Path.FILE, "aa/bb")
        do_test(questions.Path.FILE, "aa/", False)
        do_test(questions.Path.FILE, "/aa/", False)
        do_test(questions.Path.FILE, "~/aa/", False)
        do_test(questions.Path.FILE, "/aa/bb")
        do_test(questions.Path.FILE, "~/aa/.bb")

        do_test(questions.Path.DIRECTORY, "./aa/bb")
        do_test(questions.Path.DIRECTORY, "./aa/")
        do_test(questions.Path.DIRECTORY, "aa/bb")
        do_test(questions.Path.DIRECTORY, "aa/")
        do_test(questions.Path.DIRECTORY, "/aa/")
        do_test(questions.Path.DIRECTORY, "~/aa/")
        do_test(questions.Path.DIRECTORY, "/aa/bb")
        do_test(questions.Path.DIRECTORY, "~/aa/bb")

    def test_path_type_validation_existence_check(self):
        root = pathlib.Path(tempfile.mkdtemp())
        some_non_existing_dir = root / "some_non_existing_dir"
        some_existing_dir = root / "some_dir"
        some_existing_dir.mkdir()
        some_non_existing_file = root / "some_non_existing_file"
        some_existing_file = root / "some_file"
        some_existing_file.touch()

        def do_test(path_type, path, result=True):
            q = questions.Path("path_type_test", exists=True, path_type=path_type)
            if result:
                self.assertIsNone(q.validate(str(path)))
            else:
                with self.assertRaises(errors.ValidationError):
                    q.validate(str(path))

        try:
            do_test(questions.Path.ANY, some_existing_file)
            do_test(questions.Path.ANY, some_non_existing_file, False)
            do_test(questions.Path.ANY, some_existing_dir)
            do_test(questions.Path.ANY, some_non_existing_dir, False)

            do_test(questions.Path.FILE, some_existing_file)
            do_test(questions.Path.FILE, some_non_existing_file, False)
            do_test(questions.Path.FILE, some_existing_dir, False)

            do_test(questions.Path.DIRECTORY, some_existing_dir)
            do_test(questions.Path.DIRECTORY, some_non_existing_dir, False)
            do_test(questions.Path.DIRECTORY, some_existing_file, False)

        finally:
            shutil.rmtree(root)

    def test_default_value_validation(self):
        root = pathlib.Path(tempfile.mkdtemp())
        some_non_existing_dir = root / "some_non_existing_dir"
        some_existing_dir = root / "some_dir"
        some_existing_dir.mkdir()
        some_non_existing_file = root / "some_non_existing_file"
        some_existing_file = root / "some_file"
        some_existing_file.touch()

        def do_test(default, path_type, exists, result=True):
            if result:
                questions.Path("path", default=str(default), exists=exists, path_type=path_type)
            else:
                with self.assertRaises(ValueError):
                    questions.Path("path", default=str(default), exists=exists, path_type=path_type)

        do_test(some_existing_dir, questions.Path.DIRECTORY, exists=True)
        do_test(some_non_existing_dir, questions.Path.DIRECTORY, exists=True, result=False)

        do_test(some_existing_file, questions.Path.FILE, exists=True)
        do_test(some_non_existing_file, questions.Path.FILE, exists=True, result=False)

    def test_path_type_value_validation(self):
        questions.Path("abs_path", path_type=questions.Path.ANY)
        questions.Path("abs_path", path_type="any")
        questions.Path("abs_path", path_type=questions.Path.FILE)
        questions.Path("abs_path", path_type="file")
        questions.Path("abs_path", path_type=questions.Path.DIRECTORY)
        questions.Path("abs_path", path_type="directory")

        with self.assertRaises(ValueError):
            questions.Path("abs_path", path_type=questions.Path.kind)

        with self.assertRaises(ValueError):
            questions.Path("abs_path", path_type="false")


def test_tagged_value():
    LABEL = "label"
    VALUE = "l"
    tp = (LABEL, VALUE)
    tv = questions.TaggedValue(*tp)

    assert (str(tv) == str(LABEL)) is True
    assert (repr(tv) == repr(VALUE)) is True
    assert (hash(tv) == hash(tp)) is True

    assert (tv == tv) is True
    assert (tv != tv) is False
    assert (tv == tp) is True
    assert (tv == VALUE) is True
    assert (tv == "") is False
