#!/usr/bin/env python
# coding=utf-8
"""
**Simple. Powerful. Persistent LRU caching.**


**ELI5:**

    **If you call the same function with the same parameters, it does not recalculate the
    function.**  Instead, the first time, the results are stored, the second time the
    results are retrieved from storage.

    It gets worse.  Unlike a regular LRU cache, this storage survives after the program
    finishes. It's destroyed based on an expiration timer.

``config.EXPIRATION``: (int)

    Keys are destroyed in this amount of time.  Can be set to None

``config.REDISLITE_DB``: (filepath)

    Location of redislite db.  Default ``os.environ.get('REDISLITE_DB')`` AKA ``None``.
    None automatically uses a unique tmp file.  Unique tmp file means NO data
    persistence; which makes this an ordinary LRU cache.

    **TLDR; Set this if you want data persistence.**

    TIP:  Redislite automatically creates the file, but will not create directories.

``config.REDIS_CONNECTION``: (redis connection handle)

    Default is None.  If set this overrides the default behavior of creating a
    redislite connection string.  This can be used to connect to to a real redis db.
"""
from __future__ import absolute_import


__title__ = 'cache_requests'
__author__ = 'Manu Phatak'
__email__ = 'bionikspoon@gmail.com'
__version__ = '0.1.0'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Manu Phatak'

from . import decorate_requests
from .memoize import Memoize

requests = decorate_requests

import logging

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:  # pragma: no cover
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

__all__ = ['requests', 'Memoize']
