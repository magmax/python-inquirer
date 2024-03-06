import os
import sys
from pprint import pprint


sys.path.append(os.path.realpath("."))
import inquirer  # noqa
from readchar import key


# To make the search case-insensitive
def matcher(choices, pressedKey, searchString):
    if pressedKey == key.BACKSPACE:
        searchString = searchString[:-1]
    elif pressedKey.isprintable():
        searchString += pressedKey
    for i in range(len(choices)):
        if choices[i].lower().startswith(searchString.lower()):
            return (i, searchString)
    return (0, searchString)


questions = [
    inquirer.List(
        "size", message="What size do you need?",
        choices=["Jumbo", "Large", "Standard"],
        carousel=True, matcher=matcher
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
