from pprint import pprint

import inquirer  # noqa

choices_hints = {
    "Standard": "For your every day use",
    "Large": "If you need the extra kick",
    "Jumbo": "The biggest one we have",
}

questions = [
    inquirer.List("size", message="What size do you need?", choices=choices_hints.keys(), hints=choices_hints),
]

answers = inquirer.prompt(questions)

pprint(answers)
