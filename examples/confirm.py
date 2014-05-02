import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

questions = [
    inquirer.Confirm('continue',
                  message="Should I continue"),
    inquirer.Confirm('stop',
                  message="Should I stop", default=True),
]

answers = inquirer.prompt(questions)

pprint(answers)
