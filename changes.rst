Changelog
=========

2.1.11(2014/12/18)
------------------

Features
~~~~~~~~

* `#18`_ The ``Prompt`` shout raise ``KeyboardInterrupt`` if required.

2.1.3 (2014/12/27)
------------------

Bugs
~~~~

* The ``Question`` start was not shown.

2.1.2 (2014/12/16)
------------------

Features
~~~~~~~~

* `#7`_ Adding default values for `Checkbox`, by ptbrowne_


2.1.1 (2014/12/11)
------------------

Bugs
~~~~

* Status bar was hiden by question
* Fixed a :code:`force_new_line` problem with some environments.


2.1.0 (2014/12/10)
------------------

Features
~~~~~~~~

* code refactors
* Adding `ReadTheDocs`_ documentation

Bugs
~~~~

* `#6`_ Removed new line after questions
* Confirmations will not raise an exception on unknown value


2.0.2 (2014/11/27)
------------------

Features
~~~~~~~~

* Using pytest_ instead of nose_
* Documentation updated
* Added :file:`changes.rst` file with the changelog

Bugs
~~~~

* `#5`_: Fixed :code:`List` and :code:`Checkbox`, that were overriden if there was more :code:`Questions`.

2.0.1 (2014/10/31)
------------------

Features
~~~~~~~~

* `#4`_: Instantiate from JSON

  * Internal refactors
  * added load_from_dict and load_from_json factories, by mfwarren_


2.0.0 (2014/10/19)
------------------

Features
~~~~~~~~

* Complete refactor of :code:`Question`, :code:`ConsoleRender` and the way it was rendered with :code:`blessings` library.

1.X.X
-----

Special thanks to matiboy_ by his contributions to these releases.


Hall Of Fame
============

Contributors:

* matiboy_
* mfwarren_
* ptbrowne_


.. _pytest: http://pytest.org/
.. _nose: https://nose.readthedocs.org/
.. _ReadTheDocs: https://python-inquirer.readthedocs.org/

.. _#1: https://github.com/magmax/python-inquirer/issues/1
.. _#4: https://github.com/magmax/python-inquirer/pull/2
.. _#4: https://github.com/magmax/python-inquirer/pull/3
.. _#4: https://github.com/magmax/python-inquirer/pull/4
.. _#5: https://github.com/magmax/python-inquirer/issues/5
.. _#6: https://github.com/magmax/python-inquirer/issues/6
.. _#7: https://github.com/magmax/python-inquirer/pull/7
.. _#18: https://github.com/magmax/python-inquirer/issues/18

.. _ptbrowne: https://github.com/ptbrowne
.. _mfwarren: https://github.com/mfwarren
.. _matiboy: https://github.com/matiboy
