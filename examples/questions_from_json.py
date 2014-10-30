import os
import sys
import re
import json
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

questions_data = json.loads(open('examples/test_questions.json').read())
questions = [inquirer.Question(**q) for q in questions_data]

answers = inquirer.prompt(questions)

pprint(answers)
