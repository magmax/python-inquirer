import os
import sys
from pprint import pprint


sys.path.append(os.path.realpath("."))
import inquirer  # noqa


def autocomplete_fn(_text, _state):
    return "inquirer"


questions = [
    inquirer.Text(
        "name",
        message="Enter the name of this library (Press TAB to autocomplete)",
        autocomplete=autocomplete_fn,
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
