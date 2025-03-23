import unittest

import pytest
from readchar import key

import inquirer.questions as questions
import tests.integration.console_render.helper as helper
from inquirer.render import ConsoleRender


class FilterListRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()
        self.choices = sorted(str.__dict__.keys())
        self.query = ""

    def tearDown(self):
        self.base_teardown()

    def _filter_choices(self, query, collection):
        self.query = query
        self.choices = list(filter(lambda x: query in str(x), collection))
        self.query = query
        return self.choices

    def perform_query(self, query, choices=["foo", "bar", "bazz"]):
        key_input = []
        message = "A message"
        variable = "Variable Choice"
        filtered_choices = choices

        question = questions.FilterList(variable, message, choices=choices)
        filtered_choices = self._filter_choices(query, choices)
        key_input.extend(list(query))
        key_input.append(key.ENTER)
        stdin = helper.event_factory(*key_input)
        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertInStdout(query)
        self.assertInStdout(message)
        for choice in filtered_choices:
            self.assertInStdout(choice)
        return result

    def test_choices_are_shown(self):
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

    def test_filter(self, query="b"):
        result = self.perform_query(query)
        assert result == "bar"

    def test_choices_are_not_found(self, query="dont_exist"):
        res = self.perform_query(query)
        assert res == query

    def test_ctrl_w(self):
        query = "bazz"
        keys = list(query) + [key.CTRL_W, key.ENTER]
        stdin = helper.event_factory(*keys)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertInStdout(message)
        for choice in choices:
            self.assertInStdout(choice)
        assert result == "foo"

    def test_backspace(self):
        query = "b"
        keys = list(query) + [key.BACKSPACE, key.ENTER]
        stdin = helper.event_factory(*keys)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertInStdout(message)
        for choice in choices:
            self.assertInStdout(choice)
        assert result == "foo"

    def test_choose_the_first(self):
        stdin = helper.event_factory(key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.FilterList(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "foo"

    def test_choose_the_second(self):
        stdin = helper.event_factory(key.DOWN, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.FilterList(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "bar"

    def test_choose_with_long_choices(self, downkey=key.DOWN):
        stdin = helper.event_factory(
            *[downkey] * 10,
            key.ENTER,
        )
        message = "Number message"
        variable = "Number variable"
        choices = list(range(15))

        question = questions.FilterList(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == 10

    def test_tab_key(self):
        self.test_choose_with_long_choices(key.TAB)

    def test_move_up(self):
        stdin = helper.event_factory(key.DOWN, key.UP, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.FilterList(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "foo"

    def test_move_down_carousel(self):
        stdin = helper.event_factory(key.DOWN, key.DOWN, key.DOWN, key.DOWN, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.FilterList(variable, message, choices=choices, carousel=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "bar"

    def test_move_up_carousel(self):
        stdin = helper.event_factory(key.UP, key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.FilterList(variable, message, choices=choices, carousel=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        assert result == "bazz"

    def test_ctrl_c_breaks_execution(self):
        stdin_array = [key.CTRL_C]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = questions.FilterList(variable, message)

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

        question = questions.FilterList(variable, message, choices=choices.keys(), hints=choices)

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

        question = questions.FilterList(variable, message, choices=choices.keys(), hints=choices)

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

        question = questions.FilterList(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        sut.render(question)

        self.assertInStdout("bb")

    def test_custom_filter_func(self):
        def custom_func(txt, itr):
            return [list(itr)[-1]]

        keys = list("query") + [key.ENTER]
        stdin = helper.event_factory(*keys)
        message = "Foo message"
        variable = "Bar variable"
        choices = ["foo", "bar", "bazz"]

        question = questions.FilterList(variable, message, choices=choices, filter_func=custom_func)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)
        assert result == "bazz"

    def test_default_search_ignores_tags(self):
        query = "tag"
        stdin = helper.event_factory(*list(query), key.ENTER)
        message = "Foo message"
        variable = "Bar variable"
        choices = [
            ("xx", "tag1"),
            ("yy", "tag2"),
        ]

        question = questions.FilterList(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        # not found behaviour returns search/query input
        assert result == query
        assert result != "tag1"
        assert result != "tag2"
