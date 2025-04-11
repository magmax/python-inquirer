from inquirer import errors
from inquirer import questions
from inquirer.render import ConsoleRender
from tests.integration.console_render import helper


class BasicTest(helper.BaseTestCase):
    def test_rendering_erroneous_type(self):
        question = questions.Question("foo", "bar")

        sut = ConsoleRender()
        with self.assertRaises(errors.UnknownQuestionTypeError):
            sut.render(question)
