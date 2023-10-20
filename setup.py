#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='ripxospeech',
      version='1.0',
      # Modules to import from other scripts:
      packages=find_packages(),
      py_modules=['ripxospeech'],
      entry_points={
          'console_scripts': [
              'ripxospeech=ripxospeech:main'
              ],
          },
      )
