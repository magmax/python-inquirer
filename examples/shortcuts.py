import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer

text = inquirer.text(message="Enter your username")
print(text)
password = inquirer.password(message='Please enter your password'),
print(password)
checkbox = inquirer.checkbox(message='Please define your type of project?', choices=['common', 'backend', 'frontend'])
print(checkbox)
choice = inquirer.list_input("Public or private?", choices=['public', 'private'])
print(choice)
correct = inquirer.confirm("This will delete all your current labels and create a new ones. Continue?", default=False)
print(correct)
