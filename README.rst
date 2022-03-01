====================  =================================================================================
Tests                 |Tests| |Codecov|
--------------------  ---------------------------------------------------------------------------------
Downloads             |pip dm| |pip dw| |pip dd|
--------------------  ---------------------------------------------------------------------------------
About                 |License| |pip wheel| |pip pyversions| |pip implem|
--------------------  ---------------------------------------------------------------------------------
Status                |version| |status| |Documentation|
====================  =================================================================================

Collection of common interactive command line user interfaces, based on `Inquirer.js`_.

Goal and Philosophy
===================

Born as a `Inquirer.js`_ clone, it shares part of the goals and philosophy.

So, **Inquirer** should ease the process of asking end user **questions**, **parsing**, **validating** answers, managing **hierarchical prompts** and providing **error feedback**.

You can `download the python-inquirer code from GitHub`_ or `download the wheel from Pypi`_.

Platforms support
------------------

Python-inquirer supports mainly UNIX-based platforms (eq. Mac OS, Linux, etc.). Windows has experimental support, please let us know if there are any problems!

Installation
============

.. code:: console

    pip install inquirer


Documentation
=============

Documentation has been moved to `magmax.org/python-inquirer <https://magmax.org/python-inquirer/>`_.

But here you have a couple of usage examples:


Text
----

.. code:: python

  import re

  import inquirer
  questions = [
    inquirer.Text('name', message="What's your name"),
    inquirer.Text('surname', message="What's your surname"),
    inquirer.Text('phone', message="What's your phone number",
                  validate=lambda _, x: re.match('\+?\d[\d ]+\d', x),
                  )
  ]
  answers = inquirer.prompt(questions)

|inquirer text|


Editor
------

Like a Text question, but used for larger answers. It opens external text editor which is used to collect the answer.

The environment variables $VISUAL and $EDITOR, can be used to specify which editor should be used. If not present
inquirer fallbacks to `vim -> emacs -> nano` in this order based on availability in the system.

External editor handling is done using great library `python-editor <https://github.com/fmoo/python-editor>`_.

Example:

.. code:: python

  import inquirer
  questions = [
    inquirer.Editor('long_text', message="Provide long text")
  ]
  answers = inquirer.prompt(questions)


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

List questions can take one extra argument :code:`carousel=False`. If set to true, the answers will rotate (back to first when pressing down on last choice, and down to last choice when pressing up on first choice)

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

Checkbox questions can take one extra argument :code:`carousel=False`. If set to true, the answers will rotate (back to first when pressing down on last choice, and down to last choice when pressing up on first choice)

|inquirer checkbox|

Path
----

Like Text question, but with builtin validations for working with paths.

Example:

.. code:: python


  import inquirer
  questions = [
    inquirer.Path('log_file',
                   message="Where logs should be located?",
                   path_type=inquirer.Path.DIRECTORY,
                  ),
  ]
  answers = inquirer.prompt(questions)


Contributing
============

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.

License
=======

Copyright (c) 2014-2021 Miguel Ángel García (`@magmax_en`_), based on `Inquirer.js`_, by Simon Boudrias (`@vaxilart`_)

Licensed under `the MIT license`_.


.. |Tests| image:: https://github.com/magmax/python-inquirer/workflows/Tests/badge.svg
  :target: https://github.com/magmax/python-inquirer/actions?workflow=Tests
  :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/magmax/python-inquirer/branch/master/graph/badge.svg
  :target: https://app.codecov.io/gh/magmax/python-inquirer
  :alt: Codecov
.. |Documentation| image:: https://github.com/magmax/python-inquirer/workflows/Documentation/badge.svg
   :target: https://magmax.org/python-inquirer/
   :alt: Read the documentation at https://magmax.org/python-inquirer/
.. |pip version| image:: https://img.shields.io/pypi/v/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Latest PyPI version
.. |pip dm| image:: https://img.shields.io/pypi/dm/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Last month downloads from pypi
.. |pip dw| image:: https://img.shields.io/pypi/dw/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Last week downloads from pypi
.. |pip dd| image:: https://img.shields.io/pypi/dd/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Yesterday downloads from pypi
.. |License| image:: https://img.shields.io/pypi/l/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: License
.. |pip wheel| image:: https://img.shields.io/pypi/wheel/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Wheel
.. |pip pyversions| image::  	https://img.shields.io/pypi/pyversions/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Python versions
.. |pip implem| image::  	https://img.shields.io/pypi/implementation/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Python interpreters
.. |status| image::	https://img.shields.io/pypi/status/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Status
.. |version| image:: https://img.shields.io/pypi/v/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Status
.. |inquirer text| image:: http://magmax.org/python-inquirer/_images/inquirer_text.png
  :alt: Example of Text Question
.. |inquirer list| image:: http://magmax.org/python-inquirer/_images/inquirer_list.png
  :alt: Example of List Question
.. |inquirer checkbox| image:: http://magmax.org/python-inquirer/_images/inquirer_checkbox.png
  :alt: Example of Checkbox Question
.. _Inquirer.js: https://github.com/SBoudrias/Inquirer.js
.. _examples/: https://github.com/magmax/python-inquirer/tree/master/examples
.. _`download the python-inquirer code from GitHub`: https://github.com/magmax/python-inquirer
.. _`download the wheel from Pypi`: https://pypi.python.org/pypi/inquirer
.. _@vaxilart: https://twitter.com/vaxilart
.. _@magmax_en: https://twitter.com/magmax_en
.. _the MIT license: https://opensource.org/licenses/MIT
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
