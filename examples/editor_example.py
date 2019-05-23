import os
import sys
import re

sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

questions = [
    inquirer.Editor('poem', message='Write me a poem please',
                    default='Roses are red,',
                    validate=lambda _, x: x.count('\n') >= 2),
]

answers = inquirer.prompt(questions)

pprint(answers)
