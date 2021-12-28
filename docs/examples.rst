Examples
========

You can find all these examples at :code:`examples` directory.


text.py
-----------

.. literalinclude:: ../../examples/text.py

Result on something like:

|inquirer text|

confirm.py
-----------

.. literalinclude:: ../../examples/confirm.py

Result on something like:

|inquirer confirm|

list.py
-----------

.. literalinclude:: ../../examples/list.py

Result on something like:

|inquirer list|

checkbox.py
-----------

.. literalinclude:: ../../examples/checkbox.py

Result on something like:

|inquirer checkbox|


The :code:`choices` list can also be a list of tuples. The first value in each tuple should be the label displayed to the user. The second value in each tuple should be the actual value for that option. This allows you to have the user choose options that are not plain strings in the code.

.. literalinclude:: ../../examples/checkbox_tagged.py

theme.py
-----------

.. literalinclude:: ../../examples/theme.py

Result on something like:

|inquirer theme|


.. |inquirer text| image:: images/inquirer_text.png
  :alt: Example of Text Question

.. |inquirer confirm| image:: images/inquirer_confirm.png
  :alt: Example of Confirm Question

.. |inquirer list| image:: images/inquirer_list.png
  :alt: Example of List Question

.. |inquirer checkbox| image:: images/inquirer_checkbox.png
  :alt: Example of Checkbox Question

.. |inquirer theme| image:: images/inquirer_theme.gif
  :alt: Example of theme (GreenPassion)
