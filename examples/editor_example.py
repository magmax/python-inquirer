import os
import sys
from pprint import pprint

sys.path.append(os.path.realpath("."))
import inquirer  # noqa

questions = [
    inquirer.Editor(
        "poem", message="Write me a poem please", default="Roses are red,", validate=lambda _, x: x.count("\n") >= 2
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
