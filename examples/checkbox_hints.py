from pprint import pprint

import inquirer  # noqa


choices_hints = {
    ("Computers", "c"): "The really Geeky stuff",
    ("Books", "b"): "Its just so cosy",
    ("Science", "s"): "I want to know it all",
    ("Nature", "n"): "Always outdoors",
}

questions = [
    inquirer.Checkbox(
        "interests", message="What are you interested in?", choices=choices_hints.keys(), hints=choices_hints
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
