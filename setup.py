# -*- coding: utf-8 -*-

import sys
import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

version = "3.0.0"
github_ref = os.getenv("GITHUB_REF")
if github_ref and github_ref.startswith("refs/tags"):
    version = github_ref[10:]


def read_description():
    try:
        with open("README.rst", encoding="utf8") as fd:
            return fd.read()
    except TypeError:
        with open("README.rst") as fd:
            return fd.read()


def read_requirements():
    try:
        with open("requirements.txt", encoding="utf8") as fd:
            return fd.read()
    except TypeError:
        with open("requirements.txt") as fd:
            return fd.read()


class PyTest(TestCommand):
    user_options = [
        ("pytest-args=", "a", "Arguments to pass to py.test"),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args or ["--cov-report=term-missing"])
        sys.exit(errno)


setup(
    name="inquirer",
    version=version,
    description=("Collection of common interactive command line user interfaces," " based on Inquirer.js"),
    long_description=read_description(),
    cmdclass={"test": PyTest},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: " "Libraries :: Application Frameworks",
    ],
    keywords="color terminal",
    author="Miguel Ángel García",
    author_email="miguelangel.garcia@gmail.com",
    url="https://github.com/magmax/python-inquirer",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=read_requirements().splitlines(),
)
