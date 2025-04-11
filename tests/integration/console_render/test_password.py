from readchar import key

import inquirer
from inquirer.render import ConsoleRender
from tests.integration.console_render import helper


class PasswordRenderTest(helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_do_not_show_values(self):
        stdin = helper.event_factory("m", "y", " ", "p", "a", "s", "s", "w", "o", "r", "d", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"

        question = inquirer.questions.Password(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        sut.render(question)

        self.assertInStdout(message)
        self.assertNotInStdout("my password")

    def test_allows_deletion(self):
        stdin_array = ["a", key.BACKSPACE, "b", key.ENTER]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = inquirer.questions.Password(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual("b", result)

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

        question = inquirer.questions.Password(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual("abdce", result)

    def test_ctrl_c_breaks_execution(self):
        stdin_array = [key.CTRL_C]
        stdin = helper.event_factory(*stdin_array)
        message = "Foo message"
        variable = "Bar variable"

        question = inquirer.questions.Password(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        with self.assertRaises(KeyboardInterrupt):
            sut.render(question)

    def test_validate(self):
        stdin = helper.event_factory("p", "a", "s", "s", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"

        def validate(answers, current):
            return False

        question = inquirer.questions.Password(variable, message, validate=validate)

        sut = ConsoleRender(event_generator=stdin)
        with self.assertRaises(StopIteration):
            sut.render(question)

    def test_handle_validation_error_with_reason(self):
        stdin = helper.event_factory("p", "a", "s", "s", key.ENTER)
        message = "Foo message"
        variable = "Bar variable"

        def validate(answers, current):
            raise inquirer.errors.ValidationError("", reason="some reason")

        question = inquirer.questions.Password(variable, message, validate=validate)

        sut = ConsoleRender(event_generator=stdin)
        with self.assertRaises(StopIteration):
            sut.render(question)
