import sys
from pprint import pprint

import inquirer  # noqa


args = sys.argv

if 'hint' in args:
    choices_hints = {k: f'{str(v)[:10]}...' for k,v in inquirer.__dict__.items()}
else:
    choices_hints = None

carousel =  True if 'carousel' in args else False
other = True if 'other' in args else False


choice_change = []
choices = list(inquirer.__dict__.keys())
choices.sort()

if 'tag' in args:
    choices = [(k,str(inquirer.__dict__[k])[:5]) for k in choices]


def filter_func(text, collection):
    return filter(lambda x: text in x, collection)


def callback_listener(item):
    choice_change.append(item)


questions = [
    inquirer.FilterList(
        "attribute",
        message="Select item ",
        choices=choices,
        carousel=carousel,
        other=other,
        hints= choices_hints,
        filter_func=filter_func,
        choice_callback=callback_listener,
    ),
]

answers = inquirer.prompt(questions)

print(choice_change)
pprint(answers)
