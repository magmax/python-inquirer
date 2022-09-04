import os
import sys
from pprint import pprint


sys.path.append(os.path.realpath("."))
import inquirer  # noqa


choices = [
    {"name": "User01", "id": 1},
    {"name": "User02", "id": 2},
    {"name": "User03", "id": 3},
    {"name": "User04", "id": 4}  
]

questions = [
    inquirer.Checkbox(
        "users",
        message="Select Users",
        choices=choices,
        preprocessor=lambda c: c['name'],
        default=choices[2:]
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
