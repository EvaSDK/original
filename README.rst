original
========

.. image:: https://travis-ci.org/EvaSDK/original.svg?branch=master
   :target: https://travis-ci.org/EvaSDK/original
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/EvaSDK/original/badge.svg?branch=master
   :target: https://coveralls.io/github/EvaSDK/original?branch=master
   :alt: Coverage Status

.. image:: https://www.versioneye.com/user/projects/576bd5bacd6d510048bab24b/badge.svg
   :target: https://www.versioneye.com/user/projects/576bd5bacd6d510048bab24b
   :alt: Dependency Status

About
-----

A simple python photo gallery application, fork of PHP's `original <http://jimmac.musichall.cz/original.php>`_ photo gallery from Jakub 'Jimmac' Steiner.

Installation
------------

Create and activate a virtualenv::

    $ virtualenv venv
    $ . venv/bin/activate

If you simply want to run the project::

    (venv) $ pip install git+https://github.com/EvaSDK/original.git#egg=original-dev

If you need to do some development::

    (venv) $ git clone git@github.com:EvaSDK/original.git
    (venv) $ cd original
    (venv) $ pip install -e .

Run
---

Simply source your virtualenv and run::

    (venv) $ python -m original.wsgi
