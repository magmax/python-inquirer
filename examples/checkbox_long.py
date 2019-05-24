import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

questions = [
    inquirer.Checkbox('interests',
                      message="What are you interested in?",
                      choices=['Choice %s' % i for i in range(20)],
                      default=['Choice 2', 'Choice 10']),
]

answers = inquirer.prompt(questions)

pprint(answers)
