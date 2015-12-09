#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

import logging
import types
from functools import partial, wraps, update_wrapper
from os import environ, path
from tempfile import gettempdir

from redislite import StrictRedis
from singledispatch import singledispatch

try:
    # noinspection PyPep8Naming
    import cPickle as pickle  # PY2X
except ImportError:
    import pickle

logger = logging.getLogger(__name__)

temp_file = partial(path.join, gettempdir())


def patch_requests():
    import requests

    # monkeypatch + decorate requests library
    requests.get = redis_memoize(requests.get)
    requests.post = redis_memoize(requests.post)
    return requests


class Config:
    """

    Time in seconds until the key is destroyed.

    Default: ``os.environ.get('ex', 60 * 60)``  # 1 hour

    .. tip::

        Set to ``None`` for permanent caching.

    Filepath to redislite DB.

    Default: ``os.environ.get('dbfilename', 'cache_requests.redislite')``

    None automatically uses a unique tmp file.  Unique tmp file means NO
    data persistence; which makes this an ordinary LRU cache.

    .. tip::

        ``redislite`` will automatically use a unique tmp file if this is set to ``None``.
        This means new storage every time you run your program.

        **TLDR:** Make sure this is set for data persistence from one run to the next.

    .. note::

        ``redislite`` will NOT implicitly create directories.

    Redis connection handle.

    Default: ``os.environ.get('connection', None)``

    This connection takes precedence, overriding behavior related to :const:`dbfilename`

    .. note::
        Fully compatible with a full version of ``redis``.
    """

    ex = environ.get('ex', 60 * 60)  # 1 hour
    dbfilename = environ.get('dbfilename', temp_file('cache_requests.redislite'))
    connection = environ.get('connection') or partial(StrictRedis, dbfilename=dbfilename)


def normalize_signature(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs:
            args = args, kwargs
        if len(args) is 1:
            args = args[0]
        return func(args)

    return wrapper


@normalize_signature
@singledispatch
def deep_hash(args):
    """
    Recursively hash nested mixed objects (dicts, lists, other).

    :param args: an object
    :return: hash representation of the object
    :rtype: int
    """
    return hash(args)


@deep_hash.register(tuple)
@deep_hash.register(set)
@deep_hash.register(list)
def _(args):
    return hash(tuple(deep_hash(item) for item in args))


@deep_hash.register(dict)  # noqa
def _(args):
    args_copy = {}
    for key, value in args.items():
        args_copy[key] = deep_hash(value)
    return hash(frozenset(sorted(args_copy.items())))


def redis_memoize(func=None, ex=Config.ex, connection=Config.connection):
    if func is not None and callable(func):
        return RedisMemoize(func, ex=ex, connection=connection)

    if func is not None:
        raise TypeError('func must be a callable function.')

    return partial(RedisMemoize, ex=ex, connection=connection)


class RedisMemoize(object):
    def __init__(self, func, ex=Config.ex, connection=Config.connection):
        update_wrapper(self, func)
        self.func = func
        self.connection = connection() if callable(connection) else connection
        self.ex = ex

    def __call__(self, *args, **kwargs):
        memo_key = deep_hash(*args, **kwargs)

        if self[memo_key]:
            logger.debug('Results from cache hash: %s', memo_key)
            return self[memo_key]

        self[memo_key] = self.func(*args, **kwargs)
        logger.debug('Caching results for hash: %s ', memo_key)
        return self[memo_key]

    def __setitem__(self, key, value):
        if value is None:
            return False

        return self.redis.set(name=key, value=pickle.dumps(value), ex=self.ex)

    def __getitem__(self, item):
        value = self.redis.get(item)
        if not value:
            return value

        return pickle.loads(value)

    def __get__(self, instance, _):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    @property
    def redis(self):
        return self.connection

# class Memoize(object):
#     """
#     Decorator Class.  Standard LRU. With redis key/value caching.
#     """
#
#     def __init__(self, func):
#         self.func = func
#         update_wrapper(self, func)
#         self.connection = Config.connection()
#         self.ex = Config.ex
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
#         self.redis.set(name=key, value=pickle.dumps(value), ex=self.ex)
#
#     def __call__(self, *args, **kwargs):
#         """
#         Wrap :attr:`self.func`
#
#         :param args: Arguments passed to decorated func
#         :param kwargs: Keyword Arguments passed to decorated func
#         :return: func results
#         """
#
#         memo_key = deep_hash((args, kwargs))
#
#         if self[memo_key]:
#             logger.debug('Results from cache hash: %s', memo_key)
#             return self[memo_key]
#
#         self[memo_key] = self.func(*args, **kwargs)
#         logger.info('Caching results for hash: %s ', memo_key)
#         return self[memo_key]
