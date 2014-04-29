# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from inquirer import __version__

setup(name='inquirer',
      version=__version__,
      description="Collection of common interactive command line user interfaces, based on Inquirer.js",
      long_description=open('README.md').read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ],
      keywords='',
      author=u'Miguel Ángel García',
      author_email='miguelangel.garcia@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=[]),
      include_package_data=True,
      zip_safe=False,
      install_requires=[line for line in open('requirements.txt')],
      )
