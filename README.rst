=========  ============
TESTS      COVERAGE
=========  ============
|travis|   |coveralls|
=========  ============

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

Usage example::

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

  python examples/input.py


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
| message       | String        | To be shown in the prompt to the user                                                                                                             |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| default       | Any|Function  | Default value. Functions will receive the hash with previous values.                                                                              |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| choices       | List|Function | List of available options. Functions will receive the hash with previous values.                                                                  |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| validation    | Bool|Function | If the value set is valid. Functions will receive the hash with previous values and the value set in this question, and should return a boolean.  |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| unless        | Bool|Function | If the quiestion should be shown. Functions will receive the hash with previous values and should return a boolean.                               |
+---------------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------+


Prompt types
============

Text
----

Example::

  import inquirer
  questions = [
    inquirer.Text('name', message="What's your name"),
    inquirer.Text('surname', message="What's your surname"),
    inquirer.Text('phone', message="What's your phone number",
                  validation=lambda x: re.match('\d+', x),
                  )
  ]
  answers = inquirer.prompt(questions)

|inquirer text|

Password
--------


Confirm
-------

Example::

  import inquirer
  questions = [
    inquirer.Confirm('continue', message="Should I continue"),
    inquirer.Confirm('stop', message="Should I stop", default=True),
  ]
  answers = inquirer.prompt(questions)

|inquirer confirm|

License
=======

Copyright (c) 2014 Miguel Ángel García (`@magmax9`_), based on `Inquirer.js`_, by Simon Boudrias (`@vaxilart`_)

Licensed under `the MIT license`_.


.. |travis| image:: https://travis-ci.org/magmax/python-inquirer.png
  :target: `Travis`_

.. |coveralls| image:: https://coveralls.io/repos/magmax/python-inquirer/badge.png
  :target: `Coveralls`_

.. |inquirer text| image:: http://magmax.org/images/inquirer/inquirer_text.png
.. |inquirer confirm| image:: http://magmax.org/images/inquirer/inquirer_confirm.png

.. _Inquirer.js: https://github.com/SBoudrias/Inquirer.js
.. _Travis: https://travis-ci.org/magmax/python-inquirer
.. _Coveralls: https://coveralls.io/r/magmax/python-inquirer
.. _examples/: https://github.com/magmax/python-inquirer/tree/master/examples

.. _@vaxilart: https://twitter.com/vaxilart
.. _@magmax9: https://twitter.com/magmax9

.. _the MIT license: http://opensource.org/licenses/MIT
