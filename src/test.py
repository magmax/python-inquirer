import inquirer
from pprint import pprint
questions = [
  inquirer.List('size',
                message="What size do you need?",
                choices=['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
                lenlimit=12,
                ),
  inquirer.Checkbox('interests',
                    message="What are you interested in?",
                    choices=['Computers', 'Books', 'Science', 'Nature', 'Fantasy', 'History'],
                    lenlimit=3,
                    ),
]
answers = inquirer.prompt(questions)
pprint(answers)