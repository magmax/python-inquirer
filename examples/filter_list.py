import os
import sys
from pprint import pprint

try:
    from fuzzyfinder import fuzzyfinder
except ImportError:
    raise ImportError(
        "The required package 'fuzzyfinder' is not installed. Install it using:\n\n"
        "    pip install fuzzyfinder\n"
    )

sys.path.append(os.path.realpath("."))
import inquirer  # noqa


choices = [
    "apple", "banana", "grapefruit", "blueberry", "strawberry", "blackberry",
    "raspberry", "cherry", "mango", "pineapple", "watermelon", "cantaloupe",
    "honeydew", "kiwi", "papaya", "fig", "pomegranate", "date", "coconut",
    "lemon", "lime", "orange", "tangerine", "peach", "plum", "apricot",
    "pear", "persimmon", "guava", "passionfruit", "lychee", "dragonfruit",
    "starfruit", "durian", "jackfruit", "elderberry", "mulberry", "boysenberry",
    "carrot", "potato", "tomato", "cucumber", "lettuce", "spinach", "broccoli",
    "cauliflower", "cabbage", "zucchini", "squash", "pumpkin", "radish",
    "beet", "onion", "garlic", "shallot", "leek", "celery", "asparagus",
    "artichoke", "pepper", "chili", "jalapeno", "habanero", "ghost pepper",
    "serrano", "poblano", "corn", "peas", "green beans", "chickpeas",
    "lentils", "soybeans", "quinoa", "rice", "barley", "oats", "wheat"]


def filter_func(text, collection):
    g = fuzzyfinder(text, collection, accessor=lambda x: str(x))
    return list(g)


def callback_listener(item):
    with open('choice_logs.txt', 'a') as f:
        f.write(str(item) + '\n')


questions = [
    inquirer.FilterList(
        "food selection",
        message="Select item ",
        choices=choices,
        carousel=False,
        filter_func=filter_func,
        choice_callback=callback_listener
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)
