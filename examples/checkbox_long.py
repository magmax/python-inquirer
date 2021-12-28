import os
import sys
from pprint import pprint


sys.path.append(os.path.realpath("."))
import inquirer  # noqa


questions = [
    inquirer.Checkbox(
        "interests",
        message="What are you interested in?",
        choices=["Choice %s" % i for i in range(40)],
        default=["Choice 2", "Choice 10"],
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
