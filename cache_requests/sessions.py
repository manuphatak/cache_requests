#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from requests import Session as RequestsSession

from .memoize import RedisMemoize
from .utils import AttributeDict

__all__ = ['Session']


class Memoize(RedisMemoize):
    def __init__(self, *args, **kwargs):
        super(Memoize, self).__init__(*args, **kwargs)

    def __call__(self, this, *args, **kwargs):
        override = this.cache.all is None
        use_cache = getattr(this.cache, self.func.__name__) if override else override

        if not use_cache:
            return self.func(this, *args, **kwargs)

        return super(Memoize, self).__call__(this, *args, **kwargs)


class CacheConfig(AttributeDict):
    __attr__ = 'get', 'options', 'head', 'post', 'put', 'patch', 'delete', 'all'


class Session(RequestsSession):
    def __init__(self):
        super(Session, self).__init__()
        self.cache = CacheConfig(get=True, options=True, head=True, post=False, put=False, patch=False, delete=False,
                                 all=None)

    @Memoize
    def get(self, url, **kwargs):
        return super(Session, self).get(url, **kwargs)

    @Memoize
    def options(self, url, **kwargs):
        return super(Session, self).options(url, **kwargs)

    @Memoize
    def head(self, url, **kwargs):
        return super(Session, self).head(url, **kwargs)

    @Memoize
    def post(self, url, data=None, json=None, **kwargs):
        return super(Session, self).post(url, data=data, json=json, **kwargs)

    @Memoize
    def put(self, url, data=None, **kwargs):
        return super(Session, self).put(url, data=data, **kwargs)

    @Memoize
    def patch(self, url, data=None, **kwargs):
        return super(Session, self).patch(url, data=data, **kwargs)

    @Memoize
    def delete(self, url, **kwargs):
        return super(Session, self).delete(url, **kwargs)
