import sys
from pprint import pprint

import inquirer  # noqa


choices_map = str.__dict__
choices = sorted(choices_map.keys())

# prepare FilterList arguments
args = sys.argv[1:]
if "hint" in args:
    choices_hints = {k: f"{str(v)[:10]}..." for k, v in choices_map.items()}
else:
    choices_hints = None
carousel = True if "carousel" in args else False
other = True if "other" in args else False
choices = [(k, str(choices_map[k])[:5]) for k in choices] if "tag" in args else choices


def filter_func(text, collection):
    return filter(lambda x: text in str(x), collection)


questions = [
    inquirer.FilterList(
        "attribute",
        message="Select item ",
        choices=choices,
        carousel=carousel,
        other=other,
        hints=choices_hints,
        filter_func=filter_func,
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
