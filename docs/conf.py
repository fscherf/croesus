#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django
import git
import os

django.setup()

repository = git.Git(os.path.dirname(__file__))

try:
    git_describe_string = repository.describe()

except git.exc.GitCommandError:
    git_describe_string = 'UNKNOWN'

project = 'Croesus'
author = 'Florian Scherf'
copyright = 'Florian Scherf'
version = git_describe_string
release = git_describe_string

extensions = [
    'sphinx.ext.autodoc',
]

source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']
html_theme = 'sphinx_rtd_theme'
