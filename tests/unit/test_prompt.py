import unittest
import doublex

from inquirer import prompt


class PromptTests(unittest.TestCase):
    def test_prompt_returns_a_hash(self):
        self.assertEquals({}, prompt([]))

    def test_prompt_renders_a_questions(self):
        question1 = doublex.Stub()
        question1.name = 'foo'
        result1 = object()
        with doublex.Mock() as render:
            render.render(question1, {}).returns(result1)

        result = prompt([question1], render=render)

        self.assertEquals({'foo': result1}, result)

    def test_prompt_renders_all_questions(self):
        question1 = doublex.Stub()
        question1.name = 'foo'
        result1 = object()

        question2 = doublex.Stub()
        question2.name = 'bar'
        result2 = object()

        result = object()
        with doublex.Mock() as render:
            render.render(question1, {}).returns(result1)
            render.render(question2, {'foo': result1}).returns(result2)

        result = prompt([question1, question2], render=render)

        self.assertEquals({'foo': result1, 'bar': result2}, result)
