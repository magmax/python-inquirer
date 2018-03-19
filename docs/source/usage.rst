Usage
=====

The idea is quite simple:

#. Create an array of :code:`Questions`
#. Call the prompt render.

Each :code:`Question` require some common arguments. So, you just need to know which kind of :code:`Questions` and :code:`Arguments` are available.


Built-in Question types
-----------------------

+-------------+----------------------------------------------------------------------------------+
|**TEXT**     | Expects a text answer                                                            |
+-------------+----------------------------------------------------------------------------------+
|**PATH**     | Same as :code:`Text`, but allows for tab completion of the underlying filesystem |
+-------------+----------------------------------------------------------------------------------+
|**PASSWORD** | Do not prompt the answer.                                                        |
+-------------+----------------------------------------------------------------------------------+
|**CONFIRM**  | Requires a boolean answer                                                        |
+-------------+----------------------------------------------------------------------------------+
|**LIST**     | Show a list and allow to select just one answer.                                 |
+-------------+----------------------------------------------------------------------------------+
|**CHECKBOX** | Show a list and allow to select a bunch of them                                  |
+-------------+----------------------------------------------------------------------------------+

There are pictures of some of them in the :ref:`examples` section.


Question Arguments
------------------

The main object is :code:`Question`, but it should not be
instantiated. You must use any of the subclasses, listed below. All of
them have the next attributes that can be set in the initialization:

name
~~~~

It will be the key in the hash of answers. So, it is **mandatory**.

You can use any ``String`` or ``hashable`` code as value.

message
~~~~~~~

Contains the prompt to be shown to the user, and is **mandatory** too.

You can use a new style formatted string, using the previous answers, and it will be replaced automatically:

.. code:: python

          questions = [
              Text(name='name', message="What's your name?"),
              Text(name='surname', message="What's your surname, {name}")
          ]

The value can be a ``function``, with the next sign:

.. code:: python

          def get_message(answers): return str()

Example:

.. code:: python

          def get_message(answers):
              return "What's your name?"

          Text(name='name', message= get_message)

Where ``answers`` is the dictionary with previous answers.


If the ``message`` is too long for the terminal, it will be cut to fit.


default
~~~~~~~

Stores the default value to be used as answer. This allow the user just to press `Enter` to use it. It is optional, using ``None`` if there is no input and no default value.

As in ``message` , you can use a new format string or a function with the sign:

.. code:: python

          def get_default(answers): return str()

Where ``answers`` is a ``dict`` containing all previous answers.

Remember that it should be a list for `Checkbox` questions.


choices
~~~~~~~

**Mandatory** just for ``Checkbox`` and ``List`` questions; the rest of them do not use it.

It contains the list of selectable answers.

Its value can be a ``list`` of strings, new format style strings or pairs(tuples) or a `function` that returns that list, with the sign:

.. code:: python

          def get_choices(answers): return list(str())

If any of the list values is a pair, it should be a tuple like: ``(label, value)``. Then the ``label`` will be shown but the ``value`` will be returned.

As before, the ``answers`` is a `dict` containing the previous answers.


validate
~~~~~~~~

Optional attribute that allows the program to check if the answer is valid or not. It requires a `boolean` value or a `function` with the sign:

.. code:: python

          def validate(answers, current): return boolean()

Where ``answers`` is a `dict` with previous answers again and ``current`` is the current answer. Example:

.. code:: python

          Text('age', "how old are you?", validate=lambda _, c: 0 <= c < 120)

ignore
~~~~~~

Questions are statically created and some of them may be optional depending on other answers. This attribute allows to control this by hiding the question.

It's value is `boolean` or a `function` with the sign:

.. code:: python

          def ignore(answers): return boolean()

where ``answers`` contains the `dict` of previous answers again.


Creating the Question object
----------------------------

With this information, it is easy to create a ``Question`` object:

.. code:: python

          Text('name', "What's your name?")

It's possible to load the :code:`Question` objects from a :code:`dict`, or even the whole list of them, with the method :code:`load_from_dict` and :code:`load_from_list`, respectively.


The method :code:`load_from_json` has been added as commodity to use JSON inputs instead. Here you have an example:

.. literalinclude:: ../../examples/questions_from_json.py



The prompter
------------

The last step is to call the *prompter* With the list of :code:`Question`:

.. code:: python

      answers = inquirer.prompt(questions)

This line will ask the user for information and will store the answeres in a dict, using the question name as **key** and the user response as **value**.

Remember the ``prompt`` always require a list of ``Question`` as input.


Creating Custom Question Types
------------------------------
If the built-in :code:`Question` types aren't enough to cover needed functionality, custom :code:`Question` types can be
created. Two parts must be defined: a class that inherits from :code:`inquirer.questions.Question` used to define the
user interface for the :code:`Question`, and a class that inherits from
:code:`inquirer.render.console.BaseConsoleRender` used to define how the :code:`Question` handles user input.

The below example shows how to create a :code:`Question` which prepends the string :code:`'blue'` to user input
subject to a probability.

.. code:: python

      import random
      import inquirer
      from inquirer.questions import Question
      from inquirer.render.console import Text
      from inquirer.render import ConsoleRender


      # Create Question class
      class AlwaysBlue(Question):
          """
          Must subclass inquirer.questions.Question
          """
          kind = 'always_blue'  # Kind must be unique among Questions

          def __init__(self, name, message,
                       prob_blue=0.9, **kwargs):
              """
              Custom arguments to the question can be provided, but the super constructor
              should still be called
              """
              super(AlwaysBlue, self).__init__(name, message, **kwargs)
              self.prob_blue = prob_blue


      # Create Render class
      class AlwaysBlueRender(Text):
          """
          Must subclass inquirer.render.console.BaseConsoleRender, or something that
          subclasses it (like inquirer.render.console.Text, in this case)

          Custom arguments from the corresponding Question object are available in the
          self.question attribute of this object
          """
          def __init__(self, *args, **kwargs):
              super(AlwaysBlueRender, self).__init__(*args, **kwargs)

          def process_input(self, pressed):
              """
              This method controls rendering of input, so this is most likely what needs to
              be overridden for custom behavior

              In this case, the string 'blue' is prepended to user input, depending on the
              user defined probability of the event when the Question was instantiated
              """
              if random.random() < self.question.prob_blue:
                  self.current += 'blue'

              super(AlwaysBlueRender, self).process_input(pressed)


      # A ConsoleRender object must be instantiated so the custom Question and Render
      # classes can be added
      render = ConsoleRender()
      render.add_question_render(
          question_type_class=AlwaysBlue,
          question_render_class=AlwaysBlueRender
      )

      # Create a list of AlwaysBlue questions
      questions = [
          AlwaysBlue('mostly_blue', 'Always blue!'),
          AlwaysBlue('sometimes_blue', 'Sometimes blue!', prob_blue=0.2)
      ]

      # Prompt, using defined ConsoleRender object
      answers = inquirer.prompt(questions, render=render)

      # See the results
      print(answers)


Themes
------

You can change the colorscheme and some icons passing a theme object defined in inquirer.themes
There are Default and GreenPassion themes, but you can define your own via class, dict or json!

.. literalinclude:: ../../examples/theme.py

Result:

|inquirer theme|

.. |inquirer theme| image:: images/inquirer_theme.gif
  :alt: Example of theme (GreenPassion)
