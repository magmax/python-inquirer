import os
import sys
from pprint import pprint


sys.path.append(os.path.realpath("."))
import inquirer  # noqa


questions = [
    inquirer.List(
        "size",
        message="What size do you need?",
        choices=["Choice %s" % i for i in range(20)],
        carousel=False,
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
