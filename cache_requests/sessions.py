#!/usr/bin/env python
# coding=utf-8
from requests import Session as RequestsSession

from cache_requests import redis_memoize


class Session(RequestsSession):
    cache_get = True
    cache_options = True
    cache_head = True
    cache_post = False
    cache_put = False
    cache_patch = False
    cache_delete = False
    cache_all = False

    @redis_memoize(on=cache_get or cache_all)
    def get(self, url, **kwargs):
        return super(Session, self).get(url, **kwargs)

    @redis_memoize(on=cache_options or cache_all)
    def options(self, url, **kwargs):
        return super(Session, self).options(url, **kwargs)

    @redis_memoize(on=cache_head or cache_all)
    def head(self, url, **kwargs):
        return super(Session, self).head(url, **kwargs)

    @redis_memoize(on=cache_post or cache_all)
    def post(self, url, data=None, json=None, **kwargs):
        return super(Session, self).post(url, data=data, json=json, **kwargs)

    @redis_memoize(on=cache_put or cache_all)
    def put(self, url, data=None, **kwargs):
        return super(Session, self).put(url, data=data, **kwargs)

    @redis_memoize(on=cache_patch or cache_all)
    def patch(self, url, data=None, **kwargs):
        return super(Session, self).patch(url, data=data, **kwargs)

    @redis_memoize(on=cache_delete or cache_all)
    def delete(self, url, **kwargs):
        return super(Session, self).delete(url, **kwargs)
