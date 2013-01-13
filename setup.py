# YOU NEED TO EDIT THESE
AUTHOR = 'Chris Dent'
AUTHOR_EMAIL = 'cdent@peermore.com'
NAME = 'PythonHAL'
DESCRIPTION = 'HAL Composer and Consumer'
VERSION = '0.1'


import os

from setuptools import setup, find_packages


# You should carefully review the below (install_requires especially).
setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = 'http://pypi.python.org/pypi/%s' % NAME,
    platforms = 'Posix; MacOS X; Windows',
    packages = find_packages(exclude=['test']),
    install_requires = ['setuptools', 'uritemplate'],
    zip_safe = False
    )
