#!/usr/bin/env python
# coding=utf-8
"""
config module
-------------

Module configuration options
"""
import os


EXPIRATION = os.environ.get('EXPIRATION', 60 * 60)  # 1 hour
"""
Time in seconds until the key is destroyed.

Default: ``os.environ.get('EXPIRATION', 60 * 60)``  # 1 hour

.. tip::

    Set to ``None`` for permanent caching.
"""

REDISLITE_DB = os.environ.get('REDISLITE_DB', 'cache_requests.redislite')
"""
Filepath to redislite DB.

Default: ``os.environ.get('REDISLITE_DB', 'cache_requests.redislite')``

None automatically uses a unique tmp file.  Unique tmp file means NO
data persistence; which makes this an ordinary LRU cache.

.. tip::

    ``redislite`` will automatically use a unique tmp file if this is set to ``None``.
    This means new storage every time you run your program.

    **TLDR:** Make sure this is set for data persistence from one run to the next.

.. note::

    ``redislite`` will NOT implicitly create directories.
"""

REDIS_CONNECTION = os.environ.get('REDIS_CONNECTION', None)
"""
Redis connection handle.

Default: ``os.environ.get('REDIS_CONNECTION', None)``

This connection takes precedence, overriding behavior related to :const:`REDISLITE_DB`

.. note::
    Fully compatible with a full version of ``redis``.
"""