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

from requests import Session as RequestsSession

from .memoize import Memoize
from .utils import AttributeDict

__all__ = ['MemoizeRequest', 'CacheConfig', 'Session']


class MemoizeRequest(Memoize):
    """Cache session method calls."""

    def __call__(self, this, *args, **kwargs):
        """
        Call decorated function.

        :param Session this: Session object.
        :param tuple args: Function args.
        :param dict kwargs: Function kwargs.
        :return: Function results.
        """
        override = this.cache.all is None
        use_cache = getattr(this.cache, self.func.__name__) if override else override

        if not use_cache:
            return self.func(this, *args, **kwargs)

        return super(MemoizeRequest, self).__call__(this, *args, **kwargs)


class CacheConfig(AttributeDict):
    """A strict dict with attribute access."""
    __attr__ = 'get', 'options', 'head', 'post', 'put', 'patch', 'delete', 'all'


class Session(RequestsSession):
    """:class:`requests.Session` with memoized methods."""

    def __init__(self):
        """Set reference to cache configuration on object."""

        super(Session, self).__init__()
        self.cache = CacheConfig(get=True, options=True, head=True, post=False, put=False, patch=False, delete=False,
                                 all=None)

    @MemoizeRequest
    def get(self, url, **kwargs):
        """Cached by default: True"""
        return super(Session, self).get(url, **kwargs)

    @MemoizeRequest
    def options(self, url, **kwargs):
        """Cached by default: True"""

        return super(Session, self).options(url, **kwargs)

    @MemoizeRequest
    def head(self, url, **kwargs):
        """Cached by default: True"""

        return super(Session, self).head(url, **kwargs)

    @MemoizeRequest
    def post(self, url, data=None, json=None, **kwargs):
        """Cached by default: False"""

        return super(Session, self).post(url, data=data, json=json, **kwargs)

    @MemoizeRequest
    def put(self, url, data=None, **kwargs):
        """Cached by default: False"""

        return super(Session, self).put(url, data=data, **kwargs)

    @MemoizeRequest
    def patch(self, url, data=None, **kwargs):
        """Cached by default: False"""

        return super(Session, self).patch(url, data=data, **kwargs)

    @MemoizeRequest
    def delete(self, url, **kwargs):
        """Cached by default: False"""

        return super(Session, self).delete(url, **kwargs)
