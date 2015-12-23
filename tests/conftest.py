#!/usr/bin/env python
# coding=utf-8
from functools import partial

from mock import Mock
from pytest import fixture


@fixture(autouse=True)
def a_function_setup(tmpdir, monkeypatch):
    """
    :type tmpdir: py.path.local
    :type monkeypatch: _pytest.monkeypatch.monkeypatch
    """

    from redislite import StrictRedis

    default_connection = partial(StrictRedis, dbfilename=tmpdir.join('test_redis.db').strpath)

    monkeypatch.setattr('cache_requests.memoize.default_connection', default_connection)
    monkeypatch.setattr('cache_requests.utils.default_connection', default_connection)
    monkeypatch.setattr('cache_requests.sessions.default_connection', default_connection)


@fixture(autouse=True)
def function_tear_down(request):
    """:type request: _pytest.python.FixtureRequest"""
    from cache_requests.utils import default_connection

    def cleanup():
        redis = default_connection()
        redis.flushall()

    request.addfinalizer(cleanup)


@fixture
def redis_mock():
    cache = {}

    def set(name=None, value=None, **_):
        cache[name] = value

    def get(name):
        return cache.get(name)

    def delete(key):
        cache.pop(key)

    _MockRedis = Mock(spec='redislite.StrictRedis')
    _MockRedis.cache = cache
    _MockRedis.get = Mock(side_effect=get)
    _MockRedis.set = Mock(side_effect=set)
    _MockRedis.delete = Mock(side_effect=delete)
    _MockRedis.flushall = Mock()

    return _MockRedis
