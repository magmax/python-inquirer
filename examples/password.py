import os
import sys
from pprint import pprint

sys.path.append(os.path.realpath("."))
import inquirer  # noqa

questions = [inquirer.Password("password", message="What's your password")]

answers = inquirer.prompt(questions)

pprint(answers)
