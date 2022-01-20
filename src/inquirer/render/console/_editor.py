from readchar import key

from inquirer import errors
from inquirer.render.console.base import BaseConsoleRender


class Editor(BaseConsoleRender):
    title_inline = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current = ""

    def get_current_value(self):
        return "{}Press <enter> to launch your editor{}".format(
            self.theme.Editor.opening_prompt_color, self.terminal.normal
        )

    def handle_validation_error(self, error):
        if error.reason:
            return error.reason

        return f"Entered value is not a valid {self.question.name}."

    def process_input(self, pressed):
        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()

        if pressed in (key.CR, key.LF, key.ENTER):
            # The import of python-editor needs to be here, at this
            # low level to prevent 'editor' itself from importing
            # distutils.spawn until it is actually being used. This
            # has to do with ubuntu (debian) python packages
            # artificially separated from distutils.
            #
            # If this import is at top level inquirer breaks on ubuntu
            # until the user explicitly apt-get install
            # python3-distutils. With the import here it will only
            # break if the code is utilizing the Editor prompt.
            import editor
            data = editor.edit(contents=self.question.default or "")
            raise errors.EndOfInput(data.decode("utf-8"))

        raise errors.ValidationError(
            "You have pressed unknown key! " "Press <enter> to open editor or " "CTRL+C to exit."
        )
