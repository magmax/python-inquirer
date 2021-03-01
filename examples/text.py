import os
import re
import sys
from pprint import pprint

sys.path.append(os.path.realpath("."))
import inquirer  # noqa


def phone_validation(answers, current):
    if not re.match(r"\+?\d[\d ]+\d", current):
        raise inquirer.errors.ValidationError("", reason="I don't like your phone number!")

    return True


questions = [
    inquirer.Text("name", message="What's your name?"),
    inquirer.Text("surname", message="What's your surname, {name}?"),
    inquirer.Text(
        "phone",
        message="What's your phone number",
        validate=phone_validation,
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
