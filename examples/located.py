# encoding: utf-8
import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

LangQuestion = [
    inquirer.List('lang',
                  message="Select Language",
                  choices=['English', 'Français', 'Deutsche', 'Español'],
              ),
]

answers = inquirer.prompt(LangQuestion)

pprint(answers)
