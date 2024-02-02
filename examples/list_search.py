import os
import sys
from pprint import pprint


sys.path.append(os.path.realpath("."))
import inquirer  # noqa

# To make the search case-insensitive
matcher = lambda entry, search: entry.lower().startswith(search.lower())

questions = [
    inquirer.List(
        "size", message="What size do you need?", choices=["Jumbo", "Large", "Standard"], carousel=True, search=True, matcher=matcher
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
