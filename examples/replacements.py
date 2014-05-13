import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

questions = [
    inquirer.Text('name',
                  message="What's your name?"),
    inquirer.Text('surname',
                  message="{name}, what's your surname?"),
    inquirer.Text('alias',
                  message="What's your Alias [{name}]",
                  default="{surname}"),
]

answers = inquirer.prompt(questions)

pprint(answers)
