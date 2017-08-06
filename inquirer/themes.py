from collections import namedtuple
from blessings import Terminal

term = Terminal()


class BasicTheme(object):
    Question = namedtuple('question', 'prefix postfix default_color')
    Checkbox = namedtuple('common', 'selection_color selection_icon '
                                    'selected_color unselected_color '
                                    'selected_icon unselected_icon')
    List = namedtuple('List', 'selection_color selection_cursor '
                              'unselected_color')

    def __init__(self):
        self.Question.prefix = '{t.bright_green} [{t.bold_yellow}?{t.bright_green}]'
        self.Question.postfix = '{t.bright_green} >>>'
        self.Question.default_color = term.yellow
        self.Checkbox.selection_color = term.bold_black_on_bright_green
        self.Checkbox.selection_icon = '❯'
        self.Checkbox.selected_icon = '◉'
        self.Checkbox.selected_color = term.green
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = '◯'
        self.List.selection_color = term.bold_black_on_bright_green
        self.List.selection_cursor = '❯'
        self.List.unselected_color = term.normal
