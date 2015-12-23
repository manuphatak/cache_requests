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
        session = kwargs.pop('session')
        self.session = session

        super(MemoizeRequest, self).__init__(func=func, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Call decorated function.

        :param tuple args: Function args.
        :param Session session: Session object.
        :param dict kwargs: Function kwargs.
        :return: Function results.
        """

        all_is_unset = self.session.cache.all is None
        use_cache = getattr(self.session.cache, self.func.__name__) if all_is_unset else self.session.cache.all

        if not use_cache:
            return self.func(*args, **kwargs)

        kwargs.setdefault('set_cache', self.session.set_cache_cb)

        return super(MemoizeRequest, self).__call__(*args, **kwargs)

    @property
    def redis(self):
        return self.session.connection

    @redis.setter
    def redis(self, value):
        self.session.connection = value

    @property
    def ex(self):
        return self.session.ex

    @ex.setter
    def ex(self, value):
        self.session.ex = value


class CacheConfig(AttributeDict):
    """A strict dict with attribute access."""
    __attr__ = 'get', 'options', 'head', 'post', 'put', 'patch', 'delete', 'all'


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
            'all': None
        }

        # Setup
        self.cache = CacheConfig(**options)
        self.connection = connection or default_connection()
        self.ex = ex or default_ex

        # Decorate methods
        self.get = MemoizeRequest(self.get, session=self)
        self.options = MemoizeRequest(self.options, session=self)
        self.head = MemoizeRequest(self.head, session=self)
        self.post = MemoizeRequest(self.post, session=self)
        self.put = MemoizeRequest(self.put, session=self)
        self.patch = MemoizeRequest(self.patch, session=self)
        self.delete = MemoizeRequest(self.delete, session=self)

    @staticmethod
    def set_cache_cb(response):
        """:type response: requests.Response"""
        try:
            response.raise_for_status()
        except HTTPError:
            return False

        return True
