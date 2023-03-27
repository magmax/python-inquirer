import math
import sys

from blessed import Terminal

from inquirer import errors
from inquirer import events
from inquirer import themes
from inquirer.render.console._checkbox import Checkbox
from inquirer.render.console._confirm import Confirm
from inquirer.render.console._editor import Editor
from inquirer.render.console._list import List
from inquirer.render.console._password import Password
from inquirer.render.console._path import Path
from inquirer.render.console._text import Text


class ConsoleRender:
    def __init__(self, event_generator=None, theme=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._event_gen = event_generator or events.KeyEventGenerator()
        self.terminal = Terminal()
        self._previous_error = None
        self._position = 0
        self._theme = theme or themes.Default()

    def render(self, question, answers=None):
        question.answers = answers or {}

        if question.ignore:
            return question.default

        clazz = self.render_factory(question.kind)
        render = clazz(question, terminal=self.terminal, theme=self._theme, show_default=question.show_default)

        try:
            return self._event_loop(render)
        finally:
            print("")

    def _event_loop(self, render):
        try:
            while True:
                self._relocate_and_clear()
                self._print_status_bar()

                self._print_header(render)
                self._print_options(render)

                self._process_input(render)
        except errors.EndOfInput as e:
            self._go_to_end(render)
            return e.selection

    def _print_status_bar(self):
        if self._previous_error is None:
            self.clear_bottombar()
            return

        self.render_error(self._previous_error)
        self._previous_error = None

    def _print_options(self, render):
        for message, symbol, color in render.get_options():
            if hasattr(message, "decode"):  # python 2
                message = message.decode("utf-8")
            choice = f" {color}{symbol} {message}{self.terminal.normal}"
            if render.question.trim_choices:
                choice = self.trim_str(choice)
            self.print_line(choice)

    def _print_header(self, render):
        header = render.get_header()

        header_prefix_template = "{tq.brackets_color}[{tq.mark_color}?{tq.brackets_color}]{t.normal}"
        header_prefix = header_prefix_template.format(tq=self._theme.Question, t=self.terminal)
        header = f"{header_prefix} {header}"

        default_value = render.question.default
        if default_value and render.show_default:
            header += f" ({self._theme.Question.default_color}{default_value}{self.terminal.normal})"

        header_ending = ": "
        if render.question.trim_header:
            header = self.trim_str(header, extra_after_trimming=header_ending)
        else:
            header += header_ending

        full_header = f"{header}{str(render.get_current_value())}"
        self.print_str(full_header, lf=not render.title_inline)

    def _process_input(self, render):
        try:
            ev = self._event_gen.next()
            if isinstance(ev, events.KeyPressed):
                render.process_input(ev.value)
        except errors.ValidationError as e:
            self._previous_error = e.value
        except errors.EndOfInput as e:
            try:
                render.question.validate(e.selection)
                raise
            except errors.ValidationError as e:
                self._previous_error = render.handle_validation_error(e)

    def _relocate_and_clear(self):
        print("\r" + self._position * self.terminal.move_up, end="")
        self.clear_eos()
        self._position = 0

    def _go_to_end(self, render):
        positions = len(list(render.get_options())) - self._position
        if positions > 0:
            print(self._position * self.terminal.move_down, end="")
        self._position = 0

    def render_error(self, message):
        if message:
            symbol = ">> "
            size = len(symbol) + 1
            length = len(message)
            message = message.rstrip()
            message = message if length + size < self.width else message[: self.width - (size + 3)] + "..."

            self.render_in_bottombar(
                "{t.red}{s}{t.normal}{t.bold}{msg}{t.normal} ".format(msg=message, s=symbol, t=self.terminal)
            )

    def render_in_bottombar(self, message):
        with self.terminal.location(0, self.height - 2):
            self.clear_eos()
            self.print_str(message)

    def clear_bottombar(self):
        with self.terminal.location(0, self.height - 2):
            self.clear_eos()

    @staticmethod
    def render_factory(question_type):
        matrix = {
            "text": Text,
            "editor": Editor,
            "password": Password,
            "confirm": Confirm,
            "list": List,
            "checkbox": Checkbox,
            "path": Path,
        }

        if question_type not in matrix:
            raise errors.UnknownQuestionTypeError()
        return matrix.get(question_type)

    def print_line(self, msg, lf=True):
        self.print_str(msg, lf=lf)

    def print_str(self, msg, lf=False):
        print("\r" + msg, end="\n" if lf else "")
        sys.stdout.flush()

        self._position += math.floor((self.terminal.length(msg) - 1) / self.width)
        if lf:
            self._position += 1

    def clear_eos(self):
        print(self.terminal.clear_eos, end="")

    @property
    def width(self):
        return self.terminal.width or 80

    @property
    def height(self):
        return self.terminal.width or 24

    def trim_str(self, msg: str, extra_after_trimming: str = ""):
        extra_if_long = "..."
        maximum_width = self.width - len(extra_if_long + extra_after_trimming)
        if self.terminal.length(msg) > maximum_width:
            return self.terminal.truncate(msg, maximum_width) + extra_if_long + extra_after_trimming
        return msg + extra_after_trimming
