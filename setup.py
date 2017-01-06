#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='croesus',
    version='0.1',
    description='',
    url='https://github.com/fscherf/croesus',
    author='Florian Scherf',
    author_email='f.scherf@pengutronix.de',
    license='BSD',
    packages=find_packages(exclude=('tests', 'test_project',)),
    zip_safe=True,
    install_requires=[
        'Django>=1.8,<1.9',
        'python-dateutil',
        'mt-940==4.2',
        'PTable',
        'pyyaml',
        'IPython',
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Intended Audience :: Financial and Insurance Industry',
    ]
)
