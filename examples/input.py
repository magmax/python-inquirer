import os
import sys
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

questions = [
]

answers = inquirer.prompt(questions)

pprint(answers)
