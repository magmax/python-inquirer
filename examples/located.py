# encoding: utf-8
import os
import sys
from pprint import pprint

sys.path.append(os.path.realpath("."))
import inquirer  # noqa

LangQuestion = [
    inquirer.List(
        "lang",
        message="Select Language",
        choices=["English", "Français", "Deutsche", "Español"],
    ),
]

answers = inquirer.prompt(LangQuestion)

pprint(answers)
