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

# from ._config import config
from .memoize import Memoize
from .utils import AttributeDict

__all__ = ['MemoizeRequest', 'CacheConfig', 'Session']


class MemoizeRequest(Memoize):
    """Cache session method calls."""

    def __init__(self, func=None, **kwargs):
        session = kwargs.pop('session')

        if not hasattr(session, 'cache'):
            raise TypeError('Must pass in a cache config object.')

        super(MemoizeRequest, self).__init__(func=func, **kwargs)

        self.cache = session.cache

    def __call__(self, *args, **kwargs):
        """
        Call decorated function.

        :param Session this: Session object.
        :param tuple args: Function args.
        :param dict kwargs: Function kwargs.
        :return: Function results.
        """
        all_is_unset = self.cache.all is None
        use_cache = getattr(self.cache, self.func.__name__) if all_is_unset else self.cache.all

        if not use_cache:
            return self.func(*args, **kwargs)

        return super(MemoizeRequest, self).__call__(*args, **kwargs)


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
        self.get = MemoizeRequest(self.get, session=self)
        self.options = MemoizeRequest(self.options, session=self)
        self.head = MemoizeRequest(self.head, session=self)
        self.post = MemoizeRequest(self.post, session=self)
        self.put = MemoizeRequest(self.put, session=self)
        self.patch = MemoizeRequest(self.patch, session=self)
        self.delete = MemoizeRequest(self.delete, session=self)
