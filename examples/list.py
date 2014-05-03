import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

questions = [
    inquirer.List('size',
                  message="What size do you need?",
                  choices=['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
              ),
]

answers = inquirer.prompt(questions)

pprint(answers)
