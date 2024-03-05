from blessed import Terminal

import inquirer


class BaseConsoleRender:
    title_inline = False

    def __init__(self, question, theme=None, terminal=None, show_default=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question = question
        self.terminal = terminal or Terminal()
        self.answers = {}
        self.theme = theme
        self.show_default = show_default

        if isinstance(question, inquirer.List) and question.lenlimit is not None:
            self.max_options_displayed_at_once = question.lenlimit
        else:
            self.max_options_displayed_at_once = 13
        
        # Should be odd number as there is always one question selected
        self.half_options = int((self.max_options_displayed_at_once - 1) / 2)

    def other_input(self):
        other = inquirer.text(self.question.message, autocomplete=self.question.autocomplete)
        return other

    def get_header(self):
        return self.question.message

    def get_hint(self):
        return ""

    def get_current_value(self):
        return ""

    def get_options(self):
        return []

    def process_input(self, pressed):
        raise NotImplementedError("Abstract")

    def handle_validation_error(self, error):
        if error.reason:
            return error.reason

        ret = f'"{error.value}" is not a valid {self.question.name}.'
        try:
            ret.format()
            return ret
        except (ValueError, KeyError):
            return f"Entered value is not a valid {self.question.name}."
