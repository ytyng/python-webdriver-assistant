# -*- coding: utf-8 -*-

from __future__ import unicode_literals

menu = [
    ('cancel',
     ""),
    ('flake8',
     "flake8 ."),
    ('test',
     "./tests.py"),
    ('upload pypi',
     "./setup.py sdist; twine upload --skip-existing dist/*"),
]
