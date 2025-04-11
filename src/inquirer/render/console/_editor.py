import editor
from readchar import key

from inquirer import errors
from inquirer.render.console.base import BaseConsoleRender


class Editor(BaseConsoleRender):
    title_inline = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current = ""

    def get_current_value(self):
        if self.theme is None:
            raise errors.ThemeError("Theme does not have Editor theme.")
        return f"{self.theme.Editor.opening_prompt}Press <enter> to launch your editor{self.terminal.normal}"

    def handle_validation_error(self, error: errors.ValidationError) -> str:
        if error.reason:
            return error.reason

        return f"Entered value is not a valid {self.question.name}."

    def process_input(self, pressed: str) -> None:
        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()

        if pressed in (key.CR, key.LF, key.ENTER):
            data = editor.editor(text=self.question.default or "")
            raise errors.EndOfInput(data)

        raise errors.ValidationError("You have pressed unknown key! Press <enter> to open editor or CTRL+C to exit.")
