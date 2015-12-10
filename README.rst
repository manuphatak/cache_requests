==============
cache_requests
==============

.. image:: https://img.shields.io/github/downloads/bionikspoon/cache_requests/total.svg
    :target: https://github.com/bionikspoon/cache_requests
    :alt: Github Downloads

.. image:: https://badge.fury.io/py/cache_requests.svg
    :target: https://pypi.python.org/pypi/cache_requests/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/cache_requests.svg
    :target: https://pypi.python.org/pypi/cache_requests/
    :alt: Development Status

.. image:: https://travis-ci.org/bionikspoon/cache_requests.svg?branch=develop
    :target: https://travis-ci.org/bionikspoon/cache_requests?branch=develop
    :alt: Build Status

.. image:: https://coveralls.io/repos/bionikspoon/cache_requests/badge.svg?branch=develop
    :target: https://coveralls.io/github/bionikspoon/cache_requests?branch=develop&service=github
    :alt: Coverage Status

.. image:: https://readthedocs.org/projects/cache_requests/badge/?version=develop
    :target: https://cache_requests.readthedocs.org/en/develop/?badge=develop
    :alt: Documentation Status

------------

.. image:: https://img.shields.io/badge/Python-2.6,_2.7,_3.3,_3.4,,_3.5,_pypy-brightgreen.svg
    :target: https://pypi.python.org/pypi/cache_requests/
    :alt: Supported Python versions


.. image:: https://img.shields.io/pypi/l/cache_requests.svg
    :target: https://pypi.python.org/pypi/cache_requests/
    :alt: License

**Simple. Powerful. Persistent LRU caching for the requests library.**

Features
--------

* Free software: MIT license
* Documentation: https://cache_requests.readthedocs.org.
* Python version agnostic: tested against Python 2.7, 3.3, 3.4, 3.5 and Pypy

..

* Drop in decorator for the requests library.
* Automatic timer based expiration on stored items (optional).
* Backed by yahoo's powerful ``redislite``.
* Scalable with redis. Optionally accepts a ``redis`` connection.
* Exposes the powerful underlying ``Memoize`` decorator to decorate any function.
* Tested with high coverage.
* Lightweight. Simple logic.
* Lightning fast.

..

* Jump start your development cycle.
* Collect and reuse entire response objects.


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `bionikspoon/cookiecutter-pypackage`_ forked from `audreyr/cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`bionikspoon/cookiecutter-pypackage`: https://github.com/bionikspoon/cookiecutter-pypackage
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
