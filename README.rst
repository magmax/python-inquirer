==============  ===============  =========  ============
VERSION         DOWNLOADS        TESTS      COVERAGE
==============  ===============  =========  ============
|pip version|   |pip downloads|  |travis|   |coveralls|
==============  ===============  =========  ============

Collection of common interactive command line user interfaces, based on `Inquirer.js`_.

Goal and Philosophy
===================

Born as a `Inquirer.js`_ clone, it shares part of the goals and philosophy.

So, **Inquirer** should ease the process of asking end user **questions**, **parsing**, **validating** answers, managing **hierarchical prompts** and providing **error feedback**.


Documentation
=============

Installation
------------

::

   pip install inquirer

Usage example:

.. code:: python

  import inquirer

  questions = [
    inquirer.Text    ('name',     message="What's your name"),
    inquirer.Password('password', message="Add a password"),
    inquirer.Confirm ('correct',  message="Is correct"),
  ]

  answers = inquirer.prompt(questions)

Examples
--------

The `examples/`_ directory contains several examples. Feel free to run them::

  python examples/text.py


Objects
-------

The main object is ``Question``, but it should not be
instantiated. You must use any of the subclasses, listed below. All of
them have the next attributes that can be set in the initialization:

+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| **Attribute** | **Type**      | **Explanation**                                                                                                                                   |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| name          | String        | The key in the hash of answers.                                                                                                                   |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| message       | String|Func   | To be shown in the prompt to the user. Functions will receive the hash with previous values.                                                      |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| default       | Any|Function  | Default value. Functions will receive the hash with previous values.                                                                              |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| choices       | List|Function | List of available options. Functions will receive the hash with previous values.                                                                  |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| validate      | Bool|Function | If the value set is valid. Functions will receive the hash with previous values and the value set in this question, and should return a boolean.  |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| ignore        | Bool|Function | If the quiestion should be shown. Functions will receive the hash with previous values and should return a boolean.                               |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+


Prompt types
============

Text
----

``choices`` argument is not used.

Example:

.. code:: python

  import inquirer
  questions = [
    inquirer.Text('name', message="What's your name"),
    inquirer.Text('surname', message="What's your surname"),
    inquirer.Text('phone', message="What's your phone number",
                  validate=lambda x, _: re.match('\d+', x),
                  )
  ]
  answers = inquirer.prompt(questions)

|inquirer text|


Password
--------

``choices`` argument is not used.

Example:

.. code:: python

  import inquirer
  questions = [
    inquirer.Password('password', message="What's your password"),
  ]
  answers = inquirer.prompt(questions)


Confirm
-------

``choices`` argument is not used.

Example:

.. code:: python

  import inquirer
  questions = [
    inquirer.Confirm('continue', message="Should I continue"),
    inquirer.Confirm('stop', message="Should I stop", default=True),
  ]
  answers = inquirer.prompt(questions)

|inquirer confirm|


List
----

Shows a list of choices, and allows the selection of one of them.

Example:

.. code:: python


  import inquirer
  questions = [
    inquirer.List('size',
                  message="What size do you need?",
                  choices=['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
              ),
  ]
  answers = inquirer.prompt(questions)

|inquirer list|


Checkbox
--------

Shows a list of choices, with multiple selection.

Example:

.. code:: python


  import inquirer
  questions = [
    inquirer.Checkbox('interests',
                      message="What are you interested in?",
                      choices=['Computers', 'Books', 'Science', 'Nature', 'Fantasy', 'History'],
                      ),
  ]
  answers = inquirer.prompt(questions)

|inquirer checkbox|


Advanced usage
==============

Some tips:

Reusing previous answers
------------------------

Every ``String`` argument but ``name`` can use any previous answer just putting it in roots:

.. code:: python


  import inquirer
  questions = [
    inquirer.Text('name', message="What's your name?"),
    inquirer.Text('surname', message="{name}, what's your surname?"),
    inquirer.Text('alias', message="What's your Alias"
      default="{name}"),
  ]
  answers = inquirer.prompt(questions)




License
=======

Copyright (c) 2014 Miguel Ángel García (`@magmax9`_), based on `Inquirer.js`_, by Simon Boudrias (`@vaxilart`_)

Licensed under `the MIT license`_.


.. |travis| image:: https://travis-ci.org/magmax/python-inquirer.png
  :target: `Travis`_
  :alt: Travis results

.. |coveralls| image:: https://coveralls.io/repos/magmax/python-inquirer/badge.png
  :target: `Coveralls`_
  :alt: Coveralls results_

.. |pip version| image:: https://pypip.in/v/inquirer/badge.png
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Latest PyPI version

.. |pip downloads| image:: https://pypip.in/d/inquirer/badge.png
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Number of PyPI downloads

.. |inquirer text| image:: http://magmax.org/images/inquirer/inquirer_text.png
  :alt: Example of Text Question

.. |inquirer confirm| image:: http://magmax.org/images/inquirer/inquirer_confirm.png
  :alt: Example of Confirm Question

.. |inquirer list| image:: http://magmax.org/images/inquirer/inquirer_list.png
  :alt: Example of List Question

.. |inquirer checkbox| image:: http://magmax.org/images/inquirer/inquirer_checkbox.png
  :alt: Example of Checkbox Question

.. _Inquirer.js: https://github.com/SBoudrias/Inquirer.js
.. _Travis: https://travis-ci.org/magmax/python-inquirer
.. _Coveralls: https://coveralls.io/r/magmax/python-inquirer
.. _examples/: https://github.com/magmax/python-inquirer/tree/master/examples

.. _@vaxilart: https://twitter.com/vaxilart
.. _@magmax9: https://twitter.com/magmax9

.. _the MIT license: http://opensource.org/licenses/MIT
