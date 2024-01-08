from pprint import pprint

import inquirer  # noqa

choices_hints = {
    "Jumbo": "The biggest one we have",
    "Large": "If you need the extra kick",
    "Standard": "For your every day use",
}

questions = [
    inquirer.List("size", message="What size do you need?", choices=choices_hints.keys(), hints=choices_hints),
]

answers = inquirer.prompt(questions)

pprint(answers)
