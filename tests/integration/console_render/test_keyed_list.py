import unittest

import pytest
from readchar import key

import inquirer.questions as questions
import tests.integration.console_render.helper as helper
from inquirer.render import ConsoleRender


class KeyedListRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_all_choices_are_shown(self):
        stdin = helper.event_factory(key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.KeyedList(variable, message, choices=choices)

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

        question = questions.KeyedList(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "foo"

    def test_choose_the_second(self):
        stdin = helper.event_factory(key.DOWN, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.KeyedList(variable, message, choices=choices)

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

        question = questions.KeyedList(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == 10

    def test_move_up(self):
        stdin = helper.event_factory(key.DOWN, key.UP, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.KeyedList(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "foo"

    def test_move_down_carousel(self):
        stdin = helper.event_factory(key.DOWN, key.DOWN, key.DOWN, key.DOWN,
                                     key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "bar"

    def test_move_up_carousel(self):
        stdin = helper.event_factory(key.UP, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "bazz"

    def test_ctrl_c_breaks_execution(self):
        stdin_array = [key.CTRL_C]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = questions.KeyedList(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        with pytest.raises(KeyboardInterrupt):
            sut.render(question)

    def test_select_by_default_key_with_carousel_no_auto(self):
        stdin = helper.event_factory(key.UP, key.UP, "f", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "cat", "dog"]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "foo"

    def test_select_by_default_key_with_no_carousel_no_auto(self):
        stdin = helper.event_factory(key.UP, key.DOWN, "d", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "cat", "dog"]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "dog"

    def test_select_by_explicit_key_with_carousel_no_auto(self):
        stdin = helper.event_factory(key.UP, key.UP, "f", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = [
            ("foo", "foo", "f"),
            ("bar", "bar", "b"),
            ("cat", "cat", "c"),
            ("dog", "dog", "d")
        ]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "foo"

    def test_select_by_explicit_key_with_no_carousel_no_auto(self):
        stdin = helper.event_factory(key.UP, key.DOWN, "d", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = [
            ("foo", "foo", "f"),
            ("bar", "bar", "b"),
            ("cat", "cat", "c"),
            ("dog", "dog", "d")
        ]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "dog"

    def test_select_by_default_key_with_carousel_auto(self):
        stdin = helper.event_factory(key.UP, key.UP, "f")
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "cat", "dog"]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True,
                                       auto_confirm=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "foo"

    def test_select_by_default_key_with_no_carousel_auto(self):
        stdin = helper.event_factory(key.UP, key.DOWN, "d")
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "cat", "dog"]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True,
                                       auto_confirm=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "dog"

    def test_select_by_explicit_key_with_carousel_auto(self):
        stdin = helper.event_factory(key.UP, key.UP, "f")
        message = "Foo message"
        variable = "Bar variable"
        choices = [
            ("foo", "foo", "f"),
            ("bar", "bar", "b"),
            ("cat", "cat", "c"),
            ("dog", "dog", "d")
        ]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True,
                                       auto_confirm=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "foo"

    def test_select_by_explicit_key_with_no_carousel_auto(self):
        stdin = helper.event_factory(key.UP, key.DOWN, "d")
        message = "Foo message"
        variable = "Bar variable"
        choices = [
            ("foo", "foo", "f"),
            ("bar", "bar", "b"),
            ("cat", "cat", "c"),
            ("dog", "dog", "d")
        ]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True,
                                       auto_confirm=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "dog"

    def test_select_by_default_key_multiple_matches(self):
        stdin = helper.event_factory(key.UP, key.UP, "b", "b", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "baz", "cat", "dog", "car"]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "baz"

    def test_select_by_default_key_multiple_matches_variation(self):
        stdin = helper.event_factory(key.UP, key.UP, "b", "c", "b", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "baz", "cat", "dog", "car"]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "bar"

    def test_select_by_default_numeric_key_variation(self):
        stdin = helper.event_factory(key.UP, key.UP, "1", "4", "3", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["1. foo", "2. bar", "3. baz", "4. cat", "5. dog", "6. car"]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "3. baz"

    def test_select_by_default_numeric_key_multiple_matches_variation(self):
        stdin = helper.event_factory(key.UP, key.UP, "1", "3", "1", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["1. foo", "2. bar", "3. baz", "4. cat", "1. dog", "6. car"]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "1. dog"

    def test_select_by_default_numeric_key_variation_auto_select(self):
        stdin = helper.event_factory(key.UP, key.UP, "1", "4", "3", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["1. foo", "2. bar", "3. baz", "4. cat", "5. dog", "6. car"]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "3. baz"

    def test_select_by_default_numeric_key_explicit_value_auto_select_(self):
        stdin = helper.event_factory(key.UP, key.UP, "4")
        message = "Foo message"
        variable = "Bar variable"
        choices = [
            ("1. foo", "foo"),
            ("2. bar", "bar"),
            ("3. baz", "baz"),
            ("4. cat", "cat"),
            ("1. dog", "dog"),
            ("6. car", "car")
        ]

        question = questions.KeyedList(variable, message, choices=choices,
                                       carousel=True,
                                       auto_confirm=True)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "cat"
