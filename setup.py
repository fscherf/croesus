#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

if os.environ.get('TOX', False):
    packages = find_packages(exclude=['tests'])
    install_requires = []

else:
    packages = find_packages(exclude=('tests', '*.test_project',))

    install_requires = [
        'Django>=1.8,<=1.9',
        'python-dateutil',
        'PTable',
    ]

setup(
    name='croesus',
    version='0.0',
    description='',
    url='https://github.com/fscherf/croesus',
    author='Florian Scherf',
    author_email='f.scherf@pengutronix.de',
    license='BSD',
    packages=packages,
    zip_safe=True,
    install_requires=install_requires,
)
