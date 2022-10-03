import os
import sys
from pprint import pprint


sys.path.append(os.path.realpath("."))
import inquirer  # noqa


questions = [
    inquirer.List(
        "size", message="What size do you need?", choices=["Jumbo", "Large", "Standard"], carousel=True, other=True
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
