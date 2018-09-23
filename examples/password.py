import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

questions = [
    inquirer.Password('password',
                      message="What's your password")
]

answers = inquirer.prompt(questions)

pprint(answers)
