#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import find_packages, setup

MODULE_NAME="original"


def get_version():
    """ Reads project version from module. """
    with open(os.path.join(
        os.path.dirname(__file__), MODULE_NAME, '__init__.py')
    ) as init:
        for line in init.readlines():
            res = re.match(r'^__version__ = [\'"](.*)[\'"]$', line)
            if res:
                return res.group(1)


def get_long_description():
    with open(os.path.join(
        os.path.dirname(__file__), 'README.rst'
    )) as readme, open(os.path.join(
        os.path.dirname(__file__), 'CHANGES.rst'
    )) as changes:
        return readme.read() + '\n' + changes.read()


setup(
    name='original',
    version=get_version(),
    description='Photo Gallery',
    long_description=get_long_description(),
    author='Gilles Dartiguelongue',
    author_email='gilles.dartiguelongue@esiee.org',
    url='https://github.com/EvaSDK/original',
    packages=find_packages(),
    package_data={
        'original': [
            'templates/*',
            'translations/*/LC_MESSAGES/*.mo',
        ],
    },
    install_requires=[
        'flask',
        'flask-babel',
        'flask-classy',
        'pastedeploy',
        'pillow',
        'rq',
    ],
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
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
            'main=original.app:app_factory',
        ],
    },
)
