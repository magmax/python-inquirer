# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from inquirer import __version__


def read_description():
    with open('README.rst') as fd:
        return fd.read()


setup(name='inquirer',
      version=__version__,
      description="Collection of common interactive command line user interfaces, based on Inquirer.js",
      long_description=read_description(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
      ],
      keywords='color',
      author='Miguel Ángel García',
      author_email='miguelangel.garcia@gmail.com',
      url='https://github.com/magmax/python-inquirer',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'blessings >= 1.5.1',
          'readchar >= 0.7',
      ],
      )
