import os
import sys
from pprint import pprint


sys.path.append(os.path.realpath("."))
import inquirer  # noqa


questions = [
    inquirer.Text("name", message="What's your name?"),
    inquirer.Text(
        "surname", message="What's your surname, {name}?", ignore=lambda x: x["name"].lower() == "anonymous"
    ),
    inquirer.Confirm("married", message="Are you married?"),
    inquirer.Text("time_married", message="How long have you been married?", ignore=lambda x: not x["married"]),
]

answers = inquirer.prompt(questions)

pprint(answers)
