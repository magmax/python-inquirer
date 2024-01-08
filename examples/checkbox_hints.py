from pprint import pprint

import inquirer  # noqa


choices_hints = {
    "Computers": "The really Geeky stuff",
    "Books": "Its just so cosy",
    "Science": "I want to know it all",
    "Nature": "Always outdoors",
}

questions = [
    inquirer.Checkbox(
        "interests", message="What are you interested in?", choices=choices_hints.keys(), hints=choices_hints
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
