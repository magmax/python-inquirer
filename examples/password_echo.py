import os
import sys
from pprint import pprint


sys.path.append(os.path.realpath("."))

import inquirer  # noqa


questions = [
    inquirer.Password("password1", message="What's your password"),
    inquirer.Password("password2", message="Password echoing dots", echo="."),
    inquirer.Password("password3", message="Password no echo", echo=""),
]

answers = inquirer.prompt(questions)

pprint(answers)
