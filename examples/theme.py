import sys
import os
from pprint import pprint

sys.path.append(os.path.realpath("."))
import inquirer  # noqa
from inquirer.themes import GreenPassion  # noqa

q = [
    inquirer.Text("name", message="Whats your name?", default="No one"),
    inquirer.List("jon", message="Does Jon Snow know?", choices=["yes", "no"], default="no"),
    inquirer.Checkbox(
        "kill_list", message="Who you want to kill?", choices=["Cersei", "Littlefinger", "The Mountain"]
    ),
]

answers = inquirer.prompt(q, theme=GreenPassion())

pprint(answers)
