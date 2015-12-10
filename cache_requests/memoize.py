#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

import logging
import types
from functools import partial, update_wrapper

from . import config
from ._compat import pickle
from .utils import deep_hash

logger = logging.getLogger(__name__)


def memoize(func=None, ex=config.ex, connection=config.connection):
    if func is not None and callable(func):
        return RedisMemoize(func, ex=ex, connection=connection)

    if func is not None:
        raise TypeError('func must be a callable function.')

    return partial(RedisMemoize, ex=ex, connection=connection)


class RedisMemoize(object):
    def __init__(self, func, ex=config.ex, connection=config.connection):
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
