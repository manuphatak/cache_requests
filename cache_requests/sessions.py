#!/usr/bin/env python
# coding=utf-8
"""
:mod:`cache_requests.sessions`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. moduleauthor:: Manu Phatak <bionikspoon@gmail.com>

Extend :mod:`requests` with cache decorator.


Public Api
**********
    * :class:`Session`

Private API
***********
    * :class:`MemoizeRequest`
    * :class:`CacheConfig`

Source
******
"""
from __future__ import absolute_import

from requests import Session as RequestsSession, HTTPError

from .memoize import Memoize
from .utils import AttributeDict, default_connection, default_ex

__all__ = ['MemoizeRequest', 'CacheConfig', 'Session']


class MemoizeRequest(Memoize):
    """Cache session method calls."""

    def __init__(self, func=None, **kwargs):

        # setup shared cache
        session = kwargs.pop('session')
        self.cache = session.cache

        # set from shared cache defaults
        kwargs.setdefault('ex', self.cache.ex)
        kwargs.setdefault('connection', self.cache.connection)

        super(MemoizeRequest, self).__init__(func=func, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Call decorated function.

        :param tuple args: Function args.
        :param Session session: Session object.
        :param dict kwargs: Function kwargs.
        :return: Function results.
        """
        # Guard, don't cache method.
        if not self.use_cache:
            return self.func(*args, **kwargs)

        # Don't cache errors.
        kwargs.setdefault('set_cache', self.cache.set_cache_cb)

        return super(MemoizeRequest, self).__call__(*args, **kwargs)

    @property
    def use_cache(self):
        all_is_unset = self.cache.all is None
        return getattr(self.cache, self.func.__name__) if all_is_unset else self.cache.all

    @property
    def redis(self):
        return self.cache.connection

    @redis.setter
    def redis(self, value):
        self.cache.connection = value

    @property
    def ex(self):
        return self.cache.ex

    @ex.setter
    def ex(self, value):
        self.cache.ex = value


class CacheConfig(AttributeDict):
    """A strict dict with attribute access."""
    __attr__ = 'get', 'options', 'head', 'post', 'put', 'patch', 'delete', 'all', 'connection', 'ex', 'set_cache_cb'


class Session(RequestsSession):
    """:class:`requests.Session` with memoized methods."""

    def __init__(self, ex=None, connection=None):
        """Set reference to cache configuration on object."""

        super(Session, self).__init__()

        options = {
            'get': True,
            'options': True,
            'head': True,
            'post': False,
            'put': False,
            'patch': False,
            'delete': False,
            'all': None,
            'connection': connection or default_connection(),
            'ex': ex or default_ex,
            'set_cache_cb': set_cache_cb
        }

        # Setup
        self.cache = CacheConfig(**options)

        # Decorate methods
        self.get = MemoizeRequest(self.get, session=self)
        self.options = MemoizeRequest(self.options, session=self)
        self.head = MemoizeRequest(self.head, session=self)
        self.post = MemoizeRequest(self.post, session=self)
        self.put = MemoizeRequest(self.put, session=self)
        self.patch = MemoizeRequest(self.patch, session=self)
        self.delete = MemoizeRequest(self.delete, session=self)


def set_cache_cb(response):
    """:type response: requests.Response"""
    try:
        response.raise_for_status()
    except HTTPError:
        return False

    return True
