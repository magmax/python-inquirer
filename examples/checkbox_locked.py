import os
import sys
from pprint import pprint


sys.path.append(os.path.realpath("."))
import inquirer  # noqa


questions = [
    inquirer.Checkbox(
        "courses",
        message="Which courses would you like to take?",
        choices=["Programming fundamentals", "Fullstack development", "Data science", "DevOps"],
        locked=["Programming fundamentals"],
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
