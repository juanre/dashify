#!/usr/bin/env python

try:
    from setuptools import setup
except:
    ## entry_points not available, so dashify won't be installed as executable
    from distutils.core import setup

setup(name='dashify',
      version='0.0.1',
      description='Converts word separators in file names to dashes',
      author='Juan Reyero',
      author_email='juan@juanreyero.com',
      url='http://juanreyero.com/',
      py_modules=['dashify'],
      entry_points = {
          'console_scripts': [
              'dashify = dashify:as_main']})
