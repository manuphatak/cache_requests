#!/usr/bin/env python
# coding=utf-8

from functools import partial

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
