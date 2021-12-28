"""Sphinx configuration."""
from datetime import datetime


project = "inquirer"
author = "Miguel Ángel García"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]
autodoc_typehints = "description"
html_theme = "furo"
# workaround for bug: https://github.com/sphinx-doc/sphinx/issues/9383
linkcheck_ignore = [
    "contributing.html",
]
