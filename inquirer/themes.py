from blessings import Terminal

term = Terminal()


class BasicTheme(object):

    def __init__(self):
        self.question_message_prefix = '{t.bright_green} [{t.bold_yellow}?{t.bright_green}]'
        self.question_message_postfix = '{t.bright_green} >>> '
        self.choice_color = term.bold_black_on_bright_green
