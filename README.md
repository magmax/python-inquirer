---
substitutions:
  Codecov: |-
    ```{image} https://codecov.io/gh/magmax/python-inquirer/branch/master/graph/badge.svg
    :alt: Codecov
    :target: https://app.codecov.io/gh/magmax/python-inquirer
    ```
  Documentation: |-
    ```{image} https://github.com/magmax/python-inquirer/workflows/Documentation/badge.svg
    :alt: Read the documentation at https://magmax.org/python-inquirer/
    :target: https://magmax.org/python-inquirer/
    ```
  License: |-
    ```{image} https://img.shields.io/pypi/l/inquirer.svg
    :alt: License
    :target: https://pypi.python.org/pypi/inquirer
    ```
  Tests: |-
    ```{image} https://github.com/magmax/python-inquirer/workflows/Tests/badge.svg
    :alt: Tests
    :target: https://github.com/magmax/python-inquirer/actions?workflow=Tests
    ```
  inquirer checkbox: |-
    ```{image} http://magmax.org/python-inquirer/_images/inquirer_checkbox.png
    :alt: Example of Checkbox Question
    ```
  inquirer list: |-
    ```{image} http://magmax.org/python-inquirer/_images/inquirer_list.png
    :alt: Example of List Question
    ```
  inquirer text: |-
    ```{image} http://magmax.org/python-inquirer/_images/inquirer_text.png
    :alt: Example of Text Question
    ```
  pip dd: |-
    ```{image} https://img.shields.io/pypi/dd/inquirer.svg
    :alt: Yesterday downloads from pypi
    :target: https://pypi.python.org/pypi/inquirer
    ```
  pip dm: |-
    ```{image} https://img.shields.io/pypi/dm/inquirer.svg
    :alt: Last month downloads from pypi
    :target: https://pypi.python.org/pypi/inquirer
    ```
  pip dw: |-
    ```{image} https://img.shields.io/pypi/dw/inquirer.svg
    :alt: Last week downloads from pypi
    :target: https://pypi.python.org/pypi/inquirer
    ```
  pip implem: |-
    ```{image} https://img.shields.io/pypi/implementation/inquirer.svg
    :alt: Python interpreters
    :target: https://pypi.python.org/pypi/inquirer
    ```
  pip pyversions: |-
    ```{image} https://img.shields.io/pypi/pyversions/inquirer.svg
    :alt: Python versions
    :target: https://pypi.python.org/pypi/inquirer
    ```
  pip version: |-
    ```{image} https://img.shields.io/pypi/v/inquirer.svg
    :alt: Latest PyPI version
    :target: https://pypi.python.org/pypi/inquirer
    ```
  pip wheel: |-
    ```{image} https://img.shields.io/pypi/wheel/inquirer.svg
    :alt: Wheel
    :target: https://pypi.python.org/pypi/inquirer
    ```
  status: |-
    ```{image} https://img.shields.io/pypi/status/inquirer.svg
    :alt: Status
    :target: https://pypi.python.org/pypi/inquirer
    ```
  version: |-
    ```{image} https://img.shields.io/pypi/v/inquirer.svg
    :alt: Status
    :target: https://pypi.python.org/pypi/inquirer
    ```
---

```{eval-rst}
====================  =================================================================================
Tests                 |Tests| |Codecov|
--------------------  ---------------------------------------------------------------------------------
Downloads             |pip dm| |pip dw| |pip dd|
--------------------  ---------------------------------------------------------------------------------
About                 |License| |pip wheel| |pip pyversions| |pip implem|
--------------------  ---------------------------------------------------------------------------------
Status                |version| |status| |Documentation|
====================  =================================================================================
```

Collection of common interactive command line user interfaces, based on [Inquirer.js].

# Goal and Philosophy

Born as a [Inquirer.js] clone, it shares part of the goals and philosophy.

So, **Inquirer** should ease the process of asking end user **questions**, **parsing**, **validating** answers, managing **hierarchical prompts** and providing **error feedback**.

You can [download the python-inquirer code from GitHub] or [download the wheel from Pypi].

## Platforms support

Python-inquirer supports mainly UNIX-based platforms (eq. Mac OS, Linux, etc.). Windows has experimental support, please let us know if there are any problems!

# Installation

```sh
pip install inquirer
```

# Documentation

Documentation has been moved to [magmax.org/python-inquirer](https://magmax.org/python-inquirer/).

But here you have a couple of usage examples:

## Text

```python
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
```

{{ inquirer text }}

## Editor

Like a Text question, but used for larger answers. It opens external text editor which is used to collect the answer.

The environment variables \$VISUAL and \$EDITOR, can be used to specify which editor should be used. If not present
inquirer fallbacks to `vim -> emacs -> nano` in this order based on availability in the system.

External editor handling is done using great library [python-editor](https://github.com/fmoo/python-editor).

Example:

```python
import inquirer
questions = [
  inquirer.Editor('long_text', message="Provide long text")
]
answers = inquirer.prompt(questions)
```

## List

Shows a list of choices, and allows the selection of one of them.

Example:

```python
import inquirer
questions = [
  inquirer.List('size',
                message="What size do you need?",
                choices=['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
            ),
]
answers = inquirer.prompt(questions)
```

List questions can take one extra argument {code}`carousel=False`. If set to true, the answers will rotate (back to first when pressing down on last choice, and down to last choice when pressing up on first choice)

{{ inquirer list }}

## Checkbox

Shows a list of choices, with multiple selection.

Example:

```python
import inquirer
questions = [
  inquirer.Checkbox('interests',
                    message="What are you interested in?",
                    choices=['Computers', 'Books', 'Science', 'Nature', 'Fantasy', 'History'],
                    ),
]
answers = inquirer.prompt(questions)
```

Checkbox questions can take one extra argument {code}`carousel=False`. If set to true, the answers will rotate (back to first when pressing down on last choice, and down to last choice when pressing up on first choice)

{{ inquirer checkbox }}

## Path

Like Text question, but with builtin validations for working with paths.

Example:

```python
import inquirer
questions = [
  inquirer.Path('log_file',
                 message="Where logs should be located?",
                 path_type=inquirer.Path.DIRECTORY,
                ),
]
answers = inquirer.prompt(questions)
```

# Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

# License

Copyright (c) 2014-2021 Miguel Ángel García ([@magmax_en]), based on [Inquirer.js], by Simon Boudrias ([@vaxilart])

Licensed under [the MIT license].

<!-- github-only -->

[@magmax_en]: https://twitter.com/magmax_en
[@vaxilart]: https://twitter.com/vaxilart
[contributor guide]: CONTRIBUTING.md
[download the python-inquirer code from github]: https://github.com/magmax/python-inquirer
[download the wheel from pypi]: https://pypi.python.org/pypi/inquirer
[examples/]: https://github.com/magmax/python-inquirer/tree/master/examples
[inquirer.js]: https://github.com/SBoudrias/Inquirer.js
[the mit license]: https://opensource.org/licenses/MIT
