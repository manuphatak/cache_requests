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
from functools import partial, update_wrapper

import types

from ._compat import pickle
from .utils import deep_hash, default_connection, make_callback, default_ex

logger = logging.getLogger(__name__)

__all__ = ['Memoize']


class Memoize(object):
    """Decorator class.  Implements LRU cache pattern that syncs cache with :mod:`redislite` storage."""

    def __new__(cls, func=None, **kwargs):
        """
        Decorate functions with or without decorator arguments.

        :param function func: Function to be decorated.
        :param int ex: Expiration time in seconds.
        :param connection: Redis connection handle.
        """

        is_decorator_without_args = func is not None and callable(func)
        if is_decorator_without_args:
            return super(Memoize, cls).__new__(cls)

        if func is not None:
            raise TypeError('func must be a callable function.')

        return partial(cls, **kwargs)

    def __init__(self, func=None, ex=None, connection=None):
        """
        Set options.

        :param function func: Function to be decorated.
        :param int ex: Expiration time in seconds.
        :param connection: Redis connection handle.
        """

        update_wrapper(self, func)
        self.func = func
        self.connection = connection or default_connection()
        self.ex = ex or default_ex

    def __call__(self, *args, **kwargs):
        """
        Cache getter setter.

        :param tuple args: Arguments passed to function.
        :param dict kwargs: Keyword arguments passed to function.
        :param bool bust_cache: Forcefully reset cache.
        :param bool|function set_cache: Optionally skip setting cache.
        :return: Function results.
        """
        # setup
        bust_cache = kwargs.pop('bust_cache', False)
        hash_key = deep_hash(self.func.__name__, *args, **kwargs)
        set_cache_cb = make_callback(kwargs.pop('set_cache', True))
        func_akw = args, kwargs

        # Guard, don't get results from cache.
        if bust_cache:
            del self[hash_key]
            return self.put_cache_results(hash_key, func_akw, set_cache_cb)

        # Results are in cache, use results
        results_from_cache = self[hash_key]
        if results_from_cache is not None:
            return results_from_cache

        # Set and return results from cache
        return self.put_cache_results(hash_key, func_akw, set_cache_cb)

    def put_cache_results(self, key, func_akw, set_cache_cb):
        """Put function results into cache."""
        args, kwargs = func_akw

        # get function results
        func_results = self.func(*args, **kwargs)

        # optionally add results to cache
        if set_cache_cb(func_results):
            self[key] = func_results
        return func_results

    def __setitem__(self, key, value):
        """Store value in key."""

        # Guard, no value
        if value is None:
            return None

        # Serialize value
        logger.info('Caching results for hash: %s ', key)
        return self.redis.set(name=key, value=pickle.dumps(value), ex=self.ex)

    def __getitem__(self, key):
        """Get results from cache."""
        # setup, get key from cache
        value = self.redis.get(key)

        # Guard, no value, don't try to deserialize
        if not value:
            return value

        # deserialize value
        logger.debug('Retrieving item from cache: %s', key)
        return pickle.loads(value)

    def __delitem__(self, key):
        """Delete item from cache"""
        return self.redis.delete(key)

    def __get__(self, instance, _):  # pragma: no cover

        # Decorator class best practices.

        if instance is None:
            return self

        return types.MethodType(self, instance)

    @property
    def redis(self):
        """Provide access to the redis connection handle."""

        return self.connection

    @redis.setter
    def redis(self, value):
        self.connection = value
