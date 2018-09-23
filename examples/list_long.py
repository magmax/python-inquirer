import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

questions = [
    inquirer.List('size',
                  message="What size do you need?",
                  choices=['Choice %s' % i for i in range(100)],
                  carousel=False,
                  strip=True,
              ),
]

answers = inquirer.prompt(questions)

pprint(answers)
