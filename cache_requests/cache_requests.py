#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

import logging
from copy import deepcopy
from functools import partial
from functools import update_wrapper
from os import environ
from os.path import join
from tempfile import gettempdir

from redislite import StrictRedis

try:
    # noinspection PyPep8Naming
    import cPickle as pickle  # PY2X
except ImportError:
    import pickle

logger = logging.getLogger(__name__)

temp_file = partial(join, gettempdir())


def decorate_requests():
    import requests

    # monkeypatch + decorate requests library
    requests.get = redis_memoize(requests.get)
    requests.post = redis_memoize(requests.post)
    return requests


class Config:
    """

    """
    """
    Time in seconds until the key is destroyed.

    Default: ``os.environ.get('EXPIRATION', 60 * 60)``  # 1 hour

    .. tip::

        Set to ``None`` for permanent caching.
    """
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
    """
    Redis connection handle.

    Default: ``os.environ.get('connection', None)``

    This connection takes precedence, overriding behavior related to :const:`REDISLITE_DB`

    .. note::
        Fully compatible with a full version of ``redis``.
    """

    EXPIRATION = environ.get('EXPIRATION', 60 * 60)  # 1 hour
    REDISLITE_DB = environ.get('REDISLITE_DB', temp_file('cache_requests.redislite'))
    connection = environ.get('connection') or StrictRedis(dbfilename=REDISLITE_DB)


def deep_hash(*args, **kwargs):
    """
    Recursively hash nested mixed objects (dicts, lists, other).

    :param tuple args: an object
    :return: hash representation of the object
    :rtype: int
    """
    if kwargs:
        args = args, kwargs
    if len(args) is 1:
        args = args[0]
    if isinstance(args, (set, tuple, list)):
        return tuple(deep_hash(item) for item in args if item)

    if not isinstance(args, dict):
        return hash(args)

    copied_obj = deepcopy(args)
    for key, value in copied_obj.items():
        copied_obj[key] = deep_hash(value)

    return hash(tuple(frozenset(copied_obj.items())))


def redis_memoize(outer_func=None, ex=Config.EXPIRATION, connection=Config.connection):
    class MemoizeDecorator(object):
        def __init__(self, inner_func):
            self.function = inner_func
            self.connection = connection
            self.expiration = ex
            update_wrapper(self, inner_func)

        def __call__(self, *args, **kwargs):
            memo_key = deep_hash(args, kwargs)

            if self[memo_key]:
                logger.debug('Results from cache hash: %s', memo_key)
                return self[memo_key]

            self[memo_key] = self.function(*args, **kwargs)
            logger.debug('Caching results for hash: %s ', memo_key)
            return self[memo_key]

        def __setitem__(self, key, value):
            self.redis.set(name=key, value=pickle.dumps(value), ex=self.expiration)

        def __getitem__(self, item):
            value = self.redis.get(item)
            if not value:
                return None

            return pickle.loads(value)

        @property
        def redis(self):
            return self.connection

    if outer_func and callable(outer_func):
        return MemoizeDecorator(outer_func)

    return MemoizeDecorator

# class Memoize(object):
#     """
#     Decorator Class.  Standard LRU. With redis key/value caching.
#     """
#
#     def __init__(self, function):
#         self.function = function
#         update_wrapper(self, function)
#         self.connection = Config.connection()
#         self.expiration = Config.EXPIRATION
#
#     @property
#     def redis(self):
#         """
#         Get redis connection string.
#
#         :return: redis connection handle
#         """
#
#         return self.connection
#
#     def __getitem__(self, item):
#         """
#         Query db for key, de-pickle results.
#
#         :rtype : object
#         :param item: tuple of hashed args and kwargs
#         :return: object from storage
#         """
#
#         value = self.redis.get(item)
#         return None if not value else pickle.loads(value)
#
#     def __setitem__(self, key, value):
#         """
#         Store a pickled object in the db.
#
#         :param key: hash key
#         :param object value: object to store
#         """
#         self.redis.set(name=key, value=pickle.dumps(value), ex=self.expiration)
#
#     def __call__(self, *args, **kwargs):
#         """
#         Wrap :attr:`self.function`
#
#         :param args: Arguments passed to decorated function
#         :param kwargs: Keyword Arguments passed to decorated function
#         :return: function results
#         """
#
#         memo_key = deep_hash((args, kwargs))
#
#         if self[memo_key]:
#             logger.debug('Results from cache hash: %s', memo_key)
#             return self[memo_key]
#
#         self[memo_key] = self.function(*args, **kwargs)
#         logger.info('Caching results for hash: %s ', memo_key)
#         return self[memo_key]
