==============
Cache Requests
==============

.. image:: https://pypip.in/status/cache_requests/badge.svg
    :target: https://pypi.python.org/pypi/cache_requests/
    :alt: Development Status

.. image:: https://travis-ci.org/bionikspoon/cache_requests.svg?branch=develop
    :target: https://travis-ci.org/bionikspoon/cache_requests?branch=develop
    :alt: Build Status

.. image:: https://pypip.in/version/cache_requests/badge.svg
    :target: https://pypi.python.org/pypi/cache_requests
    :alt: Latest Version

.. image:: https://coveralls.io/repos/bionikspoon/cache_requests/badge.svg?branch=develop
    :target: https://coveralls.io/r/bionikspoon/cache_requests?branch=develop
    :alt: Coverage Status

.. image:: https://readthedocs.org/projects/cache-requests/badge/?version=latest
    :target: https://readthedocs.org/projects/cache-requests/?badge=latest
    :alt: Documentation Status


**Simple. Powerful. Persistent LRU caching.**

* Free software: MIT license
* Documentation: https://cache-requests.readthedocs.org.

Features
--------

* Drop in replacement for the requests library.
* Optional expiration timer on stored items.
* Backed by yahoo's powerful redislite db
* Scalable. Optionally accepts a redis connection.  Take advantage of the full power of redis.



Installation
------------

At the command line either via easy_install or pip:

.. code-block:: shell

    $ pip install cache_requests

.. code-block:: shell

    $ easy_install cache_requests

**Uninstall**

.. code-block:: shell

    $ pip uninstall cache_requests


Getting Started
---------------
To use cache_requests in a project:

.. code-block:: python

    import cache_requests
