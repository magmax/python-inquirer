import unittest

import pytest
from readchar import key

import inquirer.questions as questions
import tests.integration.console_render.helper as helper
from inquirer.render import ConsoleRender


class ListRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_all_choices_are_shown(self):
        stdin = helper.event_factory(key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        sut.render(question)

        self.assertInStdout(message)
        for choice in choices:
            self.assertInStdout(choice)

    def test_choose_the_first(self):
        stdin = helper.event_factory(key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "foo"

    def test_choose_the_second(self):
        stdin = helper.event_factory(key.DOWN, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "bar"

    def test_choose_with_long_choices(self):
        stdin = helper.event_factory(
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.DOWN,
            key.ENTER,
        )
        message = "Number message"
        variable = "Number variable"
        choices = list(range(15))

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == 10

    def test_move_up(self):
        stdin = helper.event_factory(key.DOWN, key.UP, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "foo"

    def test_move_down_carousel(self):
        stdin = helper.event_factory(key.DOWN, key.DOWN, key.DOWN, key.DOWN, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.List(variable, message, choices=choices, carousel=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "bar"

    def test_move_up_carousel(self):
        stdin = helper.event_factory(key.UP, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.List(variable, message, choices=choices, carousel=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "bazz"

    def test_ctrl_c_breaks_execution(self):
        stdin_array = [key.CTRL_C]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = questions.List(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        with pytest.raises(KeyboardInterrupt):
            sut.render(question)

    def test_first_hint_is_shown(self):
        stdin = helper.event_factory(key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = {
            "foo": "Foo",
            "bar": "Bar",
            "bazz": "Bazz",
        }

        question = questions.List(variable, message, choices=choices.keys(), hints=choices)

        sut = ConsoleRender(event_generator=stdin)
        sut.render(question)

        self.assertInStdout("Foo")

    def test_second_hint_is_shown(self):
        stdin = helper.event_factory(key.DOWN, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = {
            "foo": "Foo",
            "bar": "Bar",
            "bazz": "Bazz",
        }

        question = questions.List(variable, message, choices=choices.keys(), hints=choices)

        sut = ConsoleRender(event_generator=stdin)
        sut.render(question)

        self.assertInStdout("Bar")

    def test_taggedValue_with_dict(self):
        stdin = helper.event_factory(key.DOWN, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = [
            ("aa", {"a": 1}),
            ("bb", {"b": 2}),
        ]

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        sut.render(question)

        self.assertInStdout("bb")

    def test_page_down_jumps_a_page(self):
        stdin = helper.event_factory(key.PAGE_DOWN, key.ENTER)
        choices = list(range(20))

        question = questions.List("number", "Number message", choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == 13

    def test_page_up_jumps_a_page(self):
        stdin = helper.event_factory(key.PAGE_DOWN, key.PAGE_UP, key.ENTER)
        choices = list(range(20))

        question = questions.List("number", "Number message", choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == 0

    def test_page_down_stops_at_the_last_choice(self):
        stdin = helper.event_factory(key.PAGE_DOWN, key.PAGE_DOWN, key.ENTER)
        choices = list(range(20))

        question = questions.List("number", "Number message", choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == 19

    def test_page_up_wraps_when_carousel_is_enabled(self):
        stdin = helper.event_factory(key.PAGE_UP, key.ENTER)
        choices = list(range(20))

        question = questions.List("number", "Number message", choices=choices, carousel=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == 19

    def test_page_down_wraps_when_carousel_is_enabled(self):
        stdin = helper.event_factory(key.PAGE_DOWN, key.PAGE_DOWN, key.PAGE_DOWN, key.ENTER)
        choices = list(range(20))

        question = questions.List("number", "Number message", choices=choices, carousel=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == 0

    def test_max_options_displayed_at_once_shows_more_choices(self):
        stdin = helper.event_factory(key.ENTER)
        message = "Pick one"
        variable = "many"
        choices = [f"opt-{i:03d}" for i in range(40)]

        question = questions.List(
            variable, message, choices=choices, max_options_displayed_at_once=25
        )
        sut = ConsoleRender(event_generator=stdin)
        sut.render(question)

        self.assertInStdout("opt-000")
        self.assertInStdout("opt-024")
        self.assertNotInStdout("opt-025")

    def test_max_options_displayed_at_once_default_unchanged(self):
        stdin = helper.event_factory(key.ENTER)
        message = "Pick one"
        variable = "many"
        choices = [f"opt-{i:03d}" for i in range(40)]

        question = questions.List(variable, message, choices=choices)
        sut = ConsoleRender(event_generator=stdin)
        sut.render(question)

        self.assertInStdout("opt-000")
        self.assertInStdout("opt-012")
        self.assertNotInStdout("opt-013")
