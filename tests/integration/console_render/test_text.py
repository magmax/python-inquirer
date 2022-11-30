import re
import unittest

from readchar import key

import inquirer.questions as questions
import tests.integration.console_render.helper as helper
from inquirer import errors
from inquirer.render import ConsoleRender


class TextRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_basic_render(self):
        stdin_msg = "This is a foo message"
        stdin_array = [x for x in stdin_msg + key.ENTER]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = questions.Text(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual(stdin_msg, result)
        self.assertInStdout(message)

    def test_ignore_true_should_return(self):
        stdin = "This is a foo message"
        message = "Foo message"
        variable = "Bar variable"
        expected = ""

        question = questions.Text(variable, ignore=True, default=expected, message=message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual(expected, result)
        self.assertNotInStdout(message)

    def test_validation_fails(self):
        stdin_array = [x for x in "Invalid" + key.ENTER + key.BACKSPACE * 20 + "9999" + key.ENTER]
        stdin = helper.event_factory(*stdin_array)

        message = "Insert number"
        variable = "foo"
        expected = "9999"

        question = questions.Text(variable, validate=lambda _, x: re.match(r"\d+", x), message=message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)
        self.assertEqual(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('"Invalid" is not a valid foo')

    def test_validation_fails_with_brace(self):
        stdin_array = [x for x in "{Invalid" + key.ENTER + key.BACKSPACE * 20 + "9999" + key.ENTER]
        stdin = helper.event_factory(*stdin_array)

        message = "Insert number"
        variable = "foo"
        expected = "9999"

        question = questions.Text(variable, validate=lambda _, x: re.match(r"\d+", x), message=message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)
        self.assertEqual(expected, result)
        self.assertInStdout(message)
        self.assertInStdout("Entered value is not a valid foo")

    def test_validation_fails_with_custom_message(self):
        stdin_array = [x for x in "Invalid" + key.ENTER + key.BACKSPACE * 20 + "9999" + key.ENTER]
        stdin = helper.event_factory(*stdin_array)

        message = "Insert number"
        variable = "foo"
        expected = "9999"

        def raise_exc(x, current):
            if current != "9999":
                raise errors.ValidationError("", reason="Custom error")
            return True

        question = questions.Text(variable, validate=raise_exc, message=message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)
        self.assertEqual(expected, result)
        self.assertInStdout(message)
        self.assertInStdout("Custom error")

    def test_allows_BACKSPACE_deletion(self):
        stdin_array = ["a", key.BACKSPACE, "b", key.ENTER]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = questions.Text(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual("b", result)

    def test_allows_DELETE_deletion(self):
        stdin_array = ["a", "b", key.LEFT, key.LEFT, "c", key.SUPR, key.SUPR, key.ENTER]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = questions.Text(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual("c", result)

    def test_cursor_movement(self):
        stdin_array = [
            "a",
            key.UP,
            "b",
            key.DOWN,
            "c",
            key.LEFT,
            "d",
            key.RIGHT,
            "e",
            key.ENTER,
        ]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = questions.Text(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual("abdce", result)

    def test_TAB_without_autocomplete(self):
        stdin_array = ["a", key.TAB, "b", key.ENTER]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = questions.Text(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual("a\tb", result)

    def test_TAB_with_autocomplete(self):
        stdin_array = ["a", key.TAB, "b", key.ENTER]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = questions.Text(variable, message, autocomplete=lambda _text, _state: "abc")

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual("abcb", result)

    def test_TAB_with_non_str_autocomplete(self):
        stdin_array = ["a", key.TAB, "b", key.ENTER]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = questions.Text(variable, message, autocomplete=lambda _text, _state: 1337)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual("ab", result)

    def test_TAB_with_autocomplete_cycle(self):
        stdin_array = ["a", key.TAB, key.TAB, key.TAB, "b", key.TAB, key.ENTER]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        prev_state_cell = None

        def autocomplete_func(text, state):
            nonlocal prev_state_cell

            # Swap state memory
            prev_state = prev_state_cell
            prev_state_cell = state

            if state == 0:
                if prev_state is None:
                    # First call
                    pass
                else:
                    # After we pressed TAB 3 times and then pressed b, then TAB again
                    # state should be 0 again
                    assert prev_state == 2
                    return "it worked"
            else:
                assert state == prev_state + 1
            return text

        question = questions.Text(variable, message, autocomplete=autocomplete_func)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual("it worked", result)

    def test_ctrl_c_breaks_execution(self):
        stdin_array = [key.CTRL_C]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = questions.Text(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        with self.assertRaises(KeyboardInterrupt):
            sut.render(question)
