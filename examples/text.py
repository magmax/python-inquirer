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
                  message="What's your surname, {name}?"),
    inquirer.Text('phone',
                  message="What's your phone number",
                  validate=lambda _, x: re.match('\+?\d[\d ]+\d', x),
                  )
]

answers = inquirer.prompt(questions)

pprint(answers)
