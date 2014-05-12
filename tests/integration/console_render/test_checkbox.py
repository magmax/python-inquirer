import sys
import unittest
import inquirer.questions as questions
import inquirer.errors as errors

from . import helper
from readchar import key

from inquirer.render import ConsoleRender


class CheckboxRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_all_choices_are_shown(self):
        stdin = helper.key_factory(key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.Checkbox(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=stdin)
        result = sut.render(question)

        self.assertInStdout(message)
        for choice in choices:
            self.assertInStdout(choice)

    def test_one_choice(self):
        stdin = helper.key_factory(key.SPACE, key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.Checkbox(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=stdin)
        result = sut.render(question)

        self.assertInStdout(message)
        self.assertEqual(['foo'], result)

    def test_choose_the_second(self):
        stdin = helper.key_factory(key.DOWN, key.SPACE, key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.Checkbox(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=stdin)
        result = sut.render(question)

        self.assertInStdout(message)
        self.assertEqual(['bar'], result)

    def test_can_move(self):
        stdin = helper.key_factory(
            key.DOWN,
            key.DOWN,
            key.UP,
            key.SPACE,
            key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.Checkbox(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=stdin)
        result = sut.render(question)

        self.assertEqual(['bar'], result)

    def test_cannot_move_beyond_upper_limit(self):
        stdin = helper.key_factory(
            key.UP,
            key.UP,
            key.UP,
            key.SPACE,
            key.ENTER,)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.Checkbox(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=stdin)
        result = sut.render(question)

        self.assertEqual(['foo'], result)

    def test_cannot_move_beyond_lower_limit(self):
        stdin = helper.key_factory(
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.SPACE,
            key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.Checkbox(variable, message, choices=choices)

        sut = ConsoleRender(key_generator=stdin)
        result = sut.render(question)

        self.printStdout()

        self.assertEqual(['bazz'], result)
