Changelog
=========

2.0.3 (Unreleased)
------------------

Features
~~~~~~~~

* code refactors

Bugs
~~~~

* `#6`_ Removed new line after questions

2.0.2
-----

Features
~~~~~~~~

* Using pytest_ instead of nose_
* Documentation updated
* Added :file:`changes.rst` file with the changelog

Bugs
~~~~

* `#5`_: Fixed :code:`List` and :code:`Checkbox`, that were overriden if there was more :code:`Questions`.

2.0.1
-----

Features
~~~~~~~~

* `#4`_: Instantiate from JSON

  * Internal refactors
  * added load_from_dict and load_from_json factories


2.0.0
-----

Features
~~~~~~~~

* Complete refactor of :code:`Question`, :code:`ConsoleRender` and the way it was rendered with :code:`blessings` library.


.. _pytest: http://pytest.org/
.. _nose: https://nose.readthedocs.org/

.. _#1: https://github.com/magmax/python-inquirer/issues/1
.. _#4: https://github.com/magmax/python-inquirer/issues/4
.. _#5: https://github.com/magmax/python-inquirer/issues/5
.. _#6: https://github.com/magmax/python-inquirer/issues/6
