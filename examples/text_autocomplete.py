import os
import re
import sys
from pprint import pprint


sys.path.append(os.path.realpath("."))
import inquirer  # noqa


def autocomplete_username(_text, _state):
    return os.getlogin()


questions = [
    inquirer.Text(
        "name", message="What's your username? (Press TAB to autocomplete)", autocomplete=autocomplete_username
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
