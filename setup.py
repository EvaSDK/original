#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup, find_packages


MODULE_NAME="original"


def get_version():
    """ Reads project version from module. """
    with open(os.path.join(
        os.path.dirname(__file__), MODULE_NAME, '__init__.py')
    ) as init:
        for line in init.readlines():
            res = re.match(r'__version__ *= *[\'"]([0-9\.]*)[\'"]$', line)
            if res:
                return res.group(1)


setup(
    name='original',
    version=get_version(),
    description='Photo Gallery',
    author='Gilles Dartiguelongue',
    install_requires=[
        'flask',
        'flask_babel',
        'flask_classy',
        'pastedeploy',
        'pillow',
        'rq',
    ],
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    entry_points={
        'console_scripts': [
            'original-thumbnails = original.cli:do_thumbnails',
        ],
        'paste.app_factory': [
            'main=original.wsgi:app_factory',
        ],
    },
)
