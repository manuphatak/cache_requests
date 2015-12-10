#!/usr/bin/env python
# coding=utf-8

from functools import partial
# noinspection PyDeprecation
from imp import reload
from pytest import fixture


@fixture(autouse=True)
def function_setup(tmpdir):
    """:param py.path.local tmpdir:"""
    from cache_requests import config

    config.dbfilename = tmpdir.join('test_redis.db').strpath


@fixture(autouse=True)
def function_tear_down(request):
    from cache_requests import config

    def cleanup():
        redis = config.connection()
        redis.flushall()

    request.addfinalizer(partial(reload, config))
    request.addfinalizer(cleanup)
