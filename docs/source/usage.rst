Usage
=====

The idea is quite simple:

#. Create an array of :code:`Questions`
#. Call the prompt render.

Each :code:`Question` require some common arguments. So, you just need to know which kind of :code:`Questions` and :code:`Arguments` are available.


Question types
--------------

+-------------+--------------------------------------+
|**TEXT**     |                                      |
+-------------+--------------------------------------+
|**PASSWORD** |                                      |
+-------------+--------------------------------------+
|**CONFIRM**  |                                      |
+-------------+--------------------------------------+
|**TEXT**     |                                      |
+-------------+--------------------------------------+
|**TEXT**     |                                      |
+-------------+--------------------------------------+
|**TEXT**     |                                      |
+-------------+--------------------------------------+

Text
----

``choices`` argument is not used.


Password
--------

``choices`` argument is not used.



Confirm
-------

``choices`` argument is not used.

List
----

Shows a list of choices, and allows the selection of one of them.


Checkbox
--------

Shows a list of choices, with multiple selection.

Question Arguments
------------------

The main object is :code:`Question`, but it should not be
instantiated. You must use any of the subclasses, listed below. All of
them have the next attributes that can be set in the initialization:

+---------------+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| **Attribute** | **Type**        | **Explanation**                                                                                                                                   |
+---------------+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| name          | String          | The key in the hash of answers.                                                                                                                   |
+---------------+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| message       | String|Function | To be shown in the prompt to the user. Functions will receive the hash with previous values.                                                      |
+---------------+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| default       | Any|Function    | Default value. Functions will receive the hash with previous values.                                                                              |
+---------------+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| choices       | List|Function   | List of available options. Functions will receive the hash with previous values.                                                                  |
|               |                 | Only available for :code:`Checkbox`.                                                                                                              |
+---------------+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| validate      | Bool|Function   | If the value set is valid. Functions will receive the hash with previous values and the value set in this question, and should return a boolean.  |
+---------------+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| ignore        | Bool|Function   | If the quiestion should be shown. Functions will receive the hash with previous values and should return a boolean.                               |
+---------------+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
