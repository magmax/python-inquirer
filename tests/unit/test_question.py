import unittest
import doublex

from inquirer import questions


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
