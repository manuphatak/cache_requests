#!/usr/bin/env python
# coding=utf-8

from functools import partial

from mock import Mock
from pytest import fixture

from ._compat import reload


@fixture(autouse=True)
def function_setup(tmpdir):
    """:param py.path.local tmpdir:"""
    from cache_requests import config

    config.dbfilename = tmpdir.join('test_redis.db').strpath


@fixture(autouse=True)
def function_tear_down(request):
    """:type request: _pytest.python.FixtureRequest"""
    from cache_requests import config

    def cleanup():
        redis = config.connection()
        redis.flushall()

    request.addfinalizer(partial(reload, config))
    request.addfinalizer(cleanup)


@fixture
def MockRedis():
    from cache_requests import config

    cache = {}

    def set(name=None, value=None, **_):
        cache[name] = value

    def get(name):
        return cache.get(name)

    _MockRedis = Mock(spec='redislite.StrictRedis')
    _MockRedis.return_value = _MockRedis
    _MockRedis.get = Mock(side_effect=get)
    _MockRedis.set = Mock(side_effect=set)
    _MockRedis.flushall = Mock()

    config.connection = _MockRedis
    return _MockRedis
