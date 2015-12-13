#!/usr/bin/env python
# coding=utf-8
"""
:mod:`cache_requests.memoize`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. moduleauthor:: Manu Phatak <bionikspoon@gmail.com>

:class:`Memoize` cache decorator.

Public Api
**********
    * :class:`Memoize`

Source
******
"""
from __future__ import absolute_import

import logging
import types
from functools import partial, update_wrapper

from . import config
from ._compat import pickle
from .utils import deep_hash

logger = logging.getLogger(__name__)

__all__ = ['Memoize']


class Memoize(object):
    """Decorator class.  Implements LRU cache pattern that syncs cache with :mod:`redislite` storage."""
    _ex = NotImplemented

    def __new__(cls, func=None, ex=None, connection=None):
        """
        Decorate functions with or without decorator arguments.

        :param function func: Function to be decorated.
        :param int ex: Expiration time in seconds.
        :param connection: Redis connection handle.
        """

        if func is not None and callable(func):
            return object.__new__(cls)

        if func is not None:
            raise TypeError('func must be a callable function.')

        return partial(cls, ex=ex, connection=connection)

    def __init__(self, func, ex=None, connection=None):
        """
        Set options.

        :param function func: Function to be decorated.
        :param int ex: Expiration time in seconds.
        :param connection: Redis connection handle.
        """

        update_wrapper(self, func)
        self.func = func
        connection = config.connection if connection is None else connection
        self.connection = connection() if callable(connection) else connection
        self.ex = ex

    def __call__(self, *args, **kwargs):
        """
        Call decorated function.

        :param tuple args: Arguments passed to function.
        :param dict kwargs: Keyword arguments passed to function.
        :return: Function results.
        """

        memo_key = deep_hash(*args, **kwargs)

        if self[memo_key]:
            logger.debug('Results from cache hash: %s', memo_key)
            return self[memo_key]

        self[memo_key] = self.func(*args, **kwargs)
        logger.debug('Caching results for hash: %s ', memo_key)
        return self[memo_key]

    def __setitem__(self, key, value):
        """Store value in key."""

        if value is None:
            return False

        return self.redis.set(name=key, value=pickle.dumps(value), ex=self.ex)

    def __getitem__(self, item):
        """Get results from cache."""

        value = self.redis.get(item)
        if not value:
            return value

        return pickle.loads(value)

    def __get__(self, instance, _):
        # Decorator class best practices.

        if instance is None:
            return self  # pragma: no cover
        else:
            return types.MethodType(self, instance)

    @property
    def redis(self):
        """Provide access to the redis connection handle."""

        return self.connection

    @property
    def ex(self):
        """Lazy load expiration value from config if necessary."""

        return self._ex or config.ex

    @ex.setter
    def ex(self, value):
        self._ex = value
